import json
import uuid
import psycopg2
from datetime import datetime

import pandas as pd

# === DB Connection ===
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="ja_clients",
    user="ja_db",
    password="ja_123!"
)
cur = conn.cursor()

# === Load and flatten clients.json ===
with open("clients.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === Extract unique client names ===
client_names = list(set(data.keys()))
df = pd.DataFrame(client_names, columns=["client_name"])

print(f"📝 {len(df)} unique client names loaded.")

# === Insert into clients table ===
inserted_count = 0
for name in df["client_name"]:
    client_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO clients (client_id, client_name, mode, license_type, major_contact, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (client_id) DO NOTHING
    """, (
        client_id,
        name,
        None,
        None,
        None,
        datetime.now()
    ))
    inserted_count += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {inserted_count} clients into the database.")

