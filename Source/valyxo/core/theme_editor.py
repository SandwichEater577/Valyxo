"""Valyxo Theme Editor v0.6.0

Create, customize, and share terminal themes.

Usage:
    theme list                    List available themes
    theme use <name>              Apply a theme
    theme create <name>           Create a new theme
    theme edit <name>             Edit an existing theme
    theme export <name>           Export theme to file
    theme import <file>           Import theme from file
    theme preview <name>          Preview a theme
    theme delete <name>           Delete a custom theme
"""

import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ThemeColors:
    """Color scheme for a Valyxo theme."""
    background: str = "#0a0a0a"
    foreground: str = "#ffffff"
    primary: str = "#3b82f6"
    secondary: str = "#8b5cf6"
    success: str = "#22c55e"
    warning: str = "#eab308"
    error: str = "#ef4444"
    info: str = "#06b6d4"
    muted: str = "#6b7280"
    border: str = "#1f2937"
    selection: str = "#374151"
    cursor: str = "#ffffff"
    
    # Syntax highlighting
    syntax_keyword: str = "#c084fc"
    syntax_string: str = "#22c55e"
    syntax_number: str = "#f97316"
    syntax_comment: str = "#6b7280"
    syntax_function: str = "#3b82f6"
    syntax_variable: str = "#60a5fa"
    syntax_operator: str = "#f472b6"


@dataclass
class ThemePrompt:
    """Prompt styling for a Valyxo theme."""
    user_color: str = "#22c55e"
    host_color: str = "#3b82f6"
    path_color: str = "#8b5cf6"
    separator: str = "›"
    separator_color: str = "#6b7280"
    format: str = "{user}@{host} {path} {separator} "


@dataclass 
class ValyxoTheme:
    """Complete Valyxo theme configuration."""
    name: str
    description: str = "Custom Valyxo theme"
    author: str = ""
    version: str = "1.0.0"
    colors: ThemeColors = None
    prompt: ThemePrompt = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = ThemeColors()
        if self.prompt is None:
            self.prompt = ThemePrompt()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "version": self.version,
            "colors": asdict(self.colors),
            "prompt": asdict(self.prompt)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValyxoTheme":
        """Create theme from dictionary."""
        colors = ThemeColors(**data.get("colors", {})) if data.get("colors") else ThemeColors()
        prompt = ThemePrompt(**data.get("prompt", {})) if data.get("prompt") else ThemePrompt()
        return cls(
            name=data.get("name", "Untitled"),
            description=data.get("description", ""),
            author=data.get("author", ""),
            version=data.get("version", "1.0.0"),
            colors=colors,
            prompt=prompt
        )


# Built-in themes
BUILTIN_THEMES: Dict[str, ValyxoTheme] = {
    "dark": ValyxoTheme(
        name="dark",
        description="Default dark theme",
        author="Valyxo Team",
        colors=ThemeColors(),
        prompt=ThemePrompt()
    ),
    
    "light": ValyxoTheme(
        name="light",
        description="Light theme for bright environments",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#ffffff",
            foreground="#1f2937",
            primary="#2563eb",
            secondary="#7c3aed",
            success="#16a34a",
            warning="#ca8a04",
            error="#dc2626",
            info="#0891b2",
            muted="#9ca3af",
            border="#e5e7eb",
            selection="#dbeafe",
            cursor="#1f2937",
            syntax_keyword="#7c3aed",
            syntax_string="#16a34a",
            syntax_number="#ea580c",
            syntax_comment="#9ca3af",
            syntax_function="#2563eb",
            syntax_variable="#3b82f6",
            syntax_operator="#db2777"
        ),
        prompt=ThemePrompt(
            user_color="#16a34a",
            host_color="#2563eb",
            path_color="#7c3aed",
            separator_color="#9ca3af"
        )
    ),
    
    "monokai": ValyxoTheme(
        name="monokai",
        description="Classic Monokai color scheme",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#272822",
            foreground="#f8f8f2",
            primary="#66d9ef",
            secondary="#ae81ff",
            success="#a6e22e",
            warning="#e6db74",
            error="#f92672",
            info="#66d9ef",
            muted="#75715e",
            border="#3e3d32",
            selection="#49483e",
            cursor="#f8f8f0",
            syntax_keyword="#f92672",
            syntax_string="#e6db74",
            syntax_number="#ae81ff",
            syntax_comment="#75715e",
            syntax_function="#a6e22e",
            syntax_variable="#66d9ef",
            syntax_operator="#f92672"
        ),
        prompt=ThemePrompt(
            user_color="#a6e22e",
            host_color="#66d9ef",
            path_color="#ae81ff",
            separator_color="#75715e"
        )
    ),
    
    "dracula": ValyxoTheme(
        name="dracula",
        description="Dracula dark theme",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#282a36",
            foreground="#f8f8f2",
            primary="#bd93f9",
            secondary="#ff79c6",
            success="#50fa7b",
            warning="#f1fa8c",
            error="#ff5555",
            info="#8be9fd",
            muted="#6272a4",
            border="#44475a",
            selection="#44475a",
            cursor="#f8f8f2",
            syntax_keyword="#ff79c6",
            syntax_string="#f1fa8c",
            syntax_number="#bd93f9",
            syntax_comment="#6272a4",
            syntax_function="#50fa7b",
            syntax_variable="#8be9fd",
            syntax_operator="#ff79c6"
        ),
        prompt=ThemePrompt(
            user_color="#50fa7b",
            host_color="#8be9fd",
            path_color="#bd93f9",
            separator_color="#6272a4"
        )
    ),
    
    "nord": ValyxoTheme(
        name="nord",
        description="Arctic, bluish clean and elegant",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#2e3440",
            foreground="#eceff4",
            primary="#88c0d0",
            secondary="#b48ead",
            success="#a3be8c",
            warning="#ebcb8b",
            error="#bf616a",
            info="#81a1c1",
            muted="#4c566a",
            border="#3b4252",
            selection="#434c5e",
            cursor="#d8dee9",
            syntax_keyword="#81a1c1",
            syntax_string="#a3be8c",
            syntax_number="#b48ead",
            syntax_comment="#616e88",
            syntax_function="#88c0d0",
            syntax_variable="#8fbcbb",
            syntax_operator="#81a1c1"
        ),
        prompt=ThemePrompt(
            user_color="#a3be8c",
            host_color="#88c0d0",
            path_color="#b48ead",
            separator_color="#4c566a"
        )
    ),
    
    "solarized": ValyxoTheme(
        name="solarized",
        description="Solarized dark theme",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#002b36",
            foreground="#839496",
            primary="#268bd2",
            secondary="#6c71c4",
            success="#859900",
            warning="#b58900",
            error="#dc322f",
            info="#2aa198",
            muted="#586e75",
            border="#073642",
            selection="#073642",
            cursor="#839496",
            syntax_keyword="#859900",
            syntax_string="#2aa198",
            syntax_number="#d33682",
            syntax_comment="#586e75",
            syntax_function="#268bd2",
            syntax_variable="#b58900",
            syntax_operator="#cb4b16"
        ),
        prompt=ThemePrompt(
            user_color="#859900",
            host_color="#268bd2",
            path_color="#6c71c4",
            separator_color="#586e75"
        )
    ),
    
    "gruvbox": ValyxoTheme(
        name="gruvbox",
        description="Retro groove color scheme",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#282828",
            foreground="#ebdbb2",
            primary="#83a598",
            secondary="#d3869b",
            success="#b8bb26",
            warning="#fabd2f",
            error="#fb4934",
            info="#8ec07c",
            muted="#928374",
            border="#3c3836",
            selection="#504945",
            cursor="#ebdbb2",
            syntax_keyword="#fb4934",
            syntax_string="#b8bb26",
            syntax_number="#d3869b",
            syntax_comment="#928374",
            syntax_function="#fabd2f",
            syntax_variable="#83a598",
            syntax_operator="#fe8019"
        ),
        prompt=ThemePrompt(
            user_color="#b8bb26",
            host_color="#83a598",
            path_color="#d3869b",
            separator_color="#928374"
        )
    ),
    
    "cyberpunk": ValyxoTheme(
        name="cyberpunk",
        description="Neon cyberpunk aesthetic",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#0d0221",
            foreground="#ff00ff",
            primary="#00ffff",
            secondary="#ff00ff",
            success="#00ff00",
            warning="#ffff00",
            error="#ff0040",
            info="#00ffff",
            muted="#6b21a8",
            border="#2d1f5e",
            selection="#4c1d95",
            cursor="#00ffff",
            syntax_keyword="#ff00ff",
            syntax_string="#00ff00",
            syntax_number="#ffff00",
            syntax_comment="#6b21a8",
            syntax_function="#00ffff",
            syntax_variable="#ff79c6",
            syntax_operator="#ff0040"
        ),
        prompt=ThemePrompt(
            user_color="#00ff00",
            host_color="#00ffff",
            path_color="#ff00ff",
            separator=">",
            separator_color="#6b21a8"
        )
    ),
    
    "matrix": ValyxoTheme(
        name="matrix",
        description="Classic Matrix green-on-black",
        author="Valyxo Team",
        colors=ThemeColors(
            background="#0d0208",
            foreground="#00ff41",
            primary="#00ff41",
            secondary="#008f11",
            success="#00ff41",
            warning="#39ff14",
            error="#ff0000",
            info="#00ff41",
            muted="#003b00",
            border="#003b00",
            selection="#003b00",
            cursor="#00ff41",
            syntax_keyword="#39ff14",
            syntax_string="#00ff41",
            syntax_number="#39ff14",
            syntax_comment="#003b00",
            syntax_function="#00ff41",
            syntax_variable="#008f11",
            syntax_operator="#39ff14"
        ),
        prompt=ThemePrompt(
            user_color="#00ff41",
            host_color="#008f11",
            path_color="#39ff14",
            separator=">",
            separator_color="#003b00"
        )
    )
}


class ValyxoThemeManager:
    """Manages Valyxo themes."""
    
    def __init__(self, themes_dir: str = None):
        if themes_dir is None:
            themes_dir = os.path.join(os.path.expanduser("~"), ".valyxo", "themes")
        self.themes_dir = themes_dir
        os.makedirs(self.themes_dir, exist_ok=True)
        self.current_theme: str = "dark"
    
    def list_themes(self) -> List[Dict[str, str]]:
        """List all available themes."""
        themes = []
        
        # Built-in themes
        for name, theme in BUILTIN_THEMES.items():
            themes.append({
                "name": name,
                "description": theme.description,
                "author": theme.author,
                "builtin": True
            })
        
        # Custom themes
        for filename in os.listdir(self.themes_dir):
            if filename.endswith(".json"):
                theme_path = os.path.join(self.themes_dir, filename)
                try:
                    with open(theme_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        themes.append({
                            "name": data.get("name", filename[:-5]),
                            "description": data.get("description", "Custom theme"),
                            "author": data.get("author", "Unknown"),
                            "builtin": False
                        })
                except:
                    pass
        
        return themes
    
    def get_theme(self, name: str) -> Optional[ValyxoTheme]:
        """Get a theme by name."""
        # Check built-in first
        if name in BUILTIN_THEMES:
            return BUILTIN_THEMES[name]
        
        # Check custom themes
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        if os.path.exists(theme_path):
            try:
                with open(theme_path, 'r', encoding='utf-8') as f:
                    return ValyxoTheme.from_dict(json.load(f))
            except:
                return None
        
        return None
    
    def use_theme(self, name: str) -> str:
        """Apply a theme."""
        theme = self.get_theme(name)
        if theme is None:
            return f"✗ Theme not found: {name}"
        
        self.current_theme = name
        return f"✓ Applied theme: {name}"
    
    def create_theme(self, name: str, base: str = "dark") -> str:
        """Create a new theme based on existing one."""
        if name in BUILTIN_THEMES:
            return f"✗ Cannot overwrite built-in theme: {name}"
        
        base_theme = self.get_theme(base)
        if base_theme is None:
            base_theme = BUILTIN_THEMES["dark"]
        
        new_theme = ValyxoTheme(
            name=name,
            description=f"Custom theme based on {base}",
            author="User",
            colors=base_theme.colors,
            prompt=base_theme.prompt
        )
        
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        with open(theme_path, 'w', encoding='utf-8') as f:
            json.dump(new_theme.to_dict(), f, indent=2)
        
        return f"✓ Created theme: {name}\n  Edit at: {theme_path}"
    
    def edit_theme(self, name: str, changes: Dict[str, Any]) -> str:
        """Edit an existing theme."""
        if name in BUILTIN_THEMES:
            return f"✗ Cannot edit built-in theme: {name}"
        
        theme = self.get_theme(name)
        if theme is None:
            return f"✗ Theme not found: {name}"
        
        # Apply changes
        theme_dict = theme.to_dict()
        for key, value in changes.items():
            if "." in key:
                parts = key.split(".")
                d = theme_dict
                for part in parts[:-1]:
                    d = d.setdefault(part, {})
                d[parts[-1]] = value
            else:
                theme_dict[key] = value
        
        # Save
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        with open(theme_path, 'w', encoding='utf-8') as f:
            json.dump(theme_dict, f, indent=2)
        
        return f"✓ Updated theme: {name}"
    
    def export_theme(self, name: str, output_path: str = None) -> str:
        """Export a theme to a file."""
        theme = self.get_theme(name)
        if theme is None:
            return f"✗ Theme not found: {name}"
        
        if output_path is None:
            output_path = f"{name}.valyxo-theme.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(theme.to_dict(), f, indent=2)
        
        return f"✓ Exported theme to: {output_path}"
    
    def import_theme(self, file_path: str) -> str:
        """Import a theme from a file."""
        if not os.path.exists(file_path):
            return f"✗ File not found: {file_path}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            theme = ValyxoTheme.from_dict(data)
            
            if theme.name in BUILTIN_THEMES:
                theme.name = f"{theme.name}-custom"
            
            theme_path = os.path.join(self.themes_dir, f"{theme.name}.json")
            with open(theme_path, 'w', encoding='utf-8') as f:
                json.dump(theme.to_dict(), f, indent=2)
            
            return f"✓ Imported theme: {theme.name}"
            
        except Exception as e:
            return f"✗ Failed to import: {e}"
    
    def delete_theme(self, name: str) -> str:
        """Delete a custom theme."""
        if name in BUILTIN_THEMES:
            return f"✗ Cannot delete built-in theme: {name}"
        
        theme_path = os.path.join(self.themes_dir, f"{name}.json")
        if not os.path.exists(theme_path):
            return f"✗ Theme not found: {name}"
        
        os.remove(theme_path)
        return f"✓ Deleted theme: {name}"
    
    def preview_theme(self, name: str) -> str:
        """Generate a preview of a theme."""
        theme = self.get_theme(name)
        if theme is None:
            return f"✗ Theme not found: {name}"
        
        preview = [
            f"╭─ Theme: {theme.name} ─╮",
            f"│ {theme.description}",
            f"│ Author: {theme.author}",
            f"├─ Colors ─┤",
            f"│  Background: {theme.colors.background}",
            f"│  Foreground: {theme.colors.foreground}",
            f"│  Primary:    {theme.colors.primary}",
            f"│  Secondary:  {theme.colors.secondary}",
            f"│  Success:    {theme.colors.success}",
            f"│  Error:      {theme.colors.error}",
            f"├─ Prompt ─┤",
            f"│  Format: {theme.prompt.format}",
            f"╰──────────╯"
        ]
        
        return "\n".join(preview)
    
    def get_current_colors(self) -> ThemeColors:
        """Get colors of current theme."""
        theme = self.get_theme(self.current_theme)
        if theme:
            return theme.colors
        return ThemeColors()
    
    def get_current_prompt(self) -> ThemePrompt:
        """Get prompt config of current theme."""
        theme = self.get_theme(self.current_theme)
        if theme:
            return theme.prompt
        return ThemePrompt()
