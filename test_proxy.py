from ip_rotator.proxy_manager import ProxyManager

pm = ProxyManager()
proxy = pm.get_random_proxy()

print("🔁 Proxy Used:")
print(proxy)
