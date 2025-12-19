from typing import Optional
from .colors import Colors, color


VALYXO_LOGO = """
     ██    ██  █████  ██       █████  ██   ██  ██████  
     ██    ██ ██   ██ ██      ██   ██  ██ ██  ██    ██ 
     ██    ██ ███████ ██      ███████   ███   ██    ██ 
     ██    ██ ██   ██ ██      ██   ██   ██    ██    ██ 
      ██████  ██   ██ ███████ ██   ██   ██     ██████  
"""

VALYXOHUB_LOGO = """
  ██   ██ ██    ██ ██████  
  ██   ██ ██    ██ ██   ██ 
  ███████ ██    ██ ██████  
  ██   ██ ██    ██ ██   ██ 
  ██   ██  ██████  ██████  
"""

VALYXOSCRIPT_LOGO = """
   ███████ ██      ██████   ██████  ███████ ████████ 
   ██      ██     ██        ██      ██         ██    
   ███████ ██     ██   ███  ██   ███ ███████   ██    
        ██ ██     ██    ██  ██    ██      ██   ██    
   ███████ ███████  ██████   ██████  ███████   ██    
"""

VALYXOGPT_LOGO = """
   ██████  ██████  ████████ 
  ██       ██   ██    ██    
  ██   ███ ██████     ██    
  ██    ██ ██         ██    
   ██████  ██         ██    
"""

VALYXOAPP_LOGO = """
   █████  ██████  ██████  
  ██   ██ ██   ██ ██   ██ 
  ███████ ██████  ██████  
  ██   ██ ██      ██      
  ██   ██ ██      ██      
"""

COMPONENT_LOGOS = {
    "hub": VALYXOHUB_LOGO,
    "script": VALYXOSCRIPT_LOGO,
    "gpt": VALYXOGPT_LOGO,
    "app": VALYXOAPP_LOGO,
}

SEPARATOR = "=" * 60
THIN_SEPARATOR = "-" * 60
BANNER_SEPARATOR = "✦" * 20


def get_startup_banner(settings: Optional[dict] = None) -> str:
    """Get formatted startup banner with Valyxo logo.
    
    Args:
        settings: Settings dict with 'colors' boolean (default: True)
    
    Returns:
        Formatted startup banner string
    """
    logo = VALYXO_LOGO
    version_line = "    Version 0.5.1 | Powered by Zencoder AI"
    
    if settings and not settings.get("colors", True):
        return f"\n{logo}\n{version_line}\n"
    
    colored_logo = color(logo, Colors.ACCENT, settings)
    colored_version = color(version_line, Colors.BANNER, settings)
    return f"\n{colored_logo}\n{colored_version}\n"


def get_component_banner(component: str, settings: Optional[dict] = None) -> str:
    """Get component banner with ASCII art.
    
    Args:
        component: Component name (hub, script, gpt, app)
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Component banner string or empty if component not found
    """
    logo = COMPONENT_LOGOS.get(component.lower())
    if not logo:
        return ""
    
    if settings and not settings.get("colors", True):
        return f"\n{logo}\n"
    
    return f"\n{color(logo, Colors.ACCENT, settings)}\n"


def get_welcome_message(app_name: str = "Valyxo", version: str = "0.5.1", 
                       settings: Optional[dict] = None) -> str:
    """Get formatted welcome message.
    
    Args:
        app_name: Application name
        version: Version string
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Formatted welcome message
    """
    title = f"{app_name} v{version}"
    subtitle = "Complete Developer Ecosystem"
    
    if settings and not settings.get("colors", True):
        return f"\n{title}\n{subtitle}\n"
    
    colored_title = color(title, Colors.BANNER, settings)
    colored_subtitle = color(subtitle, Colors.TEXT, settings)
    return f"\n{colored_title}\n{colored_subtitle}\n"


def get_section_header(title: str, settings: Optional[dict] = None) -> str:
    """Get formatted section header.
    
    Args:
        title: Section title
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Formatted section header
    """
    if settings and not settings.get("colors", True):
        return f"\n{BANNER_SEPARATOR} {title} {BANNER_SEPARATOR}\n"
    
    sep = color(BANNER_SEPARATOR, Colors.ACCENT, settings)
    header = color(title, Colors.BANNER, settings)
    return f"\n{sep} {header} {sep}\n"


def get_error_banner(message: str, settings: Optional[dict] = None) -> str:
    """Get error message with banner styling.
    
    Args:
        message: Error message
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Formatted error banner
    """
    if settings and not settings.get("colors", True):
        return f"\n✗ {message}\n"
    
    symbol = color("✗", Colors.ERROR, settings)
    msg = color(message, Colors.ERROR, settings)
    return f"\n{symbol} {msg}\n"


def get_success_banner(message: str, settings: Optional[dict] = None) -> str:
    """Get success message with banner styling.
    
    Args:
        message: Success message
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Formatted success banner
    """
    if settings and not settings.get("colors", True):
        return f"\n✓ {message}\n"
    
    symbol = color("✓", Colors.GREEN, settings)
    msg = color(message, Colors.GREEN, settings)
    return f"\n{symbol} {msg}\n"


def get_info_banner(message: str, settings: Optional[dict] = None) -> str:
    """Get info message with banner styling.
    
    Args:
        message: Info message
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Formatted info banner
    """
    if settings and not settings.get("colors", True):
        return f"\n→ {message}\n"
    
    symbol = color("→", Colors.ACCENT, settings)
    msg = color(message, Colors.TEXT, settings)
    return f"\n{symbol} {msg}\n"


def get_bordered_text(text: str, settings: Optional[dict] = None) -> str:
    """Get text wrapped in border.
    
    Args:
        text: Text to border
        settings: Settings dict with 'colors' boolean
    
    Returns:
        Text wrapped in box border
    """
    border = "╭" + "─" * (len(text) + 2) + "╮"
    middle = "│ " + text + " │"
    end = "╰" + "─" * (len(text) + 2) + "╯"
    
    if settings and not settings.get("colors", True):
        return f"\n{border}\n{middle}\n{end}\n"
    
    colored_border = color(border, Colors.ACCENT, settings)
    colored_middle = color(middle, Colors.TEXT, settings)
    colored_end = color(end, Colors.ACCENT, settings)
    return f"\n{colored_border}\n{colored_middle}\n{colored_end}\n"
