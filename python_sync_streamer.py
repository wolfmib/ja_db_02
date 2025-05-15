# python_sync_streamer.py

import os
import json
from kafka import KafkaProducer
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# === CONFIG ===
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secret_542560336178-nd8m0bre9sl9ak89m6v9n90paj87q4p5.apps.googleusercontent.com.json'
FOLDER_ID = '1sSqu2eQQydKjy-WIZzXfluuk6EoTfAE4'
TOPIC = 'ja_commit_collection'
KAFKA_SERVER = 'kafka:9092'  # or 'kafka:9092' if run inside Docker

# === Get Drive Service ===
def get_drive_service():
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        raise Exception("Missing token.json")
    return build('drive', 'v3', credentials=creds)

# === List all *__commit__*.json files ===
def list_commit_json_files(service):
    query = f"'{FOLDER_ID}' in parents and name contains '__commit__' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

# === Download JSON file ===
def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return fh.getvalue().decode()

# === Send to Kafka ===
def send_to_kafka(producer, json_str, key=None):
    producer.send(TOPIC, key=key.encode() if key else None, value=json_str.encode())
    producer.flush()

# === MAIN ===
def main():
    service = get_drive_service()
    files = list_commit_json_files(service)

    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)



    print(f"📦 Found {len(files)} commit JSONs...")
    for f in files:
        name = f['name']
        if '__commit__' not in name:
            continue

        try:
            parts = name.replace('.json', '').split('__')
            repo_name = parts[0]
            branch_name = parts[1]
            timestamp = parts[3]  # ignore 'commit' middle part

            print(f"→ Sending: {name}")
            content = download_file(service, f['id'])
            data = json.loads(content)

            # Optional check: validate essential fields
            required_keys = ['repo_id', 'repo_name', 'current_branch', 'commit_sha', 'commit_message', 'updated_at']
            if not all(k in data for k in required_keys):
                print(f"⚠️ Skipped (missing fields): {name}")
                continue

            # Push to Kafka with repo_name as key
            send_to_kafka(producer, content, key=repo_name)

        except Exception as e:
            print(f"❌ Error processing {name}: {e}")


    print("✅ All commit logs sent to Kafka.")

if __name__ == "__main__":
    main()

