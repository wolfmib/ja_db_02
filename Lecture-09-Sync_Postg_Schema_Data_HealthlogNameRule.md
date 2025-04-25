# Lecture 09: Sync PostgreSQL Schema & Data to Google Drive + Health Log Architecture

## 🔄 Overview
In this lecture, we extend the `ja_db_02` automation layer by adding a third helper service for scheduled data/schema sync to Google Drive. We also centralize instance metadata, introduce structured log naming, and demonstrate full Docker-based orchestration.

---

## 🌐 Features Implemented

### 1. ➕ Added Third Helper Script
- **Script Name**: `automation_python_ja_db_02_autosyncbackto_googledrive_helper.py`
- **Purpose**: Sync all current PostgreSQL tables (schema + data) to `GoogleDrive/javis_shell/`
- Auto-detects all base tables dynamically
- Serializes and uploads:
  - `client_info_data.json`, `client_info_schema.json`, etc.

### 2. ✏️ Implemented Standardized Log Naming
- Format: `health_<project>_<appscope>_<instance>_<timestamp>.json`
- Examples:
  - `health_ja_db_02_automation_autocommit_helper_20250424-134500.json`
  - `health_ja_db_02_automation_sync_action_helper_20250424-134500.json`
- This format makes logs **queryable, sortable, and monitor-friendly**

### 3. 📂 Centralized Metadata Logic
- Function: `get_selfprogram_info()` moved to `ja_tool.py`
- Now used across all automation scripts
- Unified fields: program name, repo folder, IP, OS, device ID, etc.
- Result: Easier maintenance, no more per-script hardcoding

### 4. 🔧 Bash-based Automation in Docker
- `docker-compose.yml` updated to:
```yaml
command: bash -c "
  python3 automation_python_ja_db_02_autocommit_helper_server.py &
  python3 automation_python_ja_sync_action_helper_server.py &
  python3 automation_python_ja_db_02_autosyncbackto_googledrive_helper.py
"
```
- Allows 3 concurrent scripts in a single container
- Fully persistent + restartable

### 5. 📚 Live Demo Strategy
- Use:
```bash
docker exec -it ja_db_02-automation-1 bash
```
Then run each helper script manually:
```bash
python3 automation_python_ja_db_02_autocommit_helper_server.py
python3 automation_python_ja_sync_action_helper_server.py
python3 automation_python_ja_db_02_autosyncbackto_googledrive_helper.py
```
- Confirm outputs:
  - Health logs to `/log`
  - JSON files (`_schema.json`, `_data.json`) to root Drive folder

---

## 📊 Result
- Centralized, readable health telemetry
- Scalable automation strategy
- JSON & schema backups every 30 mins
- Clean logs with traceable instance info

---



