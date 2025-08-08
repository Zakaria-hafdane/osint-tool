import asyncio
import subprocess
import sys
import json
import os

async def lookup_maigret(username):
    try:
        # Method 1: Direct subprocess call to maigret
        # This bypasses import issues and uses the installed version
        cmd = [
            sys.executable, '-m', 'maigret',
            '--no-color', '--print-found', 
            '--json', '--timeout', '15', 
            '--max-connections', '10',
            username
        ]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=60,
            cwd=os.getcwd()  # Set current working directory
        )
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                # Convert to expected format
                platforms = {}
                for site_name, site_data in data.items():
                    if isinstance(site_data, dict) and site_data.get('url_usable'):
                        platforms[site_name] = site_data['url_usable']
                return platforms
            except json.JSONDecodeError:
                print("Failed to parse maigret JSON output")
                return {}
        else:
            print(f"Maigret command failed: {result.stderr}")
            return {}
            
    except subprocess.TimeoutExpired:
        print("Maigret search timed out")
        return {}
    except Exception as e:
        print(f"Error running maigret: {e}")
        # Try to check if maigret is installed properly
        try:
            # Test if maigret module exists
            import importlib.util
            spec = importlib.util.find_spec('maigret')
            if spec is None:
                print("Maigret is not properly installed")
            else:
                print("Maigret module found but execution failed")
        except Exception as import_error:
            print(f"Import check failed: {import_error}")
        return {}

# Fallback function if maigret fails
async def lookup_maigret_fallback(username):
    """Fallback that just returns empty results gracefully"""
    print("Maigret fallback: No results available")
    return {}