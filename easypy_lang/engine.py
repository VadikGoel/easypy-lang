"""
Easypy Language Core Engine
Main execution engine for the Easypy language
"""

import re
import os
import json
import sys
from typing import Any, Dict, List, Optional, Tuple
import subprocess
from datetime import datetime
from .modules import (
    FileModule, APIModule, DataModule, MLModule, MathModule, StringModule, WebModule,
    DiscordBotModule, AIChatModule, VizModule, GUIModule, ImageModule, AudioModule,
    SecurityModule, ScraperModule, MobileModule, NLPModule, DevOpsModule,
    FinanceModule, BlockchainModule, RoboticsModule, IoTModule, ScienceModule,
    VisionModule, CloudModule
)

class EasypyEngine:
    """Advanced Easypy Language Engine"""
    
    def __init__(self, debug=False, context=None):
        self.vars = {}
        self.functions = {}
        self.global_vars = {}
        self.debug = debug
        self.line_num = 0
        self.imported_modules = {}
        self.context = context or {}
        self.register_builtins()
        self.register_modules()
    
    def register_builtins(self):
        """Register built-in functions"""
        self.functions.update({
            'print': self.builtin_print,
            'len': self.builtin_len,
            'range': self.builtin_range,
            'str': self.builtin_str,
            'int': self.builtin_int,
            'float': self.builtin_float,
            'list': self.builtin_list,
            'dict': self.builtin_dict,
            'sum': self.builtin_sum,
            'max': self.builtin_max,
            'min': self.builtin_min,
            'type': self.builtin_type,
            'input': self.builtin_input,
            'join': self.builtin_join,
            'split': self.builtin_split,
            'upper': self.builtin_upper,
            'lower': self.builtin_lower,
            'replace': self.builtin_replace,
            'contains': self.builtin_contains,
            'sleep': self.builtin_sleep,
            'time': self.builtin_time,
            'now': self.builtin_now,
            'pip_install': self.builtin_pip_install,
            'pip_uninstall': self.builtin_pip_uninstall,
            'pip_list': self.builtin_pip_list,
            'banner': self.builtin_banner,
            'style': self.builtin_style,
        })
    
    def register_modules(self):
        """Register available modules"""
        self.available_modules = {
            'file': FileModule(),
            'api': APIModule(),
            'data': DataModule(),
            'ml': MLModule(),
            'math': MathModule(),
            'web': WebModule(),
            'string': StringModule(),
            'discord_bot': DiscordBotModule(),
            'ai_chat': AIChatModule(),
            'viz': VizModule(),
            'gui': GUIModule(),
            'image': ImageModule(),
            'audio': AudioModule(),
            'security': SecurityModule(),
            'scraper': ScraperModule(),
            'mobile': MobileModule(),
            'nlp': NLPModule(),
            'devops': DevOpsModule(),
            'finance': FinanceModule(),
            'blockchain': BlockchainModule(),
            'robot': RoboticsModule(),
            'iot': IoTModule(),
            'science': ScienceModule(),
            'vision': VisionModule(),
            'cloud': CloudModule(),
        }

    def _load_module(self, module_name):
        """Load a module into the current context"""
        if module_name in self.available_modules:
            self.imported_modules[module_name] = self.available_modules[module_name]
            print(f"✓ Loaded module: {module_name}")
        else:
            print(f"✗ Module not found: {module_name}")

    def _execute_module_function(self, module_name, func_name, args):
        """Execute a function from a loaded module"""
        if module_name not in self.imported_modules:
            raise RuntimeError(f"Module '{module_name}' not imported. Add 'use {module_name}'")
        
        module = self.imported_modules[module_name]
        if hasattr(module, func_name):
            func = getattr(module, func_name)
            try:
                # Convert args if possible
                real_args = []
                for arg in args:
                    if isinstance(arg, str) and (arg.startswith('"') or arg.startswith("'")):
                        # String literal
                        val = arg.strip('"\'')
                        # Interpolate
                        for k, v in self.vars.items():
                             val = val.replace(f"{{{k}}}", str(v))
                        real_args.append(val)
                    elif isinstance(arg, str) and arg in self.vars:
                        real_args.append(self.vars[arg])
                    elif isinstance(arg, str):
                        # Try to parse as number or json
                        try:
                            if arg.isdigit(): real_args.append(int(arg))
                            elif arg.replace('.','',1).isdigit(): real_args.append(float(arg))
                            else: real_args.append(self.get_value(arg)) 
                        except:
                            real_args.append(arg)
                    else:
                        real_args.append(arg)
                
                return func(*real_args)
            except Exception as e:
                raise RuntimeError(f"Error in {module_name}.{func_name}: {e}")
        else:
            raise RuntimeError(f"Function {func_name} not found in {module_name}")
    
    # ============ BUILT-IN FUNCTIONS ============
    
    def builtin_print(self, *args):
        print(' '.join(str(arg) for arg in args))
        return None
    
    def builtin_len(self, obj):
        return len(obj)
    
    def builtin_range(self, *args):
        return list(range(*args))
    
    def builtin_str(self, obj):
        return str(obj)
    
    def builtin_int(self, obj):
        return int(float(obj))
    
    def builtin_float(self, obj):
        return float(obj)
    
    def builtin_list(self, obj=None):
        return list(obj) if obj else []
    
    def builtin_dict(self):
        return {}
    
    def builtin_sum(self, iterable):
        return sum(iterable)
    
    def builtin_max(self, *args):
        return max(*args)
    
    def builtin_min(self, *args):
        return min(*args)
    
    def builtin_type(self, obj):
        return type(obj).__name__
    
    def builtin_input(self, prompt=""):
        return input(str(prompt))
    
    def builtin_join(self, items, separator=""):
        return separator.join(str(i) for i in items)
    
    def builtin_split(self, text, separator=" "):
        return text.split(separator)
    
    def builtin_upper(self, text):
        return str(text).upper()
    
    def builtin_lower(self, text):
        return str(text).lower()
    
    def builtin_replace(self, text, old, new):
        return str(text).replace(str(old), str(new))
    
    def builtin_contains(self, text, substring):
        return str(substring) in str(text)
    
    def builtin_sleep(self, seconds):
        import time
        time.sleep(float(seconds))
    
    def builtin_time(self):
        import time
        return time.time()
    
    def builtin_now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def builtin_pip_install(self, package_name):
        """Install a Python package using pip"""
        return subprocess.run([sys.executable, "-m", "pip", "install", str(package_name)], check=False).returncode == 0

    def builtin_pip_uninstall(self, package_name):
        """Uninstall a Python package using pip"""
        return subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", str(package_name)], check=False).returncode == 0

    def builtin_pip_list(self):
        """List installed Python packages"""
        result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True, check=False)
        return result.stdout

    def builtin_banner(self, text, style="box"):
        """Create stylized banners for text output"""
        text = str(text)
        if style == "box":
            width = len(text) + 4
            print("┌" + "─" * width + "┐")
            print(f"│  {text}  │")
            print("└" + "─" * width + "┘")
        elif style == "stars":
            print("★ " * (len(text) // 2 + 2))
            print(f"★  {text}  ★")
            print("★ " * (len(text) // 2 + 2))
        elif style == "dashes":
            print("─" * (len(text) + 4))
            print(f"  {text}  ")
            print("─" * (len(text) + 4))
        elif style == "arrows":
            print("» " * (len(text) // 2 + 1))
            print(f"  {text}  ")
            print("« " * (len(text) // 2 + 1))
        else:
            print(text)
        return text

    def builtin_style(self, text, color=None, bold=False, underline=False):
        """Apply ANSI color and styling to text"""
        text = str(text)
        codes = []
        
        # Color codes
        colors = {
            "black": 30, "red": 31, "green": 32, "yellow": 33,
            "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
            "bright_black": 90, "bright_red": 91, "bright_green": 92,
            "bright_yellow": 93, "bright_blue": 94, "bright_magenta": 95,
            "bright_cyan": 96, "bright_white": 97
        }
        
        if bold:
            codes.append(1)
        if underline:
            codes.append(4)
        if color and color.lower() in colors:
            codes.append(colors[color.lower()])
        
        if codes:
            code_str = ";".join(map(str, codes))
            return f"\033[{code_str}m{text}\033[0m"
        return text
    
    # ============ VALUE PARSING ============
    
    def clean_val(self, val: str) -> Any:
        """Convert string to appropriate type"""
        val = val.strip()
        
        if val.lower() == 'true':
            return True
        if val.lower() == 'false':
            return False
        if val.lower() in ['none', 'null', 'nil']:
            return None
        
        if re.match(r'^-?\d+(\.\d+)?$', val):
            return float(val) if '.' in val else int(val)
        
        if val.startswith('[') and val.endswith(']'):
            try:
                inner = val[1:-1].strip()
                if not inner:
                    return []
                items = [self.clean_val(item.strip()) for item in self.smart_split(inner, ',')]
                return items
            except:
                pass
        
        if val.startswith('{') and val.endswith('}'):
            try:
                inner = val[1:-1].strip()
                if not inner:
                    return {}
                result = {}
                for pair in self.smart_split(inner, ','):
                    if ':' in pair:
                        k, v = pair.split(':', 1)
                        result[k.strip()] = self.clean_val(v.strip())
                return result
            except:
                pass
        
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            return val[1:-1]
        
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', val):
            return val
        
        return val
    
    def get_value(self, val: str) -> Any:
        """Get variable value or convert string"""
        val = val.strip()
        if val in self.vars:
            return self.vars[val]
        if val in self.global_vars:
            return self.global_vars[val]
        return self.clean_val(val)
    
    def smart_split(self, text: str, delimiter: str) -> List[str]:
        """Split respecting brackets and quotes"""
        result = []
        current = ""
        depth = 0
        in_quote = False
        quote_char = None
        
        for char in text:
            if char in ('"', "'") and (not in_quote or quote_char == char):
                in_quote = not in_quote
                quote_char = char if in_quote else None
                current += char
            elif char in ('[', '{') and not in_quote:
                depth += 1
                current += char
            elif char in (']', '}') and not in_quote:
                depth -= 1
                current += char
            elif char == delimiter and depth == 0 and not in_quote:
                result.append(current)
                current = ""
            else:
                current += char
        
        if current:
            result.append(current)
        
        return result
    
    # ============ EXPRESSION EVALUATION ============
    
    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate expressions with variables"""
        expr = expr.strip()
        
        for var_name, var_val in self.vars.items():
            expr = re.sub(r'\b' + re.escape(var_name) + r'\b', repr(var_val), expr)
        
        for var_name, var_val in self.global_vars.items():
            expr = re.sub(r'\b' + re.escape(var_name) + r'\b', repr(var_val), expr)
        
        try:
            allowed_names = {
                'True': True, 'False': False, 'None': None,
                **{name: func for name, func in self.functions.items()}
            }
            result = eval(expr, {"__builtins__": {}}, allowed_names)
            return result
        except Exception as e:
            raise RuntimeError(f"Evaluation error: {e}")
    
    def evaluate_condition(self, cond: str) -> bool:
        """Evaluate conditions"""
        cond = cond.strip()
        
        if ' and ' in cond:
            parts = cond.split(' and ')
            return all(self.evaluate_condition(p.strip()) for p in parts)
        
        if ' or ' in cond:
            parts = cond.split(' or ')
            return any(self.evaluate_condition(p.strip()) for p in parts)
        
        if cond.startswith('not '):
            return not self.evaluate_condition(cond[4:].strip())
        
        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in cond:
                left_str, right_str = cond.split(op, 1)
                left = self.get_value(left_str.strip())
                right = self.get_value(right_str.strip())
                
                if op == '==':
                    return left == right
                elif op == '!=':
                    return left != right
                elif op == '>=':
                    return left >= right
                elif op == '<=':
                    return left <= right
                elif op == '>':
                    return left > right
                elif op == '<':
                    return left < right
        
        return bool(self.get_value(cond))
    
    # ============ FUNCTION HANDLING ============
    
    def parse_function_call(self, line: str) -> Any:
        """Parse and execute function calls"""
        match = re.match(r'(\w+)\((.*)\)$', line.strip())
        if match:
            func_name, args_str = match.groups()
            args = []
            if args_str.strip():
                for arg in self.smart_split(args_str, ','):
                    arg = arg.strip()
                    # Handle string arguments with interpolation
                    if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                        string_val = arg[1:-1]
                        # Replace variables in string
                        for var_name, var_val in self.vars.items():
                            string_val = string_val.replace(f'{{{var_name}}}', str(var_val))
                        for var_name, var_val in self.global_vars.items():
                            string_val = string_val.replace(f'{{{var_name}}}', str(var_val))
                        args.append(string_val)
                    else:
                        args.append(self.get_value(arg))
            
            if func_name in self.functions:
                return self.functions[func_name](*args)
            else:
                raise RuntimeError(f"Unknown function: {func_name}")
        return None
    
    # ============ EXECUTION ============
    
    def execute(self, script: str) -> None:
        """Execute Easypy script"""
        lines = script.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            self.line_num = i + 1
            
            if not line or line.startswith('#'):
                i += 1
                continue
            
            try:
                # Use statements
                if line.startswith('use '):
                    module = line.replace('use ', '').strip().split()[0]
                    self._load_module(module)
                
                # Variable assignment
                elif '=' in line and not any(x in line for x in ['==', '!=', '>=', '<=', '--->']) and not line.startswith('if') and not line.startswith('else'):
                    name, val = line.split('=', 1)
                    self.vars[name.strip()] = self.get_value(val.strip())
                
                # If/Else
                elif line.startswith('if ') and '--->' in line:
                    condition = line.split('--->', 1)[0].replace('if ', '').strip()
                    action = line.split('--->', 1)[1].strip()
                    
                    if self.evaluate_condition(condition):
                        self.execute_action(action)
                        i = self._skip_else_blocks(lines, i)
                    else:
                        i = self._handle_else_blocks(lines, i)
                
                # Loops
                elif line.startswith('loop ') and '--->' in line:
                    match = re.match(r'loop (\d+) times ---> (.*)', line)
                    if match:
                        count, action = int(match.group(1)), match.group(2).strip()
                        for _ in range(count):
                            self.execute_action(action)
                
                # While
                elif line.startswith('while ') and '--->' in line:
                    condition = line.split('--->', 1)[0].replace('while ', '').strip()
                    action = line.split('--->', 1)[1].strip()
                    iterations = 0
                    while self.evaluate_condition(condition) and iterations < 10000:
                        self.execute_action(action)
                        iterations += 1
                
                # Function calls
                elif '(' in line and ')' in line and '=' not in line:
                    self.parse_function_call(line)
                
            except Exception as e:
                print(f"❌ Error at line {self.line_num}: {e}")
                if self.debug:
                    import traceback
                    traceback.print_exc()
            
            i += 1
    
    def execute_action(self, action: str) -> None:
        """Execute an action"""
        action = action.strip()
        
        # Interpolate variables
        for var_name, var_val in self.vars.items():
            action = action.replace(f'{{{var_name}}}', str(var_val))
        
        for var_name, var_val in self.global_vars.items():
            action = action.replace(f'{{{var_name}}}', str(var_val))
        
        if '(' in action and ')' in action:
            self.parse_function_call(action)
        else:
            print(action)
    
    def _skip_else_blocks(self, lines: List[str], current: int) -> int:
        """Skip else/else if blocks"""
        i = current + 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line.startswith('else if ') or next_line.startswith('else '):
                i += 1
            else:
                return i - 1
        return i - 1
    
    def _handle_else_blocks(self, lines: List[str], current: int) -> int:
        """Handle else/else if blocks"""
        i = current + 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line.startswith('else if ') and '--->' in next_line:
                condition = next_line.split('--->', 1)[0].replace('else if ', '').strip()
                action = next_line.split('--->', 1)[1].strip()
                if self.evaluate_condition(condition):
                    self.execute_action(action)
                    return self._skip_else_blocks(lines, i)
                i += 1
            elif next_line.startswith('else ') and '--->' in next_line:
                action = next_line.split('--->', 1)[1].strip()
                self.execute_action(action)
                return i
            else:
                return i - 1
        return i - 1
    
    def _load_module(self, module: str) -> None:
        """Load and register module functions"""
        if module == 'file':
            self._load_file_module()
        elif module == 'api':
            self._load_api_module()
        elif module == 'data':
            self._load_data_module()
        elif module == 'ml':
            self._load_ml_module()
        elif module == 'math':
            self._load_math_module()
        elif module == 'string':
            self._load_string_module()
        elif module == 'web':
            self._load_web_module()
    
    def _load_file_module(self):
        """File I/O module"""
        self.functions['file_read'] = lambda path: self._file_read(path)
        self.functions['file_write'] = lambda path, content: self._file_write(path, content)
        self.functions['file_append'] = lambda path, content: self._file_append(path, content)
        self.functions['file_list'] = lambda path: self._file_list(path)
        self.functions['file_exists'] = lambda path: self._file_exists(path)
    
    def _file_read(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError(f"File not found: {path}")
    
    def _file_write(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True
    
    def _file_append(self, path, content):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(str(content) + '\n')
        return True
    
    def _file_list(self, path):
        return os.listdir(path)
    
    def _file_exists(self, path):
        return os.path.exists(path)
    
    def _load_api_module(self):
        """API module"""
        try:
            import requests
            self.functions['api_get'] = lambda url, headers={}: self._api_get(url, headers)
            self.functions['api_post'] = lambda url, data, headers={}: self._api_post(url, data, headers)
        except ImportError:
            print("⚠️  requests library not found. Install with: pip install requests")
    
    def _api_get(self, url, headers=None):
        import requests
        response = requests.get(url, headers=headers or {})
        return response.json() if response.headers.get('content-type') == 'application/json' else response.text
    
    def _api_post(self, url, data, headers=None):
        import requests
        response = requests.post(url, json=data, headers=headers or {})
        return response.json() if response.headers.get('content-type') == 'application/json' else response.text
    
    def _load_data_module(self):
        """Data processing module"""
        try:
            import pandas as pd
            self.functions['data_load_csv'] = lambda path: self._data_load_csv(path)
            self.functions['data_save_csv'] = lambda df, path: self._data_save_csv(df, path)
        except ImportError:
            print("⚠️  pandas library not found. Install with: pip install pandas")
    
    def _data_load_csv(self, path):
        import pandas as pd
        return pd.read_csv(path)
    
    def _data_save_csv(self, df, path):
        df.to_csv(path, index=False)
        return True
    
    def _load_ml_module(self):
        """Machine Learning module"""
        try:
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.linear_model import LinearRegression
            self.functions['ml_classifier'] = lambda: DecisionTreeClassifier()
            self.functions['ml_regressor'] = lambda: LinearRegression()
        except ImportError:
            print("⚠️  scikit-learn library not found. Install with: pip install scikit-learn")
    
    def _load_math_module(self):
        """Math module"""
        import math
        self.functions['math_sqrt'] = lambda x: math.sqrt(x)
        self.functions['math_power'] = lambda x, y: math.pow(x, y)
        self.functions['math_floor'] = lambda x: math.floor(x)
        self.functions['math_ceil'] = lambda x: math.ceil(x)
        self.functions['math_sin'] = lambda x: math.sin(x)
        self.functions['math_cos'] = lambda x: math.cos(x)
    
    def _load_string_module(self):
        """String utilities module"""
        self.functions['string_upper'] = lambda s: str(s).upper()
        self.functions['string_lower'] = lambda s: str(s).lower()
        self.functions['string_length'] = lambda s: len(str(s))
        self.functions['string_reverse'] = lambda s: str(s)[::-1]
    
    def _load_web_module(self):
        """Web scraping module"""
        try:
            from bs4 import BeautifulSoup
            import requests
            self.functions['web_fetch'] = lambda url: self._web_fetch(url)
        except ImportError:
            print("⚠️  beautifulsoup4 library not found. Install with: pip install beautifulsoup4")
    
    def _web_fetch(self, url):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser')
