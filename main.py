import asyncio
import sys
import traceback

# Import all the modules
from modules.email_lookup import lookup_holehe
from modules.output_saver import save_results
from modules.google_scraper import search_email_google
from modules.username_lookup import check_username
from modules.google_username import search_username_google
from export_to_csv import export_used_only

def main():
    try:
        print("\n🔍 Choose search mode:")
        print("1. Search by Email")
        print("2. Search by Username (basic)")
        print("3. Search by Username on Google")
        print("4. Search by Username with Maigret (Disabled due to installation issues)") 
        mode = input("👉 Enter choice (1/2/3/4): ").strip()

        if mode == "1":
            try:
                email = input("📧 Enter email to scan: ").strip()

                # Holehe
                holehe_result = lookup_holehe(email)
                print("\n📋 Holehe Result:")
                print(holehe_result)

                # Google
                try:
                    google_result = search_email_google(email)
                    print("\n📋 Google Email Search Result:")
                    for query, links in google_result.items():
                        print(f"\n🔸 {query}")
                        for link in links:
                            print(f"   ➤ {link}")
                except Exception as e:
                    print(f"\n⚠️ Google search failed: {e}")
                    google_result = {}

                save_results(email, {
                    "holehe": holehe_result,
                    "google": google_result
                }, mode="email")

                try:
                    export_used_only({
                        "holehe": holehe_result,
                        "google": google_result
                    }, email)
                except Exception as e:
                    print(f"\n⚠️ Export failed: {e}")

            except Exception as e:
                print(f"Error in email search: {e}")
                traceback.print_exc()

        elif mode == "2":
            try:
                username = input("👤 Enter username to scan: ").strip()
                found_accounts = check_username(username)

                print("\n📋 Found Accounts:")
                for platform, url in found_accounts.items():
                    print(f"{platform}: {url}")

                save_results(username, found_accounts, mode="username_basic")
                
            except Exception as e:
                print(f"Error in basic username search: {e}")
                traceback.print_exc()

        elif mode == "3":
            try:
                username = input("👤 Enter username to scan on Google: ").strip()
                print(f"\n🔍 Searching on Google for '{username}'...")
                result = search_username_google(username)

                print("\n📋 Google Results:")
                for query, links in result["queries"].items():
                    print(f"\n🔸 {query}")
                    for link in links:
                        print(f"   ➤ {link}")

                save_results(username, result, mode="username_google")
                
            except Exception as e:
                print(f"Error in Google username search: {e}")
                traceback.print_exc()

        elif mode == "4":
            print("\n⚠️ Maigret functionality disabled due to installation issues")
            print("This feature would search for accounts across social media platforms")
            print("It requires a complex installation that's currently failing")
            print("You can try installing maigret separately: pip install maigret")

        else:
            print("❌ Invalid option.")

    except KeyboardInterrupt:
        print("\n👋 Program interrupted by user")
    except Exception as e:
        print(f"Unexpected error in main function: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()