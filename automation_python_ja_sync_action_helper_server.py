import os
import json
import time
import uuid
from datetime import datetime
import psycopg2
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# === Configuration ===
SCOPES = ['https://www.googleapis.com/auth/drive']
JAVIS_SHELL_FOLDER_ID = '1sSqu2eQQydKjy-WIZzXfluuk6EoTfAE4'
CLIENT_SECRET_FILE = 'client_secret_542560336178-nd8m0bre9sl9ak89m6v9n90paj87q4p5.apps.googleusercontent.com.json'
CHECK_INTERVAL_MINUTES = 11
LOCAL_CLIENTS_JSON = 'latest_clients.json'
LOCAL_HEALTH_LOG = 'health_helper_server.json'

# === Database Config ===
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'ja_clients',
    'user': 'ja_db',
    'password': 'ja_123!'
}

# === Google Drive Auth ===
def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

# === Download latest clients.json ===
def download_clients_json(service):
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='clients.json' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])
    if not files:
        raise Exception("clients.json not found in javis_shell.")
    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(LOCAL_CLIENTS_JSON, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    print("✅ Downloaded clients.json from Google Drive")

# === Upload health log to /log ===
def upload_log(service):
    # Find or create 'log' folder inside javis_shell
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='log' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, fields='files(id, name)').execute()
    log_folder_id = response['files'][0]['id'] if response['files'] else None

    if not log_folder_id:
        file_metadata = {
            'name': 'log',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [JAVIS_SHELL_FOLDER_ID]
        }
        log_folder = service.files().create(body=file_metadata, fields='id').execute()
        log_folder_id = log_folder['id']

    media = MediaFileUpload(LOCAL_HEALTH_LOG, mimetype='application/json')
    file_metadata = {
        'name': 'health_helper_server.json',
        'parents': [log_folder_id],
        'mimeType': 'application/json'
    }


    # Always upload a new health log file with timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_metadata['name'] = f'health_ja_db_02_helper_server_{timestamp}.json'

    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"📤 Uploaded new health log: {file_metadata['name']} to /log")



# === Core sync logic ===
def sync_clients_and_actions():
    service = get_drive_service()
    download_clients_json(service)

    with open(LOCAL_CLIENTS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Build client_name → client_id lookup
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

            # Check for duplicates
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

    # Save health log
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "inserted_clients": inserted_clients,
        "inserted_actions": inserted_actions,
        "skipped_duplicates": skipped_duplicates
    }
    with open(LOCAL_HEALTH_LOG, "w") as f:
        json.dump(log, f, indent=2)
    upload_log(service)
    print("✅ Sync complete")

# === Loop forever every X minutes ===
if __name__ == "__main__":
    while True:
        try:
            sync_clients_and_actions()
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(CHECK_INTERVAL_MINUTES * 60)


