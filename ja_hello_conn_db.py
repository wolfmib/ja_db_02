import psycopg2
import uuid
from datetime import datetime

# === Connect to PostgreSQL ===
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="ja_clients",
    user="ja_db",
    password="ja_123!"
)

cur = conn.cursor()

# === Generate a fake client_id (UUID) ===
client_id = str(uuid.uuid4())

# === Insert into clients table ===
cur.execute("""
    INSERT INTO clients (client_id, client_name, mode, license_type, major_contact)
    VALUES (%s, %s, %s, %s, %s)
""", (client_id, "Hello World Corp", "Both", "Curacao", "Alex"))

# === Insert into client_actions table ===
cur.execute("""
    INSERT INTO client_actions (client_id, action, expected_response, comment)
    VALUES (%s, %s, %s, %s)
""", (client_id, "Initial kickoff email", "Client to provide required docs", "First follow-up done."))

# === Insert into client_domains table ===
cur.execute("""
    INSERT INTO client_domains (client_id, client_name, domain)
    VALUES (%s, %s, %s)
""", (client_id, "Hello World Corp", "helloworld.ai"))

# === Commit and close ===
conn.commit()
cur.close()
conn.close()

print("✅ Inserted one fake row in all three tables successfully!")

