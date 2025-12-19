from __future__ import annotations

import os
import shutil
from typing import Dict
import core.constants as const 
import utils.iohelpers as iohelpers


class ValyxoManSystem:
    def __init__(self):
        self.pages = self._default_pages()

    @staticmethod
    def _default_pages() -> Dict[str, Dict[str, str]]:
        return {
            "valyxoHub": {
                "COMMAND": "ValyxoHub",
                "HOWTO": (
                    "enter ValyxoScript | enter ValyxoGPT | mkdir | ls | cd | cat | grep | "
                    "nano | run | jobs | kill | man | settings | -help | quit"
                ),
                "EXAMPLE": (
                    "enter ValyxoScript\nmkdir Projects/Demo\ncd Projects/Demo\n"
                    "nano main.vs\nrun main.vs"
                ),
                "DESCRIPTION": (
                    "ValyxoHub is a terminal-based developer environment with ValyxoScript "
                    "language and ValyxoGPT assistant."
                ),
                "LANGUAGE": "System",
                "NOTES": "Files stored under ~/Projects/",
                "WARNINGS": "Do not upload ValyxoDocuments to public repos.",
                "SEE": "man ValyxoScript, man nano, man run"
            },
            "valyxoScript": {
                "COMMAND": "ValyxoScript",
                "HOWTO": (
                    "set <name> = <expr>\nprint <expr>\nif [cond] then [cmd] else [cmd]"
                    "\nvars\nexit"
                ),
                "EXAMPLE": (
                    "set x = 5\nprint x\nif [x < 10] then [print x] else [print \"no\"]"
                ),
                "DESCRIPTION": (
                    "ValyxoScript is the lightweight language used in ValyxoHub."
                ),
                "LANGUAGE": "ValyxoScript",
                "NOTES": "Expressions are evaluated safely using ast.",
                "WARNINGS": "Unknown variables raise errors.",
                "SEE": "man run, man nano"
            },
            # Keep additional pages as before; they will be exported when load_pages
            # runs
        }

    def load_pages(self) -> None:
        os.makedirs(const.MAN_DIR, exist_ok=True)
        for name, content in self.pages.items():
            filename = os.path.join(const.MAN_DIR, name.lower() + ".man")
            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self._format_manpage(content))

    def get_page(self, name: str) -> str:
        """Get a manual page by name.
        
        Args:
            name: The name of the manual page to retrieve
            
        Returns:
            The formatted manual page content, or None if not found
        """
        # First check in-memory pages
        key = name.lower()
        if key in self.pages:
            return self._format_manpage(self.pages[key])
        
        # Check for .man file
        filename = os.path.join(const.MAN_DIR, key + ".man")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        
        # Try without extension match
        for page_name in self.pages:
            if page_name.lower() == key:
                return self._format_manpage(self.pages[page_name])
        
        return None

    @staticmethod
    def _format_manpage(dic: Dict[str, str]) -> str:
        s = []
        s.append(f"COMMAND: {dic.get('COMMAND','')}\n")
        s.append("HOW TO USE:\n")
        s.append(f"{dic.get('HOWTO','')}\n\n")
        s.append("EXAMPLE:\n")
        s.append(f"{dic.get('EXAMPLE','')}\n\n")
        s.append("DESCRIPTION:\n")
        s.append(f"{dic.get('DESCRIPTION','')}\n\n")
        s.append("LANGUAGE:\n")
        s.append(f"{dic.get('LANGUAGE','')}\n\n")
        s.append("NOTES:\n")
        s.append(f"{dic.get('NOTES','')}\n\n")
        s.append("WARNINGS:\n")
        s.append(f"{dic.get('WARNINGS','')}\n\n")
        s.append("SEE ALSO:\n")
        s.append(f"{dic.get('SEE','')}\n")
        s.append(f"\nUpdated in {const.VERSION}\n")
        return "\n".join(s)

    @staticmethod
    def pager_display(text: str) -> None:
        rows, _ = shutil.get_terminal_size((80, 24))
        lines = text.splitlines()
        i = 0
        page = rows - 2
        while i < len(lines):
            chunk = lines[i:i+page]
            for ln in chunk:
                print(ln)
            i += page
            if i >= len(lines):
                break
            c = iohelpers.prompt(
                "--Press SPACE for next page, ENTER for one line, q to quit-- "
            )
            if c.lower() == "q":
                break
            if c == "":
                if i < len(lines):
                    print(lines[i])
                    i += 1
            else:
                continue
