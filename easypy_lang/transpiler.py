"""
Easypy Transpiler
Translates Easypy code (.ep) into executable Python code (.py)
"""

import re

class EasypyTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.context_stack = [] # Stack to track [class, func, other]
        self.in_block = False
        self.source_map = {} # Maps generated python line -> original ep line
        
    def transpile(self, source_code):
        """Convert Easypy source to Python source"""
        # STEP 0: NORMALIZE FORMATTING
        # This allows users to write "if(x){print(x)}" on one line, or "}}}" on one line.
        source_code = self._normalize_source(source_code)
        
        source_lines = source_code.split('\n')
        py_lines = [
            "import sys",
            "import os",
            "from easypy_lang.modules_real import *" 
        ]
        
        # Offset for the header lines added above
        current_py_line = len(py_lines) + 1 
        
        # Pre-process for multi-line support (simple paren counting)
        # We will iterate original lines but might combine them in processing?
        # Actually, simpler approach for "Unlimited":
        # Keep 1-to-1 mapping as much as possible, or insert stub lines to keep count synced.
        # But since we remove braces '}', line counts drift. 
        # So we MUST rely on self.source_map.
        
        buffer_line = ""
        buffer_start_idx = 0
        paren_depth = 0
        
        for i, line in enumerate(source_lines):
            raw_line = line.strip()
            original_line_num = i + 1
            
            # Skip empty lines but keep them in output to preserve some spacing? 
            # OR just map them.
            if not raw_line and paren_depth == 0:
                py_lines.append("")
                self.source_map[current_py_line] = original_line_num
                current_py_line += 1
                continue
                
            # Handle Multi-line concatenation
            # Count parens
            paren_depth += raw_line.count('(') - raw_line.count(')')
            paren_depth += raw_line.count('[') - raw_line.count(']')
            paren_depth += raw_line.count('{') - raw_line.count('}') # Logic block braces
             # Note: Braces {} in easypy are blocks, not dicts usually, unless in var definition. 
             # Implementation detail: We treat ' {' as block starter.
            
            if buffer_line:
                buffer_line += " " + raw_line
            else:
                buffer_line = raw_line
                buffer_start_idx = original_line_num
            
            # If we are inside an expression (parens open), don't process yet
            # EXCEPTION: If the line ends with '{', it's a block starter, usually handled immediately in our logic
            if paren_depth > 0:
                # Check if it's just a block starter line "if (..) {"
                # Our previous logic relied on line.endswith("{").
                # If we have unbalanced parens, we wait.
                # But braces { } are used for blocks. 
                # Let's trust Python's tolerance for newlines inside parens and output as is?
                # No, we need to handle the conversion logic (func, if, etc).
                pass

            # === LINE PROCESSING ===
            # We process 'line' (or buffer). 
            # To simplify "Unlimited", we process line-by-line primarily, 
            # assuming users write "if (cond) {" on one line or utilize python's line continuation.
            
            # Reverting complex multi-line buffer for reliability in this specific tool call
            # We will use the direct processing but record the source map.
            
            processed_line = self._process_line(raw_line)
            
            # Append to output
            if processed_line is not None:
                py_lines.append(processed_line)
                self.source_map[current_py_line] = original_line_num
                current_py_line += 1
            else:
                # If returns None, maybe it was a closing brace } that reduced indent only
                # We still might want to track it or just ignore
                pass

        return "\n".join(py_lines)

    def _normalize_source(self, code):
        """
        Splits code into clean lines based on { and } delimiters,
        respecting strings/quotes.
        Example: 'if(x){print(y)}' -> 
        if(x){
        print(y)
        }
        """
        normalized = []
        current_token = ""
        in_quote = False
        quote_char = ""
        
        for char in code:
            if char in ['"', "'"]:
                if not in_quote:
                    in_quote = True
                    quote_char = char
                elif char == quote_char:
                    in_quote = False
                    quote_char = ""
            
            if not in_quote:
                if char == '{':
                    # Block start: ensure it's on its own line-end or joined with prev
                    # We want "if (x) {" to stay together usually for the parser logic,
                    # BUT "func x() { print" should split.
                    # Simplest strategy: Insert newline AFTER {
                    normalized.append(current_token + "{")
                    normalized.append("\n")
                    current_token = ""
                    continue
                elif char == '}':
                    # Block end: ensure it has newline BEFORE and AFTER
                    if current_token.strip():
                        normalized.append(current_token)
                        normalized.append("\n")
                    normalized.append("}")
                    normalized.append("\n")
                    current_token = ""
                    continue
                elif char == ';':
                    # Treat semicolon as newline
                    if current_token.strip():
                        normalized.append(current_token)
                        normalized.append("\n")
                    current_token = ""
                    continue
            
            current_token += char
            
        if current_token.strip():
            normalized.append(current_token)
            
        return "".join(normalized)

    def _process_line(self, raw_line):
        # Indentation handling (Closing Brace)
        # Handle cases like "}" or "} else {" or "}}"
        while raw_line.startswith("}"):
            self.indent_level -= 1
            if self.indent_level < 0: self.indent_level = 0
            if self.context_stack: self.context_stack.pop()
            raw_line = raw_line[1:].strip()
            
        # If line was just "}", it is now empty. Return None to skip outputting a blank/garbage line.
        if not raw_line:
            return None

        # Prepare current indentation string
        indent = "    " * self.indent_level
        
        # Skip comments
        if raw_line.startswith('#') or raw_line.startswith('//'):
            return f"{indent}#{raw_line}"

        # === TRANSLATION RULES ===

        # 1. Imports
        if raw_line.startswith("use "):
            parts = raw_line.split()
            if len(parts) >= 2:
                mod = parts[1]
                # These are actually pre-loaded objects in modules_real.py
                preloaded_objects = ["gui", "file", "web", "system", "discord_bot", "api"]
                
                if mod in preloaded_objects:
                    return f"{indent}# Module '{mod}' is pre-loaded"
                else:
                    return f"{indent}import {mod}"

        # 1b. Logging/Printing
        if raw_line.startswith("log "):
            content = raw_line[4:]
            return f"{indent}print({content})"
            
        if raw_line.startswith("print "):
            content = raw_line[6:]
            return f"{indent}print({content})"

        # 2. Var and Types
        # Support "string name =", "int count =", "var x ="
        if raw_line.startswith("var "):
            raw_line = raw_line[4:]
        
        # Strip explicit types (simple approach)
        types = ["string ", "int ", "float ", "bool ", "list ", "dict "]
        for t in types:
            if raw_line.startswith(t):
                raw_line = raw_line[len(t):]
                break
        
        # 3. Functions
        if raw_line.startswith("func ") and raw_line.endswith("{"):
            defn = raw_line[5:-1].strip()
            
            # Auto-inject 'self' if inside a class
            if self.context_stack and self.context_stack[-1] == 'class':
                parts = defn.split("(", 1)
                name = parts[0]
                args = parts[1][:-1] if len(parts) > 1 else ""
                
                if args.strip():
                    defn = f"{name}(self, {args})"
                else:
                    defn = f"{name}(self)"

            self.indent_level += 1
            self.context_stack.append('func')
            return f"{indent}def {defn}:"
        
        # 3b. Async Functions
        if raw_line.startswith("async func ") and raw_line.endswith("{"):
            defn = raw_line[11:-1].strip()
            self.indent_level += 1
            self.context_stack.append('func')
            return f"{indent}async def {defn}:"

        # 4. Classes
        if raw_line.startswith("class ") and raw_line.endswith("{"):
            defn = raw_line[6:-1].strip()
            self.indent_level += 1
            self.context_stack.append('class')
            return f"{indent}class {defn}:"

        # 5. Logic
        if raw_line.startswith("if") and raw_line.endswith("{"):
            condition = raw_line[2:-1].strip()
            # Handle if(x) vs if x
            if condition.startswith("(") and condition.endswith(")"): condition = condition
            self.indent_level += 1
            self.context_stack.append('block')
            return f"{indent}if {condition}:"
        
        if raw_line.startswith("elif") and raw_line.endswith("{"):
            condition = raw_line[4:-1].strip()
            self.indent_level += 1
            self.context_stack.append('block')
            return f"{indent}elif {condition}:"

        if raw_line.startswith("else") and raw_line.endswith("{"):
            self.indent_level += 1
            self.context_stack.append('block')
            return f"{indent}else:"

        # 6. Loops
        loop_match = re.match(r'loop (\d+) times\s*\{', raw_line)
        if loop_match:
            count = loop_match.group(1)
            self.indent_level += 1
            self.context_stack.append('block')
            return f"{indent}for _ in range({count}):"
        
        if raw_line.startswith("while") and raw_line.endswith("{"):
            condition = raw_line[5:-1].strip()
            self.indent_level += 1
            self.context_stack.append('block')
            return f"{indent}while {condition}:"
            
        if raw_line.startswith("for ") and raw_line.endswith("{"):
            condition = raw_line[3:-1].strip()
            self.indent_level += 1
            self.context_stack.append('block')
            return f"{indent}for {condition}:"

        # 7. Generic Block
        if raw_line.endswith("{"):
             clean_line = raw_line[:-1].strip()
             self.indent_level += 1
             self.context_stack.append('block')
             return f"{indent}{clean_line}:"

        # 8. Standard Line
        return f"{indent}{raw_line}"
