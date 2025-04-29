import json
import random
from datetime import datetime, timedelta
import os

# Predefined context templates for different domains
DOMAIN_CONTEXTS = {
    "medical": [
        "Patient consultation completed",
        "Diagnosis updated",
        "Lab results received",
        "Follow-up scheduled",
        "Prescription issued"
    ],
    "gaming": [
        "Player level up",
        "New achievement unlocked",
        "Purchase confirmed",
        "Tournament joined",
        "Account status updated"
    ],
    "commerce": [
        "Order placed",
        "Payment confirmed",
        "Item shipped",
        "Return requested",
        "Customer support ticket created"
    ],
    "legal": [
        "Document reviewed",
        "Client meeting scheduled",
        "Case status updated",
        "Filing submitted",
        "Feedback received"
    ]
}

# Ask developer for business area
area = input("What is your business area? (e.g., medical, gaming, commerce, legal): ").strip().lower()
if area not in DOMAIN_CONTEXTS:
    print(f"❌ Area '{area}' not recognized. Available options: {', '.join(DOMAIN_CONTEXTS.keys())}")
    exit(1)

# Generate 500 rows of fake data
num_entries = 500
clients_json = {}

for _ in range(num_entries):
    object_name = f"{area.title()} Object {_+1}"
    logs = []
    date_base = datetime.now() - timedelta(days=random.randint(0, 60))
    for i in range(random.randint(1, 5)):  # 1 to 5 logs per object
        log_time = date_base + timedelta(days=i, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        log_entry = {
            "context": random.choice(DOMAIN_CONTEXTS[area]),
            "date": log_time.strftime("%Y-%m-%d-%H-%M")
        }
        logs.append(log_entry)
    clients_json[object_name] = logs

# Save to clients.json
with open("clients.json", "w") as f:
    json.dump(clients_json, f, indent=2)

print("✅ Generated 500+ rows of synthetic data into clients.json")
