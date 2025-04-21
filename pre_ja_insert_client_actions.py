import json
import psycopg2
from datetime import datetime

# === DB Connect ===
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="ja_clients",
    user="ja_db",
    password="ja_123!"
)
cur = conn.cursor()

# === Step 1: Load all client_ids into a lookup dict ===
cur.execute("SELECT client_id, client_name FROM clients")
client_rows = cur.fetchall()
client_lookup = {name.strip(): cid for cid, name in client_rows}

# === Step 2: Load JSON ===
with open("clients.json", "r", encoding="utf-8") as f:
    data = json.load(f)

insert_count = 0
for client_name, logs in data.items():
    client_id = client_lookup.get(client_name.strip())
    if not client_id:
        print(f"⚠️ Skipping unknown client: {client_name}")
        continue

    for log in logs:
        context = log.get("context", "").strip()
        date_str = log.get("date", "").strip()

        if not context:
            continue  # skip empty comment

        try:
            updated_at = datetime.strptime(date_str, "%Y-%m-%d-%H-%M")
        except Exception as e:
            print(f"⚠️ Bad date format for {client_name}: {date_str}")
            continue

        cur.execute("""
            INSERT INTO client_actions (client_id, action, expected_response, comment, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            client_id,
            context,  
            None,
            context,
            updated_at
        ))
        insert_count += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {insert_count} client_actions into the DB!")

