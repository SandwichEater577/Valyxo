#!/usr/bin/env python3
"""Valyxo v0.41 - Terminal Developer Ecosystem.

Professional development environment combining terminal CLI, AI assistance,
and scripting language. Powered by ValyxoScript and ValyxoGPT (Zencoder).

Architecture:
 - valyxo.core: Core modules and managers
   - colors: Terminal color codes
   - constants: Application configuration
   - utils: Utility functions
   - filesystem: File operations (ValyxoFileSystem)
   - gpt: AI Assistant (ValyxoGPTModule)
   - jobs: Job management (ValyxoJobsManager)
   - man: Help system (ValyxoManSystem)
 - valyxo.shell: Shell interface
 - valyxo.editor: Text editor

Key Features:
 - Modular architecture with comprehensive type hints
 - Full error handling with informative messages
 - ValyxoScript: Lightweight programming language
 - ValyxoGPT: AI-powered coding assistant
 - Professional terminal interface
"""

from valyxo.core import (
    Colors,
    color,
    DEFAULT_THEMES,
    APP_NAME,
    VERSION,
    HOME,
    ROOT_DIR,
    PROJECTS_DIR,
    SYSTEM_DIR,
    CONFIG_DIR,
    MAN_DIR,
    MAIN_PROJECT,
    CONFIG_PATH,
    THEMES_PATH,
    HISTORY_PATH,
    API_KEY_PATH,
    COMMANDS,
    LANG_MAP,
    DEFAULT_SETTINGS,
    prompt,
    path_within_root,
    normalize_virtual_path,
    highlight_valyxoscript,
    ValyxoFileSystem,
    ValyxoGPTModule,
    ValyxoJobsManager,
    ValyxoManSystem,
    get_startup_banner,
    get_welcome_message,
    get_section_header,
    get_info_banner,
)
from valyxo.script import ValyxoScriptRuntime

try:
    import readline
except ImportError:
    readline = None

try:
    import openai
except ImportError:
    openai = None


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

    def _load_settings(self):
        self.settings = DEFAULT_SETTINGS.copy()

    def run(self):
        print(get_startup_banner(self.settings))
        print(get_welcome_message(APP_NAME, "0.41", self.settings))
        print(get_info_banner("Type 'man Valyxo' for help or '-help' for commands", self.settings))


shell = None


def main():
    global shell
    shell = ValyxoShell()
    shell.initialize()
    shell.run()


if __name__ == "__main__":
    main()
