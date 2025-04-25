# Lecture 08: Superset Real-Time Dashboard Integration

## 🔄 Overview
This lecture demonstrates how to use **Apache Superset** to visualize PostgreSQL data in real time, using the `ja_clients` database as the backend. It includes a full walkthrough of dataset creation, data joining, and dashboard building inside Superset.

## 🚀 Objectives
- Integrate Superset with Dockerized PostgreSQL
- Create a reusable view for `client_name` display
- Build and display three key widgets for a real-time dashboard

---

## 📂 Datasets Used
1. `v_client_actions_with_names` – A SQL view joining `client_actions` with `clients` to replace `client_id` with readable `client_name`
2. Connected through Superset to PostgreSQL using the `bi_superset` read-only user

---

## 📊 Final Dashboard: `JA-Real-Time-Dash-01`

### 1. 📈 **Recent Client Actions** (Table)
- Query Mode: **RAW RECORDS**
- Columns: `client_name`, `comment`, `updated_at`
- Sort by: `updated_at DESC`
- Row Limit: `10`
- Purpose: Display the latest synced communication with each client

### 2. 🔹 **Top Active Clients** (Bar Chart)
- X-Axis: `client_name`
- Metric: `COUNT(*)`
- Sort By: `COUNT(*) DESC`
- Filters: Optional date range (`updated_at`)
- Series Limit: `10`
- Purpose: Visualize clients with the highest interaction volume

### 3. 📊 **Clients Activated Today** (Big Number)
- Metric: `COUNT_DISTINCT(client_id)`
- Time Range: `Today`
- Title: `Live Today`
- Purpose: Highlight unique clients that had activity today

---

## ⚙️ Auto-Refresh Setup
- Dashboard set to refresh every **5 minutes**
- Toggle in the dashboard settings (top right)

---

## 🔹 Result
A professional, real-time BI dashboard for license activity and internal task tracking that runs locally with Docker, using read-only access via `bi_superset`.

---

## 🎥 Suggested Video Demo Points
- Show dataset creation and the view in pgweb
- Explain sorting and grouping logic in the chart editors
- Highlight the value of replacing UUIDs with readable names
- Toggle refresh and showcase auto-updating metrics

---




