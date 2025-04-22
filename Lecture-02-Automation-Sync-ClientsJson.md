



# Go to GCP platform get your credential first ...

client_secret_542560336178-ndxxxxxxxxxxxxxxxxxxxx7q4p5.apps.googleusercontent.com.json

# double check you have following package
pip install psycopg2-binary google-api-python-client google-auth google-auth-oauthlib pandas

# Run the helper
python3 automation_python_ja_sync_action_helper_server.py

# you can scheudle the time, current setting 10 mins




## Note

---

### ✅ What the Script Will Do

1. **Every X minutes (default 10)**:
   - Download latest `clients.json` from your `javis_shell` Google Drive folder.

2. **Process the JSON**:
   - For each `client_name`, check if it exists in Table 1:
     - If not, insert a new record in `clients`.
   - For each `context + date` log:
     - Check if the combo already exists in `client_actions`.
     - If not, insert a new row (with comment in both `action` and `comment` for now).

3. **Log Results to** `health_helper_server.json`
   - Example:
     ```json
     {
       "timestamp": "2025-04-21T15:01:02",
       "inserted_clients": 2,
       "inserted_actions": 18,
       "skipped_duplicates": 55
     }
     ```

4. **Upload the log file** to Google Drive:
   - Folder: `javis_shell/log/`

---

### 🧠 Bonus Design Features

- **Drive Folder ID for `log`** will be auto-queried from `javis_shell`
- You can adjust the **check frequency** via a variable like `CHECK_INTERVAL_MINUTES = 10`
- Simple retry logic in case of Drive API errors or DB issues

---


# Yes Jason have recorded demo-video apr-2025
