import csv
import os

files = [
    r"c:\Users\kesav\OneDrive\Desktop\project\datasets\archive (1)\A_Z_medicines_dataset_of_India.csv",
    r"c:\Users\kesav\OneDrive\Desktop\project\datasets\archive (2)\diseases.csv"
]

for f in files:
    print(f"--- {os.path.basename(f)} ---")
    if not os.path.exists(f):
        print(f"File not found: {f}")
        continue
        
    try:
        with open(f, mode='r', encoding='utf-8-sig', errors='replace') as file:
            reader = csv.DictReader(file)
            print("Columns:", reader.fieldnames)
            for i, row in enumerate(reader):
                if i == 0:
                    print("Sample Row 1:", row)
                if i >= 2:
                    break
        
        # Count total rows more reliably
        count = 0
        with open(f, 'r', encoding='utf-8-sig', errors='replace') as file:
            for _ in file:
                count += 1
        print(f"Total lines: {count}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
    print("\n")
