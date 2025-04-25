import socket
import platform
import os



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
