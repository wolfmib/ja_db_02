Let's go! Here's how you can do both steps directly from the `psql` prompt:

---

### ✅ 1. 🔍 **Blur (LIKE) Search in Table 1 (`clients`)**

Suppose you're looking for a client with partial name like `"will land"`:

```sql
SELECT client_id, client_name
FROM clients
WHERE client_name ILIKE '%will la%';
```

> - `ILIKE` = case-insensitive LIKE  
> - `%` is the wildcard (matches any sequence of characters)

---

### ✅ 2. 🔁 Use `client_id` to Get Latest 10 Actions from Table 2

Suppose the result from step 1 gave you:

```
client_id = 'abc123...'
```

Then run:

```sql
SELECT *
FROM client_actions
WHERE client_id = 'abc123...'
ORDER BY updated_at DESC
LIMIT 10;
```

---

### 🧠 Pro Tip: Combine Both Steps into One Query

```sql
SELECT ca.*
FROM client_actions ca
JOIN clients c ON ca.client_id = c.client_id
WHERE c.client_name ILIKE '%will lan%'
ORDER BY ca.updated_at DESC
LIMIT 10;
```


---

