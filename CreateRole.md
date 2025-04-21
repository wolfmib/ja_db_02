---

### ✅ Step 1: Create the User and Set Password

In your psql shell:

```sql
CREATE USER ja_db WITH PASSWORD 'ja_123!';
```

---

### ✅ Step 2: Grant Full Access (Edit / Read / Insert / Delete)

We’ll grant permissions **table-by-table** — you can copy-paste all of this together:

```sql
GRANT CONNECT ON DATABASE ja_clients TO ja_db;
GRANT USAGE ON SCHEMA public TO ja_db;

GRANT SELECT, INSERT, UPDATE, DELETE ON clients TO ja_db;
GRANT SELECT, INSERT, UPDATE, DELETE ON client_actions TO ja_db;
GRANT SELECT, INSERT, UPDATE, DELETE ON client_domains TO ja_db;

-- Allow ja_db to use sequences (important for auto-incremented IDs like SERIAL)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ja_db;
```

✅ This gives `ja_db` permission to:
- Query data
- Insert new rows
- Update existing rows
- Delete records
- Use `SERIAL`-based ID generation (for `action_id`, `domain_id`)

---

Once this is done, lets jump to Python and connect using:
```python
psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="ja_clients",
    user="ja_db",
    password="ja_123!"
)
```

Let me know when the permissions are set, and I’ll help you write the ingestion script with one-click table inserts!
