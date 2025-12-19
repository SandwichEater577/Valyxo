from .colors import Colors, color, DEFAULT_THEMES
from .constants import (
    APP_NAME, VERSION, HOME, ROOT_DIR, PROJECTS_DIR, SYSTEM_DIR,
    CONFIG_DIR, MAN_DIR, MAIN_PROJECT, CONFIG_PATH, THEMES_PATH,
    HISTORY_PATH, API_KEY_PATH, COMMANDS, LANG_MAP, DEFAULT_SETTINGS
)
from .utils import prompt, path_within_root, normalize_virtual_path, highlight_valyxoscript
from .filesystem import ValyxoFileSystem
from .gpt import ValyxoGPTModule
from .jobs import ValyxoJobsManager
from .man import ValyxoManSystem
from .branding import (
    VALYXO_LOGO, VALYXOHUB_LOGO, VALYXOSCRIPT_LOGO, VALYXOGPT_LOGO, VALYXOAPP_LOGO,
    SEPARATOR, THIN_SEPARATOR, BANNER_SEPARATOR,
    get_startup_banner, get_component_banner, get_welcome_message,
    get_section_header, get_error_banner, get_success_banner,
    get_info_banner, get_bordered_text
)

# v0.6.0 New Modules
from .plugins import ValyxoPlugin, ValyxoPluginManager, create_plugin_template
from .packages import ValyxoPackageManager, BUILTIN_PACKAGES
from .git import ValyxoGit
from .templates import list_templates, create_project, get_template_info, TEMPLATES
from .theme_editor import ValyxoTheme, ValyxoThemeManager, BUILTIN_THEMES
from .keybindings import ValyxoKeybindManager, Keybinding, DEFAULT_KEYBINDINGS
from .snippets import ValyxoSnippetManager, Snippet, BUILTIN_SNIPPETS
from .autocomplete import ValyxoAutoComplete, create_autocomplete
from .script_extensions import (
    ValyxoArray, ValyxoObject, ValyxoScriptExtensions, 
    BUILTIN_FUNCTIONS, integrate_extensions
)

__all__ = [
    # Existing exports
    'Colors', 'color', 'DEFAULT_THEMES',
    'APP_NAME', 'VERSION', 'HOME', 'ROOT_DIR', 'PROJECTS_DIR', 'SYSTEM_DIR',
    'CONFIG_DIR', 'MAN_DIR', 'MAIN_PROJECT', 'CONFIG_PATH', 'THEMES_PATH',
    'HISTORY_PATH', 'API_KEY_PATH', 'COMMANDS', 'LANG_MAP', 'DEFAULT_SETTINGS',
    'prompt', 'path_within_root', 'normalize_virtual_path', 'highlight_valyxoscript',
    'ValyxoFileSystem', 'ValyxoGPTModule', 'ValyxoJobsManager', 'ValyxoManSystem',
    'VALYXO_LOGO', 'VALYXOHUB_LOGO', 'VALYXOSCRIPT_LOGO', 'VALYXOGPT_LOGO', 'VALYXOAPP_LOGO',
    'SEPARATOR', 'THIN_SEPARATOR', 'BANNER_SEPARATOR',
    'get_startup_banner', 'get_component_banner', 'get_welcome_message',
    'get_section_header', 'get_error_banner', 'get_success_banner',
    'get_info_banner', 'get_bordered_text',
    
    # v0.6.0 New exports
    'ValyxoPlugin', 'ValyxoPluginManager', 'create_plugin_template',
    'ValyxoPackageManager', 'BUILTIN_PACKAGES',
    'ValyxoGit',
    'list_templates', 'create_project', 'get_template_info', 'TEMPLATES',
    'ValyxoTheme', 'ValyxoThemeManager', 'BUILTIN_THEMES',
    'ValyxoKeybindManager', 'Keybinding', 'DEFAULT_KEYBINDINGS',
    'ValyxoSnippetManager', 'Snippet', 'BUILTIN_SNIPPETS',
    'ValyxoAutoComplete', 'create_autocomplete',
    'ValyxoArray', 'ValyxoObject', 'ValyxoScriptExtensions',
    'BUILTIN_FUNCTIONS', 'integrate_extensions',
]
