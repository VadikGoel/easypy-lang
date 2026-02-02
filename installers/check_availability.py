import requests
import sys

package_name = "easypy-lang"
url = f"https://pypi.org/pypi/{package_name}/json"

print(f"Checking availability for '{package_name}'...")

try:
    response = requests.get(url)
    if response.status_code == 200:
        print(f"❌ BAD NEWS: The name '{package_name}' is ALREADY TAKEN on PyPI!")
        print("   You cannot upload with this name unless you own it.")
        print("   Please change 'name=' in setup.py to something else.")
        sys.exit(1)
    elif response.status_code == 404:
        print(f"✅ GOOD NEWS: The name '{package_name}' is AVAILABLE!")
        print("   The 403 error is definitely a Password/Token issue.")
        sys.exit(0)
    else:
        print(f"❓ ALL: Got status code {response.status_code}")
except Exception as e:
    print(f"Error checking: {e}")
