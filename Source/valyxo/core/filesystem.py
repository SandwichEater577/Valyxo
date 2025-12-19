import os
from typing import Optional
from .constants import PROJECTS_DIR, SYSTEM_DIR, CONFIG_DIR, MAIN_PROJECT, MAN_DIR, LANG_MAP
from .utils import prompt, path_within_root


class ValyxoFileSystem:
    """File system manager for ValyxoHub.
    
    Handles directory structure, file creation, and path validation within
    the designated root directory.
    """

    def __init__(self, root_dir: str) -> None:
        """Initialize file system manager.
        
        Args:
            root_dir: Root directory for all operations
        """
        self.cwd: Optional[str] = None
        self.active_file: Optional[str] = None
        self.root_dir = root_dir

    def set_cwd(self, path: str) -> None:
        """Set current working directory.
        
        Args:
            path: Directory path to set
        """
        self.cwd = path

    def set_active_file(self, filename: str) -> None:
        """Set active file for editing.
        
        Args:
            filename: File path
        """
        self.active_file = filename

    def ensure_dirs(self) -> None:
        """Create all necessary system directories."""
        for directory in [PROJECTS_DIR, SYSTEM_DIR, CONFIG_DIR, MAIN_PROJECT, MAN_DIR]:
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory {directory}: {e}")

    def create_file(self, cwd: str, filename: str, ask_lang: bool = True) -> Optional[str]:
        """Create a new file with appropriate extension.
        
        Args:
            cwd: Current working directory
            filename: File name (with or without extension)
            ask_lang: Ask user for language if no extension
        
        Returns:
            Absolute path to created file, or None if path invalid
        """
        try:
            if "." in filename:
                return self._create_with_extension(cwd, filename)
            return self._create_with_language(cwd, filename, ask_lang)
        except OSError as e:
            print(f"Error creating file: {e}")
            return None

    def _create_with_extension(self, cwd: str, filename: str) -> Optional[str]:
        """Create file with explicit extension.
        
        Args:
            cwd: Current working directory
            filename: File name with extension
        
        Returns:
            Absolute path or None if invalid
        """
        path = os.path.join(cwd, filename)
        path = path_within_root(path, self.root_dir)
        
        if not path:
            return None
        
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
        return path

    def _create_with_language(self, cwd: str, filename: str, ask_lang: bool) -> Optional[str]:
        """Create file with language-determined extension.
        
        Args:
            cwd: Current working directory
            filename: File name without extension
            ask_lang: Ask user for language
        
        Returns:
            Absolute path or None if invalid
        """
        ext = self.ask_language(filename) if ask_lang else ".vs"
        if not ext:
            ext = ".vs"
        
        full_filename = filename + ext
        path = os.path.join(cwd, full_filename)
        path = path_within_root(path, self.root_dir)
        
        if not path:
            return None
        
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
        return path

    @staticmethod
    def ask_language(base_name: str) -> str:
        """Prompt user for programming language.
        
        Args:
            base_name: File name for context in prompt
        
        Returns:
            File extension (e.g., '.vs', '.js', '.py')
        """
        prompt_msg = f"Language for {base_name}? (default: VS) [VS|JS|Python|Java]: "
        supported = sorted(set(LANG_MAP.values()))
        
        while True:
            ans = prompt(prompt_msg).strip()
            
            if not ans:
                return ".vs"
            
            normalized = ans.lower().strip().lstrip(".")
            ext = LANG_MAP.get(normalized)
            
            if ext:
                return ext
            
            for key, value in LANG_MAP.items():
                if key.lower() == normalized:
                    return value
            
            print(f"Unknown language. Supported: {', '.join(supported)}")
