def check_username(username):
    """
    Simple username checker that returns predefined URLs
    """
    # Return a simple set of URLs for demonstration
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
    }
    
    return platforms