import json
import csv
import os
from glob import glob

def export_used_only():
    result_files = sorted(glob("data/results/*_email_*.json"), key=os.path.getmtime, reverse=True)
    if not result_files:
        print("❌ No result files found.")
        return

    latest_file = result_files[0]
    print(f"📂 Using latest result: {latest_file}")

    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base_name = os.path.splitext(os.path.basename(latest_file))[0]
    csv_file = f"data/results/{base_name}_USED_AND_LIMITED.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Platform", "Result", "Source"])

        holehe_lines = data['holehe'].splitlines()
        for line in holehe_lines:
            if line.startswith("[") and "]" in line:
                symbol, platform = line.split("]", 1)
                symbol = symbol.strip("[")
                platform = platform.strip()

                if symbol == "+":
                    writer.writerow([platform, "Used", "Holehe"])
                elif symbol == "x":
                    writer.writerow([platform, "Rate Limited", "Holehe"])
                # skip [-]

        for query, results in data['google'].items():
            for result in results:
                if not result.startswith("❌") and not result.startswith("Error"):
                    writer.writerow([query, result, "Google"])

    print(f"✅ Export complete: {csv_file}")

# 🔁 Execute if run directly
if __name__ == "__main__":
    export_used_only()
