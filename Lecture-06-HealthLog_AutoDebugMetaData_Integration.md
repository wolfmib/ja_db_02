# Lecture 06: Health Log + Auto Debug Metadata Integration

## 🔄 Overview
This lecture demonstrates the latest enhancements to our Dockerized automation system:
- ✨ **Automatic health logs** with device metadata
- ✅ Integrated with both: `ja_sync_action_helper_server` and `ja_db_02_autocommit_helper_server`
- ⬆️ Uploads real-time JSON logs to Google Drive `/log/`

## 🌐 Use Cases
- Real-time observability for different scripts and services
- Identify which machine / repo is sending health updates
- Debug missing or duplicated actions at-a-glance

## 📂 Output: Sample Health Logs

### Health Log from `automation_python_ja_sync_action_helper_server.py`
```json
{
  "timestamp": "2025-04-23T08:57:36.886293",
  "inserted_clients": 0,
  "inserted_actions": 1,
  "skipped_duplicates": 295,
  "environment": {
    "program_name": "automation_python_ja_sync_action_helper_server.py",
    "repo_folder": "ja_db_02",
    "device_info": {
      "hostname": "Johnny-MacMini-Work-Stataion.local",
      "ip_address": "Unavailable",
      "os": "Darwin",
      "os_version": "Darwin Kernel Version 23.3.0...",
      "machine": "arm64"
    }
  }
}
```

### Health Log from `automation_python_ja_db_02_autocommit_helper_server.py`
```json
{
  "program_name": "automation_python_ja_db_02_autocommit_helper_server.py",
  "repo_folder": "ja_db_02",
  "device_info": {
    "hostname": "Johnny-MacMini-Work-Stataion.local",
    "ip_address": "Unavailable",
    "os": "Darwin",
    "os_version": "Darwin Kernel Version 23.3.0...",
    "machine": "arm64"
  },
  "timestamp": "2025-04-23T08:11:47.001688+00:00"
}
```

## 🚀 Where the Logs Go
- Uploaded to: `Google Drive > javis_shell > log`
- Naming format:
  - `health_ja_db_02_helper_server-01_<timestamp>.json`
  - `health_ja_db_02_helper_server-02_<timestamp>.json`

## 📅 Interval Control
- `automation_python_ja_sync_action_helper_server.py`
  - Runs every 10 minutes
  - Logs DB ingestion stats + system environment
- `automation_python_ja_db_02_autocommit_helper_server.py`
  - Runs once daily
  - Logs current repo + GitHub auto-push results

## 🔄 Next Steps (for the video demo)
- Show `.env` setup and Dockerfile logic
- Run `docker compose build && down && up -d`
- Check `/log` folder in Google Drive for fresh JSON logs
- Open logs in browser to highlight metadata


---


