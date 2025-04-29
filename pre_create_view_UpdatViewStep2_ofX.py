import psycopg2
import csv

# Database connection , Creaet Talbe, u need ja_admin
conn = psycopg2.connect(
    host="localhost",
    port=15432,
    dbname="ja_clients",
    user="ja_admin",  # use the superuser
    password="securepass"  # replace with the actual password
)
cur = conn.cursor()

# Define the table name you want to create
table_name = "demo_v_client_actions"

# Step 1: Drop the existing table if it exists
cur.execute(f"DROP TABLE IF EXISTS {table_name};")


"""
csv: updated_at	action_id	client_id	client_name	action	expected_response	comment

-------------------+--------------------------+-----------+----------+---------
 updated_at        | timestamp with time zone |           |          | 
 action_id         | integer                  |           |          | 
 client_id         | uuid                     |           |          | 
 client_name       | text                     |           |          | 
 action            | text                     |           |          | 
 expected_response | text                     |           |          | 
 comment           | text                     |      
"""
# Step 2: Create a simplified table matching the actual CSV structure
cur.execute(f"""
    CREATE TABLE {table_name} (
        updated_at TIMESTAMPTZ,
        action_id INTEGER,
        client_id UUID,
        client_name TEXT,
        action TEXT,
        expected_response TEXT,
        comment TEXT
    );
""")

# Step 3: Read from CSV and insert data accordingly
with open("demo_use_fake_v_client_actions_with_names.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute(f"""
            INSERT INTO {table_name} (updated_at, action_id, client_id, client_name, action, expected_response, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            row['updated_at'],
            int(row['action_id']) if row['action_id'] else None,
            row['client_id'],
            row['client_name'],
            row['action'],
            row['expected_response'],
            row['comment']
        ))

# Step 4: Commit changes and close
conn.commit()
cur.close()
conn.close()

print(f"✅ Table `{table_name}` created and populated from demo CSV.")

