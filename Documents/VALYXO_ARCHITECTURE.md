# Valyxo v0.31 - Modular Architecture

## Overview

Valyxo has been refactored with a **professional, modular architecture** designed for maintainability, scalability, and clean code organization.

## Directory Structure

```
src/
├── Valyxo.py                 # Main entry point
└── valyxo/                   # Valyxo package
    ├── __init__.py           # Package initialization with central exports
    ├── core/                 # Core functionality module
    │   ├── __init__.py       # Exports all core components
    │   ├── colors.py         # Color definitions and theme management
    │   ├── constants.py      # Application constants and configuration
    │   ├── utils.py          # Utility functions
    │   ├── filesystem.py     # File system operations (ValyxoFileSystem)
    │   ├── gpt.py            # GPT module (ValyxoGPTModule)
    │   ├── jobs.py           # Job management (ValyxoJobsManager)
    │   └── man.py            # Manual/help system (ValyxoManSystem)
    ├── shell/                # Shell interface module
    │   └── __init__.py       # Shell components
    └── editor/               # Editor module
        └── __init__.py       # Editor components
```

## Module Breakdown

### Core Module (`valyxo.core`)

The backbone of Valyxo, containing all essential functionality organized into focused modules:

#### **colors.py** - Color & Theme Management
- **Colors** class: ANSI color code constants
- **color()** function: Apply colors with settings-aware disabling
- **DEFAULT_THEMES** dict: Pre-defined color themes (neon, classic, hacker, ocean)

**Usage:**
```python
from valyxo.core import Colors, color, DEFAULT_THEMES
```

#### **constants.py** - Application Configuration
- **APP_NAME**: Application identifier
- **VERSION**: Version string
- **Directory Constants**: ROOT_DIR, PROJECTS_DIR, SYSTEM_DIR, CONFIG_DIR, etc.
- **Path Constants**: CONFIG_PATH, THEMES_PATH, HISTORY_PATH, API_KEY_PATH
- **COMMANDS**: Available commands list
- **LANG_MAP**: Language extension mapping
- **DEFAULT_SETTINGS**: Default configuration values

**Usage:**
```python
from valyxo.core import APP_NAME, VERSION, ROOT_DIR, COMMANDS, LANG_MAP
```

#### **utils.py** - Utility Functions
- **prompt()**: Safe input with interrupt handling
- **path_within_root()**: Validate paths are within allowed root
- **normalize_virtual_path()**: Convert absolute paths to virtual paths (~/)
- **highlight_valyxoscript()**: Syntax highlighting for ValyxoScript

**Usage:**
```python
from valyxo.core import prompt, path_within_root, normalize_virtual_path, highlight_valyxoscript
```

#### **filesystem.py** - File System Operations
- **ValyxoFileSystem** class: Manages file and directory operations
  - `set_cwd()`: Set current working directory
  - `set_active_file()`: Track active file
  - `ensure_dirs()`: Create necessary directories
  - `create_file()`: Create files with language detection
  - `ask_language()`: Interactive language selection

**Usage:**
```python
from valyxo.core import ValyxoFileSystem

fs = ValyxoFileSystem(ROOT_DIR)
fs.ensure_dirs()
fs.create_file(cwd, filename)
```

#### **gpt.py** - AI Assistant Module
- **ValyxoGPTModule** class: Manages conversation with Zencoder AI
  - `_load_api_key()`: Load API key from storage
  - `set_api_key()`: Store API key securely
  - `add_message()`: Add to conversation history (max 40 messages)
  - `get_response()`: Get AI response using Zencoder
  - `_zencoder_response()`: Intelligent response generation

**Usage:**
```python
from valyxo.core import ValyxoGPTModule

gpt = ValyxoGPTModule()
response = gpt.get_response("How do I define a function?")
```

#### **jobs.py** - Job Management
- **ValyxoJobsManager** class: Background job tracking
  - `create_job()`: Start a new job
  - `update_status()`: Update job status
  - `stop_job()`: Terminate a job
  - `list_jobs()`: Display all active jobs
  - Thread-safe with locks

**Usage:**
```python
from valyxo.core import ValyxoJobsManager

jobs = ValyxoJobsManager()
pid = jobs.create_job(filepath)
jobs.stop_job(pid)
```

#### **man.py** - Manual/Help System
- **ValyxoManSystem** class: Help documentation system
  - `_default_pages()`: Load help content
  - `load_pages()`: Create help file pages
  - `_format_manpage()`: Format help documentation
  - `pager_display()`: Display help with pagination

**Usage:**
```python
from valyxo.core import ValyxoManSystem

man = ValyxoManSystem()
man.load_pages()
man.pager_display(help_text)
```

### Shell Module (`valyxo.shell`)

Placeholder for shell interface implementation.

### Editor Module (`valyxo.editor`)

Placeholder for editor implementation.

## Central Exports

### From `valyxo.core.__init__.py`

All core components are exported for easy access:

```python
from valyxo.core import (
    # Colors
    Colors, color, DEFAULT_THEMES,
    
    # Constants
    APP_NAME, VERSION, HOME, ROOT_DIR, PROJECTS_DIR, SYSTEM_DIR,
    CONFIG_DIR, MAN_DIR, MAIN_PROJECT, CONFIG_PATH, THEMES_PATH,
    HISTORY_PATH, API_KEY_PATH, COMMANDS, LANG_MAP, DEFAULT_SETTINGS,
    
    # Utils
    prompt, path_within_root, normalize_virtual_path, highlight_valyxoscript,
    
    # Classes
    ValyxoFileSystem, ValyxoGPTModule, ValyxoJobsManager, ValyxoManSystem,
)
```

### From `valyxo.__init__.py`

Package-level exports for convenience:

```python
from valyxo import (
    Colors, color, DEFAULT_THEMES,
    APP_NAME, VERSION, DEFAULT_SETTINGS,
    ValyxoFileSystem, ValyxoGPTModule, ValyxoJobsManager, ValyxoManSystem,
)
```

## Main Entry Point (`src/Valyxo.py`)

The simplified main file that imports from the modular structure:

```python
from valyxo.core import (
    Colors, APP_NAME, VERSION, ROOT_DIR, COMMANDS, LANG_MAP,
    ValyxoFileSystem, ValyxoGPTModule, ValyxoJobsManager, ValyxoManSystem,
)

class ValyxoShell:
    def __init__(self):
        self.filesystem = ValyxoFileSystem(ROOT_DIR)
        self.gpt = ValyxoGPTModule()
        self.jobs = ValyxoJobsManager()
        self.man = ValyxoManSystem()
        self.settings = {}

    def initialize(self):
        self.filesystem.ensure_dirs()
        self.man.load_pages()
        self._load_settings()

    def run(self):
        print(f"Welcome to {APP_NAME} {VERSION}")

def main():
    shell = ValyxoShell()
    shell.initialize()
    shell.run()
```

## Design Principles

### 1. **Separation of Concerns**
Each module has a single responsibility:
- Colors module handles colors and themes
- Constants module manages configuration
- Utils module provides helper functions
- Filesystem module manages file operations
- GPT module handles AI interactions
- Jobs module manages background processes
- Man module handles documentation

### 2. **Single Responsibility Principle (SRP)**
Each class and function does one thing well, making the code:
- Easier to test
- Easier to maintain
- Easier to extend

### 3. **DRY (Don't Repeat Yourself)**
Common functionality is centralized:
- Color codes in one place
- Constants in one place
- Utility functions in one place

### 4. **Clean Imports**
Central `__init__.py` files provide clean, discoverable exports:
- `from valyxo.core import Colors`
- `from valyxo.core import ValyxoFileSystem`

### 5. **Maintainability**
- Clear file structure makes navigation easy
- Each file is focused and concise
- Dependencies are explicit and minimal

## Benefits of This Architecture

1. **Scalability**: New features can be added without cluttering existing files
2. **Testability**: Each module can be tested independently
3. **Reusability**: Components can be used in other projects
4. **Readability**: Code is organized logically
5. **Maintainability**: Changes are localized to specific modules
6. **Professional**: Industry-standard modular structure

## Adding New Features

To add a new feature:

1. **Identify the category** (core, shell, editor)
2. **Create a new module** in the appropriate directory
3. **Implement the feature** with focused, testable code
4. **Export from `__init__.py`** for clean imports
5. **Update documentation** as needed

Example: Adding a new feature to core:

```python
# src/valyxo/core/myfeature.py
class MyFeature:
    def do_something(self):
        pass

# Update src/valyxo/core/__init__.py
from .myfeature import MyFeature
__all__ = [..., 'MyFeature']
```

## Import Examples

### Option 1: Import specific items
```python
from valyxo.core import Colors, ValyxoFileSystem, ROOT_DIR
```

### Option 2: Import from core
```python
from valyxo.core import ValyxoFileSystem
```

### Option 3: Import from package
```python
from valyxo import ValyxoFileSystem
```

### Option 4: Import module
```python
from valyxo.core import filesystem
fs = filesystem.ValyxoFileSystem(root_dir)
```

## Testing

To test the modular structure:

```bash
python test_imports.py
```

This verifies all modules import correctly and are properly configured.

---

**Valyxo v0.31** - Clean, modular, professional architecture.
