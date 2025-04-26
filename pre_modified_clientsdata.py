import pandas as pd
import random
from faker import Faker
import os

# Load CSV
file_path = "v_client_actions_with_names.csv"
df = pd.read_csv(file_path)

# Initialize Faker
fake = Faker()

# Function to anonymize names
def anonymize_name(original_name):
    # Add slight modifications for realism
    fake_suffix = random.choice([" Corp", " Ltd", " Intl", " Group", " Ventures"])
    return fake.company() + fake_suffix

# Apply anonymization
if "client_name" in df.columns:
    df["client_name"] = df["client_name"].apply(anonymize_name)

# Slightly modify 'action' or 'context' columns if they exist
def anonymize_text(text):
    if isinstance(text, str):
        return text.replace("email", "notice").replace("submission", "update")
    return text

for col in df.columns:
    if any(key in col.lower() for key in ["action", "context", "response"]):
        df[col] = df[col].apply(anonymize_text)

# Save the anonymized CSV
output_path = "demo_use_fake_v_client_actions_with_names.csv"
df.to_csv(output_path, index=False)
print(output_path,"done!!")

#import ace_tools as tools; tools.display_dataframe_to_user(name="Demo-Fake-Data Client Actions View", dataframe=df)

