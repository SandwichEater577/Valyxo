#!/usr/bin/env python3
"""
NovaHub D-Edition single-file (Phase 1)
Features implemented:
 - Project folder auto-create under ~/NovaHubDocuments
 - Prompt: NovaHub=~/Projects/<activefolder>/<activefile==>
 - Virtual filesystem (Projects/System/Config)
 - Commands: mkdir, ls, cd, cat, grep, nano, run, jobs, kill, man, -help, settings, quit
 - nano = NovaScript-based file editor (edits saved on exit; lines NOT executed)
 - NovaScript runtime with safe AST eval & bracketed if [..] then [..] else [..]
 - run supports background with & (job control via threads)
 - man pages stored and paged (SPACE/ENTER/q)
 - autosuggest via difflib + y/n
 - language mapping (NS, JS, Python, Java)
 - settings persist in Config/config.json
 - simulated NovaGPT
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

# --------------- CONFIG & STATE ----------------
APP_NAME = "NovaHub"
VERSION = "NovaHub D-Edition v0.89"
HOME = os.path.expanduser("~")
ROOT_FOLDER_NAME = "NovaHubDocuments"
ROOT_DIR = os.path.join(HOME, ROOT_FOLDER_NAME)
PROJECTS_DIR = os.path.join(ROOT_DIR, "Projects")
SYSTEM_DIR = os.path.join(ROOT_DIR, "System")
CONFIG_DIR = os.path.join(ROOT_DIR, "Config")
MAN_DIR = os.path.join(SYSTEM_DIR, "man")
MAIN_PROJECT = os.path.join(PROJECTS_DIR, "Main")

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

# Commands list for suggestions
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
    "-help",
    "settings",
    "quit",
]

# Language mapping
LANG_MAP = {
    "ns": ".ns", "novascript": ".ns", "nova": ".ns", "nscript": ".ns",
    ".ns": ".ns",
    "js": ".js", "javascript": ".js", "node": ".js", ".js": ".js",
    "python": ".py", "py": ".py", ".py": ".py",
    "java": ".java", ".java": ".java",
}

# Settings default
DEFAULT_SETTINGS = {
    "suggestions": True,
    "colors": True,
    "start_cwd": MAIN_PROJECT,
    "remember_language": False
}

# Colors (if enabled)
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"

def color(txt, code):
    if not SETTINGS.get("colors", True):
        return txt
    return f"{code}{txt}{C.RESET}"

# runtime & job tracking
JOBS = {}
JOB_COUNTER = 0
JOBS_LOCK = threading.Lock()

# current state
CWD = None          # current working directory (absolute)
ACTIVE_FILE = None  # currently active filename (basename)
SETTINGS = {}

# ASCII banner
BANNER = r"""
 _      ____  _     ____    _     _     ____  
/ \  /|/  _ \/ \ |\/  _ \  / \ /|/ \ /\/  __\ 
| |\ ||| / \|| | //| / \|  | |_||| | ||| | // 
| | \||| \_/|| \// | |-||  | | ||| \_/|| |_\
\_/  \|\____/\__/  \_/ \|  \_/ \|\____/\____/
"""

# ------------------- UTILITIES -------------------
def ensure_dirs():
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    os.makedirs(SYSTEM_DIR, exist_ok=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(MAIN_PROJECT, exist_ok=True)
    os.makedirs(MAN_DIR, exist_ok=True)

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
        save_settings()

def save_settings():
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(SETTINGS, f, indent=2)
    except Exception as e:
        print("Failed to save settings:", e)

def prompt(text):
    try:
        return input(text)
    except KeyboardInterrupt:
        print()
        return ""
    except EOFError:
        return ""

def path_within_root(path):
    # Return the absolute normalized path if inside ROOT_DIR, else None
    abs_path = os.path.abspath(path)
    try:
        common = os.path.commonpath([abs_path, ROOT_DIR])
        if common != os.path.abspath(ROOT_DIR):
            return None
    except Exception:
        return None
    return abs_path

def normalize_virtual_path(abs_path):
    # Returns path relative to ROOT_DIR with ~/ prefix
    try:
        rp = os.path.relpath(abs_path, ROOT_DIR)
        if rp == ".":
            rp = ""
        return os.path.join("~", rp).replace("\\", "/")
    except Exception:
        return "~"

def current_prompt():
    base = normalize_virtual_path(CWD)
    if ACTIVE_FILE:
        return f"NovaHub={base}/{ACTIVE_FILE}==> "
    else:
        return f"NovaHub={base}==> "

def autosuggest(user_text):
    if not SETTINGS.get("suggestions", True):
        return None
    candidates = COMMANDS + [ "man " + name for name in ["NovaScript","NovaGPT","nano","run","mkdir","ls","cd","cat","grep","jobs","settings"] ]
    matches = difflib.get_close_matches(user_text, candidates, n=1, cutoff=0.6)
    if matches:
        suggestion = matches[0]
        yn = prompt(color(f'Did you mean "{suggestion}"? (y/n) ', C.YELLOW)).strip().lower()
        if yn in ("y", "yes"):
            return suggestion
    return None

# ------------------ NovaScript Runtime (safe) ------------------
class NovaScriptRuntime:
    def __init__(self):
        self.vars = {}

    def safe_eval(self, expr):
        try:
            node = ast.parse(expr, mode="eval").body
            return self._eval_node(node)
        except Exception as e:
            raise RuntimeError(f"Expression error: {e}")

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id in self.vars:
                return self.vars[node.id]
            raise RuntimeError(f"Unknown variable: {node.id}")
        if isinstance(node, ast.BinOp):
            l = self._eval_node(node.left)
            r = self._eval_node(node.right)
            if isinstance(node.op, ast.Add): return l + r
            if isinstance(node.op, ast.Sub): return l - r
            if isinstance(node.op, ast.Mult): return l * r
            if isinstance(node.op, ast.Div): return l / r
            if isinstance(node.op, ast.Mod): return l % r
            if isinstance(node.op, ast.Pow): return l ** r
            if isinstance(node.op, ast.FloorDiv): return l // r
            raise RuntimeError("Unsupported op")
        if isinstance(node, ast.UnaryOp):
            v = self._eval_node(node.operand)
            if isinstance(node.op, ast.USub): return -v
            if isinstance(node.op, ast.UAdd): return +v
            if isinstance(node.op, ast.Not): return not v
            raise RuntimeError("Unsupported unary op")
        if isinstance(node, ast.Compare):
            left = self._eval_node(node.left)
            for op, comp in zip(node.ops, node.comparators):
                right = self._eval_node(comp)
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
                return all(self._eval_node(v) for v in node.values)
            if isinstance(node.op, ast.Or):
                return any(self._eval_node(v) for v in node.values)
        raise RuntimeError("Unsupported expression")

    def run_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return None
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

# ------------------ File System Commands ------------------
def cmd_mkdir(args):
    # mkdir name  -> folder
    # mkdir "name" --lang  -> create file with extension
    if not args:
        print("Usage: mkdir <name> or mkdir \"name\" --LANG")
        return
    # join args as string
    raw = " ".join(args)
    # check for --lang
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

    cwd = CWD
    # if name contains dot -> create file
    if "." in name or lang:
        filename = name
        if not "." in name and lang:
            ext = LANG_MAP.get(lang.lower())
            if not ext:
                print("Unknown language:", lang)
                return
            filename = name + ext
        create_file_in_cwd(cwd, filename)
        return
    # otherwise create folder
    folder = os.path.join(cwd, name)
    folder = path_within_root(folder)
    if not folder:
        print("Invalid folder path")
        return
    os.makedirs(folder, exist_ok=True)
    print("Created folder:", normalize_virtual_path(folder))

def create_file_in_cwd(cwd, filename, ask_lang_if_no_ext=True):
    # if filename already contains extension -> create
    if "." in filename:
        path = os.path.join(cwd, filename)
        path = path_within_root(path)
        if not path: 
            print("Invalid path")
            return None
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
        print("Created file:", normalize_virtual_path(path))
        return path
    # else ask language if configured
    ext = None
    if ask_lang_if_no_ext:
        ext = ask_language_for(filename)
    if not ext:
        ext = ".ns"
    filename = filename + ext
    path = os.path.join(cwd, filename)
    path = path_within_root(path)
    if not path:
        print("Invalid path")
        return None
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
    print("Created file:", normalize_virtual_path(path))
    return path

def ask_language_for(base_name):
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
        # also allow full names
        for k,v in LANG_MAP.items():
            if k.lower() == a:
                return v
        print("Unknown language. Supported:", ", ".join(sorted(set(LANG_MAP.values()))))

def cmd_ls(args):
    dirpath = CWD if not args else os.path.join(CWD, args[0])
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

def cmd_cd(args):
    global CWD, ACTIVE_FILE
    if not args:
        target = MAIN_PROJECT
    else:
        raw = args[0]
        if raw.startswith("/"):
            target = os.path.join(ROOT_DIR, raw.lstrip("/"))
        else:
            target = os.path.join(CWD, raw)
    target = os.path.abspath(target)
    t = path_within_root(target)
    if not t or not os.path.isdir(t):
        print("No such directory (within NovaHub)")
        return
    CWD = t
    ACTIVE_FILE = None

def cmd_cat(args):
    if not args:
        print("Usage: cat <file>")
        return
    fp = os.path.join(CWD, args[0])
    p = path_within_root(fp)
    if not p or not os.path.isfile(p):
        print("No such file")
        return
    with open(p, "r", encoding="utf-8") as f:
        print(f.read())

def cmd_grep(args):
    if len(args) < 2:
        print("Usage: grep <pattern> <file>")
        return
    pattern = args[0]
    filepath = os.path.join(CWD, args[1])
    p = path_within_root(filepath)
    if not p or not os.path.isfile(p):
        print("No such file")
        return
    pat = re.compile(pattern)
    with open(p, "r", encoding="utf-8") as f:
        for i, line in enumerate(f,1):
            if pat.search(line):
                print(f"{i}:{line.rstrip()}")

# ------------------ nano (editor mode) ------------------
def cmd_nano(args):
    global ACTIVE_FILE
    # nano -> NewFile
    if not args:
        # choose NewFile name
        base = "NewFile"
        i = 1
        while True:
            name = base if i==1 else f"{base}{i}"
            candidate = os.path.join(CWD, name + ".ns")
            if not os.path.exists(candidate):
                break
            i += 1
        # ask language, but default ns
        ext = ask_language_for(name)
        filename = name + ext
    else:
        name = args[0]
        # if contains ., use as is
        if "." in name:
            filename = name
        else:
            # ask language
            ext = ask_language_for(name)
            filename = name + ext
    # create file if missing
    path = os.path.join(CWD, filename)
    p = path_within_root(path)
    if not p:
        print("Invalid path")
        return
    if not os.path.exists(p):
        with open(p, "w", encoding="utf-8") as f:
            f.write("")  # empty
    ACTIVE_FILE = os.path.basename(filename)
    print(color(f"Entering NovaScript File Editor for {ACTIVE_FILE}. (type 'exit' to save and leave, 'quit' to leave without saving)", C.CYAN))
    # Load current content into buffer (list of lines)
    with open(p, "r", encoding="utf-8") as f:
        buffer = [line.rstrip("\n") for line in f.readlines()]
    # Editor loop: user types lines; commands: save, exit, quit, show, delete <n>, replace <n> <text>, insert <n> <text>
    while True:
        line = prompt("NovaScript(FileEdit)=> ")
        if line is None:
            continue
        cmd = line.strip()
        if cmd == "exit":
            # save and leave
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(buffer) + ("\n" if buffer else ""))
            print("Saved", ACTIVE_FILE)
            ACTIVE_FILE = None
            return
        if cmd == "quit":
            print("Discarding changes and leaving editor.")
            ACTIVE_FILE = None
            return
        if cmd == "save":
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(buffer) + ("\n" if buffer else ""))
            print("Saved", ACTIVE_FILE)
            continue
        if cmd == "show":
            print("\n".join(buffer))
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
        # Otherwise treat as new code line appended
        buffer.append(line)

# ------------------ run (execute NovaScript file) ------------------
def run_script_file(filepath, bg=False):
    global JOB_COUNTER, JOBS
    p = path_within_root(os.path.join(CWD, filepath))
    if not p or not os.path.isfile(p):
        print("No such file")
        return
    if not bg:
        # foreground run
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
    # background run
    def job_thread(pid, path):
        runtime = NovaScriptRuntime()
        with open(path, "r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f.readlines()]
        try:
            for ln in lines:
                if JOBS.get(pid, {}).get("stop"):
                    JOBS[pid]["status"] = "terminated"
                    return
                runtime.run_line(ln)
            JOBS[pid]["status"] = "finished"
        except Exception as e:
            JOBS[pid]["status"] = "error: " + str(e)
    with JOBS_LOCK:
        JOB_COUNTER += 1
        pid = JOB_COUNTER
        JOBS[pid] = {"path": p, "status": "running", "thread": None, "start": time.time(), "stop": False}
    t = threading.Thread(target=job_thread, args=(pid,p), daemon=True)
    JOBS[pid]["thread"] = t
    t.start()
    print(f"Started job #{pid}: {os.path.basename(filepath)}")

def cmd_run(args):
    if not args:
        print("Usage: run <script> [&]")
        return
    bg = False
    if args[-1] == "&":
        bg = True
        args = args[:-1]
    filepath = args[0]
    run_script_file(filepath, bg=bg)

def cmd_jobs(args):
    with JOBS_LOCK:
        for pid,info in sorted(JOBS.items()):
            age = int(time.time() - info.get("start", time.time()))
            print(f"#{pid} {os.path.basename(info['path'])} [{info['status']}] ({age}s)")

def cmd_kill(args):
    if not args:
        print("Usage: kill <jobid>")
        return
    try:
        pid = int(args[0])
    except:
        print("Invalid job id")
        return
    with JOBS_LOCK:
        if pid not in JOBS:
            print("No such job")
            return
        JOBS[pid]["stop"] = True
        JOBS[pid]["status"] = "terminating"
    print(f"Signaled job {pid} to terminate.")

# ------------------ man pages and pager ------------------
def load_default_manpages():
    # create simple manpages if missing
    pages = {
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
            "DESCRIPTION": "NovaScript-based file editor: edits are saved to file when exiting. Lines typed are NOT executed.",
            "LANGUAGE": "Editor",
            "NOTES": "Default language is NS (.ns). No line numbers displayed.",
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
        }
    }
    for name,content in pages.items():
        filename = os.path.join(MAN_DIR, name.lower() + ".man")
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(format_manpage(content))

def format_manpage(dic):
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

def pager_display(text):
    # simple pager: page size by terminal
    rows, cols = shutil.get_terminal_size((80, 24))
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
            # enter => show one line
            # show one line then continue waiting
            if i < len(lines):
                print(lines[i])
                i += 1
        else:
            # space or other => continue to next page
            continue

def cmd_man(args):
    if not args:
        print("Usage: man <topic> | man command | man lang")
        return
    topic = args[0].strip().lower()
    if topic == "command":
        # list commands alphabetically
        print("Available commands:")
        for c in sorted([ "mkdir","ls","cd","cat","grep","nano","run","jobs","kill","man","-help","settings","quit","enter NovaScript","enter NovaGPT" ]):
            print("  " + c)
        return
    if topic == "lang":
        langs = sorted(set([k for k in LANG_MAP.keys() if not k.startswith(".")]))
        print("Available languages:")
        for l in langs:
            print("  " + l)
        return
    # try file
    file_candidate = os.path.join(MAN_DIR, topic + ".man")
    if os.path.exists(file_candidate):
        with open(file_candidate, "r", encoding="utf-8") as f:
            pager_display(f.read())
        return
    # try suggestions
    matches = difflib.get_close_matches(topic, [fn[:-4] for fn in os.listdir(MAN_DIR) if fn.endswith(".man")], n=1, cutoff=0.6)
    if matches:
        sug = matches[0]
        ans = prompt(color(f'Did you mean "{sug}"? (y/n) ', C.YELLOW)).strip().lower()
        if ans in ("y","yes"):
            file_candidate = os.path.join(MAN_DIR, sug + ".man")
            with open(file_candidate, "r", encoding="utf-8") as f:
                pager_display(f.read())
            return
    print("No manual entry for", topic)

# ------------------ NovaGPT simple ------------------
def handle_novagpt_input(raw):
    raw = raw.strip()
    if not raw:
        return None
    if raw.startswith("Nova@"):
        payload = raw[len("Nova@"):].strip()
        if (payload.startswith('"') and payload.endswith('"')) or (payload.startswith("'") and payload.endswith("'")):
            payload = payload[1:-1]
        return simulated_nova_reply(payload)
    # fallback
    return simulated_nova_reply(raw)

def simulated_nova_reply(user_text):
    low = user_text.lower()
    if "how" in low and "work" in low:
        return "Explain what you want to build and I will give step-by-step guidance."
    if "loop" in low:
        return "NovaScript currently supports 'if' and variables; loops planned next."
    if "hello" in low:
        return "Hello! I'm NovaGPT (simulated). Ask me about NovaScript or NovaHub."
    return f"[NovaGPT] (simulated): I got: \"{user_text}\""

# ------------------ Settings ------------------
def cmd_settings(args):
    if not args:
        print("Settings:")
        for k,v in SETTINGS.items():
            print(f"  {k} : {v}")
        print("To toggle: settings toggle <name>")
        return
    if args[0] == "toggle" and len(args) == 2:
        key = args[1]
        if key in SETTINGS:
            SETTINGS[key] = not SETTINGS[key]
            save_settings()
            print(key, "set to", SETTINGS[key])
        else:
            print("No such setting")
        return
    if args[0] == "show":
        cmd_settings([])
        return
    print("Unknown settings command. Use: settings toggle <name>")

# ------------------ Main loop ------------------
def initialize():
    ensure_dirs()
    load_settings()
    load_default_manpages()
    # set initial CWD to MAIN_PROJECT from settings
    global CWD, ACTIVE_FILE
    start = SETTINGS.get("start_cwd", MAIN_PROJECT)
    if not os.path.isdir(start):
        os.makedirs(start, exist_ok=True)
    CWD = os.path.abspath(start)
    ACTIVE_FILE = None

def handle_input_line(line):
    if not line:
        return
    # split command & args
    parts = line.strip().split()
    cmd = parts[0]
    args = parts[1:]
    # direct commands
    if cmd == "mkdir":
        cmd_mkdir(args)
        return
    if cmd == "ls":
        cmd_ls(args)
        return
    if cmd == "cd":
        cmd_cd(args)
        return
    if cmd == "cat":
        cmd_cat(args)
        return
    if cmd == "grep":
        cmd_grep(args)
        return
    if cmd == "nano":
        cmd_nano(args)
        return
    if cmd == "run":
        cmd_run(args)
        return
    if cmd == "jobs":
        cmd_jobs(args)
        return
    if cmd == "kill":
        cmd_kill(args)
        return
    if cmd == "man":
        cmd_man(args)
        return
    if cmd in ("-help","help"):
        print("Available commands:")
        print("  mkdir, ls, cd, cat, grep, nano, run, jobs, kill, man, settings, -help, quit")
        print("  enter NovaScript  OR  enter NScript")
        print("  enter NovaGPT     OR  enter NGPT")
        return
    if cmd == "settings":
        cmd_settings(args)
        return
    if cmd == "enter":
        # require exact second argument like NovaScript or NScript (case-insensitive)
        if not args:
            print("Usage: enter NovaScript  OR  enter NScript")
            return
        target = args[0]
        if target.lower() in ("novascript","nscript"):
            enter_novascript_interpreter()
            return
        if target.lower() in ("novagpt","ngpt"):
            enter_novagpt_chat()
            return
        print("Unknown enter target")
        return
    if cmd == "quit":
        print("Goodbye — exiting NovaHub.")
        sys.exit(0)
    # try autosuggest
    suggestion = autosuggest(line)
    if suggestion:
        # run suggested command
        handle_input_line(suggestion)
        return
    print("Invalid command. Type -help.")

# ------------------ Modes: NovaScript interpreter ------------------
def enter_novascript_interpreter():
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

# ------------------ Modes: NovaGPT chat ------------------
def enter_novagpt_chat():
    print(color("\nEntering NovaGPT chat. Use Nova@\"message\" or type normally. Type 'exit' to return.\n", C.MAGENTA))
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
        reply = handle_novagpt_input(ln)
        if reply:
            print(color(reply, C.GREEN))

# ------------------ START ------------------
def main():
    initialize()
    print(color(VERSION, C.BOLD + C.CYAN))
    print(color(BANNER, C.CYAN))
    # show initial path
    while True:
        try:
            line = prompt(current_prompt()).strip()
        except KeyboardInterrupt:
            print("\nExiting NovaHub...")
            break
        if not line:
            continue
        handle_input_line(line)

if __name__ == "__main__":
    main()