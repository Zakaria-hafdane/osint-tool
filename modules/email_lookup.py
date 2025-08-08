import requests

def lookup_emailrep(email):
    print(f"🔍 Checking EmailRep.io for: {email}")
    try:
        response = requests.get(f"https://emailrep.io/{email}", headers={"User-Agent": "osint-tool"})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"EmailRep returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

import subprocess

def lookup_holehe(email):
    print(f"\n🔍 Running Holehe for: {email}")
    try:
        result = subprocess.run(
            ["holehe", email],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"❌ Error: {result.stderr}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"
