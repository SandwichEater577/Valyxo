#!/usr/bin/env python3
"""Valyxo v0.6.0 - Terminal Developer Ecosystem.

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
   - plugins: Plugin system (ValyxoPluginManager)
   - packages: Package manager (ValyxoPackageManager)
   - git: Git integration (ValyxoGit)
   - templates: Project templates
   - theme_editor: Theme customization
   - keybindings: Customizable shortcuts
   - snippets: Code snippets
   - autocomplete: Smart tab completion
 - valyxo.shell: Shell interface
 - valyxo.editor: Text editor

Key Features:
 - Modular architecture with comprehensive type hints
 - Full error handling with informative messages
 - ValyxoScript: Lightweight programming language with arrays, objects
 - ValyxoGPT: AI-powered coding assistant
 - Plugin system for extensibility
 - Built-in package manager
 - Git integration
 - Project templates
 - Theme customization
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
    # v0.6.0 New imports
    ValyxoPluginManager,
    ValyxoPackageManager,
    ValyxoGit,
    list_templates,
    create_project,
    ValyxoThemeManager,
    ValyxoKeybindManager,
    ValyxoSnippetManager,
    ValyxoAutoComplete,
    create_autocomplete,
    integrate_extensions,
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
        
        # v0.6.0 New managers
        self.plugins = ValyxoPluginManager()
        self.packages = ValyxoPackageManager()
        self.git = ValyxoGit()
        self.theme_manager = ValyxoThemeManager()
        self.keybinds = ValyxoKeybindManager()
        self.snippets = ValyxoSnippetManager()
        self.autocomplete = create_autocomplete()
        
        # Extend ValyxoScript with new features
        self.script_extensions = integrate_extensions(self.script)
        
        self.settings = {}
        self.cwd = MAIN_PROJECT
        self.running = False
        self.history = []

    def initialize(self):
        try:
            self.filesystem.ensure_dirs()
            self.man.load_pages()
            self._load_settings()
            self.filesystem.set_cwd(self.cwd)
            self.plugins.discover()  # Find available plugins
            self.autocomplete.update_history(self.history)
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
        print(get_welcome_message(APP_NAME, "0.6.0", self.settings))
        print(get_info_banner("Type '-help' for commands or 'man Valyxo' for full help", self.settings))
        
        self.running = True
        while self.running:
            try:
                user_input = prompt(self._get_prompt()).strip()
                if user_input:
                    self.history.append(user_input)
                    self.autocomplete.update_history(self.history)
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
        elif cmd == "enter":
            self._handle_enter(args)
        # v0.6.0 New commands
        elif cmd == "git":
            self._handle_git(args)
        elif cmd == "plugin":
            self._handle_plugin(args)
        elif cmd in ["package", "pkg"]:
            self._handle_package(args)
        elif cmd in ["create", "new"]:
            self._handle_create(args)
        elif cmd == "snippet":
            self._handle_snippet(args)
        elif cmd == "keybind":
            self._handle_keybind(args)
        else:
            # Try plugin commands
            if self.plugins.has_command(cmd):
                result = self.plugins.execute_command(cmd, args)
                if result:
                    print(result)
            else:
                print(get_error_banner(f"Unknown command: {cmd}. Type '-help' for available commands.", self.settings))

    def _show_help(self):
        help_text = """
╭─ Valyxo v0.6.0 Commands ────────────────────────────────────╮
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
│ Project Management:                                         │
│   create <template> <name>   Create project from template   │
│   git <command>              Git operations                 │
│                                                             │
│ Extensions:                                                 │
│   plugin [list|install|enable]  Manage plugins              │
│   package [list|install]        Manage packages             │
│   snippet [list|add|use]        Manage snippets             │
│                                                             │
│ Customization:                                              │
│   theme [list|set|create]    Manage themes                  │
│   keybind [list|set]         Manage keybindings             │
│                                                             │
│ Tools:                                                      │
│   enter ValyxoScript     Enter script interpreter           │
│   enter ValyxoGPT        Chat with AI assistant             │
│   jobs                   List running processes             │
│   kill <pid>             Terminate process                  │
│   settings [list|set]    Manage settings                    │
│   man <command>          View documentation                 │
│   -help                  Show this help                     │
│   quit                   Exit Valyxo                        │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
"""
        print(help_text)

    def _handle_enter(self, args: str):
        """Handle enter command to switch modes."""
        mode = args.lower().strip()
        if mode in ["valyxoscript", "vscript", "vs"]:
            self._enter_valyxoscript()
        elif mode in ["valyxogpt", "vgpt", "gpt"]:
            self._enter_valyxogpt()
        else:
            print(get_error_banner("Usage: enter <ValyxoScript|ValyxoGPT>", self.settings))
            print(get_info_banner("  Aliases: vscript, vs, vgpt, gpt", self.settings))

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
            themes = self.theme_manager.list_themes()
            for theme in themes:
                current = "→" if theme['name'] == self.theme_manager.current_theme else " "
                builtin = "(builtin)" if theme.get('builtin') else "(custom)"
                print(f"  {current} {theme['name']:<15} {builtin} {theme.get('description', '')}")
        elif args.startswith("set "):
            theme_name = args[4:].strip()
            result = self.theme_manager.use_theme(theme_name)
            print(result)
            self.settings["theme"] = theme_name
        elif args.startswith("create "):
            parts = args[7:].strip().split()
            name = parts[0]
            base = parts[1] if len(parts) > 1 else "dark"
            result = self.theme_manager.create_theme(name, base)
            print(result)
        elif args.startswith("preview "):
            name = args[8:].strip()
            print(self.theme_manager.preview_theme(name))
        elif args.startswith("export "):
            name = args[7:].strip()
            result = self.theme_manager.export_theme(name)
            print(result)
        elif args.startswith("import "):
            path = args[7:].strip()
            result = self.theme_manager.import_theme(path)
            print(result)
        elif args.startswith("delete "):
            name = args[7:].strip()
            result = self.theme_manager.delete_theme(name)
            print(result)
        else:
            print(get_error_banner("Usage: theme [list|set|create|preview|export|import|delete] <name>", self.settings))

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

    # ═══════════════════════════════════════════════════════════════════
    # v0.6.0 NEW COMMAND HANDLERS
    # ═══════════════════════════════════════════════════════════════════

    def _handle_git(self, args: str):
        """Handle git commands."""
        if not args:
            print(get_info_banner("Usage: git <command> [args]", self.settings))
            print("  status, add, commit, push, pull, branch, checkout, log, diff, clone")
            return
        
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower()
        subargs = parts[1] if len(parts) > 1 else ""
        
        try:
            if subcmd == "status":
                result = self.git.status(self.cwd)
            elif subcmd == "add":
                result = self.git.add(self.cwd, subargs.split() if subargs else ["."])
            elif subcmd == "commit":
                if not subargs:
                    print(get_error_banner("Usage: git commit <message>", self.settings))
                    return
                result = self.git.commit(self.cwd, subargs)
            elif subcmd == "push":
                result = self.git.push(self.cwd)
            elif subcmd == "pull":
                result = self.git.pull(self.cwd)
            elif subcmd == "branch":
                if subargs:
                    result = self.git.create_branch(self.cwd, subargs)
                else:
                    result = self.git.list_branches(self.cwd)
            elif subcmd == "checkout":
                if not subargs:
                    print(get_error_banner("Usage: git checkout <branch>", self.settings))
                    return
                result = self.git.checkout(self.cwd, subargs)
            elif subcmd == "log":
                result = self.git.log(self.cwd)
            elif subcmd == "diff":
                result = self.git.diff(self.cwd, subargs if subargs else None)
            elif subcmd == "clone":
                if not subargs:
                    print(get_error_banner("Usage: git clone <url> [directory]", self.settings))
                    return
                url_parts = subargs.split()
                url = url_parts[0]
                dest = url_parts[1] if len(url_parts) > 1 else None
                result = self.git.clone(url, dest)
            elif subcmd == "stash":
                result = self.git.stash(self.cwd, "push" if not subargs else subargs)
            else:
                print(get_error_banner(f"Unknown git command: {subcmd}", self.settings))
                return
            
            print(result)
        except Exception as e:
            print(get_error_banner(f"Git error: {e}", self.settings))

    def _handle_plugin(self, args: str):
        """Handle plugin commands."""
        if not args or args == "list":
            plugins = self.plugins.list_plugins()
            if not plugins:
                print(get_info_banner("No plugins installed", self.settings))
                return
            print(get_section_header("Installed Plugins", self.settings))
            for plugin in plugins:
                status = "✓" if plugin.get("enabled") else "○"
                print(f"  {status} {plugin['name']} v{plugin.get('version', '?')} - {plugin.get('description', '')}")
            return
        
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower()
        subargs = parts[1] if len(parts) > 1 else ""
        
        if subcmd == "install":
            if not subargs:
                print(get_error_banner("Usage: plugin install <path>", self.settings))
                return
            result = self.plugins.load_plugin(subargs)
            print(result)
        elif subcmd == "enable":
            if not subargs:
                print(get_error_banner("Usage: plugin enable <name>", self.settings))
                return
            result = self.plugins.enable_plugin(subargs)
            print(result)
        elif subcmd == "disable":
            if not subargs:
                print(get_error_banner("Usage: plugin disable <name>", self.settings))
                return
            result = self.plugins.disable_plugin(subargs)
            print(result)
        elif subcmd == "create":
            if not subargs:
                print(get_error_banner("Usage: plugin create <name>", self.settings))
                return
            from valyxo.core import create_plugin_template
            result = create_plugin_template(subargs, self.cwd)
            print(result)
        else:
            print(get_error_banner("Usage: plugin [list|install|enable|disable|create]", self.settings))

    def _handle_package(self, args: str):
        """Handle package manager commands."""
        if not args or args == "list":
            print(get_section_header("Installed Packages", self.settings))
            installed = self.packages.list_installed()
            if not installed:
                print("  (no packages installed)")
            for pkg in installed:
                print(f"  • {pkg}")
            print("\n" + get_section_header("Built-in Packages", self.settings))
            for name, pkg in self.packages.get_builtin_packages().items():
                print(f"  • {name}")
            return
        
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower()
        subargs = parts[1] if len(parts) > 1 else ""
        
        if subcmd == "install":
            if not subargs:
                print(get_error_banner("Usage: package install <name>", self.settings))
                return
            result = self.packages.install(subargs)
            print(result)
        elif subcmd == "uninstall":
            if not subargs:
                print(get_error_banner("Usage: package uninstall <name>", self.settings))
                return
            result = self.packages.uninstall(subargs)
            print(result)
        elif subcmd == "search":
            results = self.packages.search(subargs if subargs else "")
            if not results:
                print(get_info_banner("No packages found", self.settings))
            else:
                print(get_section_header(f"Search Results for '{subargs}'", self.settings))
                for pkg in results:
                    print(f"  • {pkg}")
        elif subcmd == "info":
            if not subargs:
                print(get_error_banner("Usage: package info <name>", self.settings))
                return
            info = self.packages.get_package_info(subargs)
            if info:
                print(get_section_header(f"Package: {subargs}", self.settings))
                for key, value in info.items():
                    print(f"  {key}: {value}")
            else:
                print(get_error_banner(f"Package not found: {subargs}", self.settings))
        else:
            print(get_error_banner("Usage: package [list|install|uninstall|search|info]", self.settings))

    def _handle_create(self, args: str):
        """Handle project creation from templates."""
        if not args:
            print(get_section_header("Available Templates", self.settings))
            for tmpl in list_templates():
                print(f"  • {tmpl['name']:<15} {tmpl['description']}")
            print("\n" + get_info_banner("Usage: create <template> <project_name>", self.settings))
            return
        
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            print(get_error_banner("Usage: create <template> <project_name>", self.settings))
            return
        
        template_name = parts[0]
        project_name = parts[1]
        
        result = create_project(template_name, project_name, self.cwd)
        print(result)

    def _handle_snippet(self, args: str):
        """Handle snippet commands."""
        if not args or args == "list":
            print(self.snippets.format_snippets())
            return
        
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower()
        subargs = parts[1] if len(parts) > 1 else ""
        
        if subcmd == "add":
            if not subargs:
                print(get_error_banner("Usage: snippet add <name>", self.settings))
                return
            print(get_info_banner(f"Creating snippet: {subargs}", self.settings))
            print("Enter the snippet prefix (trigger):")
            prefix = prompt("  prefix> ").strip()
            print("Enter the snippet body (end with empty line):")
            lines = []
            while True:
                line = prompt("  > ")
                if not line:
                    break
                lines.append(line)
            body = "\n".join(lines)
            print("Enter description (optional):")
            desc = prompt("  desc> ").strip()
            result = self.snippets.add_snippet(subargs, prefix, body, desc)
            print(result)
        elif subcmd == "use":
            if not subargs:
                print(get_error_banner("Usage: snippet use <name>", self.settings))
                return
            expanded = self.snippets.use_snippet(subargs)
            if expanded:
                print(expanded)
            else:
                print(get_error_banner(f"Snippet not found: {subargs}", self.settings))
        elif subcmd == "delete":
            if not subargs:
                print(get_error_banner("Usage: snippet delete <name>", self.settings))
                return
            result = self.snippets.delete_snippet(subargs)
            print(result)
        elif subcmd == "search":
            results = self.snippets.search_snippets(subargs if subargs else "")
            if not results:
                print(get_info_banner("No snippets found", self.settings))
            else:
                for s in results[:10]:
                    print(f"  {s.prefix:<10} {s.name:<15} {s.description}")
        elif subcmd == "info":
            print(self.snippets.format_snippet(subargs))
        else:
            print(get_error_banner("Usage: snippet [list|add|use|delete|search|info]", self.settings))

    def _handle_keybind(self, args: str):
        """Handle keybinding commands."""
        if not args or args == "list":
            print(self.keybinds.format_keybindings())
            return
        
        parts = args.split(maxsplit=2)
        subcmd = parts[0].lower()
        
        if subcmd == "set":
            if len(parts) < 3:
                print(get_error_banner("Usage: keybind set <key> <command>", self.settings))
                return
            key = parts[1]
            command = parts[2]
            result = self.keybinds.set_keybinding(key, command)
            print(result)
        elif subcmd == "remove":
            if len(parts) < 2:
                print(get_error_banner("Usage: keybind remove <key>", self.settings))
                return
            result = self.keybinds.remove_keybinding(parts[1])
            print(result)
        elif subcmd == "reset":
            result = self.keybinds.reset_keybindings()
            print(result)
        else:
            print(get_error_banner("Usage: keybind [list|set|remove|reset]", self.settings))


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
