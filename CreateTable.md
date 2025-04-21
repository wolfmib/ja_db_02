
---

### ✅ Step 1: Create `clients` table

```sql
CREATE TABLE clients (
    client_id UUID PRIMARY KEY,
    client_name TEXT NOT NULL,
    mode TEXT CHECK (mode IN ('B2B', 'B2C', 'Both')),
    license_type TEXT CHECK (license_type IN ('Curacao', 'MGA')),
    major_contact TEXT,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);
```

---

### ✅ Step 2: Create `client_actions` table

```sql
CREATE TABLE client_actions (
    action_id SERIAL PRIMARY KEY,
    client_id UUID REFERENCES clients(client_id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    expected_response TEXT,
    comment TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### ✅ Step 3: Create `client_domains` table

```sql
CREATE TABLE client_domains (
    domain_id SERIAL PRIMARY KEY,
    client_id UUID REFERENCES clients(client_id) ON DELETE CASCADE,
    client_name TEXT,
    domain TEXT NOT NULL
);
```

---

### ✅ Step 4: Insert One Fake Row Into Each Table

#### 1. Insert a fake client

```sql
INSERT INTO clients (client_id, client_name, mode, license_type, major_contact)
VALUES ('11111111-1111-1111-1111-111111111111', 'Fake Corp Ltd', 'B2B', 'MGA', 'Jayce');
```

#### 2. Insert a fake action

```sql
INSERT INTO client_actions (client_id, action, expected_response, comment)
VALUES ('11111111-1111-1111-1111-111111111111', 'Send license application reminder', 'Client to confirm submission', 'Sent via email on Monday');
```

#### 3. Insert a fake domain

```sql
INSERT INTO client_domains (client_id, client_name, domain)
VALUES ('11111111-1111-1111-1111-111111111111', 'Fake Corp Ltd', 'fakecorp.io');
```

---

Once that’s done, run:

```sql
\dt
```

To see your 3 tables — and:

```sql
SELECT * FROM clients;
SELECT * FROM client_actions;
SELECT * FROM client_domains;
```

