import csv
import os

DISEASES_CSV = r"c:\Users\kesav\OneDrive\Desktop\project\datasets\archive (2)\diseases.csv"

if os.path.exists(DISEASES_CSV):
    with open(DISEASES_CSV, mode='r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "Dengue" in row['name']:
                print(f"Name: {row['name']}")
                print(f"Primary Symptoms: '{row['symptoms_primary']}'")
                print(f"Secondary Symptoms: '{row['symptoms_secondary']}'")
                break
else:
    print("CSV not found")
