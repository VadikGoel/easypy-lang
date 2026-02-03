# Easypy: Coding for Everyone 🚀

![Easypy Banner](https://img.shields.io/pypi/v/easypy-lang?color=blue&style=for-the-badge) ![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge) ![Downloads](https://img.shields.io/pypi/dm/easypy-lang?style=for-the-badge)

**Easypy** is a new programming language designed for humans, not robots. It strips away the complex syntax of traditional languages and replaces it with clear, English-like commands.

Whether you want to build websites, analyze data, or create AI chatbots, Easypy makes it accessible to everyone.

## 📦 Installation

### Option 1: Install via Pip (Recommended)
Simply install the package via pip:

```bash
pip install easypy-lang
```

### Option 2: Run via Docker (No Install Needed)
Don't want to install Python? Run Easypy directly in a container:

```bash
# Pull the image
docker pull vadikgoel/easypy-lang

# Run interactive mode
docker run -it vadikgoel/easypy-lang
```

## ✨ Features

- **English-like Syntax**: Write code that reads like a story.
- **Built-in Power**: Comes with modules for AI, Web, Data Science, and GUI out of the box.
- **Python Compatible**: Runs on top of the robust Python ecosystem.
- **Zero Configuration**: No complex build tools or compilers needed.

## � Modules (Batteries Included)

| Module | Purpose | Example |
|--------|---------|---------|
| `gui` | Desktop Apps | `gui.create_app("My App")` |
| `ml` | Machine Learning | `ml.model("classifier")` |
| `ai` | AI Helpers | `ai.ask("Hello")` |
| `db` | Database | `db.sqlite("my.db")` |
| `game` | 2D Games | `game.window()` |
| `web` | Internet | `web.get("https://google.com")` |
| `file` | File I/O | `file.write("test.txt", "Hi")` |
| `datetime`| Date & Time | `datetime.now()` |
| `discord` | Bots | `class MyBot(discord.Client)` |

## �🚀 Quick Start

Create a file named `hello.easy` and write your first program:

```python
# Say hello
log "Hello, World!"

# Simple math
var x = 10
var y = 20
log "The sum is: " + (x + y)

# Ask the user
input name "What is your name?"
log "Nice to meet you, " + name
```

Run it from your terminal:

```bash
easypy hello.easy
```

## 📚 Documentation

For full documentation, tutorials, and the interactive playground, please check the `docs/` folder included in the repository or visit our [Documentation](https://vadikgoel.github.io/easypy-lang/).

## 🤝 Contributing

We welcome contributions! Please feel free to open issues or submit pull requests on our GitHub page.

---
*Easypy - Making programming simple, powerful, and fun.*
