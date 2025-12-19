"""Valyxo Auto-Complete System v0.6.0

Smart tab completion for commands, files, and arguments.

Usage:
    Press TAB to auto-complete
    Press TAB TAB to show all completions
    Press SHIFT+TAB for previous completion
"""

import os
import re
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass


@dataclass
class Completion:
    """A completion suggestion."""
    text: str  # The completion text
    display: str  # What to show in menu
    description: str = ""  # Description/hint
    kind: str = "text"  # "command", "file", "directory", "argument", "snippet", "history"
    insert_text: str = None  # Text to actually insert (if different from text)
    score: int = 0  # Relevance score
    
    def __post_init__(self):
        if self.insert_text is None:
            self.insert_text = self.text


class CompletionProvider:
    """Base class for completion providers."""
    
    def get_completions(self, text: str, cursor_pos: int, context: Dict[str, Any]) -> List[Completion]:
        """Get completions for the given text and cursor position."""
        raise NotImplementedError


class CommandCompletionProvider(CompletionProvider):
    """Provides completions for built-in commands."""
    
    COMMANDS = {
        # Core commands
        "help": "Show help information",
        "exit": "Exit Valyxo",
        "quit": "Exit Valyxo",
        "clear": "Clear the screen",
        "history": "Show command history",
        "alias": "Create command alias",
        "unalias": "Remove command alias",
        
        # File system
        "ls": "List directory contents",
        "dir": "List directory contents",
        "cd": "Change directory",
        "pwd": "Print working directory",
        "mkdir": "Create directory",
        "rmdir": "Remove directory",
        "rm": "Remove files",
        "cp": "Copy files",
        "mv": "Move/rename files",
        "cat": "Display file contents",
        "touch": "Create empty file",
        "find": "Find files",
        "grep": "Search in files",
        
        # Editor
        "nano": "Open text editor",
        "edit": "Open text editor",
        
        # ValyxoScript
        "run": "Run a ValyxoScript file",
        "eval": "Evaluate ValyxoScript expression",
        
        # Git (new)
        "git": "Git version control",
        "status": "Show git status",
        "add": "Stage files for commit",
        "commit": "Commit changes",
        "push": "Push to remote",
        "pull": "Pull from remote",
        "branch": "Manage branches",
        "checkout": "Switch branches",
        "clone": "Clone repository",
        "log": "Show commit log",
        "diff": "Show changes",
        
        # Themes (new)
        "theme": "Manage themes",
        
        # Plugins (new)
        "plugin": "Manage plugins",
        
        # Packages (new)
        "package": "Manage packages",
        "pkg": "Manage packages",
        "install": "Install a package",
        "uninstall": "Uninstall a package",
        
        # Templates (new)
        "create": "Create project from template",
        "new": "Create project from template",
        
        # Snippets (new)
        "snippet": "Manage code snippets",
        
        # Keybindings (new)
        "keybind": "Manage keybindings",
        "keys": "Show keybindings",
        
        # Settings
        "settings": "Open settings",
        "config": "Configure Valyxo",
        
        # Jobs
        "jobs": "List background jobs",
        "fg": "Bring job to foreground",
        "bg": "Send job to background",
        "kill": "Kill a process",
        
        # System
        "echo": "Print text",
        "date": "Show current date/time",
        "whoami": "Show current user",
        "hostname": "Show hostname",
        "env": "Show environment variables",
        "export": "Set environment variable",
        
        # Valyxo specific
        "valyxo": "Valyxo information",
        "version": "Show version",
        "update": "Check for updates",
        "man": "Show manual page",
        "gpt": "Ask ValyxoGPT",
    }
    
    SUBCOMMANDS = {
        "git": ["status", "add", "commit", "push", "pull", "branch", "checkout", "log", "diff", "clone", "stash", "remote"],
        "theme": ["list", "use", "create", "edit", "export", "import", "delete", "preview"],
        "plugin": ["list", "install", "uninstall", "enable", "disable", "update", "create"],
        "package": ["list", "install", "uninstall", "search", "update", "info"],
        "pkg": ["list", "install", "uninstall", "search", "update", "info"],
        "snippet": ["list", "add", "edit", "delete", "use", "search", "export", "import"],
        "keybind": ["list", "set", "remove", "reset", "export", "import"],
        "create": ["python", "node", "react", "flask", "express", "valyxoscript", "html", "cli"],
        "new": ["python", "node", "react", "flask", "express", "valyxoscript", "html", "cli"],
    }
    
    def get_completions(self, text: str, cursor_pos: int, context: Dict[str, Any]) -> List[Completion]:
        completions = []
        
        # Get the word being typed
        words = text[:cursor_pos].split()
        
        if not words or (len(words) == 1 and not text.endswith(' ')):
            # Completing command name
            prefix = words[0] if words else ""
            for cmd, desc in self.COMMANDS.items():
                if cmd.startswith(prefix.lower()):
                    completions.append(Completion(
                        text=cmd,
                        display=cmd,
                        description=desc,
                        kind="command",
                        score=100 if cmd == prefix else 50
                    ))
        else:
            # Completing subcommand or argument
            cmd = words[0].lower()
            if cmd in self.SUBCOMMANDS:
                prefix = words[-1] if not text.endswith(' ') else ""
                for subcmd in self.SUBCOMMANDS[cmd]:
                    if subcmd.startswith(prefix.lower()):
                        completions.append(Completion(
                            text=subcmd,
                            display=subcmd,
                            description=f"{cmd} {subcmd}",
                            kind="argument",
                            score=50
                        ))
        
        return completions


class FileCompletionProvider(CompletionProvider):
    """Provides completions for file and directory paths."""
    
    FILE_COMMANDS = {"cd", "cat", "nano", "edit", "rm", "cp", "mv", "run", "ls", "mkdir", "touch", "find", "grep", "source"}
    
    def get_completions(self, text: str, cursor_pos: int, context: Dict[str, Any]) -> List[Completion]:
        completions = []
        
        words = text[:cursor_pos].split()
        if not words:
            return completions
        
        cmd = words[0].lower()
        
        # Check if this command expects file/path arguments
        if cmd not in self.FILE_COMMANDS and len(words) < 2:
            return completions
        
        # Get the path being typed
        if text.endswith(' '):
            path_prefix = ""
        else:
            path_prefix = words[-1] if len(words) > 1 else ""
        
        # Handle relative/absolute paths
        cwd = context.get("cwd", os.getcwd())
        
        if path_prefix.startswith("~"):
            base_dir = os.path.expanduser("~")
            path_prefix = path_prefix[1:].lstrip("/\\")
        elif os.path.isabs(path_prefix):
            base_dir = os.path.dirname(path_prefix) or "/"
            path_prefix = os.path.basename(path_prefix)
        else:
            if "/" in path_prefix or "\\" in path_prefix:
                parts = path_prefix.replace("\\", "/").rsplit("/", 1)
                base_dir = os.path.join(cwd, parts[0])
                path_prefix = parts[1] if len(parts) > 1 else ""
            else:
                base_dir = cwd
        
        # List directory contents
        try:
            if os.path.isdir(base_dir):
                for entry in os.listdir(base_dir):
                    if entry.startswith(path_prefix) or not path_prefix:
                        full_path = os.path.join(base_dir, entry)
                        is_dir = os.path.isdir(full_path)
                        
                        display_name = entry + ("/" if is_dir else "")
                        
                        completions.append(Completion(
                            text=entry + ("/" if is_dir else ""),
                            display=display_name,
                            description="Directory" if is_dir else "File",
                            kind="directory" if is_dir else "file",
                            score=70 if is_dir else 60
                        ))
        except PermissionError:
            pass
        except Exception:
            pass
        
        return completions


class HistoryCompletionProvider(CompletionProvider):
    """Provides completions from command history."""
    
    def __init__(self, history: List[str] = None):
        self.history = history or []
    
    def update_history(self, history: List[str]):
        self.history = history
    
    def get_completions(self, text: str, cursor_pos: int, context: Dict[str, Any]) -> List[Completion]:
        completions = []
        prefix = text[:cursor_pos].lower()
        
        seen = set()
        for cmd in reversed(self.history):
            if cmd.lower().startswith(prefix) and cmd not in seen:
                seen.add(cmd)
                completions.append(Completion(
                    text=cmd,
                    display=cmd[:50] + "..." if len(cmd) > 50 else cmd,
                    description="From history",
                    kind="history",
                    score=40
                ))
                if len(completions) >= 10:
                    break
        
        return completions


class SnippetCompletionProvider(CompletionProvider):
    """Provides completions for snippets."""
    
    def __init__(self, snippets: Dict[str, Any] = None):
        self.snippets = snippets or {}
    
    def update_snippets(self, snippets: Dict[str, Any]):
        self.snippets = snippets
    
    def get_completions(self, text: str, cursor_pos: int, context: Dict[str, Any]) -> List[Completion]:
        completions = []
        words = text[:cursor_pos].split()
        
        if not words:
            return completions
        
        prefix = words[-1] if not text.endswith(' ') else ""
        
        for name, snippet in self.snippets.items():
            trigger = snippet.get("prefix", name)
            if trigger.startswith(prefix):
                completions.append(Completion(
                    text=trigger,
                    display=f"⟨{trigger}⟩",
                    description=snippet.get("description", "Snippet"),
                    kind="snippet",
                    insert_text=snippet.get("body", trigger),
                    score=80
                ))
        
        return completions


class EnvironmentCompletionProvider(CompletionProvider):
    """Provides completions for environment variables."""
    
    def get_completions(self, text: str, cursor_pos: int, context: Dict[str, Any]) -> List[Completion]:
        completions = []
        
        # Check if we're completing an env var
        text_before = text[:cursor_pos]
        
        # Find $VAR pattern
        match = re.search(r'\$(\w*)$', text_before)
        if not match:
            return completions
        
        prefix = match.group(1)
        
        for key, value in os.environ.items():
            if key.startswith(prefix.upper()):
                display_value = value[:30] + "..." if len(value) > 30 else value
                completions.append(Completion(
                    text=key,
                    display=f"${key}",
                    description=display_value,
                    kind="variable",
                    insert_text=key,
                    score=60
                ))
        
        return completions


class ValyxoAutoComplete:
    """Main auto-complete system for Valyxo."""
    
    def __init__(self):
        self.providers: List[CompletionProvider] = [
            CommandCompletionProvider(),
            FileCompletionProvider(),
            HistoryCompletionProvider(),
            EnvironmentCompletionProvider(),
        ]
        
        self.current_completions: List[Completion] = []
        self.completion_index: int = -1
        self.original_text: str = ""
    
    def add_provider(self, provider: CompletionProvider):
        """Add a completion provider."""
        self.providers.append(provider)
    
    def update_history(self, history: List[str]):
        """Update command history for history provider."""
        for provider in self.providers:
            if isinstance(provider, HistoryCompletionProvider):
                provider.update_history(history)
    
    def update_snippets(self, snippets: Dict[str, Any]):
        """Update snippets for snippet provider."""
        for provider in self.providers:
            if isinstance(provider, SnippetCompletionProvider):
                provider.update_snippets(snippets)
    
    def get_completions(self, text: str, cursor_pos: int = None, context: Dict[str, Any] = None) -> List[Completion]:
        """Get all completions from all providers."""
        if cursor_pos is None:
            cursor_pos = len(text)
        if context is None:
            context = {"cwd": os.getcwd()}
        
        all_completions = []
        
        for provider in self.providers:
            try:
                completions = provider.get_completions(text, cursor_pos, context)
                all_completions.extend(completions)
            except Exception:
                pass
        
        # Sort by score and deduplicate
        seen = set()
        unique = []
        for c in sorted(all_completions, key=lambda x: -x.score):
            if c.text not in seen:
                seen.add(c.text)
                unique.append(c)
        
        return unique
    
    def complete(self, text: str, cursor_pos: int = None, context: Dict[str, Any] = None) -> Tuple[str, List[Completion]]:
        """Complete the current text. Returns (completed_text, all_completions)."""
        if cursor_pos is None:
            cursor_pos = len(text)
        
        completions = self.get_completions(text, cursor_pos, context)
        
        if not completions:
            return text, []
        
        if len(completions) == 1:
            # Single completion - apply it
            return self._apply_completion(text, cursor_pos, completions[0]), completions
        
        # Multiple completions - find common prefix
        common = self._common_prefix([c.text for c in completions])
        if common and len(common) > len(self._get_word_at_cursor(text, cursor_pos)):
            return self._apply_completion(text, cursor_pos, Completion(text=common, display=common)), completions
        
        return text, completions
    
    def cycle_completion(self, text: str, direction: int = 1) -> str:
        """Cycle through completions. direction: 1=next, -1=prev"""
        if not self.current_completions:
            self.original_text = text
            _, self.current_completions = self.complete(text)
            if not self.current_completions:
                return text
        
        if not self.current_completions:
            return text
        
        self.completion_index = (self.completion_index + direction) % len(self.current_completions)
        completion = self.current_completions[self.completion_index]
        
        return self._apply_completion(self.original_text, len(self.original_text), completion)
    
    def reset(self):
        """Reset completion state."""
        self.current_completions = []
        self.completion_index = -1
        self.original_text = ""
    
    def _get_word_at_cursor(self, text: str, cursor_pos: int) -> str:
        """Get the word being typed at cursor."""
        before = text[:cursor_pos]
        words = before.split()
        if not words:
            return ""
        if text.endswith(' '):
            return ""
        return words[-1]
    
    def _apply_completion(self, text: str, cursor_pos: int, completion: Completion) -> str:
        """Apply a completion to the text."""
        before = text[:cursor_pos]
        after = text[cursor_pos:]
        
        # Find the word we're replacing
        words = before.split()
        if words and not before.endswith(' '):
            # Replace the last word
            prefix = ' '.join(words[:-1])
            if prefix:
                prefix += ' '
            return prefix + completion.insert_text + after
        else:
            # Append new word
            return before + completion.insert_text + after
    
    def _common_prefix(self, strings: List[str]) -> str:
        """Find common prefix of a list of strings."""
        if not strings:
            return ""
        
        shortest = min(strings, key=len)
        for i, char in enumerate(shortest):
            for s in strings:
                if s[i] != char:
                    return shortest[:i]
        return shortest
    
    def format_completions(self, completions: List[Completion], max_items: int = 20) -> str:
        """Format completions for display."""
        if not completions:
            return ""
        
        lines = []
        
        # Group by kind
        by_kind: Dict[str, List[Completion]] = {}
        for c in completions[:max_items]:
            kind = c.kind
            if kind not in by_kind:
                by_kind[kind] = []
            by_kind[kind].append(c)
        
        for kind, items in by_kind.items():
            lines.append(f"─ {kind.upper()} ─")
            for c in items:
                desc = f" ({c.description})" if c.description else ""
                lines.append(f"  {c.display}{desc}")
        
        if len(completions) > max_items:
            lines.append(f"  ... and {len(completions) - max_items} more")
        
        return "\n".join(lines)


# Helper function to create autocomplete instance
def create_autocomplete() -> ValyxoAutoComplete:
    """Create a configured ValyxoAutoComplete instance."""
    ac = ValyxoAutoComplete()
    ac.add_provider(SnippetCompletionProvider())
    return ac
