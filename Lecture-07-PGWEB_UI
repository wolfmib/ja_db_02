# Lecture 07: Indexing Optimization Demo with pgweb UI

## 🔄 Overview
This video demonstrates how to visually explore and optimize PostgreSQL query performance using the pgweb browser UI, integrated directly into our Docker Compose setup for `ja_db_02`.

## 🎉 What You'll See in This Lecture

### 1. 🚀 Accessing the pgweb Interface
- After running:
```bash
docker compose up -d
```
- Open [http://localhost:8081](http://localhost:8081) in your browser

### 2. 🔍 Inspecting Table Structures
- View tables:
  - `clients` (Table 1)
  - `client_actions` (Table 2)
  - `client_domains` (Table 3)
- Use the **Structure** tab to review columns and data types

### 3. 🔍 Searching Data Without SQL (ILIKE in UI)
- Go to **Rows** tab
- Use the visual query filter:
  - `column: client_name`
  - `operator: ILIKE`
  - `value: %JA Com%`
- Click **Apply** to find results using wildcard search

### 4. 📈 Running SQL Queries (With and Without Index)
#### 4.1 Unoptimized Query (Before Index)
```sql
EXPLAIN ANALYZE
SELECT * FROM client_actions
WHERE client_id = '...'
ORDER BY updated_at DESC
LIMIT 5;
```
- Observe: `Seq Scan` and higher cost value (e.g. `cost=0.00..12.56`)

#### 4.2 Create an Index
```sql
CREATE INDEX idx_client_actions_client_id_updated_at
ON client_actions (client_id, updated_at DESC);
```

#### 4.3 Optimized Query (After Index)
```sql
EXPLAIN ANALYZE
SELECT * FROM client_actions
WHERE client_id = '...'
ORDER BY updated_at DESC
LIMIT 5;
```
- Observe: `Index Scan` and lower cost (e.g. `cost=0.27..8.62`)

### 5. 🔢 Viewing All Indexes
- Navigate to the **Indexes** tab inside pgweb
- Or run this query:
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'client_actions';
```

### 6. ❌ Deleting an Index for Resetting Demo
- Use this command to drop it before demo:
```sql
DROP INDEX IF EXISTS idx_client_actions_client_id_updated_at;
```

---

## 📚 What You Learn Here
- The real cost difference between sequential scan and index scan
- How PostgreSQL uses indexes under the hood
- When and why to create indexes (and when not to)
- How to view, test, and delete indexes through pgweb UI

---

## 🔹 Final Tip
Use pgweb + `EXPLAIN ANALYZE` as your debugging lens before optimizing any query-heavy system — this is your dev-side microscope 🤍🤓


