"""Valyxo Keybindings System v0.6.0

Customizable keyboard shortcuts for the terminal.

Usage:
    keybind list                      List all keybindings
    keybind set <key> <command>       Set a keybinding
    keybind remove <key>              Remove a keybinding
    keybind reset                     Reset to defaults
    keybind export                    Export keybindings
    keybind import <file>             Import keybindings
"""

import os
import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict


@dataclass
class Keybinding:
    """A single keybinding configuration."""
    key: str  # e.g., "ctrl+c", "alt+f", "f1"
    command: str
    description: str = ""
    enabled: bool = True
    context: str = "global"  # "global", "editor", "prompt"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Keybinding":
        return cls(**data)


# Default keybindings
DEFAULT_KEYBINDINGS: List[Keybinding] = [
    # General
    Keybinding("ctrl+c", "interrupt", "Interrupt current command"),
    Keybinding("ctrl+d", "exit", "Exit Valyxo"),
    Keybinding("ctrl+l", "clear", "Clear screen"),
    Keybinding("ctrl+z", "suspend", "Suspend current process"),
    
    # History
    Keybinding("up", "history:prev", "Previous command in history"),
    Keybinding("down", "history:next", "Next command in history"),
    Keybinding("ctrl+r", "history:search", "Search command history"),
    Keybinding("ctrl+p", "history:prev", "Previous command (alternative)"),
    Keybinding("ctrl+n", "history:next", "Next command (alternative)"),
    
    # Cursor movement
    Keybinding("ctrl+a", "cursor:home", "Move cursor to start of line"),
    Keybinding("ctrl+e", "cursor:end", "Move cursor to end of line"),
    Keybinding("ctrl+b", "cursor:left", "Move cursor left"),
    Keybinding("ctrl+f", "cursor:right", "Move cursor right"),
    Keybinding("alt+b", "cursor:word-left", "Move cursor word left"),
    Keybinding("alt+f", "cursor:word-right", "Move cursor word right"),
    Keybinding("home", "cursor:home", "Move cursor to start"),
    Keybinding("end", "cursor:end", "Move cursor to end"),
    
    # Editing
    Keybinding("ctrl+u", "edit:clear-line", "Clear line before cursor"),
    Keybinding("ctrl+k", "edit:clear-after", "Clear line after cursor"),
    Keybinding("ctrl+w", "edit:delete-word", "Delete word before cursor"),
    Keybinding("alt+d", "edit:delete-word-after", "Delete word after cursor"),
    Keybinding("ctrl+h", "edit:backspace", "Backspace"),
    Keybinding("ctrl+t", "edit:transpose", "Transpose characters"),
    Keybinding("alt+t", "edit:transpose-words", "Transpose words"),
    Keybinding("ctrl+y", "edit:paste", "Paste from kill ring"),
    
    # Auto-complete
    Keybinding("tab", "complete", "Auto-complete"),
    Keybinding("shift+tab", "complete:prev", "Previous completion"),
    Keybinding("ctrl+space", "complete:menu", "Show completion menu"),
    
    # Commands
    Keybinding("ctrl+g", "git:status", "Show git status"),
    Keybinding("ctrl+shift+g", "git:menu", "Open git menu"),
    Keybinding("f1", "help", "Show help"),
    Keybinding("f2", "theme:menu", "Theme menu"),
    Keybinding("f3", "plugin:menu", "Plugin menu"),
    Keybinding("f5", "run:file", "Run current file"),
    Keybinding("f12", "settings", "Open settings"),
    
    # Editor mode
    Keybinding("ctrl+o", "open", "Open file", context="prompt"),
    Keybinding("ctrl+s", "save", "Save file", context="editor"),
    Keybinding("ctrl+shift+s", "save:as", "Save as", context="editor"),
    Keybinding("ctrl+q", "quit", "Quit editor", context="editor"),
    Keybinding("ctrl+x", "cut", "Cut selection", context="editor"),
    Keybinding("ctrl+c", "copy", "Copy selection", context="editor"),
    Keybinding("ctrl+v", "paste", "Paste", context="editor"),
    Keybinding("ctrl+z", "undo", "Undo", context="editor"),
    Keybinding("ctrl+shift+z", "redo", "Redo", context="editor"),
    Keybinding("ctrl+/", "comment", "Toggle comment", context="editor"),
    Keybinding("ctrl+shift+/", "block-comment", "Block comment", context="editor"),
]


class ValyxoKeybindManager:
    """Manages Valyxo keybindings."""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".valyxo")
        self.config_dir = config_dir
        self.keybindings_file = os.path.join(config_dir, "keybindings.json")
        os.makedirs(config_dir, exist_ok=True)
        
        self.keybindings: Dict[str, Keybinding] = {}
        self.handlers: Dict[str, Callable] = {}
        
        self._load_keybindings()
    
    def _load_keybindings(self):
        """Load keybindings from file or defaults."""
        # Start with defaults
        for kb in DEFAULT_KEYBINDINGS:
            key = self._normalize_key(kb.key)
            self.keybindings[key] = kb
        
        # Override with custom
        if os.path.exists(self.keybindings_file):
            try:
                with open(self.keybindings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for kb_data in data.get("keybindings", []):
                        kb = Keybinding.from_dict(kb_data)
                        key = self._normalize_key(kb.key)
                        self.keybindings[key] = kb
            except:
                pass
    
    def _save_keybindings(self):
        """Save current keybindings to file."""
        custom = []
        for key, kb in self.keybindings.items():
            # Only save non-default bindings
            default = self._get_default(key)
            if default is None or kb.command != default.command:
                custom.append(kb.to_dict())
        
        data = {"keybindings": custom}
        with open(self.keybindings_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def _normalize_key(self, key: str) -> str:
        """Normalize key string for consistent lookup."""
        parts = key.lower().split("+")
        modifiers = sorted([p for p in parts[:-1]])
        main_key = parts[-1]
        return "+".join(modifiers + [main_key])
    
    def _get_default(self, key: str) -> Optional[Keybinding]:
        """Get default keybinding for a key."""
        normalized = self._normalize_key(key)
        for kb in DEFAULT_KEYBINDINGS:
            if self._normalize_key(kb.key) == normalized:
                return kb
        return None
    
    def list_keybindings(self, context: str = None) -> List[Keybinding]:
        """List all keybindings, optionally filtered by context."""
        result = []
        for kb in self.keybindings.values():
            if context is None or kb.context == context or kb.context == "global":
                if kb.enabled:
                    result.append(kb)
        return sorted(result, key=lambda x: x.key)
    
    def get_keybinding(self, key: str) -> Optional[Keybinding]:
        """Get keybinding for a key."""
        return self.keybindings.get(self._normalize_key(key))
    
    def set_keybinding(self, key: str, command: str, description: str = "", context: str = "global") -> str:
        """Set a keybinding."""
        normalized = self._normalize_key(key)
        self.keybindings[normalized] = Keybinding(
            key=key,
            command=command,
            description=description,
            enabled=True,
            context=context
        )
        self._save_keybindings()
        return f"✓ Set keybinding: {key} → {command}"
    
    def remove_keybinding(self, key: str) -> str:
        """Remove a keybinding."""
        normalized = self._normalize_key(key)
        if normalized in self.keybindings:
            kb = self.keybindings[normalized]
            kb.enabled = False
            self._save_keybindings()
            return f"✓ Removed keybinding: {key}"
        return f"✗ Keybinding not found: {key}"
    
    def reset_keybindings(self) -> str:
        """Reset all keybindings to defaults."""
        self.keybindings.clear()
        for kb in DEFAULT_KEYBINDINGS:
            key = self._normalize_key(kb.key)
            self.keybindings[key] = kb
        
        if os.path.exists(self.keybindings_file):
            os.remove(self.keybindings_file)
        
        return "✓ Reset keybindings to defaults"
    
    def export_keybindings(self, output_path: str = None) -> str:
        """Export keybindings to a file."""
        if output_path is None:
            output_path = "valyxo-keybindings.json"
        
        data = {
            "keybindings": [kb.to_dict() for kb in self.keybindings.values() if kb.enabled]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return f"✓ Exported keybindings to: {output_path}"
    
    def import_keybindings(self, file_path: str, merge: bool = True) -> str:
        """Import keybindings from a file."""
        if not os.path.exists(file_path):
            return f"✗ File not found: {file_path}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not merge:
                self.keybindings.clear()
            
            count = 0
            for kb_data in data.get("keybindings", []):
                kb = Keybinding.from_dict(kb_data)
                key = self._normalize_key(kb.key)
                self.keybindings[key] = kb
                count += 1
            
            self._save_keybindings()
            return f"✓ Imported {count} keybindings"
            
        except Exception as e:
            return f"✗ Failed to import: {e}"
    
    def register_handler(self, command: str, handler: Callable):
        """Register a handler for a command."""
        self.handlers[command] = handler
    
    def handle_key(self, key: str, context: str = "global") -> Optional[str]:
        """Handle a key press, return the command if matched."""
        normalized = self._normalize_key(key)
        kb = self.keybindings.get(normalized)
        
        if kb and kb.enabled:
            if kb.context == "global" or kb.context == context:
                return kb.command
        
        return None
    
    def execute(self, command: str) -> Any:
        """Execute a command by name."""
        if command in self.handlers:
            return self.handlers[command]()
        return None
    
    def format_keybindings(self, context: str = None) -> str:
        """Format keybindings for display."""
        keybindings = self.list_keybindings(context)
        
        if not keybindings:
            return "No keybindings configured"
        
        lines = ["╭─ Keybindings ─╮"]
        
        current_context = None
        for kb in sorted(keybindings, key=lambda x: (x.context, x.key)):
            if kb.context != current_context:
                current_context = kb.context
                lines.append(f"├─ {current_context.upper()} ─┤")
            
            desc = kb.description if kb.description else kb.command
            lines.append(f"│  {kb.key:<20} {desc}")
        
        lines.append("╰────────────────╯")
        return "\n".join(lines)


# Key parsing helpers
def parse_key_event(event_key: str) -> str:
    """Parse a key event to normalized format."""
    # Handle common key names
    key_map = {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        "home": "home",
        "end": "end",
        "pageup": "pageup",
        "pagedown": "pagedown",
        "insert": "insert",
        "delete": "delete",
        "backspace": "backspace",
        "enter": "enter",
        "return": "enter",
        "escape": "escape",
        "esc": "escape",
        "tab": "tab",
        "space": "space",
    }
    
    parts = event_key.lower().split("+")
    modifiers = []
    main_key = parts[-1]
    
    for part in parts[:-1]:
        if part in ("ctrl", "control"):
            modifiers.append("ctrl")
        elif part in ("alt", "option", "meta"):
            modifiers.append("alt")
        elif part in ("shift",):
            modifiers.append("shift")
        elif part in ("super", "win", "cmd", "command"):
            modifiers.append("super")
    
    if main_key in key_map:
        main_key = key_map[main_key]
    
    return "+".join(sorted(modifiers) + [main_key])


def key_to_display(key: str) -> str:
    """Convert key string to display format."""
    display_map = {
        "ctrl": "Ctrl",
        "alt": "Alt",
        "shift": "Shift",
        "super": "⌘",
        "up": "↑",
        "down": "↓",
        "left": "←",
        "right": "→",
        "enter": "↵",
        "tab": "⇥",
        "escape": "Esc",
        "backspace": "⌫",
        "delete": "Del",
        "space": "Space",
    }
    
    parts = key.split("+")
    display_parts = []
    
    for part in parts:
        if part.lower() in display_map:
            display_parts.append(display_map[part.lower()])
        elif part.startswith("f") and part[1:].isdigit():
            display_parts.append(part.upper())
        else:
            display_parts.append(part.upper())
    
    return "+".join(display_parts)
