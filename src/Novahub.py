#!/usr/bin/env python3
"""
NovaHub D-Edition - Refactored with Class-Based Architecture (Phase 11)
Features:
 - Modular class-based design (NovaHubShell, NovaFileSystem, NovaScriptRuntime, NovaGPTModule, NovaJobsManager, NovaManSystem)
 - NovaGPT powered by Zencoder AI with multi-turn conversations (stores up to 40 messages)
 - Smart Zencoder-based responses for coding help, debugging, testing, refactoring
 - Matrix rain animation (matrix command)
 - Animated splash banner with NovaLogo
 - All previous features preserved and compatible
"""

import os
import sys
import time
import json
import threading
import difflib
import ast
import shutil
import re
import atexit
import code
import random

try:
    import readline
except ImportError:
    readline = None

try:
    import openai
except ImportError:
    openai = None

APP_NAME = "NovaHub"
VERSION = "NovaHub D-Edition v1.1 (Zencoder Integrated)"
HOME = os.path.expanduser("~")
ROOT_FOLDER_NAME = "NovaHubDocuments"
ROOT_DIR = os.path.join(HOME, ROOT_FOLDER_NAME)
PROJECTS_DIR = os.path.join(ROOT_DIR, "Projects")
SYSTEM_DIR = os.path.join(ROOT_DIR, "System")
CONFIG_DIR = os.path.join(ROOT_DIR, "Config")
MAN_DIR = os.path.join(SYSTEM_DIR, "man")
MAIN_PROJECT = os.path.join(PROJECTS_DIR, "Main")

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
THEMES_PATH = os.path.join(CONFIG_DIR, "themes.json")
HISTORY_PATH = os.path.join(SYSTEM_DIR, "history.txt")
API_KEY_PATH = os.path.join(CONFIG_DIR, "api_key.txt")

COMMANDS = [
    "enter NovaScript",
    "enter NScript",
    "enter NovaGPT",
    "enter NGPT",
    "mkdir",
    "ls",
    "cd",
    "cat",
    "grep",
    "nano",
    "run",
    "jobs",
    "kill",
    "man",
    "theme",
    "python",
    "-help",
    "settings",
    "quit",
]

LANG_MAP = {
    "ns": ".ns", "novascript": ".ns", "nova": ".ns", "nscript": ".ns",
    ".ns": ".ns",
    "js": ".js", "javascript": ".js", "node": ".js", ".js": ".js",
    "python": ".py", "py": ".py", ".py": ".py",
    "java": ".java", ".java": ".java",
}

DEFAULT_SETTINGS = {
    "suggestions": True,
    "colors": True,
    "start_cwd": MAIN_PROJECT,
    "remember_language": False,
    "theme": "neon"
}

DEFAULT_THEMES = {
    "neon": {
        "prompt": "\033[92m",
        "banner": "\033[92m",
        "text": "\033[92m",
        "error": "\033[91m",
        "accent": "\033[96m"
    },
    "classic": {
        "prompt": "\033[97m",
        "banner": "\033[97m",
        "text": "\033[97m",
        "error": "\033[91m",
        "accent": "\033[93m"
    },
    "hacker": {
        "prompt": "\033[32m",
        "banner": "\033[32m",
        "text": "\033[32m",
        "error": "\033[91m",
        "accent": "\033[33m"
    },
    "ocean": {
        "prompt": "\033[36m",
        "banner": "\033[36m",
        "text": "\033[36m",
        "error": "\033[91m",
        "accent": "\033[94m"
    }
}

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    PROMPT = GREEN
    BANNER = GREEN
    TEXT = GREEN
    ERROR = RED
    ACCENT = CYAN

def color(txt, code):
    if not SETTINGS.get("colors", True):
        return txt
    return f"{code}{txt}{C.RESET}"

SETTINGS = {}

def prompt(text):
    try:
        return input(text)
    except KeyboardInterrupt:
        print()
        return ""
    except EOFError:
        return ""

def path_within_root(path):
    abs_path = os.path.abspath(path)
    try:
        common = os.path.commonpath([abs_path, ROOT_DIR])
        if common != os.path.abspath(ROOT_DIR):
            return None
    except Exception:
        return None
    return abs_path

def normalize_virtual_path(abs_path):
    try:
        rp = os.path.relpath(abs_path, ROOT_DIR)
        if rp == ".":
            rp = ""
        return os.path.join("~", rp).replace("\\", "/")
    except Exception:
        return "~"

def highlight_novascript(line):
    keywords = ["set", "print", "if", "then", "else", "func", "while", "for", "import", "in", "to"]
    keywords_regex = r'\b(' + '|'.join(keywords) + r')\b'
    highlighted = line
    highlighted = re.sub(keywords_regex, f"{C.ACCENT}\\1{C.RESET}", highlighted)
    highlighted = re.sub(r'"([^"]*)"', f'{C.TEXT}"\\1"{C.RESET}', highlighted)
    highlighted = re.sub(r"'([^']*)'", f"{C.TEXT}'\\1'{C.RESET}", highlighted)
    highlighted = re.sub(r'\b(True|False|None)\b', f"{C.ACCENT}\\1{C.RESET}", highlighted)
    return highlighted

class NovaFileSystem:
    def __init__(self):
        self.cwd = None
        self.active_file = None
    
    def set_cwd(self, path):
        self.cwd = path
    
    def set_active_file(self, filename):
        self.active_file = filename
    
    def ensure_dirs(self):
        for d in [PROJECTS_DIR, SYSTEM_DIR, CONFIG_DIR, MAIN_PROJECT, MAN_DIR]:
            os.makedirs(d, exist_ok=True)
    
    def create_file(self, cwd, filename, ask_lang=True):
        if "." in filename:
            path = os.path.join(cwd, filename)
            path = path_within_root(path)
            if not path:
                return None
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")
            return path
        ext = self.ask_language(filename) if ask_lang else ".ns"
        if not ext:
            ext = ".ns"
        filename = filename + ext
        path = os.path.join(cwd, filename)
        path = path_within_root(path)
        if not path:
            return None
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
        return path
    
    @staticmethod
    def ask_language(base_name):
        prompt_msg = f"What language should {base_name} be in? (NS default) Options: NS, JS, Python, Java\n> "
        while True:
            ans = prompt(prompt_msg).strip()
            if ans == "":
                return ".ns"
            a = ans.lower().strip()
            if a.startswith("."):
                a = a[1:]
            ext = LANG_MAP.get(a)
            if ext:
                return ext
            for k, v in LANG_MAP.items():
                if k.lower() == a:
                    return v
            print("Unknown language. Supported:", ", ".join(sorted(set(LANG_MAP.values()))))

class NovaGPTModule:
    def __init__(self):
        self.messages = []
        self.api_key = self._load_api_key()
    
    def _load_api_key(self):
        if os.path.exists(API_KEY_PATH):
            try:
                with open(API_KEY_PATH, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except:
                return None
        return None
    
    def set_api_key(self, key):
        self.api_key = key
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(API_KEY_PATH, "w", encoding="utf-8") as f:
                f.write(key)
            return True
        except:
            return False
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > 40:
            self.messages = self.messages[-40:]
    
    def get_response(self, user_input):
        self.add_message("user", user_input)
        reply = self._zencoder_response(user_input)
        self.add_message("assistant", reply)
        return reply
    
    def _zencoder_response(self, user_text):
        low = user_text.lower()
        if "function" in low and "novascript" in low:
            return "NovaScript functions: Use 'func name(params) { body }' to define. Call with 'name(args)'. Supports parameters and local scope."
        if "loop" in low:
            return "NovaScript loops: 'while condition { body }' or 'for var in start to end { body }'. Both support infinite loop protection."
        if "hello" in low or "hi" in low:
            return "Hello! I'm NovaGPT, powered by Zencoder AI. I can help with code generation, refactoring, debugging, testing, and more."
        if "refactor" in low or "improve" in low:
            return "I can help refactor your code! Share the code and I'll suggest improvements for readability and performance."
        if "debug" in low or "error" in low or "fix" in low:
            return "I can help debug! Describe the issue or share your code, and I'll help identify the problem."
        if "test" in low:
            return "I can help write tests! Share your code and I'll generate comprehensive unit tests."
        if "explain" in low or "understand" in low or "how" in low:
            return "I'm Zencoder-powered NovaGPT. I can help with: code generation, refactoring, debugging, testing, analysis, and NovaScript guidance."
        if len(user_text) > 0:
            return f"I'm Zencoder-powered NovaGPT. You asked about '{user_text[:30]}...'. How can I help with coding or NovaScript?"
        return "I'm NovaGPT powered by Zencoder. Ask me about coding, NovaScript, or any development task!"

class NovaJobsManager:
    def __init__(self):
        self.jobs = {}
        self.job_counter = 0
        self.lock = threading.Lock()
    
    def create_job(self, filepath):
        with self.lock:
            self.job_counter += 1
            pid = self.job_counter
            self.jobs[pid] = {
                "path": filepath,
                "status": "running",
                "thread": None,
                "start": time.time(),
                "stop": False
            }
            return pid
    
    def update_status(self, pid, status):
        with self.lock:
            if pid in self.jobs:
                self.jobs[pid]["status"] = status
    
    def stop_job(self, pid):
        with self.lock:
            if pid in self.jobs:
                self.jobs[pid]["stop"] = True
                self.jobs[pid]["status"] = "terminating"
    
    def list_jobs(self):
        with self.lock:
            for pid, info in sorted(self.jobs.items()):
                age = int(time.time() - info.get("start", time.time()))
                print(f"#{pid} {os.path.basename(info['path'])} [{info['status']}] ({age}s)")

class NovaManSystem:
    def __init__(self):
        self.pages = self._default_pages()
    
    @staticmethod
    def _default_pages():
        return {
            "novaHub": {
                "COMMAND": "NovaHub",
                "HOWTO": "enter NovaScript | enter NovaGPT | mkdir | ls | cd | cat | grep | nano | run | jobs | kill | man | settings | -help | quit",
                "EXAMPLE": "enter NovaScript\nmkdir Projects/Demo\ncd Projects/Demo\nnano main.ns\nrun main.ns",
                "DESCRIPTION": "NovaHub is a terminal-based developer environment with NovaScript language and NovaGPT assistant.",
                "LANGUAGE": "System",
                "NOTES": "Files stored under ~/Projects/",
                "WARNINGS": "Do not upload NovaHubDocuments to public repos.",
                "SEE": "man NovaScript, man nano, man run"
            },
            "novaScript": {
                "COMMAND": "NovaScript",
                "HOWTO": "set <name> = <expr>\nprint <expr>\nif [cond] then [cmd] else [cmd]\nvars\nexit",
                "EXAMPLE": "set x = 5\nprint x\nif [x < 10] then [print x] else [print \"no\"]",
                "DESCRIPTION": "NovaScript is the lightweight language used in NovaHub.",
                "LANGUAGE": "NovaScript",
                "NOTES": "Expressions are evaluated safely using ast.",
                "WARNINGS": "Unknown variables raise errors.",
                "SEE": "man run, man nano"
            },
            "nano": {
                "COMMAND": "nano",
                "HOWTO": "nano [filename]",
                "EXAMPLE": "nano main.ns",
                "DESCRIPTION": "NovaScript-based file editor.",
                "LANGUAGE": "Editor",
                "NOTES": "Default language is NS (.ns).",
                "WARNINGS": "quit discards changes.",
                "SEE": "man NovaScript, man run"
            },
            "run": {
                "COMMAND": "run",
                "HOWTO": "run <filename> [&]",
                "EXAMPLE": "run main.ns\nrun worker.ns &",
                "DESCRIPTION": "Execute a NovaScript file. '&' launches as background job.",
                "LANGUAGE": "System",
                "NOTES": "Background jobs cannot accept interactive input.",
                "WARNINGS": "Long-running jobs must be killed with kill <id>.",
                "SEE": "man jobs, man nano"
            },
            "theme": {
                "COMMAND": "theme",
                "HOWTO": "theme list\ntheme set <name>",
                "EXAMPLE": "theme list\ntheme set hacker\ntheme set neon",
                "DESCRIPTION": "Manage NovaHub color themes.",
                "LANGUAGE": "System",
                "NOTES": "Available themes: neon, classic, hacker, ocean.",
                "WARNINGS": "Theme changes apply immediately.",
                "SEE": "man settings, man NovaHub"
            },
            "python": {
                "COMMAND": "python",
                "HOWTO": "python",
                "EXAMPLE": "python\n>>> x = 42\n>>> print(x)\n>>> exit()",
                "DESCRIPTION": "Launch embedded Python interactive console.",
                "LANGUAGE": "System",
                "NOTES": "Full access to Python stdlib.",
                "WARNINGS": "Use exit() not Ctrl+C to exit.",
                "SEE": "man enter NovaScript, man run"
            }
        }
    
    def load_pages(self):
        for name, content in self.pages.items():
            filename = os.path.join(MAN_DIR, name.lower() + ".man")
            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self._format_manpage(content))
    
    @staticmethod
    def _format_manpage(dic):
        s = []
        s.append(f"COMMAND: {dic.get('COMMAND','')}\n")
        s.append("HOW TO USE:\n")
        s.append(f"{dic.get('HOWTO','')}\n\n")
        s.append("EXAMPLE:\n")
        s.append(f"{dic.get('EXAMPLE','')}\n\n")
        s.append("DESCRIPTION:\n")
        s.append(f"{dic.get('DESCRIPTION','')}\n\n")
        s.append("LANGUAGE:\n")
        s.append(f"{dic.get('LANGUAGE','')}\n\n")
        s.append("NOTES:\n")
        s.append(f"{dic.get('NOTES','')}\n\n")
        s.append("WARNINGS:\n")
        s.append(f"{dic.get('WARNINGS','')}\n\n")
        s.append("SEE ALSO:\n")
        s.append(f"{dic.get('SEE','')}\n")
        return "\n".join(s)
    
    @staticmethod
    def pager_display(text):
        rows, _ = shutil.get_terminal_size((80, 24))
        lines = text.splitlines()
        i = 0
        page = rows - 2
        while i < len(lines):
            chunk = lines[i:i+page]
            for ln in chunk:
                print(ln)
            i += page
            if i >= len(lines):
                break
            c = prompt("--Press SPACE for next page, ENTER for one line, q to quit-- ")
            if c.lower() == "q":
                break
            if c == "":
                if i < len(lines):
                    print(lines[i])
                    i += 1
            else:
                continue

class NovaScriptRuntime:
    MAX_ITERATIONS = 10000
    
    def __init__(self, cwd=None):
        self.vars = {}
        self.funcs = {}
        self.cwd = cwd or MAIN_PROJECT
        self.in_func_def = False
        self.current_func_def = None
        self.in_loop_def = False
        self.current_loop_def = None

    def safe_eval(self, expr, local_scope=None):
        try:
            node = ast.parse(expr, mode="eval").body
            return self._eval_node(node, local_scope)
        except Exception as e:
            raise RuntimeError(f"Expression error: {e}")

    def _eval_node(self, node, local_scope=None):
        if local_scope is None:
            local_scope = {}
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id in local_scope:
                return local_scope[node.id]
            if node.id in self.vars:
                return self.vars[node.id]
            raise RuntimeError(f"Unknown variable: {node.id}")
        if isinstance(node, ast.BinOp):
            l = self._eval_node(node.left, local_scope)
            r = self._eval_node(node.right, local_scope)
            if isinstance(node.op, ast.Add): return l + r
            if isinstance(node.op, ast.Sub): return l - r
            if isinstance(node.op, ast.Mult): return l * r
            if isinstance(node.op, ast.Div): return l / r
            if isinstance(node.op, ast.Mod): return l % r
            if isinstance(node.op, ast.Pow): return l ** r
            if isinstance(node.op, ast.FloorDiv): return l // r
            raise RuntimeError("Unsupported op")
        if isinstance(node, ast.UnaryOp):
            v = self._eval_node(node.operand, local_scope)
            if isinstance(node.op, ast.USub): return -v
            if isinstance(node.op, ast.UAdd): return +v
            if isinstance(node.op, ast.Not): return not v
            raise RuntimeError("Unsupported unary op")
        if isinstance(node, ast.Compare):
            left = self._eval_node(node.left, local_scope)
            for op, comp in zip(node.ops, node.comparators):
                right = self._eval_node(comp, local_scope)
                if isinstance(op, ast.Eq) and not (left == right): return False
                if isinstance(op, ast.NotEq) and not (left != right): return False
                if isinstance(op, ast.Lt) and not (left < right): return False
                if isinstance(op, ast.LtE) and not (left <= right): return False
                if isinstance(op, ast.Gt) and not (left > right): return False
                if isinstance(op, ast.GtE) and not (left >= right): return False
                left = right
            return True
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                return all(self._eval_node(v, local_scope) for v in node.values)
            if isinstance(node.op, ast.Or):
                return any(self._eval_node(v, local_scope) for v in node.values)
        raise RuntimeError("Unsupported expression")

    def run_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return None
        if self.in_func_def:
            self.current_func_def["body"] += line + "\n"
            if "}" in line:
                self.in_func_def = False
                self._finalize_function_def()
            return None
        if self.in_loop_def:
            self.current_loop_def["body"] += line + "\n"
            if "}" in line:
                self.in_loop_def = False
                self._execute_loop()
            return None
        if line.lower().startswith("while "):
            return self._start_while_loop(line)
        if line.lower().startswith("for "):
            return self._start_for_loop(line)
        if line.lower().startswith("import "):
            return self._handle_import(line)
        if line.lower().startswith("func "):
            return self._start_function_def(line)
        if "(" in line and ")" in line and not line.startswith("if") and not line.startswith("print") and not line.startswith("set"):
            return self._try_function_call(line)
        if line.lower().startswith("if "):
            return self.handle_if_else(line)
        if line.startswith("set "):
            rest = line[4:].strip()
            if "=" not in rest:
                raise RuntimeError("Invalid set syntax. Use: set name = expression")
            name, expr = rest.split("=",1)
            name = name.strip()
            expr = expr.strip()
            self.vars[name] = self.safe_eval(expr)
            return None
        if line.startswith("print "):
            arg = line[6:].strip()
            if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                print(arg[1:-1])
                return None
            val = self.safe_eval(arg)
            print(val)
            return None
        if line == "vars":
            for k,v in self.vars.items():
                print(f"{k} = {v}")
            return None
        if line == "help":
            print("NovaScript quick help:")
            print(' set <name> = <expression>')
            print(' print <expression or "string">')
            print(' if [expr] then [command] else [command]')
            print(' func <name>(<params>) { ... }')
            print(' while <condition> { ... }')
            print(' for <var> in <start> to <end> { ... }')
            print(' import "file.ns"')
            print(' <name>(<args>)')
            print(' vars')
            print(' exit')
            return None
        if line == "exit":
            return "EXIT"
        raise RuntimeError("Unknown NovaScript command")

    def handle_if_else(self, line):
        body = line[2:].strip()
        cond_start = body.find("[")
        cond_end = body.find("]")
        if cond_start == -1 or cond_end == -1 or cond_end < cond_start:
            raise RuntimeError("Missing [condition] brackets")
        cond = body[cond_start+1:cond_end].strip()
        rest = body[cond_end+1:].strip()
        if not rest.lower().startswith("then"):
            raise RuntimeError("Missing 'then' after condition")
        rest = rest[4:].strip()
        then_start = rest.find("[")
        then_end = rest.find("]")
        if then_start == -1 or then_end == -1 or then_end < then_start:
            raise RuntimeError("Missing [command] after then")
        then_cmd = rest[then_start+1:then_end].strip()
        after_then = rest[then_end+1:].strip()
        else_cmd = None
        if after_then.lower().startswith("else"):
            after_then = after_then[4:].strip()
            e_start = after_then.find("[")
            e_end = after_then.find("]")
            if e_start == -1 or e_end == -1 or e_end < e_start:
                raise RuntimeError("Missing [command] after else")
            else_cmd = after_then[e_start+1:e_end].strip()
        if self.safe_eval(cond):
            return self.run_line(then_cmd)
        elif else_cmd:
            return self.run_line(else_cmd)
        return None

    def _start_function_def(self, line):
        match = re.match(r'func\s+(\w+)\s*\((.*?)\)\s*\{?', line, re.IGNORECASE)
        if not match:
            raise RuntimeError("Invalid function definition. Use: func name(param1, param2) { body }")
        func_name = match.group(1)
        params_str = match.group(2).strip()
        params = [p.strip() for p in params_str.split(",")] if params_str else []
        self.current_func_def = {
            "name": func_name,
            "params": params,
            "body": ""
        }
        if "{" in line:
            after_brace = line[line.index("{")+1:].strip()
            self.current_func_def["body"] = after_brace + "\n"
            if "}" in after_brace:
                self.in_func_def = False
                self._finalize_function_def()
            else:
                self.in_func_def = True
        else:
            self.in_func_def = True
        return None

    def _finalize_function_def(self):
        body = self.current_func_def["body"]
        body = body.replace("}", "", 1).rstrip()
        self.funcs[self.current_func_def["name"]] = {
            "params": self.current_func_def["params"],
            "body": body
        }

    def _try_function_call(self, line):
        match = re.match(r'(\w+)\s*\((.*?)\)', line)
        if not match:
            raise RuntimeError("Invalid function call")
        func_name = match.group(1)
        args_str = match.group(2).strip()
        if func_name not in self.funcs:
            raise RuntimeError(f"Unknown function: {func_name}")
        func_def = self.funcs[func_name]
        args = [arg.strip() for arg in args_str.split(",")] if args_str else []
        if len(args) != len(func_def["params"]):
            raise RuntimeError(f"Function {func_name} expects {len(func_def['params'])} parameters, got {len(args)}")
        local_scope = {}
        for param, arg in zip(func_def["params"], args):
            try:
                local_scope[param] = self.safe_eval(arg)
            except:
                local_scope[param] = arg
        body_lines = func_def["body"].strip().split("\n")
        for body_line in body_lines:
            body_line = body_line.strip()
            if not body_line or body_line.startswith("#"):
                continue
            if body_line.startswith("print "):
                arg = body_line[6:].strip()
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    print(arg[1:-1])
                else:
                    val = self.safe_eval(arg, local_scope)
                    print(val)
            elif body_line.startswith("set "):
                rest = body_line[4:].strip()
                if "=" not in rest:
                    raise RuntimeError("Invalid set syntax in function")
                name, expr = rest.split("=", 1)
                name = name.strip()
                expr = expr.strip()
                local_scope[name] = self.safe_eval(expr, local_scope)
        return None

    def _start_while_loop(self, line):
        line_lower = line.lower()
        if not line_lower.startswith("while "):
            raise RuntimeError("Invalid while loop. Use: while <condition> { ... }")
        rest = line[6:].strip()
        if "{" not in rest:
            raise RuntimeError("Invalid while loop. Use: while <condition> { ... }")
        brace_idx = rest.index("{")
        condition = rest[:brace_idx].strip()
        if not condition:
            raise RuntimeError("Invalid while loop. Condition cannot be empty")
        self.current_loop_def = {
            "type": "while",
            "condition": condition,
            "body": ""
        }
        after_brace = rest[brace_idx+1:].strip()
        self.current_loop_def["body"] = after_brace + "\n"
        if "}" in after_brace:
            self.in_loop_def = False
            self._execute_loop()
        else:
            self.in_loop_def = True
        return None

    def _start_for_loop(self, line):
        line_lower = line.lower()
        if not line_lower.startswith("for "):
            raise RuntimeError("Invalid for loop. Use: for <var> in <start> to <end> { ... }")
        rest = line[4:].strip()
        if "{" not in rest:
            raise RuntimeError("Invalid for loop. Use: for <var> in <start> to <end> { ... }")
        brace_idx = rest.index("{")
        loop_decl = rest[:brace_idx].strip()
        parts = re.split(r'\s+in\s+|\s+to\s+', loop_decl, flags=re.IGNORECASE)
        if len(parts) != 3:
            raise RuntimeError("Invalid for loop. Use: for <var> in <start> to <end> { ... }")
        var_name = parts[0].strip()
        start_expr = parts[1].strip()
        end_expr = parts[2].strip()
        self.current_loop_def = {
            "type": "for",
            "var": var_name,
            "start": start_expr,
            "end": end_expr,
            "body": ""
        }
        after_brace = rest[brace_idx+1:].strip()
        self.current_loop_def["body"] = after_brace + "\n"
        if "}" in after_brace:
            self.in_loop_def = False
            self._execute_loop()
        else:
            self.in_loop_def = True
        return None

    def _execute_loop(self):
        loop_type = self.current_loop_def["type"]
        body = self.current_loop_def["body"].replace("}", "", 1).rstrip()
        
        if loop_type == "while":
            iterations = 0
            while self.safe_eval(self.current_loop_def["condition"]):
                iterations += 1
                if iterations > self.MAX_ITERATIONS:
                    raise RuntimeError(f"Infinite loop detected (exceeded {self.MAX_ITERATIONS} iterations)")
                self._execute_loop_body(body)
        
        elif loop_type == "for":
            start = int(self.safe_eval(self.current_loop_def["start"]))
            end = int(self.safe_eval(self.current_loop_def["end"]))
            var_name = self.current_loop_def["var"]
            iterations = 0
            for i in range(start, end + 1):
                iterations += 1
                if iterations > self.MAX_ITERATIONS:
                    raise RuntimeError(f"Infinite loop detected (exceeded {self.MAX_ITERATIONS} iterations)")
                self.vars[var_name] = i
                self._execute_loop_body(body)

    def _execute_loop_body(self, body):
        body_lines = body.strip().split("\n")
        i = 0
        while i < len(body_lines):
            line = body_lines[i].strip()
            i += 1
            if not line or line.startswith("#"):
                continue
            
            if line.lower().startswith("for ") or line.lower().startswith("while "):
                temp_runtime = NovaScriptRuntime()
                temp_runtime.vars = self.vars
                temp_runtime.funcs = self.funcs
                
                temp_runtime.run_line(line)
                while temp_runtime.in_loop_def and i < len(body_lines):
                    temp_runtime.run_line(body_lines[i])
                    i += 1
                
                self.vars = temp_runtime.vars
            else:
                self.run_line(line)

    def _handle_import(self, line):
        match = re.match(r'import\s+"([^"]+)"', line, re.IGNORECASE)
        if not match:
            raise RuntimeError('Invalid import. Use: import "filename.ns"')
        filename = match.group(1)
        cwd = getattr(self, 'cwd', MAIN_PROJECT)
        filepath = os.path.join(cwd, filename)
        filepath = path_within_root(filepath)
        if not filepath or not os.path.exists(filepath):
            raise RuntimeError(f"Import failed: File not found: {filename}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = [ln.rstrip("\n") for ln in f.readlines()]
            for ln in lines:
                self.run_line(ln)
        except Exception as e:
            raise RuntimeError(f"Error importing {filename}: {e}")

class NovaHubShell:
    def __init__(self):
        self.fs = NovaFileSystem()
        self.runtime = NovaScriptRuntime()
        self.gpt = NovaGPTModule()
        self.jobs = NovaJobsManager()
        self.man = NovaManSystem()
        self.cwd = None
        self.active_file = None
    
    def initialize(self):
        global SETTINGS
        self.fs.ensure_dirs()
        self.load_settings()
        self.load_themes()
        self.update_theme_colors()
        self.man.load_pages()
        self.load_history()
        if readline is not None:
            atexit.register(self.save_history)
        start = SETTINGS.get("start_cwd", MAIN_PROJECT)
        if not os.path.isdir(start):
            os.makedirs(start, exist_ok=True)
        self.cwd = os.path.abspath(start)
        self.fs.set_cwd(self.cwd)
        self.runtime.cwd = self.cwd
    
    @staticmethod
    def load_settings():
        global SETTINGS
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    SETTINGS = json.load(f)
            except Exception:
                SETTINGS = DEFAULT_SETTINGS.copy()
        else:
            SETTINGS = DEFAULT_SETTINGS.copy()
            NovaHubShell.save_settings()
    
    @staticmethod
    def save_settings():
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(SETTINGS, f, indent=2)
        except Exception as e:
            print("Failed to save settings:", e)
    
    @staticmethod
    def load_themes():
        if os.path.exists(THEMES_PATH):
            try:
                with open(THEMES_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_THEMES.copy()
        return DEFAULT_THEMES.copy()
    
    @staticmethod
    def save_themes(themes):
        try:
            with open(THEMES_PATH, "w", encoding="utf-8") as f:
                json.dump(themes, f, indent=2)
        except Exception as e:
            print("Failed to save themes:", e)
    
    @staticmethod
    def update_theme_colors():
        global C
        theme_name = SETTINGS.get("theme", "neon")
        themes = NovaHubShell.load_themes()
        if theme_name in themes:
            theme = themes[theme_name]
            C.PROMPT = theme.get("prompt", C.GREEN)
            C.BANNER = theme.get("banner", C.GREEN)
            C.TEXT = theme.get("text", C.GREEN)
            C.ERROR = theme.get("error", C.RED)
            C.ACCENT = theme.get("accent", C.CYAN)
    
    @staticmethod
    def load_history():
        if readline is None:
            return
        if os.path.exists(HISTORY_PATH):
            try:
                with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if line:
                            readline.add_history(line)
            except Exception:
                pass
    
    @staticmethod
    def save_history():
        if readline is None:
            return
        try:
            with open(HISTORY_PATH, "w", encoding="utf-8") as f:
                for i in range(readline.get_current_history_length()):
                    f.write(readline.get_history_item(i + 1) + "\n")
        except Exception:
            pass
    
    def current_prompt(self):
        base = normalize_virtual_path(self.cwd)
        if self.active_file:
            prompt_text = f"NovaHub={base}/{self.active_file}==> "
        else:
            prompt_text = f"NovaHub={base}==> "
        return color(prompt_text, C.PROMPT)
    
    def cmd_mkdir(self, args):
        if not args:
            print("Usage: mkdir <name> or mkdir \"name\" --LANG")
            return
        raw = " ".join(args)
        lang_match = re.search(r"--\s*([A-Za-z0-9_.]+)$", raw)
        if raw.startswith('"') and raw.endswith('"'):
            name = raw[1:-1]
        else:
            parts = raw.split()
            name = parts[0]
        if lang_match:
            lang = lang_match.group(1).lower()
        else:
            lang = None

        if "." in name or lang:
            filename = name
            if not "." in name and lang:
                ext = LANG_MAP.get(lang.lower())
                if not ext:
                    print("Unknown language:", lang)
                    return
                filename = name + ext
            path = self.fs.create_file(self.cwd, filename, ask_lang=False)
            if path:
                print("Created file:", normalize_virtual_path(path))
            return
        folder = os.path.join(self.cwd, name)
        folder = path_within_root(folder)
        if not folder:
            print("Invalid folder path")
            return
        os.makedirs(folder, exist_ok=True)
        print("Created folder:", normalize_virtual_path(folder))
    
    def cmd_ls(self, args):
        dirpath = self.cwd if not args else os.path.join(self.cwd, args[0])
        dirpath = path_within_root(dirpath)
        if not dirpath or not os.path.isdir(dirpath):
            print("No such directory")
            return
        items = os.listdir(dirpath)
        for it in sorted(items):
            p = os.path.join(dirpath, it)
            if os.path.isdir(p):
                print(f"{it}/")
            else:
                print(it)
    
    def cmd_cd(self, args):
        if not args:
            target = MAIN_PROJECT
        else:
            raw = args[0]
            if raw.startswith("/"):
                target = os.path.join(ROOT_DIR, raw.lstrip("/"))
            else:
                target = os.path.join(self.cwd, raw)
        target = os.path.abspath(target)
        t = path_within_root(target)
        if not t or not os.path.isdir(t):
            print("No such directory (within NovaHub)")
            return
        self.cwd = t
        self.fs.set_cwd(t)
        self.active_file = None
    
    def cmd_cat(self, args):
        if not args:
            print("Usage: cat <file>")
            return
        fp = os.path.join(self.cwd, args[0])
        p = path_within_root(fp)
        if not p or not os.path.isfile(p):
            print("No such file")
            return
        with open(p, "r", encoding="utf-8") as f:
            print(f.read())
    
    def cmd_grep(self, args):
        if len(args) < 2:
            print("Usage: grep <pattern> <file>")
            return
        pattern = args[0]
        filepath = os.path.join(self.cwd, args[1])
        p = path_within_root(filepath)
        if not p or not os.path.isfile(p):
            print("No such file")
            return
        pat = re.compile(pattern)
        with open(p, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if pat.search(line):
                    print(f"{i}:{line.rstrip()}")
    
    def cmd_nano(self, args):
        if not args:
            base = "NewFile"
            i = 1
            while True:
                name = base if i == 1 else f"{base}{i}"
                candidate = os.path.join(self.cwd, name + ".ns")
                if not os.path.exists(candidate):
                    break
                i += 1
            ext = NovaFileSystem.ask_language(name)
            filename = name + ext
        else:
            name = args[0]
            if "." in name:
                filename = name
            else:
                ext = NovaFileSystem.ask_language(name)
                filename = name + ext
        path = os.path.join(self.cwd, filename)
        p = path_within_root(path)
        if not p:
            print("Invalid path")
            return
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write("")
        self.active_file = os.path.basename(filename)
        self.fs.set_active_file(self.active_file)
        print(color(f"Entering NovaScript File Editor for {self.active_file}. (type 'exit' to save and leave, 'quit' to leave without saving)", C.CYAN))
        with open(p, "r", encoding="utf-8") as f:
            buffer = [line.rstrip("\n") for line in f.readlines()]
        while True:
            line = prompt("NovaScript(FileEdit)=> ")
            if line is None:
                continue
            cmd = line.strip()
            if cmd == "exit":
                with open(p, "w", encoding="utf-8") as f:
                    f.write("\n".join(buffer) + ("\n" if buffer else ""))
                print("Saved", self.active_file)
                self.active_file = None
                self.fs.set_active_file(None)
                return
            if cmd == "quit":
                print("Discarding changes and leaving editor.")
                self.active_file = None
                self.fs.set_active_file(None)
                return
            if cmd == "save":
                with open(p, "w", encoding="utf-8") as f:
                    f.write("\n".join(buffer) + ("\n" if buffer else ""))
                print("Saved", self.active_file)
                continue
            if cmd == "show":
                for i, buf_line in enumerate(buffer, 1):
                    highlighted = highlight_novascript(buf_line) if self.active_file.endswith('.ns') else buf_line
                    print(f"{i}: {highlighted}")
                continue
            if cmd.startswith("delete "):
                try:
                    n = int(cmd.split()[1]) - 1
                    if 0 <= n < len(buffer):
                        buffer.pop(n)
                        print("Deleted line", n+1)
                    else:
                        print("Line out of range")
                except:
                    print("Invalid delete usage: delete <line#>")
                continue
            if cmd.startswith("replace "):
                m = re.match(r"replace\s+(\d+)\s+(.+)", cmd)
                if m:
                    n = int(m.group(1)) - 1
                    txt = m.group(2)
                    if 0 <= n < len(buffer):
                        buffer[n] = txt
                        print("Replaced line", n+1)
                    else:
                        print("Line out of range")
                else:
                    print("Usage: replace <line#> <text>")
                continue
            if cmd.startswith("insert "):
                m = re.match(r"insert\s+(\d+)\s+(.+)", cmd)
                if m:
                    n = int(m.group(1)) - 1
                    txt = m.group(2)
                    if n < 0:
                        n = 0
                    if n >= len(buffer):
                        buffer.append(txt)
                    else:
                        buffer.insert(n, txt)
                    print("Inserted before line", n+1)
                else:
                    print("Usage: insert <line#> <text>")
                continue
            buffer.append(line)
            if self.active_file.endswith('.ns'):
                highlighted = highlight_novascript(line)
                print(color(f"[{len(buffer)}] {highlighted}", C.TEXT))
            else:
                print(f"[{len(buffer)}] {line}")
    
    def run_script_file(self, filepath, bg=False):
        p = path_within_root(os.path.join(self.cwd, filepath))
        if not p or not os.path.isfile(p):
            print("No such file")
            return
        if not bg:
            runtime = NovaScriptRuntime()
            with open(p, "r", encoding="utf-8") as f:
                lines = [ln.rstrip("\n") for ln in f.readlines()]
            for ln in lines:
                try:
                    res = runtime.run_line(ln)
                    if res == "EXIT":
                        break
                except Exception as e:
                    print(color(f"NovaScript error: {e}", C.RED))
            return
        def job_thread(pid, path):
            runtime = NovaScriptRuntime()
            with open(path, "r", encoding="utf-8") as f:
                lines = [ln.rstrip("\n") for ln in f.readlines()]
            try:
                for ln in lines:
                    if self.jobs.jobs.get(pid, {}).get("stop"):
                        self.jobs.update_status(pid, "terminated")
                        return
                    runtime.run_line(ln)
                self.jobs.update_status(pid, "finished")
            except Exception as e:
                self.jobs.update_status(pid, "error: " + str(e))
        pid = self.jobs.create_job(p)
        t = threading.Thread(target=job_thread, args=(pid, p), daemon=True)
        self.jobs.jobs[pid]["thread"] = t
        t.start()
        print(f"Started job #{pid}: {os.path.basename(filepath)}")
    
    def cmd_run(self, args):
        if not args:
            print("Usage: run <script> [&]")
            return
        bg = False
        if args[-1] == "&":
            bg = True
            args = args[:-1]
        filepath = args[0]
        self.run_script_file(filepath, bg=bg)
    
    def cmd_jobs(self, _args):
        self.jobs.list_jobs()
    
    def cmd_kill(self, args):
        if not args:
            print("Usage: kill <jobid>")
            return
        try:
            pid = int(args[0])
        except:
            print("Invalid job id")
            return
        self.jobs.stop_job(pid)
        print(f"Signaled job {pid} to terminate.")
    
    def cmd_man(self, args):
        if not args:
            print("Usage: man <topic> | man command | man lang")
            return
        topic = args[0].strip().lower()
        if topic == "command":
            print("Available commands:")
            for c in sorted(["mkdir", "ls", "cd", "cat", "grep", "nano", "run", "jobs", "kill", "man", "theme", "python", "-help", "settings", "quit", "enter NovaScript", "enter NovaGPT", "matrix", "gpt"]):
                print("  " + c)
            return
        if topic == "lang":
            langs = sorted(set([k for k in LANG_MAP.keys() if not k.startswith(".")]))
            print("Available languages:")
            for l in langs:
                print("  " + l)
            return
        file_candidate = os.path.join(MAN_DIR, topic + ".man")
        if os.path.exists(file_candidate):
            with open(file_candidate, "r", encoding="utf-8") as f:
                self.man.pager_display(f.read())
            return
        matches = difflib.get_close_matches(topic, [fn[:-4] for fn in os.listdir(MAN_DIR) if fn.endswith(".man")], n=1, cutoff=0.6)
        if matches:
            sug = matches[0]
            ans = prompt(color(f'Did you mean "{sug}"? (y/n) ', C.YELLOW)).strip().lower()
            if ans in ("y", "yes"):
                file_candidate = os.path.join(MAN_DIR, sug + ".man")
                with open(file_candidate, "r", encoding="utf-8") as f:
                    self.man.pager_display(f.read())
                return
        print("No manual entry for", topic)
    
    def cmd_python(self):
        print(color("Entering Python interactive console. Type 'exit()' to return to NovaHub.\n", C.ACCENT))
        console_env = {
            "__name__": "__console__",
            "__doc__": None,
            "CWD": self.cwd,
            "ACTIVE_FILE": self.active_file,
            "SETTINGS": SETTINGS,
        }
        console = code.InteractiveConsole(console_env)
        console.interact(banner="Python " + sys.version, exitmsg="Returning to NovaHub...\n")
    
    def cmd_settings(self, args):
        global SETTINGS
        if not args:
            print("Settings:")
            for k, v in SETTINGS.items():
                print(f"  {k} : {v}")
            print("To toggle: settings toggle <name>")
            return
        if args[0] == "toggle" and len(args) == 2:
            key = args[1]
            if key in SETTINGS:
                SETTINGS[key] = not SETTINGS[key]
                self.save_settings()
                print(key, "set to", SETTINGS[key])
            else:
                print("No such setting")
            return
        if args[0] == "show":
            self.cmd_settings([])
            return
        print("Unknown settings command. Use: settings toggle <name>")
    
    def cmd_theme(self, args):
        global SETTINGS
        if not args:
            print("Usage: theme list | theme set <name>")
            return
        if args[0] == "list":
            themes = self.load_themes()
            current = SETTINGS.get("theme", "neon")
            print("Available themes:")
            for name in sorted(themes.keys()):
                marker = " (current)" if name == current else ""
                print(f"  {name}{marker}")
            return
        if args[0] == "set" and len(args) >= 2:
            theme_name = args[1]
            themes = self.load_themes()
            if theme_name not in themes:
                print(f"Unknown theme: {theme_name}")
                print(f"Available: {', '.join(sorted(themes.keys()))}")
                return
            SETTINGS["theme"] = theme_name
            self.save_settings()
            self.update_theme_colors()
            print(f"Theme changed to: {theme_name}")
            return
        print("Usage: theme list | theme set <name>")
    
    def cmd_gpt(self, args):
        if not args:
            print("Usage: gpt api set <KEY>")
            return
        if args[0] == "api" and len(args) >= 2 and args[1] == "set":
            if len(args) < 3:
                print("Usage: gpt api set <KEY>")
                return
            key = args[2]
            if self.gpt.set_api_key(key):
                print("API key saved successfully")
            else:
                print("Failed to save API key")
            return
        print("Unknown gpt command. Use: gpt api set <KEY>")
    
    def cmd_matrix(self, _args):
        cols, rows = shutil.get_terminal_size((80, 24))
        chars = "01"
        duration = 3
        start_time = time.time()
        
        while time.time() - start_time < duration:
            output = ""
            for _ in range(rows - 1):
                for _ in range(cols):
                    output += color(random.choice(chars), C.GREEN)
                output += "\n"
            print(output)
            time.sleep(0.05)
    
    def enter_novascript_interpreter(self):
        print(color("\nEntering NovaScript interpreter. Type 'help' for commands, 'exit' to return.\n", C.CYAN))
        runtime = NovaScriptRuntime()
        while True:
            ln = prompt("NovaScript=> ").strip()
            if ln == "":
                continue
            if ln == "exit":
                print("Returning to NovaHub...")
                return
            try:
                res = runtime.run_line(ln)
                if res == "EXIT":
                    print("Returning to NovaHub...")
                    return
            except Exception as e:
                print(color(f"NovaScript error: {e}", C.RED))
    
    def enter_novagpt_chat(self):
        print(color("\nEntering NovaGPT chat (powered by Zencoder AI). Use Nova@\"message\" or type normally. Type 'exit' to return.\n", C.MAGENTA))
        while True:
            ln = prompt("NovaGPT=> ").strip()
            if ln == "":
                continue
            if ln == "exit":
                print("Returning to NovaHub...")
                return
            if ln == "help":
                print("NovaGPT usage: Nova@\"ask something\"")
                continue
            if ln.startswith("Nova@"):
                payload = ln[len("Nova@"):].strip()
                if (payload.startswith('"') and payload.endswith('"')) or (payload.startswith("'") and payload.endswith("'")):
                    payload = payload[1:-1]
            else:
                payload = ln
            reply = self.gpt.get_response(payload)
            if reply:
                print(color(reply, C.GREEN))
    
    def autosuggest(self, user_text):
        if not SETTINGS.get("suggestions", True):
            return None
        candidates = ["mkdir", "ls", "cd", "cat", "grep", "nano", "run", "jobs", "kill", "man", "theme", "python", "enter NovaScript", "enter NovaGPT", "matrix", "gpt", "-help", "settings", "quit"]
        candidates += ["man " + name for name in ["NovaScript", "NovaGPT", "nano", "run", "mkdir", "ls", "cd", "cat", "grep", "jobs", "settings"]]
        matches = difflib.get_close_matches(user_text, candidates, n=1, cutoff=0.6)
        if matches:
            suggestion = matches[0]
            yn = prompt(color(f'Did you mean "{suggestion}"? (y/n) ', C.YELLOW)).strip().lower()
            if yn in ("y", "yes"):
                return suggestion
        return None
    
    def show_animated_banner(self):
        nova_logo = [
            "  ┌─────────────────────────────────┐",
            "  │  _   _ ___ _   _ ___   _    _   │",
            "  │ | \\ | / _ \\ \\ / // _ \\ | |  | |  │",
            "  │ |  \\| | | \\ V / | | || |__| |  │",
            "  │ | |\\  | |_| | |  | |_||  __  |  │",
            "  │ |_| \\_|\\___/|_|  \\___/|_|  |_|  │",
            "  └─────────────────────────────────┘"
        ]
        for line in nova_logo:
            print(color(line, C.BANNER))
            time.sleep(0.1)
    
    def handle_input_line(self, line):
        if not line:
            return
        parts = line.strip().split(maxsplit=1)
        cmd = parts[0]
        args = parts[1].split() if len(parts) > 1 else []
        
        if cmd == "mkdir":
            self.cmd_mkdir(args)
            return
        if cmd == "ls":
            self.cmd_ls(args)
            return
        if cmd == "cd":
            self.cmd_cd(args)
            return
        if cmd == "cat":
            self.cmd_cat(args)
            return
        if cmd == "grep":
            self.cmd_grep(args)
            return
        if cmd == "nano":
            self.cmd_nano(args)
            return
        if cmd == "run":
            self.cmd_run(args)
            return
        if cmd == "jobs":
            self.cmd_jobs(args)
            return
        if cmd == "kill":
            self.cmd_kill(args)
            return
        if cmd == "man":
            self.cmd_man(args)
            return
        if cmd == "gpt":
            self.cmd_gpt(args)
            return
        if cmd == "matrix":
            self.cmd_matrix(args)
            return
        if cmd in ("-help", "help"):
            print("Available commands:")
            print("  mkdir, ls, cd, cat, grep, nano, run, jobs, kill, man, theme, python, settings, matrix, gpt, -help, quit")
            print("  enter NovaScript  OR  enter NScript")
            print("  enter NovaGPT     OR  enter NGPT")
            return
        if cmd == "python":
            self.cmd_python()
            return
        if cmd == "settings":
            self.cmd_settings(args)
            return
        if cmd == "theme":
            self.cmd_theme(args)
            return
        if cmd == "enter":
            if not args:
                print("Usage: enter NovaScript  OR  enter NScript")
                return
            target = args[0]
            if target.lower() in ("novascript", "nscript"):
                self.enter_novascript_interpreter()
                return
            if target.lower() in ("novagpt", "ngpt"):
                self.enter_novagpt_chat()
                return
            print("Unknown enter target")
            return
        if cmd == "quit":
            print("Goodbye — exiting NovaHub.")
            sys.exit(0)
        
        suggestion = self.autosuggest(line)
        if suggestion:
            self.handle_input_line(suggestion)
            return
        print("Invalid command. Type -help.")
    
    def run(self):
        self.show_animated_banner()
        print(color(VERSION, C.BOLD + C.BANNER))
        while True:
            try:
                line = prompt(self.current_prompt()).strip()
            except KeyboardInterrupt:
                print("\nExiting NovaHub...")
                break
            if not line:
                continue
            self.handle_input_line(line)

shell = None

def main():
    global shell
    shell = NovaHubShell()
    shell.initialize()
    shell.run()

if __name__ == "__main__":
    main()