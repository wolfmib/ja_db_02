# Lecture 04: AutoCommit + AutoHealth Helper Setup with Docker

## 🔄 Overview
This lecture covers how to fully automate your PostgreSQL-based project using two helper scripts inside Docker:

- `automation_python_ja_sync_action_helper_server.py`  ➔ Syncs `clients.json` from Google Drive to PostgreSQL
- `automation_python_ja_db_02_autocommit_helper_server.py`  ➔ Auto-commits your Git repo daily and uploads a commit log to Google Drive

## 📊 Architecture
```
Docker Compose
├── PostgreSQL DB (ja_db_02-db-1)
└── Automation Service (ja_db_02-automation-1)
     ├── Sync Script (every 10 mins)
     └── Git Auto-Commit Script (every 1440 mins / 24 hours)
```

## 🔧 Setup Instructions

### 1. Add Required Files
Ensure your repo contains the following files:
- `automation_python_ja_sync_action_helper_server.py`
- `automation_python_ja_db_02_autocommit_helper_server.py`
- `.env` with GitHub credentials:

```
GITHUB_USER=wolfmib
GITHUB_TOKEN=ghp_YourTokenHere
GITHUB_REPO=https://github.com/wolfmib/ja_db_02.git
```

### 2. Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Git identity config
RUN git config --global user.name "wolfmib" && \
    git config --global user.email "wolfmib@gmail.com"

COPY . .

RUN pip install --no-cache-dir -r requirements.txt || true
RUN pip install --no-cache-dir google-api-python-client google-auth google-auth-oauthlib psycopg2-binary pandas

CMD ["bash", "-c", "python3 automation_python_ja_sync_action_helper_server.py & python3 automation_python_ja_db_02_autocommit_helper_server.py"]
```

### 3. docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ja_admin
      POSTGRES_PASSWORD: securepass
      POSTGRES_DB: ja_clients
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  automation:
    build: .
    env_file:
      - .env
    volumes:
      - .:/app
    depends_on:
      - db

volumes:
  pgdata:
```

### 4. Run Everything
```bash
docker compose build
docker compose up -d
docker compose logs -f automation
```

## 🎓 What You Learn Here
- How to set up fully autonomous Python services in Docker
- Daily Git push with auto-commit logs to Drive
- GitHub push authentication via token
- De-duplication and database sync from Google Drive

## 🔹 Log Output
Google Drive:
- `/javis_shell/clients.json` ➔ source of truth
- `/javis_shell/log/health_helper_server_*.json` ➔ DB sync logs
- `/javis_shell/log/autocommit_ja_db_02_info_*.json` ➔ Git commit logs

GitHub:
- Commit messages like:
  ```
  automation updated at 2025-04-22 14:24
  ```

## 🚀 Ready to Deploy
One-liner setup:
```bash
git clone https://github.com/wolfmib/ja_db_02.git && cd ja_db_02 && docker compose up -d
```


