from typing import Optional, Dict, Any


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    PROMPT = GREEN
    BANNER = GREEN
    TEXT = GREEN
    ERROR = RED
    ACCENT = CYAN


def color(txt: str, code: str, settings: Optional[Dict[str, Any]] = None) -> str:
    """Apply ANSI color code to text.
    
    Args:
        txt: Text to colorize
        code: ANSI color code
        settings: Settings dict with 'colors' boolean (default: True)
    
    Returns:
        Colorized text or plain text if colors disabled
    """
    if settings and not settings.get("colors", True):
        return txt
    return f"{code}{txt}{Colors.RESET}"


DEFAULT_THEMES = {
    "neon": {
        "prompt": "\033[92m",
        "banner": "\033[92m",
        "text": "\033[92m",
        "error": "\033[91m",
        "accent": "\033[96m"
    },
    "classic": {
        "prompt": "\033[97m",
        "banner": "\033[97m",
        "text": "\033[97m",
        "error": "\033[91m",
        "accent": "\033[93m"
    },
    "hacker": {
        "prompt": "\033[32m",
        "banner": "\033[32m",
        "text": "\033[32m",
        "error": "\033[91m",
        "accent": "\033[33m"
    },
    "ocean": {
        "prompt": "\033[36m",
        "banner": "\033[36m",
        "text": "\033[36m",
        "error": "\033[91m",
        "accent": "\033[94m"
    }
}
