# Dockerfile for auto-running both Python automation scripts
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (including git)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*


# Set Git identity for auto commits
RUN git config --global user.name "wolfmib" && \
    git config --global user.email "wolfmib@gmail.com"


# Copy your repo files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || true
RUN pip install --no-cache-dir google-api-python-client google-auth google-auth-oauthlib psycopg2-binary pandas

# Run both scripts in the background
CMD ["bash", "-c", "python3 automation_python_ja_sync_action_helper_server.py & python3 automation_python_ja_db_02_autocommit_helper_server.py"]

