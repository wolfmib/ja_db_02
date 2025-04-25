---

## ✅ Step 1: Add Superset to `docker-compose.yml`

Add this **below your other services**:

```yaml
  superset:
    image: apache/superset
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_SECRET_KEY=supersecretkey123
    volumes:
      - ./superset_home:/app/superset_home
    depends_on:
      - db
```

> This will expose Superset on [http://localhost:8088](http://localhost:8088)

---

## ✅ Step 2: Create PostgreSQL Role for Superset

### Connect to Postgres (from host):
```bash
docker exec -it ja_db_02-db-1 psql -U ja_admin -d ja_clients
```

### Then run the following SQL inside `psql`:

```sql
-- Create Superset read-only role
CREATE ROLE bi_superset WITH LOGIN PASSWORD 'bi_superset123!';

-- Allow connection and usage
GRANT CONNECT ON DATABASE ja_clients TO bi_superset;
GRANT USAGE ON SCHEMA public TO bi_superset;

-- Grant read access to all current tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi_superset;

-- Ensure future tables are readable too
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO bi_superset;
```

✅ This user can **read anything** in the DB but **cannot modify or delete anything**.

---

## 🔁 Final Reminder: Rebuild and Restart

```bash
docker compose build
docker compose up -d
```

Then open Superset at:
```bash
http://localhost:8088
```

