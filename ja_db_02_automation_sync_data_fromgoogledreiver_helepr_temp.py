"""
Template: ja_db_02_automation_sync_data_fromgoogledreiver_helepr_temp.py
Purpose: Sync structured data from Google Drive to PostgreSQL with health monitoring
Editable by: Developer (adapt fields, schema mapping, filenames)
"""

import os
import json
import time
import uuid
import socket
import platform
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# Load environment variables
load_dotenv()

# === ENV Configuration ===
SCOPES = [os.getenv("GOOGLE_SCOPES")]
JAVIS_SHELL_FOLDER_ID = os.getenv("JAVIS_SHELL_FOLDER_ID")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
JA_DATA_FILE = os.getenv("JA_DATA_FILE")  # e.g. clients.json
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 30))

LOCAL_CLIENTS_JSON = f'latest_{JA_DATA_FILE}'
LOCAL_HEALTH_LOG = 'log/health_helper_server.json'
os.makedirs("log", exist_ok=True)

DB_CONFIG = {
    'host': 'db',  # docker-compose service name
    'port': 5432,
    'dbname': 'ja_clients',
    'user': 'ja_db',
    'password': 'ja_123!'
}

def get_selfprogram_info():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = "Unavailable"
    return {
        "program_name": os.path.basename(__file__),
        "repo_folder": os.path.basename(os.getcwd()),
        "device_info": {
            "hostname": socket.gethostname(),
            "ip_address": ip_address,
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine()
        }
    }

def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def download_data_json(service):
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='{JA_DATA_FILE}' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])
    if not files:
        raise Exception(f"{JA_DATA_FILE} not found in Google Drive folder.")
    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(LOCAL_CLIENTS_JSON, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    print(f"✅ Downloaded {JA_DATA_FILE} from Google Drive")

def upload_health_log(service, data):
    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    data["environment"] = get_selfprogram_info()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    filename = f"log/health__ja_db_02__automation__sync_fromdrive__{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='log' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, fields='files(id, name)').execute()
    log_folder_id = response['files'][0]['id'] if response['files'] else None
    if not log_folder_id:
        log_folder = service.files().create(body={
            'name': 'log',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [JAVIS_SHELL_FOLDER_ID]
        }, fields='id').execute()
        log_folder_id = log_folder['id']
    media = MediaFileUpload(filename, mimetype='application/json')
    service.files().create(body={
        'name': os.path.basename(filename),
        'parents': [log_folder_id],
        'mimeType': 'application/json'
    }, media_body=media).execute()
    print(f"📤 Uploaded health log: {filename}")

def sync_data():
    service = get_drive_service()
    download_data_json(service)
    with open(LOCAL_CLIENTS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT client_id, client_name FROM clients")
    existing_clients = cur.fetchall()
    client_map = {name.strip(): cid for cid, name in existing_clients}

    inserted_clients = 0
    inserted_actions = 0
    skipped_duplicates = 0

    for client_name, logs in data.items():
        client_name = client_name.strip()
        client_id = client_map.get(client_name)

        if not client_id:
            client_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO clients (client_id, client_name, last_updated)
                VALUES (%s, %s, NOW())
            """, (client_id, client_name))
            client_map[client_name] = client_id
            inserted_clients += 1

        for log in logs:
            context = log.get("context", "").strip()
            date_str = log.get("date", "").strip()
            if not context:
                continue
            try:
                updated_at = datetime.strptime(date_str, "%Y-%m-%d-%H-%M")
            except:
                continue

            cur.execute("""
                SELECT 1 FROM client_actions
                WHERE client_id = %s AND comment = %s AND updated_at = %s
            """, (client_id, context, updated_at))
            if cur.fetchone():
                skipped_duplicates += 1
                continue

            cur.execute("""
                INSERT INTO client_actions (client_id, action, expected_response, comment, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (client_id, context, None, context, updated_at))
            inserted_actions += 1

    conn.commit()
    cur.close()
    conn.close()

    log_summary = {
        "inserted_clients": inserted_clients,
        "inserted_actions": inserted_actions,
        "skipped_duplicates": skipped_duplicates
    }
    upload_health_log(service, log_summary)
    print("✅ Sync complete")

if __name__ == "__main__":
    while True:
        try:
            sync_data()
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(CHECK_INTERVAL_MINUTES * 60)

