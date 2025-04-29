
# 🧩 ja_db_02  
A PostgreSQL + Superset + Automation stack using Docker & GitHub Actions CI/CD.

---

## 🐳 Install Docker (macOS)  
> _Note: Commands may vary for Linux._

```bash
brew install --cask docker
```

---

## 🛠️ Install Docker Compose (v2 for Apple Silicon)  
```bash
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-darwin-aarch64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

---

## ⚙️ Setup Docker Compose  
All configurations are included in the repository.  
To run the stack:

```bash
docker compose up -d
```

---

## 🧪 Enter the Database Container  

```bash
docker exec -it ja_db_02-db-1 psql -U ja_admin -d ja_clients
# or use the helper:
source docker_enter_jadb-02.sh
```

---

## 🎥 Video Demo Series

### 🔹 Part 1 – Initial Setup & Docker Stack  
Cloned from GitHub: `wolfmib/ja_db_02`  
Spins up:
- PostgreSQL DB  
- Superset  
- PgWeb  
- Python automation services  

▶️ [Watch Video (Part 1)](https://youtu.be/VYFy2XTltWA?si=ftjzkvPWPwukE5Io)  
📏 Length: ~5 mins

---

### 🔹 Part 2 – PostgreSQL, Superset & PgWeb  
Covers:
- Access DB with `docker exec`
- Show DB schema via `\dt`, roles via `\du`
- Use PgWeb as admin UI
- Build real-time dashboards in Superset

▶️ [Watch Video (Part 2)](https://youtu.be/gQzvH8l1FRE?si=SCaPgiBGADC7TeXB)  
📏 Length: ~4 mins  
💡 *You can also skip and explore the `Lectures ` documents directly.*

---

### 🔹 Part 3 – Python Helper Services  

Each helper is containerized with structured logging to `/log`.

#### ✅ `autocommit_helper_server.py`
- Automates daily Git commit & push  
- Sends health log every 30 mins  
- Stores log:  
  ```
  health__ja_db_02__automation__autocommit_helper01__{timestamp}.json
  ```

#### ✅ `sync_action_helper_server.py`
- Downloads `clients.json` from Google Drive  
- Inserts/updates `clients` and `client_actions` tables  
- Tracks inserted vs skipped rows  

#### ✅ `autosyncbackto_googledrive_helper.py`
- Exports ALL PostgreSQL tables (schema + data)  
- Pushes files to Google Drive  
- Sends full-system health log  

▶️ [Watch Video (Part 3)](https://youtu.be/U5m7e9yrAxA?si=0GGNRI1U4ufG2zE1)  
📏 Length: TBD  
💡 *You can also clone the repo and read the `Lectures  ` docuemrnts directly.*

---

L