import os
import json
import time
import subprocess
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# issue: docker dont need this,
#        but run local, you need this
from dotenv import load_dotenv
load_dotenv()


## Harcode Libaray
import socket
import platform
#import os # <<duplicate

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





# === Configuration ===
SCOPES = ['https://www.googleapis.com/auth/drive']
JAVIS_SHELL_FOLDER_ID = '1sSqu2eQQydKjy-WIZzXfluuk6EoTfAE4'
CREDENTIALS_FILE = 'client_secret_542560336178-nd8m0bre9sl9ak89m6v9n90paj87q4p5.apps.googleusercontent.com.json'
COMMIT_INTERVAL_MINUTES = 1440  # ⏱️ Lets do it one day, its .. 24*60 = 1440 mins  Set your schedule here

# === Get Google Drive Service ===
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

# === Perform Git Commit and Capture Metadata ===
def auto_git_commit():
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"automation updated at {now_str}"


    # load github credential
    github_user = os.getenv("GITHUB_USER")
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPO")  # Must be the full URL like h

    if not (github_user and github_token and github_repo):
        raise Exception("❌ Missing GITHUB_USER, GITHUB_TOKEN, or GITHUB_REPO in environment.")

    # Inject HTTPS URL with token
    secure_url = github_repo.replace("https://", f"https://{github_user}:{github_token}@")
    subprocess.run(["git", "remote", "set-url", "origin", secure_url], check=True)


    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push"], check=True)

    # Get committed files
    result = subprocess.run(["git", "diff", "--name-only", "HEAD~1"], stdout=subprocess.PIPE, check=True)
    changed_files = result.stdout.decode().strip().split("\n")

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "commit_message": commit_msg,
        "changed_files": changed_files
    }

# === Upload Commit Log to Google Drive /log Folder ===
def upload_commit_log(service, log_data):

    # add env 
    log_data["environment"] = get_selfprogram_info()


    # Ensure /log folder exists
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='log' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, fields='files(id)').execute()
    log_folder_id = response['files'][0]['id'] if response['files'] else None

    if not log_folder_id:
        file_metadata = {
            'name': 'log',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [JAVIS_SHELL_FOLDER_ID]
        }
        log_folder = service.files().create(body=file_metadata, fields='id').execute()
        log_folder_id = log_folder['id']

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    log_filename = f'autocommit_ja_db_02_info_{timestamp}.json'
    with open(log_filename, "w") as f:
        json.dump(log_data, f, indent=2)

    media = MediaFileUpload(log_filename, mimetype='application/json')
    file_metadata = {
        'name': log_filename,
        'parents': [log_folder_id],
        'mimeType': 'application/json'
    }
    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"✅ Uploaded commit log: {log_filename}")

# === Main Loop ===
if __name__ == "__main__":
    service = get_drive_service()
    while True:
        try:
            commit_log = auto_git_commit()
            upload_commit_log(service, commit_log)
        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {e}")
        except Exception as ex:
            print(f"❌ Unexpected error: {ex}")
        time.sleep(COMMIT_INTERVAL_MINUTES * 60)

