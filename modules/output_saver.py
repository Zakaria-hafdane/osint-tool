# modules/output_saver.py

import json
import os
from datetime import datetime

def save_results(identifier, data, mode="email"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = identifier.replace("@", "_").replace(".", "_")
    filename = f"data/results/{safe_name}_{mode}_{timestamp}.json"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\n💾 Results saved to: {filename}")
