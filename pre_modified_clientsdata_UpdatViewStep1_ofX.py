import pandas as pd
import random
from faker import Faker

# Load CSV
file_path = "v_client_actions_with_names.csv"
df = pd.read_csv(file_path)

# Initialize Faker
fake = Faker()

# Step 1: Create consistent anonymized names per original client_name
unique_client_names = df["client_name"].unique()
name_map = {
    original: fake.company() + " " + random.choice(["Corp", "Ltd", "Group", "Holdings", "Ventures"])
    for original in unique_client_names
}
df["client_name"] = df["client_name"].map(name_map)

# Step 2: Anonymize action and copy to comment
def anonymize_action(text):
    if isinstance(text, str):
        replacements = {
            "email": "notice",
            "submission": "update",
            "reminder": "alert",
            "contact": "reach-out",
            "token": "identifier"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
    return text

df["action"] = df["action"].apply(anonymize_action)
df["comment"] = df["action"]  # Copy anonymized action to comment

# Save to new demo file
output_path = "demo_use_fake_v_client_actions_with_names.csv"
df.to_csv(output_path, index=False)
print(f"✅ Anonymized data saved to: {output_path}")
