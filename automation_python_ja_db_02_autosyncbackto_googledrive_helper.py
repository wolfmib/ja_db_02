# health__ja_db_02__automation__syncbackto_gdrive_helper03__

# === Configuration ===
from ja_tool import get_google_env
# google-env
google_env = get_google_env()
SCOPES = google_env["SCOPES"]
JAVIS_SHELL_FOLDER_ID = google_env["JAVIS_SHELL_FOLDER_ID"]
CREDENTIALS_FILE = google_env["CREDENTIALS_FILE"]

# Local env
DRIVE_FOLDER_ID = JAVIS_SHELL_FOLDER_ID # << dupplicase Drive_Folder = main folder
SYNC_INTERVAL_MINUTES = 1


import psycopg2
import json
import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import time
from datetime import datetime, timezone
from ja_tool import get_selfprogram_info



os.makedirs("log", exist_ok=True)







DB_CONFIG = {
    "dbname": "ja_clients",
    "user": "ja_db",
    "password": "ja_123!",
    "host": "db",  # inside Docker use service name
                    #"host": "localhost",
    "port": "5432"
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

def upload_to_drive(file_path, remote_name):
    service = get_drive_service()
    media = MediaFileUpload(file_path, mimetype='application/json')
    file_metadata = {
        'name': remote_name,
        'parents': [DRIVE_FOLDER_ID],
        'mimeType': 'application/json'
    }
    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"✅ Uploaded: {remote_name}")

def export_table_schema_and_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()


    ## issue-apr-2025: we need automatice get current table
    ## ###########  issue2-apr-2025: ja_db need to granted , go you admin and set for him
    """
                    -- issue2-apr-2025: ja_db need to granted , go you admin and set
                    GRANT SELECT ON ALL TABLES IN SCHEMA public TO ja_db;

                    -- Future-proof:
                    ALTER DEFAULT PRIVILEGES IN SCHEMA public
                    GRANT SELECT ON TABLES TO ja_db;

    """
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public'
        AND table_type = 'BASE TABLE'
        AND table_name NOT LIKE 'pg_%'
        AND table_name NOT LIKE 'sql_%';
    """)




    tables = cursor.fetchall()

    print("📋 Tables found in DB:")
    for t in tables:
        print("-", t[0])

 
    for table in tables:
        table_name = table[0]

        # Export schema
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """)
        columns = cursor.fetchall()
        schema = {
            "table": table_name,
            "columns": [col[0] for col in columns],
            "details": [{"name": col[0], "type": col[1], "nullable": col[2]} for col in columns]
        }

        schema_filename = f"{table_name}_schema.json"
        with open(schema_filename, "w") as f:
            json.dump(schema, f, indent=2)
        upload_to_drive(schema_filename, schema_filename)

        # Export data
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]

        ## issue-TypeError: Object of type datetime is not JSON serializable apr-2025
        ####################
        def serialize_row(row):
            return {k: (str(v) if isinstance(v, (datetime, bytes)) else v) for k, v in zip(colnames, row)}

        data = [serialize_row(row) for row in rows]
        ####################
        ## issue-TypeError: Object of type datetime is not JSON serializable apr-2025

        data_filename = f"{table_name}_data.json"
        with open(data_filename, "w") as f:
            json.dump(data, f, indent=2)
        upload_to_drive(data_filename, data_filename)

    cursor.close()
    conn.close()


## ====  Harcode Libaray  Depended get_selfprogram_info() ===
def upload_health_info(service):
    from datetime import datetime, timezone
    import json


    # issue-apr-26-2025, fixed the name read inside ja_tool, the program-name will always display as 'ja_tool..'
    myselfname = os.path.basename(__file__)
    health_data = get_selfprogram_info(myselfname)
    health_data["timestamp"] = datetime.now(timezone.utc).isoformat()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    # renaming base-on guide-01-code apr-2025
    filename = f"health__ja_db_02__automation__syncbackto_gdrive_helper03__{timestamp}.json"


    #fixed issue for the something..
    log_dir = os.path.join(os.getcwd(), "log")
    os.makedirs(log_dir, exist_ok=True)

    openfilename = os.path.join(log_dir, filename)

    with open(openfilename, "w") as f:
        json.dump(health_data, f, indent=2)

    # Upload to same /log folder as before
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='log' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, fields='files(id)').execute()
    log_folder_id = response['files'][0]['id'] if response['files'] else None

    if not log_folder_id:
        file_metadata = {
            'name': 'log',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [JAVIS_SHELL_FOLDER_ID]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        log_folder_id = folder['id']

    media = MediaFileUpload(openfilename, mimetype='application/json')
    file_metadata = {
        'name': filename,
        'parents': [log_folder_id],
        'mimeType': 'application/json'
    }
    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"✅ Uploaded health info: {filename}")



# === Main Loop ===
if __name__ == "__main__":
    service = get_drive_service()
    while True:
        try:
            export_table_schema_and_data()
            upload_health_info(service)
        except Exception as ex:
            print(f"❌ Error: {ex}")

        time.sleep(SYNC_INTERVAL_MINUTES * 60)
