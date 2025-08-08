import asyncio  # ✅ REQUIRED for Maigret

from modules.email_lookup import lookup_holehe
from modules.output_saver import save_results
from modules.google_scraper import search_email_google
from modules.username_lookup import check_username
from modules.google_username import search_username_google
from export_to_csv import export_used_only
from modules.maigret_lookup import lookup_maigret  # Maigret

def main():
    print("\n🔍 Choose search mode:")
    print("1. Search by Email")
    print("2. Search by Username (basic)")
    print("3. Search by Username on Google")
    print("4. Search by Username with Maigret") 
    mode = input("👉 Enter choice (1/2/3/4): ").strip()

    if mode == "1":
        email = input("📧 Enter email to scan: ").strip()

        # Holehe
        holehe_result = lookup_holehe(email)
        print("\n📋 Holehe Result:")
        print(holehe_result)

        # Google
        google_result = search_email_google(email)
        print("\n📋 Google Email Search Result:")
        for query, links in google_result.items():
            print(f"\n🔸 {query}")
            for link in links:
                print(f"   ➤ {link}")

        save_results(email, {
            "holehe": holehe_result,
            "google": google_result
        }, mode="email")

        export_used_only({
            "holehe": holehe_result,
            "google": google_result
        }, email)

    elif mode == "2":
        username = input("👤 Enter username to scan: ").strip()
        found_accounts = check_username(username)

        print("\n📋 Found Accounts:")
        for platform, url in found_accounts.items():
            print(f"{platform}: {url}")

        save_results(username, found_accounts, mode="username_basic")

    elif mode == "3":
        username = input("👤 Enter username to scan on Google: ").strip()
        result = search_username_google(username)

        print("\n📋 Google Results:")
        for query, links in result["queries"].items():
            print(f"\n🔸 {query}")
            for link in links:
                print(f"   ➤ {link}")

        save_results(username, result, mode="username_google")

    elif mode == "4":
        username = input("👤 Enter username for Maigret scan: ").strip()
        print("\n🔍 Scanning with Maigret...")

        results = asyncio.run(lookup_maigret(username))

        if not results:
            print("❌ No results found.")
        else:
            print("\n📋 Maigret Results:")
            for platform, url in results.items():
                print(f"{platform}: {url}")

        save_results(username, results, mode="maigret")

    else:
        print("❌ Invalid option.")

if __name__ == "__main__":
    main()
