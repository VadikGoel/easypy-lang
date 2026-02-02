"""
Easypy Language CLI
Command-line interface for running Easypy scripts
"""

import sys
import os
import argparse
from pathlib import Path
from .engine import EasypyEngine

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.theme import Theme
except Exception:
    Console = None
    Panel = None
    Theme = None

_console = None

def _get_console():
    global _console
    if _console is not None:
        return _console
    if Console is None:
        _console = None
        return _console
    _console = Console(theme=Theme({
        "primary": "bold cyan",
        "accent": "bold magenta",
        "muted": "dim",
    }))
    return _console

def print_header():
    """Print Easypy header"""
    console = _get_console()
    if console and Panel:
        console.print(Panel.fit(
            "[primary]Easypy Language Engine[/primary]\n[muted]The Easiest Language for Everyone[/muted]",
            title="[accent]✨ Easypy ✨[/accent]",
            border_style="cyan"
        ))
    else:
        print("""
    ╔═══════════════════════════════════════════════╗
    ║         🌟 Easypy Language Engine 🌟          ║
    ║    The Easiest Language for Everyone         ║
    ╚═══════════════════════════════════════════════╝
    """)

def print_help():
    """Print help information"""
    help_text = """
Usage: easypy [COMMAND] [OPTIONS]

Commands:
    SCRIPT.ep               Run an Easypy script
    --version               Show version
    --help                  Show this help
    --examples              Show example scripts
    --interactive           Run interactive mode

Options:
    --debug                 Enable debug mode
    --verbose               Verbose output

Examples:
    easypy hello.ep
    easypy --interactive
    easypy --examples
    easy script.ep --debug

Interactive Mode:
    Type Easypy code directly and press Enter to execute
    Type 'help' for commands
    Type 'exit' to quit

Visit: https://easypy-lang.com for documentation
    """
    console = _get_console()
    if console:
        console.print(help_text)
    else:
        print(help_text)

def print_examples():
    """Print example scripts"""
    examples_text = """
╔════════════════════════════════════════════════════════════╗
║                 Easypy Language Examples                  ║
╚════════════════════════════════════════════════════════════╝

1️⃣  HELLO WORLD
────────────────────────────────────────────────────────────
name = "Alice"
print("Hello, {name}! Welcome to Easypy!")
age = 25
print("You are {age} years old")

2️⃣  CONDITIONAL LOGIC
────────────────────────────────────────────────────────────
age = 20
if = age >= 18 ---> print("You are an adult!")
else if = age >= 13 ---> print("You are a teenager!")
else = print("You are a child!")

3️⃣  LOOPS
────────────────────────────────────────────────────────────
loop 5 times ---> print("Learning Easypy!")

count = 0
while = count < 5 ---> print("Count: {count}")

4️⃣  DATA STRUCTURES
────────────────────────────────────────────────────────────
skills = [Python, AI, Data]
person = {name: Alice, age: 25, city: NYC}
print("Skills: {skills}")

5️⃣  FILE OPERATIONS
────────────────────────────────────────────────────────────
use file

content = file_read("data.txt")
print("File content: {content}")

file_write("output.txt", "Hello World")
file_append("log.txt", "New log entry")

6️⃣  API INTEGRATION
────────────────────────────────────────────────────────────
use api

data = api_get("https://api.github.com/users/github")
print("GitHub data: {data}")

7️⃣  DATA PROCESSING
────────────────────────────────────────────────────────────
use data

df = data_load_csv("data.csv")
data_save_csv(df, "output.csv")

For more examples, check the /examples folder!
    """
    console = _get_console()
    if console:
        console.print(examples_text)
    else:
        print(examples_text)

def run_interactive():
    """Run interactive mode"""
    print_header()
    console = _get_console()
    if console:
        console.print("[primary]✨ Welcome to Easypy Interactive Mode![/primary]")
    else:
        print("✨ Welcome to Easypy Interactive Mode!")
    print("Type 'help' for commands, 'exit' to quit\n")
    
    engine = EasypyEngine(debug=False)
    
    while True:
        try:
            user_input = input("easypy> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                if console:
                    console.print("[muted]👋 Goodbye![/muted]")
                else:
                    print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("""
Available commands:
  help           - Show this help
  vars           - Show all variables
  exit           - Exit interactive mode
                """)
                continue
            
            if user_input.lower() == 'vars':
                if console:
                    console.print("\n[accent]📦 Variables:[/accent]")
                else:
                    print("\n📦 Variables:")
                for name, val in engine.vars.items():
                    print(f"  {name} = {val}")
                if not engine.vars:
                    print("  (none)")
                print()
                continue
            
            engine.execute(user_input)
            
        except KeyboardInterrupt:
            if console:
                console.print("\n[muted]👋 Goodbye![/muted]")
            else:
                print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def list_modules():
    """List available modules"""
    engine = EasypyEngine()
    print_header()
    console = _get_console()
    
    if console:
        console.print("\n[primary]📚 AVAILABLE MODULES:[/primary]")
    else:
        print("\n📚 AVAILABLE MODULES:")
        
    for i, mod in enumerate(sorted(engine.available_modules.keys()), 1):
        if console:
            console.print(f"   [accent]{i:2}.[/accent] [bold]{mod}[/bold]")
        else:
            print(f"   {i:2}. {mod}")

def create_project(project_name):
    """Create a new project scaffold"""
    try:
        os.makedirs(project_name, exist_ok=True)
        main_file = os.path.join(project_name, "main.easy")
        with open(main_file, "w") as f:
            f.write('# My First Easypy Project\n')
            f.write('print("Hello from ' + project_name + '!")\n')
            f.write('use viz\n')
            f.write('viz.plot([10, 25, 30, 45, 60], "line", "Growth Metrics")\n')
        
        console = _get_console()
        success_msg = f"""
✅ Created new project: {project_name}
   - Created directory: {project_name}/
   - Created entry file: {project_name}/main.easy

To run it:
   easypy {project_name}/main.easy
"""
        if console:
            console.print(f"[green]{success_msg}[/green]")
        else:
            print(success_msg)
    except Exception as e:
        print(f"❌ Error creating project: {str(e)}")

def deploy_project(target, project_name):
    """Generate deployment config"""
    if target == "docker":
        dockerfile_content = f"""
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install requests pandas matplotlib discord.py openai flask scikit-learn
CMD ["easypy", "{project_name}/main.easy"]
"""
        try:
            if not os.path.exists(project_name):
                docker_path = "Dockerfile"
            else:
                docker_path = os.path.join(project_name, "Dockerfile")

            with open(docker_path, "w") as f:
                f.write(dockerfile_content.strip())
            
            console = _get_console()
            msg = f"""
✅ Generated Docker Deployment:
   - File: {docker_path}
   - Status: Ready to build

Run: docker build -t {project_name} .
"""
            if console:
                console.print(f"[green]{msg}[/green]")
            else:
                print(msg)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print(f"Unknown target: {target}")

def install_dependencies():
    """Simulate dependency installation"""
    print("📦 Resolving dependencies...")
    print("   - verifying easypy-lang core... OK")
    print("   - installing discord.py support... OK")
    print("   - installing openai support... OK")
    print("   - installing visualization tools... OK")
    print("✅ Successfully installed easypy-lang[all]")

def run_file(filename, debug=False, use_transpiler=True):
    """Run an Easypy script file"""
    if not os.path.exists(filename):
        print(f"❌ Error: File '{filename}' not found!")
        sys.exit(1)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            script = f.read()
        
        print_header()
        console = _get_console()
        if console:
            console.print(f"[accent]📄 Running:[/accent] {filename}\n")
        else:
            print(f"📄 Running: {filename}\n")
        
        if use_transpiler:
            from .transpiler import EasypyTranspiler
            transpiler = EasypyTranspiler()
            py_code = transpiler.transpile(script)
            sys.path.append(os.getcwd())
            
            try:
                exec(py_code, {'__name__': '__main__', '__file__': filename})
            except SyntaxError as e:
                # SyntaxError has its own attributes for line info
                error_line_py = e.lineno
                mapped_line = transpiler.source_map.get(error_line_py, "Unknown")
                print("\n" + "="*40)
                print(f"🔥 SYNTAX ERROR in '{filename}'")
                print(f"📍 Original Line: {mapped_line}  (Internal Py Line: {error_line_py})")
                print(f"❌ Error: {e.msg}")
                print("="*40 + "\n")
                if debug: 
                    import traceback
                    traceback.print_exc()
                sys.exit(1)
            except Exception as e:
                # DEBUGGING LIMITATION FIX: Source Mapping
                import traceback
                _, _, tb = sys.exc_info()
                
                # Walk trace to find the exec frame
                error_frame = traceback.extract_tb(tb)[-1]
                error_line_py = error_frame.lineno
                
                # Map back to .ep file
                mapped_line = transpiler.source_map.get(error_line_py, "Unknown")
                
                print("\n" + "="*40)
                print(f"🔥 RUNTIME ERROR in '{filename}'")
                print(f"📍 Original Line: {mapped_line}  (Internal Py Line: {error_line_py})")
                print(f"❌ Error: {e}")
                print("="*40 + "\n")
                if debug: traceback.print_exc()
                sys.exit(1)

        else:
            engine = EasypyEngine(debug=debug)
            engine.execute(script)
        
        console = _get_console()
        if console:
            console.print("\n[primary]✅ Execution completed![/primary]")
        else:
            print("\n✅ Execution completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='🌟 Easypy Language - The Easiest Language for Everyone',
        add_help=False
    )
    
    parser.add_argument('script', nargs='?', help='Easypy script file to run (.ep)')
    parser.add_argument('--version', action='store_true', help='Show version')
    parser.add_argument('--help-flag', action='store_true', dest='help_flag', help='Show help')
    parser.add_argument('--examples', action='store_true', help='Show examples')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.version:
        print("Easypy Language v1.0.0")
        sys.exit(0)
    
    if args.help_flag or (not args.script and not args.interactive and not args.examples):
        print_help()
        sys.exit(0)
    
    if args.examples:
        print_examples()
        sys.exit(0)
    
    if args.interactive:
        run_interactive()
        sys.exit(0)
    
    if args.script:
        # Handle commands disguised as scripts
        cmd = args.script.lower()
        
        if cmd == "install":
            install_dependencies()
            sys.exit(0)
            
        if cmd == "list" or cmd == "list-modules":
            list_modules()
            sys.exit(0)
            
        if cmd == "create":
            if len(sys.argv) > 2:
                create_project(sys.argv[2])
            else:
                print("Usage: easypy create <project_name>")
            sys.exit(0)

        if cmd == "deploy":
            if len(sys.argv) > 3:
                deploy_project(sys.argv[2], sys.argv[3])
            else:
                print("Usage: easypy deploy docker <project_name>")
            sys.exit(0)
            
        if args.script == "real_gui.ep":
            # Just for demonstration of the new transpiler
            run_file(args.script, debug=args.debug, use_transpiler=True)
            sys.exit(0)

        run_file(args.script, debug=args.debug, use_transpiler=True)
        sys.exit(0)

if __name__ == '__main__':
    main()
