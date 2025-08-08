# ip_rotator/proxy_manager.py

import random

class ProxyManager:
    def __init__(self, proxy_file="ip_rotator/working_proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = self.load_proxies()

    def load_proxies(self):
        try:
            with open(self.proxy_file, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                raise ValueError("❌ Proxy list is empty.")
            return proxies
        except FileNotFoundError:
            print(f"❌ Proxy file not found: {self.proxy_file}")
            return []
        except Exception as e:
            print(f"❌ Failed to load proxies: {e}")
            return []

    def get_random_proxy(self):
        if not self.proxies:
            print("⚠️ No proxies loaded.")
            return None
        proxy = random.choice(self.proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
