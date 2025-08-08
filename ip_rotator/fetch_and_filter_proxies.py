# ip_rotator/fetch_and_filter_proxies.py

import requests
import concurrent.futures
import os
import psutil
import speedtest

# =============================
# 📊 SYSTEM ANALYSIS FUNCTIONS
# =============================

def get_cpu_threads():
    return os.cpu_count()

def get_ram_gb():
    return round(psutil.virtual_memory().total / (1024 ** 3))

def get_internet_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Mbps
        return round(download_speed)
    except Exception:
        return 50  # fallback value

def estimate_threads(cpu_threads, ram_gb, internet_mbps):
    cpu_score = cpu_threads * 2
    ram_score = ram_gb * 2
    net_score = internet_mbps / 2
    estimated = int(cpu_score + ram_score + net_score)
    return max(50, min(estimated, 400))

# =============================
# 🌐 PROXY FETCH & TEST
# =============================

def fetch_proxies():
    print("📥 Fetching proxies...")
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=2000&country=all"
    ]
    proxies = set()
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            proxies.update(response.text.strip().splitlines())
        except Exception as e:
            print(f"❌ Failed to fetch from {url}: {e}")
    return list(proxies)

def test_proxy(proxy):
    url = "https://www.google.com"
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        r = requests.get(url, proxies=proxies, timeout=7)
        if r.status_code == 200:
            print(f"✅ {proxy}")
            return proxy
    except:
        pass
    return None

def save_working_proxies(valid_proxies, path="ip_rotator/working_proxies.txt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for proxy in valid_proxies:
            f.write(proxy + "\n")
    print(f"\n💾 Saved {len(valid_proxies)} working proxies to {path}")

# =============================
# 🚀 MAIN
# =============================

if __name__ == "__main__":
    cpu = get_cpu_threads()
    ram = get_ram_gb()
    net = get_internet_speed()

    print(f"\n🧠 CPU Threads: {cpu}")
    print(f"💾 RAM: {ram} GB")
    print(f"🌐 Internet Speed: {net} Mbps")

    max_threads = estimate_threads(cpu, ram, net)
    print(f"\n✅ Using {max_threads} threads...\n")

    proxy_list = fetch_proxies()
    print(f"🔍 Testing {len(proxy_list)} proxies...")

    valid_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(test_proxy, proxy) for proxy in proxy_list]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_proxies.append(result)

    save_working_proxies(valid_proxies)
