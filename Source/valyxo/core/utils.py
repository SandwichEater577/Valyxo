import os
import re
from typing import Optional
from .colors import Colors


def prompt(text: str) -> str:
    """Read user input with interrupt handling.
    
    Args:
        text: Prompt message
    
    Returns:
        User input or empty string on interrupt/EOF
    """
    try:
        return input(text)
    except KeyboardInterrupt:
        print()
        return ""
    except EOFError:
        return ""


def path_within_root(path: str, root_dir: str) -> Optional[str]:
    """Validate path is within root directory.
    
    Args:
        path: Path to validate
        root_dir: Root directory
    
    Returns:
        Absolute path if valid, None if outside root or invalid
    """
    try:
        abs_path = os.path.abspath(path)
        abs_root = os.path.abspath(root_dir)
        common = os.path.commonpath([abs_path, abs_root])
        
        if common != abs_root:
            return None
        return abs_path
    except ValueError:
        return None


def normalize_virtual_path(abs_path: str, root_dir: str) -> str:
    """Convert absolute path to virtual path notation.
    
    Args:
        abs_path: Absolute path
        root_dir: Root directory
    
    Returns:
        Virtual path (e.g., ~/Projects/File.vs) or ~ if invalid
    """
    try:
        abs_root = os.path.abspath(root_dir)
        rel_path = os.path.relpath(abs_path, abs_root)
        
        if rel_path == ".":
            return "~"
        return os.path.join("~", rel_path).replace("\\", "/")
    except (ValueError, TypeError):
        return "~"


def highlight_valyxoscript(line: str) -> str:
    """Apply syntax highlighting to ValyxoScript line.
    
    Args:
        line: ValyxoScript code line
    
    Returns:
        Highlighted line with ANSI color codes
    """
    keywords = ["set", "print", "if", "then", "else", "func", "while", "for", "import", "in", "to"]
    keywords_regex = r'\b(' + '|'.join(keywords) + r')\b'
    
    highlighted = line
    highlighted = re.sub(keywords_regex, f"{Colors.ACCENT}\\1{Colors.RESET}", highlighted)
    highlighted = re.sub(r'"([^"]*)"', f'{Colors.TEXT}"\\1"{Colors.RESET}', highlighted)
    highlighted = re.sub(r"'([^']*)'", f"{Colors.TEXT}'\\1'{Colors.RESET}", highlighted)
    highlighted = re.sub(r'\b(True|False|None)\b', f"{Colors.ACCENT}\\1{Colors.RESET}", highlighted)
    return highlighted
