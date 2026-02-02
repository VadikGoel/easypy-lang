"""
EPI - EasyPy Installer
A friendly wrapper around PIP for EasyPy users.
"""

import sys
import subprocess
import shutil

def install_package(package_name):
    print(f"📦 [EPI] Attempting to install package: '{package_name}'...")
    
    # Check if pip is available
    if not shutil.which("pip") and not sys.executable:
        print("❌ Error: Python Environment not found. Cannot install packages.")
        return

    try:
        # Try installing via pip
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success! Package '{package_name}' is installed.")
            print(f"\n[INFO] You can now use it in your code like: use {package_name}")
            print(f"[NOTE] If this is not the package you intended, you can search pypi.org")
            print(f"       and use: pip install {package_name}")
        else:
            print(f"⚠️ [EPI] Could not install '{package_name}' automatically.")
            print(f"   Error details: {result.stderr.strip().splitlines()[-1] if result.stderr else 'Unknown error'}")
            print(f"\n[SUGGESTION] Try installing it directly using standard Python command:")
            print(f"   pip install {package_name}")
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: epi <package_name>")
        return

    package = sys.argv[1]
    install_package(package)

if __name__ == "__main__":
    main()
