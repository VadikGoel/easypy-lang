"""
Easypy Real Modules
Implementations that perform ACTUAL system actions
"""

import sys
import os
import time
import json
import threading

# Global Aliases for Easypy -> Python compatibility
true = True
false = False
null = None

# Built-in String Helpers
def upper(s): return str(s).upper()
def lower(s): return str(s).lower()

# ==================== GUI (Tkinter) ====================
class _GUIImpl:
    def __init__(self):
        self.tk = None
        self.windows = []

    def create_app(self, title, width=800, height=600):
        try:
            import tkinter as tk
        except ImportError:
             print("❌ Error: 'tkinter' not found. This is usually built-in to Python.")
             return None
             
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{width}x{height}")
        self.windows.append(root)
        return root

    def button(self, parent, label, on_click=None):
        import tkinter as tk
        def handler():
            if on_click:
                if callable(on_click):
                    on_click()
                else:
                    print(f"Button '{label}' clicked (No valid function passed)")
        btn = tk.Button(parent, text=label, command=handler)
        btn.pack(pady=5)
        return btn

    def label(self, parent, text):
        import tkinter as tk
        lbl = tk.Label(parent, text=text)
        lbl.pack(pady=5)
        return lbl

    def textbox(self, parent, placeholder=""):
        import tkinter as tk
        entry = tk.Entry(parent)
        entry.insert(0, placeholder)
        entry.pack(pady=5)
        return entry
        
    def show(self, app):
        print(f"🖥️ Opening Window: {app.title()}")
        app.mainloop()

gui = _GUIImpl()


# ==================== SYSTEM ====================
class _FileImpl:
    def create(self, path, content=""):
        self.write(path, content)
        
    def write(self, path, content=""):
        with open(path, "w", encoding='utf-8') as f:
            f.write(str(content))
        print(f"✓ File written: {path}")

    def append(self, path, content=""):
        with open(path, "a", encoding='utf-8') as f:
            f.write(str(content))
        print(f"✓ File appended: {path}")
        
    def read(self, path):
        if not os.path.exists(path):
            print(f"❌ Error: File not found '{path}'")
            return ""
        with open(path, "r", encoding='utf-8') as f:
            return f.read()

file = _FileImpl()

# ==================== WEB ====================
class _WebImpl:
    def open(self, url):
        import webbrowser
        webbrowser.open(url)
        print(f"✓ Opened browser: {url}")
        
    def get(self, url):
        try:
            import requests
            return requests.get(url).text
        except ImportError:
            print("❌ Error: 'requests' module missing. Run: pip install requests")
            return None

web = _WebImpl()

# ==================== DISCORD (Simplified Sync Wrapper) ====================
# Note: Real discord requires async. We will do a blocking runner for simplicity in v1 transpiler.
class _DiscordImpl:
    def create(self, token):
        print("Disclaimer: Real Discord bots require an Event Loop.")
        print("To run a real bot, we would generate an async Python script.")
        print(f"✓ Stored token: {token[:5]}...")
        return {"token": token}

discord_bot = _DiscordImpl()
