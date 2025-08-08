# modules/username_lookup.py

import requests

def check_username(username):
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}",
        "Twitter": f"https://www.twitter.com/{username}",
        "GitHub": f"https://www.github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "VSCO": f"https://vsco.co/{username}",
        "Tumblr": f"https://{username}.tumblr.com",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
    }

    found = {}

    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found[platform] = url
                print(f"✅ Found on {platform}: {url}")
            else:
                print(f"❌ Not found on {platform}")
        except requests.RequestException:
            print(f"⚠️ Error checking {platform}")

    return found
