import pandas as pd
import os

# Exactly matching your screenshot paths
csv_path = "./data/master_clauses.csv"
txt_folder = "./data/full_contract_txt 2/full_contract_txt"  # Exact name with the space and inner folder!

print("Loading Master Clauses CSV...")
df = pd.read_csv(csv_path)

print(f"Total contracts listed in CSV: {len(df)}")

# Let's check the very first contract in your CSV
first_filename = df.iloc[0]['Filename']
# Ensure it looks for a .txt file
txt_filename = first_filename.replace(".pdf", ".txt")
full_path = os.path.join(txt_folder, txt_filename)

if os.path.exists(full_path):
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print("\n--- SUCCESS! SYSTEM IS CONNECTED ---")
    print(f"File found: {txt_filename}")
    print(f"Contract Length: {len(content)} characters.")
    print(f"Sample Text: {content[:200]}...")
else:
    print(f"\n[ERROR] Could not find file at: {full_path}")
    print("Check if your folder name has the space correctly!")
