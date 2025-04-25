import socket
import platform
import os



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
