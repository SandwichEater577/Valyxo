"""Valyxo Plugin System v0.6.0

Allows users to create, install, and manage plugins to extend Valyxo functionality.

Plugin structure:
    plugins/
        my_plugin/
            plugin.json     # Plugin manifest
            main.py         # Plugin entry point
"""

import os
import json
import importlib.util
from typing import Dict, List, Optional, Callable, Any
from .constants import ROOT_DIR


PLUGINS_DIR = os.path.join(ROOT_DIR, "plugins")


class ValyxoPlugin:
    """Base class for Valyxo plugins."""
    
    def __init__(self, name: str, version: str, description: str = ""):
        self.name = name
        self.version = version
        self.description = description
        self.enabled = True
        self.commands: Dict[str, Callable] = {}
    
    def register_command(self, name: str, handler: Callable, help_text: str = "") -> None:
        """Register a new command for the plugin."""
        self.commands[name] = {
            "handler": handler,
            "help": help_text
        }
    
    def on_load(self) -> None:
        """Called when plugin is loaded. Override in subclass."""
        pass
    
    def on_unload(self) -> None:
        """Called when plugin is unloaded. Override in subclass."""
        pass


class ValyxoPluginManager:
    """Manages plugin lifecycle: loading, unloading, and execution."""
    
    def __init__(self):
        self.plugins: Dict[str, ValyxoPlugin] = {}
        self.plugin_commands: Dict[str, str] = {}  # command -> plugin_name
        os.makedirs(PLUGINS_DIR, exist_ok=True)
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in the plugins directory."""
        if not os.path.exists(PLUGINS_DIR):
            return []
        
        plugins = []
        for item in os.listdir(PLUGINS_DIR):
            plugin_dir = os.path.join(PLUGINS_DIR, item)
            manifest_path = os.path.join(plugin_dir, "plugin.json")
            if os.path.isdir(plugin_dir) and os.path.exists(manifest_path):
                plugins.append(item)
        return plugins
    
    def load_plugin(self, name: str) -> Optional[str]:
        """Load a plugin by name.
        
        Returns:
            Error message if failed, None if successful
        """
        plugin_dir = os.path.join(PLUGINS_DIR, name)
        manifest_path = os.path.join(plugin_dir, "plugin.json")
        main_path = os.path.join(plugin_dir, "main.py")
        
        if not os.path.exists(manifest_path):
            return f"Plugin manifest not found: {manifest_path}"
        
        if not os.path.exists(main_path):
            return f"Plugin entry point not found: {main_path}"
        
        try:
            # Load manifest
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Load plugin module
            spec = importlib.util.spec_from_file_location(f"valyxo_plugin_{name}", main_path)
            if not spec or not spec.loader:
                return f"Failed to load plugin module: {name}"
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get plugin class
            if hasattr(module, 'Plugin'):
                plugin_instance = module.Plugin()
            elif hasattr(module, 'plugin'):
                plugin_instance = module.plugin
            else:
                # Create basic plugin from manifest
                plugin_instance = ValyxoPlugin(
                    name=manifest.get('name', name),
                    version=manifest.get('version', '1.0.0'),
                    description=manifest.get('description', '')
                )
            
            # Register commands
            if hasattr(module, 'commands'):
                for cmd_name, cmd_info in module.commands.items():
                    plugin_instance.register_command(cmd_name, cmd_info['handler'], cmd_info.get('help', ''))
            
            plugin_instance.on_load()
            self.plugins[name] = plugin_instance
            
            # Register all plugin commands
            for cmd_name in plugin_instance.commands:
                self.plugin_commands[cmd_name] = name
            
            return None
            
        except json.JSONDecodeError as e:
            return f"Invalid plugin manifest: {e}"
        except Exception as e:
            return f"Failed to load plugin: {e}"
    
    def unload_plugin(self, name: str) -> Optional[str]:
        """Unload a plugin by name."""
        if name not in self.plugins:
            return f"Plugin not loaded: {name}"
        
        try:
            plugin = self.plugins[name]
            plugin.on_unload()
            
            # Unregister commands
            for cmd_name in plugin.commands:
                if cmd_name in self.plugin_commands:
                    del self.plugin_commands[cmd_name]
            
            del self.plugins[name]
            return None
        except Exception as e:
            return f"Failed to unload plugin: {e}"
    
    def get_plugin(self, name: str) -> Optional[ValyxoPlugin]:
        """Get a loaded plugin by name."""
        return self.plugins.get(name)
    
    def execute_command(self, command: str, args: str) -> Optional[Any]:
        """Execute a plugin command.
        
        Returns:
            Command result or None if command not found
        """
        if command not in self.plugin_commands:
            return None
        
        plugin_name = self.plugin_commands[command]
        plugin = self.plugins.get(plugin_name)
        
        if not plugin or command not in plugin.commands:
            return None
        
        handler = plugin.commands[command]['handler']
        return handler(args)
    
    def is_plugin_command(self, command: str) -> bool:
        """Check if a command is provided by a plugin."""
        return command in self.plugin_commands
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins with their info."""
        return [
            {
                "name": name,
                "version": plugin.version,
                "description": plugin.description,
                "enabled": plugin.enabled,
                "commands": list(plugin.commands.keys())
            }
            for name, plugin in self.plugins.items()
        ]
    
    def list_available(self) -> List[Dict[str, str]]:
        """List all available plugins (installed but not necessarily loaded)."""
        available = []
        for name in self.discover_plugins():
            manifest_path = os.path.join(PLUGINS_DIR, name, "plugin.json")
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                available.append({
                    "name": name,
                    "version": manifest.get("version", "unknown"),
                    "description": manifest.get("description", ""),
                    "loaded": name in self.plugins
                })
            except:
                available.append({
                    "name": name,
                    "version": "unknown",
                    "description": "Error reading manifest",
                    "loaded": name in self.plugins
                })
        return available


def create_plugin_template(name: str) -> str:
    """Create a new plugin template.
    
    Returns:
        Path to created plugin or error message
    """
    plugin_dir = os.path.join(PLUGINS_DIR, name)
    
    if os.path.exists(plugin_dir):
        return f"Plugin already exists: {name}"
    
    try:
        os.makedirs(plugin_dir, exist_ok=True)
        
        # Create manifest
        manifest = {
            "name": name,
            "version": "1.0.0",
            "description": f"A Valyxo plugin: {name}",
            "author": "",
            "valyxo_version": ">=0.6.0"
        }
        
        with open(os.path.join(plugin_dir, "plugin.json"), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        # Create main.py
        main_content = f'''"""
{name} - Valyxo Plugin
"""

from valyxo.core.plugins import ValyxoPlugin


class Plugin(ValyxoPlugin):
    def __init__(self):
        super().__init__(
            name="{name}",
            version="1.0.0",
            description="A custom Valyxo plugin"
        )
    
    def on_load(self):
        """Called when the plugin is loaded."""
        print(f"{{self.name}} plugin loaded!")
        
        # Register custom commands
        self.register_command(
            "{name.lower()}_hello",
            self.cmd_hello,
            "Say hello from {name}"
        )
    
    def on_unload(self):
        """Called when the plugin is unloaded."""
        print(f"{{self.name}} plugin unloaded!")
    
    def cmd_hello(self, args: str) -> None:
        """Example command handler."""
        print(f"Hello from {name}! Args: {{args}}")


# Alternative: Define commands dict for simpler plugins
# commands = {{
#     "my_command": {{
#         "handler": lambda args: print(f"Running with: {{args}}"),
#         "help": "Description of my_command"
#     }}
# }}
'''
        
        with open(os.path.join(plugin_dir, "main.py"), 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        return plugin_dir
        
    except Exception as e:
        return f"Failed to create plugin: {e}"
