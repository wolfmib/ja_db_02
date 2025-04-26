# health__ja_db_02__automation__autocommit_helper01__

# === Configuration ===
from ja_tool import get_google_env
from ja_tool import get_github_env

# google-env
google_env = get_google_env()
SCOPES = google_env["SCOPES"]
JAVIS_SHELL_FOLDER_ID = google_env["JAVIS_SHELL_FOLDER_ID"]
CREDENTIALS_FILE = google_env["CREDENTIALS_FILE"]

# github-env
github_env = get_github_env()
GITHUB_USER=github_env["GITHUB_USER"]
GITHUB_TOKEN=github_env["GITHUB_TOKEN"]
GITHUB_REPO=github_env["GITHUB_REPO"]
    
# Local env
COMMIT_INTERVAL_MINUTES = 1  # ⏱️ Lets do it one day, its .. 24*60 = 1440 mins  Set your schedule here
HEALTH_INTERVAL_MINUTES = 1 # health


import os
import json
import time
import subprocess
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# issue-apr-2025: docker dont need this,
#        but run local, you need this
from dotenv import load_dotenv
load_dotenv()


# issue-apr-2025: despache , use timezone now
from datetime import  timezone


os.makedirs("log", exist_ok=True)


## ==== Harcode Libaray ===
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

## ====  Harcode Libaray  Depended get_selfprogram_info() ===
def upload_health_info(service):
    from datetime import datetime, timezone
    import json

    health_data = get_selfprogram_info()
    health_data["timestamp"] = datetime.now(timezone.utc).isoformat()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")



    filename = f"health__ja_db_02__automation__autocommit_helper01__{timestamp}.json"

    # issue , why the health still in the home, not inside log
    log_dir = os.path.join(os.getcwd(), "log")
    os.makedirs(log_dir, exist_ok=True)
    Openfilename = os.path.join(log_dir, filename)
    print("💡 Writing local health file to:",  Openfilename)


    with open(Openfilename, "w") as f:
        json.dump(health_data, f, indent=2)

    # issue-03 duplicte log  apr-25-2025
    query = f"'{JAVIS_SHELL_FOLDER_ID}' in parents and name='log' and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, fields='files(id, name)').execute()

    log_folder_id = None
    for folder in response.get('files', []):
        if folder['name'] == 'log':
            log_folder_id = folder['id']
            break



    if not log_folder_id:
        file_metadata = {
            'name': 'log',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [JAVIS_SHELL_FOLDER_ID]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        log_folder_id = folder['id']

    media = MediaFileUpload(Openfilename, mimetype='application/json')
    file_metadata = {
        'name': filename,
        'parents': [log_folder_id],
        'mimeType': 'application/json'
    }
    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"✅ Uploaded health info: {Openfilename}")









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
    now = datetime.now(timezone.utc)
    now_str = now.strftime("%Y-%m-%d %H:%M")
    commit_msg = f"automation updated at {now_str}"


    # load github credential
    github_user = GITHUB_USER
    github_token = GITHUB_TOKEN
    github_repo = GITHUB_REPO

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

    ## rename-base-on code-guide-01   apr-2025
    ## put the local to log/

    log_filename = f'action_ja_db_02_automation_autocommit_helper01_{timestamp}.json'

    #fixed issue for the something..
    log_dir = os.path.join(os.getcwd(), "log")
    os.makedirs(log_dir, exist_ok=True)

    openfilename = os.path.join(log_dir, log_filename)
    with open(openfilename, "w") as f:
        json.dump(log_data, f, indent=2)



    # fixed the bug for upload correct path
    media = MediaFileUpload(openfilename, mimetype='application/json')
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
    last_commit_time = time.time()
    last_health_time = time.time()

    while True:
        now = time.time()

        try:
            if now - last_commit_time >= COMMIT_INTERVAL_MINUTES * 60:
                commit_log = auto_git_commit()
                upload_commit_log(service, commit_log)
                last_commit_time = now
                print("Sent Autocommit")

            if now - last_health_time >= HEALTH_INTERVAL_MINUTES * 60:
                upload_health_info(service)
                last_health_time = now
                print("Sent Health")

        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {e}")
        except Exception as ex:
            print(f"❌ Unexpected error: {ex}")

        time.sleep(30)  # check every 30 seconds for responsiveness
