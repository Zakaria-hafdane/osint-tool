# modules/google_username.py

import random
import requests
import re
import time
from bs4 import BeautifulSoup
from ip_rotator.proxy_manager import ProxyManager

proxy_manager = ProxyManager()

headers = {
    "User-Agent": "Mozilla/5.0"
}

def search_username_google(username, num_results=15):
    queries = [
        f'"{username}"',
        f'intitle:{username}',
        f'inurl:{username}',
        f'"{username}" profile',
        f'"{username}" user',
        f'"{username}" account'
    ]

    results = {}
    MAX_RETRIES = 3

    for query in queries:
        print(f"\n🔎 Searching Google: {query}")
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
        success = False

        for attempt in range(MAX_RETRIES):
            proxy = proxy_manager.get_random_proxy()
            print(f"🔁 Attempt {attempt+1}/{MAX_RETRIES} using proxy: {proxy}")

            try:
                response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                links = []

                for a in soup.find_all('a'):
                    href = a.get('href')
                    if href and href.startswith("/url?q="):
                        clean_link = re.split(r"&", href.replace("/url?q=", ""))[0]
                        links.append(clean_link)

                results[query] = links if links else ["❌ No results found."]
                success = True
                break

            except Exception as e:
                print(f"⚠️ Proxy failed: {e}")
                if attempt == MAX_RETRIES - 1:
                    results[query] = [f"Error: {str(e)}"]

            time.sleep(1)

        time.sleep(random.uniform(2, 4))

    return results
