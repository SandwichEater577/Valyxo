#!/usr/bin/env python3
"""Valyxo v0.5.1 - Terminal Developer Ecosystem.

Professional development environment combining terminal CLI, AI assistance,
and scripting language. Powered by ValyxoScript and ValyxoGPT (Zencoder).

Architecture:
 - valyxo.core: Core modules and managers
   - colors: Terminal color codes
   - constants: Application configuration
   - utils: Utility functions
   - filesystem: File operations (ValyxoFileSystem)
   - gpt: AI Assistant (ValyxoGPTModule)
   - jobs: Job management (ValyxoJobsManager)
   - man: Help system (ValyxoManSystem)
 - valyxo.shell: Shell interface
 - valyxo.editor: Text editor

Key Features:
 - Modular architecture with comprehensive type hints
 - Full error handling with informative messages
 - ValyxoScript: Lightweight programming language
 - ValyxoGPT: AI-powered coding assistant
 - Professional terminal interface
"""

import os
import sys
from valyxo.core import (
    Colors,
    color,
    DEFAULT_THEMES,
    APP_NAME,
    VERSION,
    HOME,
    ROOT_DIR,
    PROJECTS_DIR,
    SYSTEM_DIR,
    CONFIG_DIR,
    MAN_DIR,
    MAIN_PROJECT,
    CONFIG_PATH,
    THEMES_PATH,
    HISTORY_PATH,
    API_KEY_PATH,
    COMMANDS,
    LANG_MAP,
    DEFAULT_SETTINGS,
    prompt,
    path_within_root,
    normalize_virtual_path,
    highlight_valyxoscript,
    ValyxoFileSystem,
    ValyxoGPTModule,
    ValyxoJobsManager,
    ValyxoManSystem,
    get_startup_banner,
    get_welcome_message,
    get_section_header,
    get_info_banner,
    get_error_banner,
    get_success_banner,
)
from valyxo.script import ValyxoScriptRuntime

try:
    import readline
except ImportError:
    readline = None

try:
    import openai
except ImportError:
    openai = None


class ValyxoShell:
    def __init__(self):
        self.filesystem = ValyxoFileSystem(ROOT_DIR)
        self.gpt = ValyxoGPTModule()
        self.jobs = ValyxoJobsManager()
        self.man = ValyxoManSystem()
        self.script = ValyxoScriptRuntime()
        self.settings = {}
        self.cwd = MAIN_PROJECT
        self.running = False

    def initialize(self):
        try:
            self.filesystem.ensure_dirs()
            self.man.load_pages()
            self._load_settings()
            self.filesystem.set_cwd(self.cwd)
        except Exception as e:
            print(get_error_banner(f"Initialization error: {e}", self.settings))
            sys.exit(1)

    def _load_settings(self):
        self.settings = DEFAULT_SETTINGS.copy()

    def _get_prompt(self) -> str:
        virtual_path = normalize_virtual_path(self.cwd, ROOT_DIR)
        prompt_text = f"valyxo:{virtual_path}> "
        if self.settings.get("colors", True):
            prompt_text = color(prompt_text, Colors.BANNER, self.settings)
        return prompt_text

    def run(self):
        print(get_startup_banner(self.settings))
        print(get_welcome_message(APP_NAME, "0.5.1", self.settings))
        print(get_info_banner("Type '-help' for commands or 'man Valyxo' for full help", self.settings))
        
        self.running = True
        while self.running:
            try:
                user_input = prompt(self._get_prompt()).strip()
                if user_input:
                    self._handle_command(user_input)
            except KeyboardInterrupt:
                print("\n" + get_info_banner("Use 'quit' to exit", self.settings))
            except Exception as e:
                print(get_error_banner(f"Error: {e}", self.settings))

    def _handle_command(self, cmd_line: str):
        parts = cmd_line.split(maxsplit=1)
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd in ["quit", "exit"]:
            self.running = False
            print(get_success_banner("Goodbye!", self.settings))
        elif cmd == "-help":
            self._show_help()
        elif cmd == "man":
            self._handle_man(args)
        elif cmd == "mkdir":
            self._handle_mkdir(args)
        elif cmd == "ls":
            self._handle_ls(args)
        elif cmd == "cd":
            self._handle_cd(args)
        elif cmd == "cat":
            self._handle_cat(args)
        elif cmd == "grep":
            self._handle_grep(args)
        elif cmd == "nano":
            self._handle_nano(args)
        elif cmd == "run":
            self._handle_run(args)
        elif cmd == "jobs":
            self._handle_jobs()
        elif cmd == "kill":
            self._handle_kill(args)
        elif cmd == "theme":
            self._handle_theme(args)
        elif cmd == "settings":
            self._handle_settings(args)
        elif cmd in ["enter valyxoscript", "enter vscript"]:
            self._enter_valyxoscript()
        elif cmd in ["enter valyxogpt", "enter vgpt"]:
            self._enter_valyxogpt()
        else:
            print(get_error_banner(f"Unknown command: {cmd}. Type '-help' for available commands.", self.settings))

    def _show_help(self):
        help_text = """
╭─ Valyxo v0.5.1 Commands ────────────────────────────────────╮
│                                                             │
│ Navigation & Files:                                         │
│   cd <path>              Change directory                   │
│   ls [path]              List files/folders                 │
│   mkdir <path>           Create directory                   │
│   cat <file>             Display file contents              │
│   nano <file>            Edit file                          │
│   grep <pattern>         Search files                       │
│                                                             │
│ Execution:                                                  │
│   run <file>             Execute script                     │
│   python <code>          Run Python code                    │
│                                                             │
│ Tools:                                                      │
│   enter ValyxoScript     Enter script interpreter           │
│   enter ValyxoGPT        Chat with AI assistant             │
│   jobs                   List running processes             │
│   kill <pid>             Terminate process                  │
│   theme [list|set]       Manage themes                      │
│   settings [list|set]    Manage settings                    │
│   man <command>          View documentation                 │
│   -help                  Show this help                     │
│   quit                   Exit Valyxo                        │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
"""
        print(help_text)

    def _handle_man(self, cmd: str):
        if not cmd:
            print(get_info_banner("Usage: man <command>", self.settings))
            return
        
        try:
            page = self.man.get_page(cmd.strip())
            if page:
                print(page)
            else:
                print(get_error_banner(f"No manual entry for '{cmd}'", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error reading manual: {e}", self.settings))

    def _handle_mkdir(self, path: str):
        if not path:
            print(get_error_banner("Usage: mkdir <directory_path>", self.settings))
            return
        try:
            full_path = os.path.join(self.cwd, path)
            os.makedirs(full_path, exist_ok=True)
            print(get_success_banner(f"Created directory: {path}", self.settings))
        except Exception as e:
            print(get_error_banner(f"Failed to create directory: {e}", self.settings))

    def _handle_ls(self, path: str = ""):
        try:
            target = self.cwd if not path else os.path.join(self.cwd, path)
            if not os.path.isdir(target):
                print(get_error_banner(f"Not a directory: {path}", self.settings))
                return
            
            items = os.listdir(target)
            if not items:
                print(get_info_banner("(empty directory)", self.settings))
                return
            
            for item in sorted(items):
                item_path = os.path.join(target, item)
                prefix = "📁" if os.path.isdir(item_path) else "📄"
                print(f"  {prefix} {item}")
        except Exception as e:
            print(get_error_banner(f"Error listing directory: {e}", self.settings))

    def _handle_cd(self, path: str):
        if not path:
            self.cwd = MAIN_PROJECT
            print(get_success_banner(f"Changed to: {normalize_virtual_path(self.cwd, ROOT_DIR)}", self.settings))
            return
        
        try:
            new_cwd = os.path.join(self.cwd, path)
            if not os.path.isdir(new_cwd):
                print(get_error_banner(f"Directory not found: {path}", self.settings))
                return
            
            self.cwd = new_cwd
            self.filesystem.set_cwd(self.cwd)
            print(get_success_banner(f"Changed to: {normalize_virtual_path(self.cwd, ROOT_DIR)}", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error changing directory: {e}", self.settings))

    def _handle_cat(self, filepath: str):
        if not filepath:
            print(get_error_banner("Usage: cat <file>", self.settings))
            return
        try:
            full_path = os.path.join(self.cwd, filepath)
            with open(full_path, 'r', encoding='utf-8') as f:
                print(f.read())
        except FileNotFoundError:
            print(get_error_banner(f"File not found: {filepath}", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error reading file: {e}", self.settings))

    def _handle_grep(self, args: str):
        if not args:
            print(get_error_banner("Usage: grep <pattern> [path]", self.settings))
            return
        try:
            parts = args.split(maxsplit=1)
            pattern = parts[0]
            search_path = self.cwd if len(parts) < 2 else os.path.join(self.cwd, parts[1])
            
            if not os.path.exists(search_path):
                print(get_error_banner(f"Path not found: {args}", self.settings))
                return
            
            matches = 0
            if os.path.isfile(search_path):
                with open(search_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if pattern in line:
                            print(f"  {i}: {line.rstrip()}")
                            matches += 1
            else:
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                for i, line in enumerate(f, 1):
                                    if pattern in line:
                                        rel_path = os.path.relpath(filepath, self.cwd)
                                        print(f"  {rel_path}:{i}: {line.rstrip()}")
                                        matches += 1
                        except:
                            pass
            
            if matches == 0:
                print(get_info_banner(f"No matches found for '{pattern}'", self.settings))
            else:
                print(get_success_banner(f"Found {matches} match(es)", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error searching: {e}", self.settings))

    def _handle_nano(self, filepath: str):
        if not filepath:
            print(get_error_banner("Usage: nano <file>", self.settings))
            return
        
        try:
            full_path = os.path.join(self.cwd, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            content = ""
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            print(get_section_header(f"Editing: {filepath}", self.settings))
            print("(Enter your content below. Type CTRL+D to save or CTRL+C to cancel)\n")
            
            try:
                lines = []
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                content = '\n'.join(lines)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(get_success_banner(f"File saved: {filepath}", self.settings))
            except KeyboardInterrupt:
                print("\n" + get_info_banner("Cancelled", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error editing file: {e}", self.settings))

    def _handle_run(self, filepath: str):
        if not filepath:
            print(get_error_banner("Usage: run <file>", self.settings))
            return
        
        try:
            full_path = os.path.join(self.cwd, filepath)
            if not os.path.exists(full_path):
                print(get_error_banner(f"File not found: {filepath}", self.settings))
                return
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._execute_valyxoscript(content)
        except Exception as e:
            print(get_error_banner(f"Error running file: {e}", self.settings))

    def _handle_jobs(self):
        jobs = self.jobs.get_jobs()
        if not jobs:
            print(get_info_banner("No running jobs", self.settings))
            return
        
        print(get_section_header("Running Jobs", self.settings))
        for job in jobs:
            print(f"  [{job['pid']}] {job['cmd']}")

    def _handle_kill(self, pid_str: str):
        if not pid_str:
            print(get_error_banner("Usage: kill <pid>", self.settings))
            return
        try:
            pid = int(pid_str)
            self.jobs.kill_job(pid)
            print(get_success_banner(f"Process {pid} terminated", self.settings))
        except ValueError:
            print(get_error_banner("Invalid PID (must be a number)", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error killing process: {e}", self.settings))

    def _handle_theme(self, args: str):
        if not args or args == "list":
            print(get_section_header("Available Themes", self.settings))
            for theme in DEFAULT_THEMES:
                print(f"  • {theme}")
        elif args.startswith("set "):
            theme_name = args[4:].strip()
            self.settings["theme"] = theme_name
            print(get_success_banner(f"Theme changed to: {theme_name}", self.settings))
        else:
            print(get_error_banner("Usage: theme [list|set <name>]", self.settings))

    def _handle_settings(self, args: str):
        if not args or args == "list":
            print(get_section_header("Current Settings", self.settings))
            for key, value in self.settings.items():
                print(f"  {key}: {value}")
        elif args.startswith("set "):
            parts = args[4:].split('=', 1)
            if len(parts) == 2:
                key, value = parts[0].strip(), parts[1].strip()
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                self.settings[key] = value
                print(get_success_banner(f"Setting {key} = {value}", self.settings))
            else:
                print(get_error_banner("Usage: settings set <key>=<value>", self.settings))
        else:
            print(get_error_banner("Usage: settings [list|set <key>=<value>]", self.settings))

    def _enter_valyxoscript(self):
        print(get_section_header("ValyxoScript Interpreter", self.settings))
        print(get_info_banner("Type 'exit' or press CTRL+D to exit", self.settings))
        
        try:
            while True:
                try:
                    line = prompt("vscript> ").strip()
                    if not line:
                        continue
                    if line in ["exit", "quit"]:
                        break
                    self._execute_valyxoscript(line)
                except KeyboardInterrupt:
                    print("\n" + get_info_banner("Type 'exit' to quit", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error: {e}", self.settings))

    def _execute_valyxoscript(self, code: str):
        try:
            for line in code.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    self.script.run_line(line)
        except RuntimeError as e:
            print(get_error_banner(f"Script error: {e}", self.settings))
        except Exception as e:
            print(get_error_banner(f"Execution error: {e}", self.settings))

    def _enter_valyxogpt(self):
        print(get_section_header("ValyxoGPT Assistant", self.settings))
        print(get_info_banner("Type 'exit' or press CTRL+D to exit", self.settings))
        
        try:
            while True:
                try:
                    user_input = prompt("you: ").strip()
                    if not user_input:
                        continue
                    if user_input in ["exit", "quit"]:
                        break
                    
                    response = self.gpt.get_response(user_input)
                    print(f"gpt: {response}\n")
                except KeyboardInterrupt:
                    print("\n" + get_info_banner("Type 'exit' to quit", self.settings))
        except Exception as e:
            print(get_error_banner(f"Error: {e}", self.settings))


shell = None


def main():
    global shell
    try:
        shell = ValyxoShell()
        shell.initialize()
        shell.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
