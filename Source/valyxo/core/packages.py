"""Valyxo Package Manager v0.6.0

Manages ValyxoScript packages and dependencies.

Commands:
    valyxo install <package>    Install a package
    valyxo uninstall <package>  Remove a package
    valyxo list                 List installed packages
    valyxo search <query>       Search available packages
"""

import os
import json
import shutil
import urllib.request
from typing import Dict, List, Optional, Any
from .constants import ROOT_DIR, CONFIG_DIR


PACKAGES_DIR = os.path.join(ROOT_DIR, "packages")
PACKAGES_REGISTRY = os.path.join(CONFIG_DIR, "packages.json")

# Built-in packages that come with Valyxo
BUILTIN_PACKAGES = {
    "math": {
        "name": "math",
        "version": "1.0.0",
        "description": "Mathematical functions and constants",
        "author": "Valyxo",
        "functions": ["abs", "min", "max", "round", "floor", "ceil", "sqrt", "pow", "pi", "e"]
    },
    "string": {
        "name": "string",
        "version": "1.0.0",
        "description": "String manipulation utilities",
        "author": "Valyxo",
        "functions": ["upper", "lower", "trim", "split", "join", "replace", "contains", "startswith", "endswith"]
    },
    "array": {
        "name": "array",
        "version": "1.0.0",
        "description": "Array/list utilities",
        "author": "Valyxo",
        "functions": ["len", "push", "pop", "shift", "unshift", "slice", "reverse", "sort", "find", "filter", "map"]
    },
    "file": {
        "name": "file",
        "version": "1.0.0",
        "description": "File system operations",
        "author": "Valyxo",
        "functions": ["read", "write", "append", "exists", "delete", "copy", "move", "list_dir"]
    },
    "http": {
        "name": "http",
        "version": "1.0.0",
        "description": "HTTP request utilities",
        "author": "Valyxo",
        "functions": ["get", "post", "put", "delete", "json_parse", "json_stringify"]
    },
    "time": {
        "name": "time",
        "version": "1.0.0",
        "description": "Date and time utilities",
        "author": "Valyxo",
        "functions": ["now", "timestamp", "format", "parse", "sleep", "timer"]
    },
    "random": {
        "name": "random",
        "version": "1.0.0",
        "description": "Random number generation",
        "author": "Valyxo",
        "functions": ["random", "randint", "choice", "shuffle", "uuid"]
    },
    "json": {
        "name": "json",
        "version": "1.0.0",
        "description": "JSON parsing and serialization",
        "author": "Valyxo",
        "functions": ["parse", "stringify", "pretty"]
    }
}


class ValyxoPackageManager:
    """Manages packages for ValyxoScript."""
    
    def __init__(self):
        self.installed: Dict[str, Dict[str, Any]] = {}
        os.makedirs(PACKAGES_DIR, exist_ok=True)
        self._load_registry()
    
    def _load_registry(self) -> None:
        """Load installed packages registry."""
        if os.path.exists(PACKAGES_REGISTRY):
            try:
                with open(PACKAGES_REGISTRY, 'r', encoding='utf-8') as f:
                    self.installed = json.load(f)
            except:
                self.installed = {}
        else:
            self.installed = {}
    
    def _save_registry(self) -> None:
        """Save installed packages registry."""
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(PACKAGES_REGISTRY, 'w', encoding='utf-8') as f:
            json.dump(self.installed, f, indent=2)
    
    def install(self, package_name: str, version: str = "latest") -> str:
        """Install a package.
        
        Returns:
            Success or error message
        """
        # Check if it's a built-in package
        if package_name in BUILTIN_PACKAGES:
            pkg = BUILTIN_PACKAGES[package_name]
            self.installed[package_name] = {
                "name": pkg["name"],
                "version": pkg["version"],
                "description": pkg["description"],
                "builtin": True,
                "functions": pkg["functions"]
            }
            self._save_registry()
            return f"✓ Installed {package_name}@{pkg['version']} (built-in)"
        
        # Check for local package
        local_path = os.path.join(PACKAGES_DIR, package_name)
        if os.path.exists(local_path):
            manifest_path = os.path.join(local_path, "package.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                self.installed[package_name] = {
                    "name": manifest.get("name", package_name),
                    "version": manifest.get("version", "1.0.0"),
                    "description": manifest.get("description", ""),
                    "path": local_path,
                    "functions": manifest.get("exports", [])
                }
                self._save_registry()
                return f"✓ Installed {package_name}@{manifest.get('version', '1.0.0')} (local)"
        
        return f"✗ Package not found: {package_name}"
    
    def uninstall(self, package_name: str) -> str:
        """Uninstall a package.
        
        Returns:
            Success or error message
        """
        if package_name not in self.installed:
            return f"✗ Package not installed: {package_name}"
        
        pkg = self.installed[package_name]
        
        # Can't uninstall built-in packages, just remove from registry
        if pkg.get("builtin"):
            del self.installed[package_name]
            self._save_registry()
            return f"✓ Removed {package_name} from active packages"
        
        # Remove local package directory
        if "path" in pkg and os.path.exists(pkg["path"]):
            try:
                shutil.rmtree(pkg["path"])
            except Exception as e:
                return f"✗ Failed to remove package files: {e}"
        
        del self.installed[package_name]
        self._save_registry()
        return f"✓ Uninstalled {package_name}"
    
    def list_installed(self) -> List[Dict[str, Any]]:
        """List all installed packages."""
        return [
            {
                "name": name,
                "version": info.get("version", "unknown"),
                "description": info.get("description", ""),
                "builtin": info.get("builtin", False)
            }
            for name, info in self.installed.items()
        ]
    
    def list_available(self) -> List[Dict[str, Any]]:
        """List all available packages (built-in + local)."""
        available = []
        
        # Add built-in packages
        for name, pkg in BUILTIN_PACKAGES.items():
            available.append({
                "name": name,
                "version": pkg["version"],
                "description": pkg["description"],
                "installed": name in self.installed,
                "builtin": True
            })
        
        # Add local packages
        if os.path.exists(PACKAGES_DIR):
            for item in os.listdir(PACKAGES_DIR):
                if item not in BUILTIN_PACKAGES:
                    pkg_path = os.path.join(PACKAGES_DIR, item)
                    if os.path.isdir(pkg_path):
                        manifest_path = os.path.join(pkg_path, "package.json")
                        if os.path.exists(manifest_path):
                            try:
                                with open(manifest_path, 'r', encoding='utf-8') as f:
                                    manifest = json.load(f)
                                available.append({
                                    "name": item,
                                    "version": manifest.get("version", "1.0.0"),
                                    "description": manifest.get("description", ""),
                                    "installed": item in self.installed,
                                    "builtin": False
                                })
                            except:
                                pass
        
        return available
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search available packages by name or description."""
        query = query.lower()
        results = []
        
        for pkg in self.list_available():
            if query in pkg["name"].lower() or query in pkg.get("description", "").lower():
                results.append(pkg)
        
        return results
    
    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a package."""
        if package_name in self.installed:
            return self.installed[package_name]
        if package_name in BUILTIN_PACKAGES:
            return BUILTIN_PACKAGES[package_name]
        return None
    
    def get_package_functions(self, package_name: str) -> List[str]:
        """Get list of functions exported by a package."""
        info = self.get_package_info(package_name)
        if info:
            return info.get("functions", [])
        return []
    
    def is_installed(self, package_name: str) -> bool:
        """Check if a package is installed."""
        return package_name in self.installed


def create_package_template(name: str, directory: str = None) -> str:
    """Create a new package template.
    
    Returns:
        Path to created package or error message
    """
    if directory is None:
        directory = PACKAGES_DIR
    
    pkg_dir = os.path.join(directory, name)
    
    if os.path.exists(pkg_dir):
        return f"Package already exists: {name}"
    
    try:
        os.makedirs(pkg_dir, exist_ok=True)
        
        # Create package.json
        manifest = {
            "name": name,
            "version": "1.0.0",
            "description": f"A ValyxoScript package: {name}",
            "author": "",
            "valyxo_version": ">=0.6.0",
            "exports": ["hello"]
        }
        
        with open(os.path.join(pkg_dir, "package.json"), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        # Create main.vs (ValyxoScript)
        main_content = f'''# {name} - ValyxoScript Package
# Version 1.0.0

# Define package functions
func hello(name) {{
    print "Hello from {name} package!"
    print "Name: " + name
}}

# Export functions by listing them in package.json "exports" array
'''
        
        with open(os.path.join(pkg_dir, "main.vs"), 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        # Create README
        readme = f'''# {name}

A ValyxoScript package.

## Installation

```
valyxo install {name}
```

## Usage

```valyxoscript
import {name}

{name}.hello("World")
```

## Functions

- `hello(name)` - Greets the user
'''
        
        with open(os.path.join(pkg_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme)
        
        return pkg_dir
        
    except Exception as e:
        return f"Failed to create package: {e}"
