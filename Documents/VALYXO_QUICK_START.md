# Valyxo - Developer Quick Start Guide

## Project Structure

```
src/
├── Valyxo.py                 ← Main entry point (91 lines)
└── valyxo/
    ├── __init__.py           ← Package exports
    └── core/                 ← Core modules
        ├── colors.py         ← Colors and themes (48 lines)
        ├── constants.py      ← Configuration (57 lines)
        ├── utils.py          ← Helper functions (46 lines)
        ├── filesystem.py     ← File operations (65 lines)
        ├── gpt.py            ← AI module (67 lines)
        ├── jobs.py           ← Job manager (40 lines)
        └── man.py            ← Help system (125 lines)
```

## Module Overview

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| **colors.py** | Color management | Colors, color() |
| **constants.py** | App configuration | COMMANDS, LANG_MAP, DEFAULT_SETTINGS |
| **utils.py** | Helper functions | prompt(), path_within_root() |
| **filesystem.py** | File operations | ValyxoFileSystem |
| **gpt.py** | AI assistant | ValyxoGPTModule |
| **jobs.py** | Process management | ValyxoJobsManager |
| **man.py** | Documentation | ValyxoManSystem |

## Common Imports

```python
# Import everything you need from core
from valyxo.core import (
    Colors, APP_NAME, VERSION,
    ValyxoFileSystem, ValyxoGPTModule,
    prompt, highlight_valyxoscript
)

# Or import specific modules
from valyxo.core import filesystem
fs = filesystem.ValyxoFileSystem(root_dir)

# Or import individual classes
from valyxo.core.filesystem import ValyxoFileSystem
from valyxo.core.gpt import ValyxoGPTModule
```

## Key Classes

### ValyxoFileSystem
```python
fs = ValyxoFileSystem(ROOT_DIR)
fs.ensure_dirs()
fs.set_cwd(path)
fs.create_file(cwd, filename)
```

### ValyxoGPTModule
```python
gpt = ValyxoGPTModule()
response = gpt.get_response("Your question here")
gpt.set_api_key(key)
```

### ValyxoJobsManager
```python
jobs = ValyxoJobsManager()
pid = jobs.create_job(filepath)
jobs.list_jobs()
jobs.stop_job(pid)
```

### ValyxoManSystem
```python
man = ValyxoManSystem()
man.load_pages()
man.pager_display(text)
```

## Adding New Code

### To add a new utility function:
1. Add function to `valyxo/core/utils.py`
2. Add to `__all__` in `valyxo/core/__init__.py`
3. Use: `from valyxo.core import your_function`

### To add a new class:
1. Create file: `valyxo/core/myfeature.py`
2. Define class: `class MyClass: ...`
3. Export in `valyxo/core/__init__.py`
4. Use: `from valyxo.core import MyClass`

### To add a new theme:
1. Edit `valyxo/core/colors.py`
2. Add to `DEFAULT_THEMES` dict
3. Use: `DEFAULT_THEMES["mytheme"]`

## Testing

Run the import test:
```bash
python test_imports.py
```

Expected output: All modules show `[OK]`

## File Size Summary

| File | Lines | Purpose |
|------|-------|---------|
| Valyxo.py | 91 | Entry point |
| colors.py | 48 | Colors/themes |
| constants.py | 57 | Configuration |
| utils.py | 46 | Helpers |
| filesystem.py | 65 | File ops |
| gpt.py | 67 | AI module |
| jobs.py | 40 | Job mgmt |
| man.py | 125 | Help system |
| **TOTAL** | **539** | **Core code** |

## Design Benefits

✓ **Modular** - Each file has one responsibility
✓ **Testable** - Components test independently
✓ **Scalable** - Easy to add new features
✓ **Maintainable** - Clear organization
✓ **Professional** - Industry-standard structure

## Next Steps

1. Review `VALYXO_ARCHITECTURE.md` for detailed documentation
2. Explore each module in `src/valyxo/core/`
3. Run `python test_imports.py` to verify setup
4. Start integrating features using the clean import system

---

**Valyxo v0.31** - Clean, modular, production-ready code.
