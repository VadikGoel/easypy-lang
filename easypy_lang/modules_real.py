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

# ==================== ML (Machine Learning - Sklearn Wrapper) ====================
class _MLImpl:
    def model(self, type="classifier"):
        try:
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.linear_model import LinearRegression
            
            if type == "classifier":
                print("🔹 Created KNN Classifier")
                return _SimpleModel(KNeighborsClassifier(n_neighbors=3))
            elif type == "regression":
                print("🔹 Created Linear Regression Model")
                return _SimpleModel(LinearRegression())
        except ImportError:
            print("❌ Error: 'scikit-learn' not installed.")
            return None
            
class _SimpleModel:
    def __init__(self, internal):
        self.model = internal
        self.trained = False
        
    def train(self, inputs, outputs):
        try:
            self.model.fit(inputs, outputs)
            self.trained = True
            print("✅ Model trained!")
        except Exception as e:
            print(f"❌ Training Failed: {e}")

    def predict(self, input_data):
        if not self.trained:
            print("⚠️ Model not trained yet!")
            return None
        return self.model.predict([input_data])[0]

ml = _MLImpl()

# ==================== AI (Simple NLP/Chat) ====================
class _AIImpl:
    def ask(self, prompt):
        # Placeholder for actual LLM or API
        responses = {
            "hello": "Hello there! How can I help?",
            "easypy": "Easypy is the easiest language ever!",
            "time": f"The time is {time.strftime('%H:%M')}"
        }
        for k, v in responses.items():
            if k in prompt.lower():
                return v
        return f"User asked: '{prompt}' (AI Backend not connected)"

ai = _AIImpl()

# ==================== GAME (Turtle Graphics) ====================
class _GameImpl:
    def window(self, width=600, height=600, title="Easypy Game"):
        import turtle
        s = turtle.Screen()
        s.setup(width, height)
        s.title(title)
        s.bgcolor("black")
        return s

    def player(self, shape="turtle", color="lime"):
        import turtle
        p = turtle.Turtle()
        p.shape(shape)
        p.color(color)
        p.speed(0)
        return p
        
game = _GameImpl()

# Helper for implicit 'ml_classifier' in examples often seen
def ml_classifier(): return ml.model("classifier")

# ==================== DATA (Database & Storage) ====================
class _DBImpl:
    def sqlite(self, path="database.db"):
        import sqlite3
        try:
            conn = sqlite3.connect(path)
            print(f"✓ Connected to SQLite: {path}")
            return _SQLiteConn(conn)
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            return None

    def save_json(self, path, data):
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"✓ Data saved to {path}")
        except Exception as e:
            print(f"❌ Save JSON Failed: {e}")

    def load_json(self, path):
        try:
            if not os.path.exists(path):
                return {}
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Load JSON Failed: {e}")
            return None

class _SQLiteConn:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
    
    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ SQL Error: {e}")
            return []
            
    def close(self):
        self.conn.close()

db = _DBImpl()

# ==================== DATE & TIME ====================
class _DateImpl:
    def now(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def today(self):
        return time.strftime("%Y-%m-%d")

    def timestamp(self):
        return time.time()

datetime = _DateImpl()


