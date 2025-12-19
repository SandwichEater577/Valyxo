import os
import shutil
from typing import Dict
from .constants import MAN_DIR
from .utils import prompt


class ValyxoManSystem:
    """Manual pages system for Valyxo.
    
    Manages help documentation and command references with paged display.
    """

    def __init__(self) -> None:
        """Initialize manual system with default pages."""
        self.pages: Dict[str, Dict[str, str]] = self._default_pages()

    @staticmethod
    def _default_pages() -> Dict[str, Dict[str, str]]:
        """Get default manual pages.
        
        Returns:
            Dictionary of manual page names and content
        """
        return {
            "valyxoHub": {
                "COMMAND": "Valyxo",
                "HOWTO": "enter ValyxoScript | enter ValyxoGPT | mkdir | ls | cd | cat | grep | nano | run | jobs | kill | man | settings | -help | quit",
                "EXAMPLE": "enter ValyxoScript\nmkdir Projects/Demo\ncd Projects/Demo\nnano main.vs\nrun main.vs",
                "DESCRIPTION": "Valyxo is a terminal-based developer environment with ValyxoScript language and ValyxoGPT assistant.",
                "LANGUAGE": "System",
                "NOTES": "Files stored under ~/Projects/",
                "WARNINGS": "Do not upload ValyxoDocuments to public repos.",
                "SEE": "man ValyxoScript, man nano, man run"
            },
            "valyxoscript": {
                "COMMAND": "ValyxoScript",
                "HOWTO": "set <name> = <expr>\nprint <expr>\nif [cond] then [cmd] else [cmd]\nvars\nexit",
                "EXAMPLE": "set x = 5\nprint x\nif [x < 10] then [print x] else [print \"no\"]",
                "DESCRIPTION": "ValyxoScript is the lightweight language used in Valyxo.",
                "LANGUAGE": "ValyxoScript",
                "NOTES": "Expressions are evaluated safely using ast.",
                "WARNINGS": "Unknown variables raise errors.",
                "SEE": "man run, man nano"
            },
            "nano": {
                "COMMAND": "nano",
                "HOWTO": "nano [filename]",
                "EXAMPLE": "nano main.vs",
                "DESCRIPTION": "ValyxoScript-based file editor.",
                "LANGUAGE": "Editor",
                "NOTES": "Default language is VS (.vs).",
                "WARNINGS": "quit discards changes.",
                "SEE": "man ValyxoScript, man run"
            },
            "run": {
                "COMMAND": "run",
                "HOWTO": "run <filename> [&]",
                "EXAMPLE": "run main.vs\nrun worker.vs &",
                "DESCRIPTION": "Execute a ValyxoScript file. '&' launches as background job.",
                "LANGUAGE": "System",
                "NOTES": "Background jobs cannot accept interactive input.",
                "WARNINGS": "Long-running jobs must be killed with kill <id>.",
                "SEE": "man jobs, man nano"
            },
            "theme": {
                "COMMAND": "theme",
                "HOWTO": "theme list\ntheme set <name>",
                "EXAMPLE": "theme list\ntheme set hacker\ntheme set neon",
                "DESCRIPTION": "Manage Valyxo color themes.",
                "LANGUAGE": "System",
                "NOTES": "Available themes: neon, classic, hacker, ocean.",
                "WARNINGS": "Theme changes apply immediately.",
                "SEE": "man settings, man Valyxo"
            },
            "python": {
                "COMMAND": "python",
                "HOWTO": "python",
                "EXAMPLE": "python\n>>> x = 42\n>>> print(x)\n>>> exit()",
                "DESCRIPTION": "Launch embedded Python interactive console.",
                "LANGUAGE": "System",
                "NOTES": "Full access to Python stdlib.",
                "WARNINGS": "Use exit() not Ctrl+C to exit.",
                "SEE": "man enter ValyxoScript, man run"
            }
        }

    def load_pages(self) -> None:
        """Load manual pages to disk if they don't exist."""
        try:
            os.makedirs(MAN_DIR, exist_ok=True)
        except OSError as e:
            print(f"Error creating man directory: {e}")
            return
        
        for name, content in self.pages.items():
            filename = os.path.join(MAN_DIR, name.lower() + ".man")
            if os.path.exists(filename):
                continue
            
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self._format_manpage(content))
            except (OSError, IOError) as e:
                print(f"Error writing manual page {name}: {e}")

    @staticmethod
    def _format_manpage(data: Dict[str, str]) -> str:
        """Format manual page content.
        
        Args:
            data: Manual page data dictionary
        
        Returns:
            Formatted manual page string
        """
        command = data.get("COMMAND", "")
        
        ascii_headers = {
            "Valyxo": "  ██    ██  █████  ██       █████  ██   ██  ██████  \n" +
                     "  ██    ██ ██   ██ ██      ██   ██  ██ ██  ██    ██ \n" +
                     "  ██    ██ ███████ ██      ███████   ███   ██    ██ \n" +
                     "  ██    ██ ██   ██ ██      ██   ██   ██    ██    ██ \n" +
                     "   ██████  ██   ██ ███████ ██   ██   ██     ██████  ",
            "ValyxoScript": "   ███████ ██      ██████   ██████  ███████ ████████ \n" +
                          "   ██      ██     ██        ██      ██         ██    \n" +
                          "   ███████ ██     ██   ███  ██   ███ ███████   ██    \n" +
                          "        ██ ██     ██    ██  ██    ██      ██   ██    \n" +
                          "   ███████ ███████  ██████   ██████  ███████   ██    ",
        }
        
        header = ascii_headers.get(command, "")
        
        sections = [
            ("COMMAND", data.get("COMMAND", "")),
            ("HOW TO USE", data.get("HOWTO", "")),
            ("EXAMPLE", data.get("EXAMPLE", "")),
            ("DESCRIPTION", data.get("DESCRIPTION", "")),
            ("LANGUAGE", data.get("LANGUAGE", "")),
            ("NOTES", data.get("NOTES", "")),
            ("WARNINGS", data.get("WARNINGS", "")),
            ("SEE ALSO", data.get("SEE", ""))
        ]
        
        lines = []
        if header:
            lines.append(header)
            lines.append("\n" + "=" * 60 + "\n")
        
        for section_name, section_content in sections:
            lines.append(f"{section_name}:")
            lines.append(f"{section_content}\n")
        
        return "\n".join(lines)

    @staticmethod
    def pager_display(text: str) -> None:
        """Display text in paginated format.
        
        Args:
            text: Text to display
        """
        rows, _ = shutil.get_terminal_size((80, 24))
        lines = text.splitlines()
        
        if not lines:
            return
        
        lines_per_page = max(rows - 2, 1)
        i = 0
        
        while i < len(lines):
            chunk = lines[i:i + lines_per_page]
            for line in chunk:
                print(line)
            
            i += lines_per_page
            
            if i >= len(lines):
                break
            
            response = prompt("--Press SPACE for next, ENTER for one line, q to quit--: ")
            
            if response.lower() == "q":
                break
            elif response == "":
                if i < len(lines):
                    print(lines[i])
                    i += 1
