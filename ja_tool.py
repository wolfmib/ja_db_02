# ja_tool.py
import socket
import platform
import os



from dotenv import load_dotenv

# Load .env in both local and Docker-friendly ways
load_dotenv()  # Works locally



def get_custom_env():

    data_jsonfilename = os.getenv("JA_DATA_FILE")

    missing = []
    if not data_jsonfilename:
        missing.append("- JA_DATA_FILE is not set. Example: 'clients.json'")
  
    if missing:
        raise ValueError("\n\n[❌ SELF-CUSTOM Env Missing Configuration]\n" + "\n".join(missing))

    return {
        "JA_DATA_FILE": data_jsonfilename,
    }

  



# Example .env setup for Google API integration:
# GOOGLE_SCOPES=https://www.googleapis.com/auth/drive
# JAVIS_SHELL_FOLDER_ID=1sSqu2eQQydKjy-WIZzXfluuk6EoTfAE4
# GOOGLE_CREDENTIALS_FILE=client_secret_542560336178-johnny-xxxxxxxx.xxxxxxx.apps.googleusercontent.com.json

def get_google_env():
    """
    Returns Google API configuration from environment variables or default fallback.
    If any required variable is missing, raises a ValueError with guidance.
    Automatically loads .env (recommended for both local and container use).
    """
    scope = os.getenv("GOOGLE_SCOPES")
    folder_id = os.getenv("JAVIS_SHELL_FOLDER_ID")
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")

    missing = []
    if not scope:
        missing.append("- GOOGLE_SCOPES is not set. Example: 'https://www.googleapis.com/auth/drive'")
    if not folder_id:
        missing.append("- JAVIS_SHELL_FOLDER_ID is not set. Please copy your Google Drive folder ID.")
    if not credentials_file:
        missing.append("- GOOGLE_CREDENTIALS_FILE is not set. Example: 'client_secret_...json'")

    if missing:
        raise ValueError("\n\n[❌ Google Env Missing Configuration]\n" + "\n".join(missing))

    return {
        "SCOPES": [scope],
        "JAVIS_SHELL_FOLDER_ID": folder_id,
        "CREDENTIALS_FILE": credentials_file
    }


def get_github_env():
    """
    Returns github-api
    """
    github_user = os.getenv("GITHUB_USER")
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPO")

    missing = []
    if not github_user:
        missing.append("- GITHUB_USER is not set. Example: 'wolfmib'")
    if not github_token:
        missing.append("-  GITHUB_TOKEN is not set. Please create your git-hub-token")
    if not github_repo:
        missing.append("- GITHUB_REPO is not set. Example: 'https://github.com/wolfmib/ja_db_02.git'")

    if missing:
        raise ValueError("\n\n[❌ GITHUB Env Missing Configuration]\n" + "\n".join(missing))

    return {
        "GITHUB_USER": github_user,
        "GITHUB_TOKEN": github_token,
        "GITHUB_REPO": github_repo
    } 



# Future ready:
# def get_slack_env(): ...
# def get_db_env(): ...








def get_selfprogram_info(i_pass_programname):
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = "Unavailable"

    return {
        "program_name":  i_pass_programname,#os.path.basename(__file__),
        "repo_folder": os.path.basename(os.getcwd()),
        "device_info": {
            "hostname": socket.gethostname(),
            "ip_address": ip_address,
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine()
        }
    }
