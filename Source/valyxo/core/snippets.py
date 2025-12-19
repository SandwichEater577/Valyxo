"""Valyxo Code Snippets v0.6.0

Save and reuse code blocks with expansion.

Usage:
    snippet list                      List all snippets
    snippet add <name>                Add new snippet (interactive)
    snippet edit <name>               Edit a snippet
    snippet delete <name>             Delete a snippet
    snippet use <name>                Insert a snippet
    snippet export                    Export snippets
    snippet import <file>             Import snippets
    snippet search <query>            Search snippets
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Snippet:
    """A code snippet with metadata."""
    name: str  # Short name for quick access
    prefix: str  # Trigger for expansion
    body: str  # The actual code
    description: str = ""
    language: str = "any"  # Language hint
    tags: List[str] = None
    placeholders: Dict[str, str] = None  # ${1:default}, ${2:name}
    created_at: str = ""
    updated_at: str = ""
    use_count: int = 0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.placeholders is None:
            self.placeholders = {}
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Snippet":
        return cls(**data)
    
    def expand(self, variables: Dict[str, str] = None) -> str:
        """Expand the snippet with given variables."""
        result = self.body
        
        # Replace placeholders with defaults or provided values
        if variables:
            for key, value in variables.items():
                result = result.replace(f"${{{key}}}", value)
        
        # Replace remaining placeholders with their defaults
        import re
        pattern = r'\$\{(\d+):([^}]+)\}'
        
        def replace_placeholder(match):
            num = match.group(1)
            default = match.group(2)
            if variables and num in variables:
                return variables[num]
            return default
        
        result = re.sub(pattern, replace_placeholder, result)
        
        # Remove simple ${n} placeholders
        result = re.sub(r'\$\{\d+\}', '', result)
        
        return result


# Built-in snippets
BUILTIN_SNIPPETS: Dict[str, Snippet] = {
    # Python
    "pydef": Snippet(
        name="pydef",
        prefix="def",
        body='def ${1:function_name}(${2:args}):\n    """${3:Description}"""\n    ${4:pass}',
        description="Python function definition",
        language="python",
        tags=["python", "function"]
    ),
    "pyclass": Snippet(
        name="pyclass",
        prefix="class",
        body='class ${1:ClassName}:\n    """${2:Description}"""\n    \n    def __init__(self, ${3:args}):\n        ${4:pass}',
        description="Python class definition",
        language="python",
        tags=["python", "class", "oop"]
    ),
    "pymain": Snippet(
        name="pymain",
        prefix="main",
        body='def main():\n    ${1:pass}\n\n\nif __name__ == "__main__":\n    main()',
        description="Python main entry point",
        language="python",
        tags=["python", "main"]
    ),
    "pytry": Snippet(
        name="pytry",
        prefix="try",
        body='try:\n    ${1:pass}\nexcept ${2:Exception} as e:\n    ${3:print(f"Error: {e}")}',
        description="Python try-except block",
        language="python",
        tags=["python", "error", "exception"]
    ),
    "pywith": Snippet(
        name="pywith",
        prefix="with",
        body='with ${1:open("file.txt")} as ${2:f}:\n    ${3:pass}',
        description="Python with statement",
        language="python",
        tags=["python", "context"]
    ),
    
    # JavaScript
    "jsfunction": Snippet(
        name="jsfunction",
        prefix="fn",
        body='function ${1:name}(${2:params}) {\n    ${3:// body}\n}',
        description="JavaScript function",
        language="javascript",
        tags=["javascript", "function"]
    ),
    "jsarrow": Snippet(
        name="jsarrow",
        prefix="arrow",
        body='const ${1:name} = (${2:params}) => {\n    ${3:// body}\n};',
        description="JavaScript arrow function",
        language="javascript",
        tags=["javascript", "function", "arrow"]
    ),
    "jsclass": Snippet(
        name="jsclass",
        prefix="class",
        body='class ${1:ClassName} {\n    constructor(${2:params}) {\n        ${3:// constructor}\n    }\n}',
        description="JavaScript class",
        language="javascript",
        tags=["javascript", "class", "oop"]
    ),
    "jsasync": Snippet(
        name="jsasync",
        prefix="async",
        body='async function ${1:name}(${2:params}) {\n    try {\n        ${3:// body}\n    } catch (error) {\n        console.error(error);\n    }\n}',
        description="JavaScript async function",
        language="javascript",
        tags=["javascript", "async", "function"]
    ),
    "jsfetch": Snippet(
        name="jsfetch",
        prefix="fetch",
        body='const response = await fetch("${1:url}");\nconst data = await response.json();',
        description="JavaScript fetch request",
        language="javascript",
        tags=["javascript", "fetch", "api"]
    ),
    
    # React
    "reactfc": Snippet(
        name="reactfc",
        prefix="rfc",
        body='function ${1:Component}({ ${2:props} }) {\n    return (\n        <div>\n            ${3:content}\n        </div>\n    );\n}\n\nexport default ${1:Component};',
        description="React functional component",
        language="javascript",
        tags=["react", "component", "javascript"]
    ),
    "reactstate": Snippet(
        name="reactstate",
        prefix="useState",
        body='const [${1:state}, set${1/(.*)/${1:/capitalize}/}] = useState(${2:initial});',
        description="React useState hook",
        language="javascript",
        tags=["react", "hooks", "state"]
    ),
    "reacteffect": Snippet(
        name="reacteffect",
        prefix="useEffect",
        body='useEffect(() => {\n    ${1:// effect}\n    \n    return () => {\n        ${2:// cleanup}\n    };\n}, [${3:dependencies}]);',
        description="React useEffect hook",
        language="javascript",
        tags=["react", "hooks", "effect"]
    ),
    
    # HTML
    "html5": Snippet(
        name="html5",
        prefix="html",
        body='<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>${1:Document}</title>\n</head>\n<body>\n    ${2}\n</body>\n</html>',
        description="HTML5 boilerplate",
        language="html",
        tags=["html", "boilerplate"]
    ),
    "htmlform": Snippet(
        name="htmlform",
        prefix="form",
        body='<form action="${1:#}" method="${2:post}">\n    <label for="${3:input}">${4:Label}</label>\n    <input type="${5:text}" id="${3:input}" name="${3:input}">\n    <button type="submit">${6:Submit}</button>\n</form>',
        description="HTML form",
        language="html",
        tags=["html", "form"]
    ),
    
    # CSS
    "cssflex": Snippet(
        name="cssflex",
        prefix="flex",
        body='display: flex;\njustify-content: ${1:center};\nalign-items: ${2:center};',
        description="CSS flexbox",
        language="css",
        tags=["css", "flex", "layout"]
    ),
    "cssgrid": Snippet(
        name="cssgrid",
        prefix="grid",
        body='display: grid;\ngrid-template-columns: ${1:repeat(3, 1fr)};\ngap: ${2:1rem};',
        description="CSS grid",
        language="css",
        tags=["css", "grid", "layout"]
    ),
    
    # ValyxoScript
    "vsfunc": Snippet(
        name="vsfunc",
        prefix="func",
        body='func ${1:name}(${2:args}) {\n    ${3:# body}\n}',
        description="ValyxoScript function",
        language="valyxoscript",
        tags=["valyxoscript", "function"]
    ),
    "vsloop": Snippet(
        name="vsloop",
        prefix="loop",
        body='loop ${1:i} from ${2:1} to ${3:10} {\n    ${4:# body}\n}',
        description="ValyxoScript loop",
        language="valyxoscript",
        tags=["valyxoscript", "loop"]
    ),
    "vsif": Snippet(
        name="vsif",
        prefix="if",
        body='if ${1:condition} {\n    ${2:# then}\n} else {\n    ${3:# else}\n}',
        description="ValyxoScript if-else",
        language="valyxoscript",
        tags=["valyxoscript", "conditional"]
    ),
    
    # Shell/Bash
    "shebang": Snippet(
        name="shebang",
        prefix="#!/",
        body='#!/usr/bin/env ${1:bash}\n\n${2:# Script}',
        description="Shell shebang",
        language="bash",
        tags=["bash", "shell"]
    ),
    "shfunction": Snippet(
        name="shfunction",
        prefix="fn",
        body='${1:function_name}() {\n    ${2:# body}\n}',
        description="Shell function",
        language="bash",
        tags=["bash", "shell", "function"]
    ),
    "shif": Snippet(
        name="shif",
        prefix="if",
        body='if [ ${1:condition} ]; then\n    ${2:# then}\nelse\n    ${3:# else}\nfi',
        description="Shell if-else",
        language="bash",
        tags=["bash", "shell", "conditional"]
    ),
    "shfor": Snippet(
        name="shfor",
        prefix="for",
        body='for ${1:item} in ${2:items}; do\n    ${3:# body}\ndone',
        description="Shell for loop",
        language="bash",
        tags=["bash", "shell", "loop"]
    ),
}


class ValyxoSnippetManager:
    """Manages code snippets."""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".valyxo")
        self.config_dir = config_dir
        self.snippets_file = os.path.join(config_dir, "snippets.json")
        os.makedirs(config_dir, exist_ok=True)
        
        self.snippets: Dict[str, Snippet] = {}
        self._load_snippets()
    
    def _load_snippets(self):
        """Load snippets from file and builtins."""
        # Load builtins
        for name, snippet in BUILTIN_SNIPPETS.items():
            self.snippets[name] = snippet
        
        # Override with custom
        if os.path.exists(self.snippets_file):
            try:
                with open(self.snippets_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for snippet_data in data.get("snippets", []):
                        snippet = Snippet.from_dict(snippet_data)
                        self.snippets[snippet.name] = snippet
            except:
                pass
    
    def _save_snippets(self):
        """Save custom snippets to file."""
        custom = []
        for name, snippet in self.snippets.items():
            if name not in BUILTIN_SNIPPETS:
                custom.append(snippet.to_dict())
        
        data = {"snippets": custom}
        with open(self.snippets_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def list_snippets(self, language: str = None, tag: str = None) -> List[Snippet]:
        """List snippets, optionally filtered."""
        result = []
        for snippet in self.snippets.values():
            if language and snippet.language != language and snippet.language != "any":
                continue
            if tag and tag not in snippet.tags:
                continue
            result.append(snippet)
        return sorted(result, key=lambda x: x.name)
    
    def get_snippet(self, name: str) -> Optional[Snippet]:
        """Get a snippet by name or prefix."""
        # Try exact name match
        if name in self.snippets:
            return self.snippets[name]
        
        # Try prefix match
        for snippet in self.snippets.values():
            if snippet.prefix == name:
                return snippet
        
        return None
    
    def add_snippet(self, name: str, prefix: str, body: str, 
                    description: str = "", language: str = "any",
                    tags: List[str] = None) -> str:
        """Add a new snippet."""
        if name in BUILTIN_SNIPPETS:
            return f"✗ Cannot overwrite builtin snippet: {name}"
        
        snippet = Snippet(
            name=name,
            prefix=prefix,
            body=body,
            description=description,
            language=language,
            tags=tags or []
        )
        
        self.snippets[name] = snippet
        self._save_snippets()
        return f"✓ Added snippet: {name}"
    
    def edit_snippet(self, name: str, changes: Dict[str, Any]) -> str:
        """Edit an existing snippet."""
        if name in BUILTIN_SNIPPETS and name not in self._get_custom_names():
            # Copy builtin to custom before editing
            snippet = Snippet(**BUILTIN_SNIPPETS[name].to_dict())
        elif name in self.snippets:
            snippet = self.snippets[name]
        else:
            return f"✗ Snippet not found: {name}"
        
        # Apply changes
        for key, value in changes.items():
            if hasattr(snippet, key):
                setattr(snippet, key, value)
        
        snippet.updated_at = datetime.now().isoformat()
        self.snippets[name] = snippet
        self._save_snippets()
        return f"✓ Updated snippet: {name}"
    
    def _get_custom_names(self) -> List[str]:
        """Get names of custom snippets only."""
        if os.path.exists(self.snippets_file):
            try:
                with open(self.snippets_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [s["name"] for s in data.get("snippets", [])]
            except:
                pass
        return []
    
    def delete_snippet(self, name: str) -> str:
        """Delete a custom snippet."""
        if name in BUILTIN_SNIPPETS and name not in self._get_custom_names():
            return f"✗ Cannot delete builtin snippet: {name}"
        
        if name not in self.snippets:
            return f"✗ Snippet not found: {name}"
        
        del self.snippets[name]
        self._save_snippets()
        
        # Reload builtins if we deleted an override
        if name in BUILTIN_SNIPPETS:
            self.snippets[name] = BUILTIN_SNIPPETS[name]
        
        return f"✓ Deleted snippet: {name}"
    
    def use_snippet(self, name: str, variables: Dict[str, str] = None) -> Optional[str]:
        """Get expanded snippet content."""
        snippet = self.get_snippet(name)
        if snippet is None:
            return None
        
        # Increment use count
        snippet.use_count += 1
        if name not in BUILTIN_SNIPPETS:
            self._save_snippets()
        
        return snippet.expand(variables)
    
    def search_snippets(self, query: str) -> List[Snippet]:
        """Search snippets by name, prefix, description, or tags."""
        query = query.lower()
        results = []
        
        for snippet in self.snippets.values():
            score = 0
            
            if query in snippet.name.lower():
                score += 3
            if query in snippet.prefix.lower():
                score += 3
            if query in snippet.description.lower():
                score += 2
            if any(query in tag.lower() for tag in snippet.tags):
                score += 1
            if query in snippet.body.lower():
                score += 1
            
            if score > 0:
                results.append((score, snippet))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in results]
    
    def export_snippets(self, output_path: str = None, include_builtins: bool = False) -> str:
        """Export snippets to file."""
        if output_path is None:
            output_path = "valyxo-snippets.json"
        
        snippets_data = []
        for name, snippet in self.snippets.items():
            if include_builtins or name not in BUILTIN_SNIPPETS:
                snippets_data.append(snippet.to_dict())
        
        data = {"snippets": snippets_data}
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return f"✓ Exported {len(snippets_data)} snippets to: {output_path}"
    
    def import_snippets(self, file_path: str, overwrite: bool = False) -> str:
        """Import snippets from file."""
        if not os.path.exists(file_path):
            return f"✗ File not found: {file_path}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            count = 0
            skipped = 0
            
            for snippet_data in data.get("snippets", []):
                snippet = Snippet.from_dict(snippet_data)
                
                if snippet.name in self.snippets and not overwrite:
                    skipped += 1
                    continue
                
                if snippet.name in BUILTIN_SNIPPETS and not overwrite:
                    skipped += 1
                    continue
                
                self.snippets[snippet.name] = snippet
                count += 1
            
            self._save_snippets()
            msg = f"✓ Imported {count} snippets"
            if skipped > 0:
                msg += f" (skipped {skipped} existing)"
            return msg
            
        except Exception as e:
            return f"✗ Failed to import: {e}"
    
    def format_snippets(self, language: str = None) -> str:
        """Format snippets for display."""
        snippets = self.list_snippets(language=language)
        
        if not snippets:
            return "No snippets found"
        
        lines = ["╭─ Snippets ─╮"]
        
        current_lang = None
        for s in sorted(snippets, key=lambda x: (x.language, x.name)):
            if s.language != current_lang:
                current_lang = s.language
                lines.append(f"├─ {current_lang.upper()} ─┤")
            
            desc = s.description[:30] if s.description else ""
            lines.append(f"│  {s.prefix:<10} {s.name:<15} {desc}")
        
        lines.append("╰─────────────╯")
        return "\n".join(lines)
    
    def format_snippet(self, name: str) -> str:
        """Format a single snippet for display."""
        snippet = self.get_snippet(name)
        if snippet is None:
            return f"✗ Snippet not found: {name}"
        
        lines = [
            f"╭─ {snippet.name} ─╮",
            f"│ Prefix: {snippet.prefix}",
            f"│ Language: {snippet.language}",
            f"│ Description: {snippet.description}",
            f"│ Tags: {', '.join(snippet.tags)}",
            f"├─ Body ─┤",
        ]
        
        for line in snippet.body.split('\n'):
            lines.append(f"│ {line}")
        
        lines.append("╰──────────╯")
        return "\n".join(lines)
