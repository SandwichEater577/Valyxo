import os
from typing import Dict, List, Any

APP_NAME: str = "Valyxo"
VERSION: str = "Valyxo v0.6.0"

HOME: str = os.getcwd()
ROOT_FOLDER_NAME: str = os.path.join("Data", "ValyxoDocuments")
ROOT_DIR: str = os.path.join(HOME, ROOT_FOLDER_NAME)
PROJECTS_DIR: str = os.path.join(ROOT_DIR, "Projects")
SYSTEM_DIR: str = os.path.join(ROOT_DIR, "System")
CONFIG_DIR: str = os.path.join(ROOT_DIR, "Config")
MAN_DIR: str = os.path.join(SYSTEM_DIR, "man")
MAIN_PROJECT: str = os.path.join(PROJECTS_DIR, "Main")

CONFIG_PATH: str = os.path.join(CONFIG_DIR, "config.json")
THEMES_PATH: str = os.path.join(CONFIG_DIR, "themes.json")
HISTORY_PATH: str = os.path.join(SYSTEM_DIR, "history.txt")
API_KEY_PATH: str = os.path.join(CONFIG_DIR, "api_key.txt")

COMMANDS: List[str] = [
    "enter ValyxoScript",
    "enter VScript",
    "enter ValyxoGPT",
    "enter VGPT",
    "mkdir",
    "ls",
    "cd",
    "cat",
    "grep",
    "nano",
    "run",
    "jobs",
    "kill",
    "man",
    "theme",
    "python",
    "-help",
    "settings",
    "quit",
]

LANG_MAP: Dict[str, str] = {
    "vs": ".vs",
    "valyxoscript": ".vs",
    "valyx": ".vs",
    "vscript": ".vs",
    ".vs": ".vs",
    "js": ".js",
    "javascript": ".js",
    "node": ".js",
    ".js": ".js",
    "python": ".py",
    "py": ".py",
    ".py": ".py",
    "java": ".java",
    ".java": ".java",
}

DEFAULT_SETTINGS: Dict[str, Any] = {
    "suggestions": True,
    "colors": True,
    "start_cwd": MAIN_PROJECT,
    "remember_language": False,
    "theme": "neon",
    "debug": False
}
