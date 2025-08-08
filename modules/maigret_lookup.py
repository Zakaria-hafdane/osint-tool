import os
import sys
import asyncio

# 👇 Add path to local maigret folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../maigret')))

from main import maigret
from settings import Settings
from sites import MaigretDatabase

async def lookup_maigret(username):
    settings = Settings()
    settings.max_connections = 10
    settings.timeout = 15
    settings.print_found_only = True
    settings.is_verbose = False
    settings.console_output = False

    db = MaigretDatabase()
    sites_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../maigret/maigret/resources/sites.json'))
    db.load_from_file(sites_path)

    site_dict = db.sites_dict

    results = await maigret(username, site_dict, settings=settings, logger=None)

    platforms = {}
    for site_name, result in results.items():
        if getattr(result, "is_success", False) and getattr(result, "url", None):
            platforms[site_name] = result.url

    return platforms
