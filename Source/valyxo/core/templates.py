"""Valyxo Project Templates v0.6.0

Create projects from templates with a single command.

Usage:
    valyxo create <template> <project_name>

Templates:
    python          Python project with setup.py
    node            Node.js project with package.json
    react           React application
    flask           Flask web application
    express         Express.js API server
    valyxoscript    ValyxoScript project
    html            Static HTML/CSS/JS website
    cli             Command-line tool template
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


TEMPLATES: Dict[str, Dict[str, Any]] = {
    "python": {
        "name": "Python Project",
        "description": "Python project with modern structure",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""Main entry point for {project_name}."""


def main():
    """Main function."""
    print("Hello from {project_name}!")


if __name__ == "__main__":
    main()
''',
            "requirements.txt": '''# Project dependencies
# Add your dependencies here
''',
            "setup.py": '''from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    author="",
    description="{project_name} - A Python project",
)
''',
            "README.md": '''# {project_name}

A Python project created with Valyxo.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## License

MIT
''',
            ".gitignore": '''__pycache__/
*.py[cod]
*$py.class
.env
.venv
venv/
*.egg-info/
dist/
build/
.pytest_cache/
'''
        },
        "folders": ["src", "tests"]
    },
    
    "node": {
        "name": "Node.js Project",
        "description": "Node.js project with npm",
        "files": {
            "index.js": '''/**
 * Main entry point for {project_name}
 */

function main() {{
    console.log("Hello from {project_name}!");
}}

main();

module.exports = {{ main }};
''',
            "package.json": '''{
    "name": "{project_name_lower}",
    "version": "1.0.0",
    "description": "{project_name} - A Node.js project",
    "main": "index.js",
    "scripts": {
        "start": "node index.js",
        "test": "echo \\"No tests yet\\""
    },
    "keywords": [],
    "author": "",
    "license": "MIT"
}
''',
            "README.md": '''# {project_name}

A Node.js project created with Valyxo.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

## License

MIT
''',
            ".gitignore": '''node_modules/
.env
.DS_Store
*.log
dist/
'''
        },
        "folders": ["src", "tests"]
    },
    
    "react": {
        "name": "React Application",
        "description": "React app with Vite",
        "files": {
            "index.html": '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''',
            "package.json": '''{
    "name": "{project_name_lower}",
    "private": true,
    "version": "0.0.0",
    "type": "module",
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "devDependencies": {
        "@vitejs/plugin-react": "^4.0.0",
        "vite": "^5.0.0"
    }
}
''',
            "vite.config.js": '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
})
''',
            "src/main.jsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
''',
            "src/App.jsx": '''import { useState } from 'react'

function App() {{
    const [count, setCount] = useState(0)

    return (
        <div className="app">
            <h1>{project_name}</h1>
            <p>Count: {{count}}</p>
            <button onClick={{() => setCount(c => c + 1)}}>
                Increment
            </button>
        </div>
    )
}}

export default App
''',
            "src/index.css": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.app {
    text-align: center;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

button {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 1rem;
}

button:hover {
    background: #2563eb;
}
''',
            "README.md": '''# {project_name}

A React application created with Valyxo.

## Getting Started

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## License

MIT
''',
            ".gitignore": '''node_modules/
dist/
.env
.DS_Store
'''
        },
        "folders": ["src", "public"]
    },
    
    "flask": {
        "name": "Flask Web Application",
        "description": "Flask API/web app",
        "files": {
            "app.py": '''"""Flask application for {project_name}."""

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="{project_name}")


@app.route("/api/hello")
def hello():
    return jsonify({{"message": "Hello from {project_name}!"}})


if __name__ == "__main__":
    app.run(debug=True)
''',
            "requirements.txt": '''flask>=2.0.0
python-dotenv>=1.0.0
''',
            "templates/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>{project_name}</h1>
        <p>Your Flask application is running!</p>
    </div>
</body>
</html>
''',
            "static/style.css": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    text-align: center;
}
''',
            "README.md": '''# {project_name}

A Flask web application created with Valyxo.

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Visit http://localhost:5000

## License

MIT
''',
            ".gitignore": '''__pycache__/
*.py[cod]
.env
venv/
instance/
'''
        },
        "folders": ["templates", "static"]
    },
    
    "express": {
        "name": "Express.js API",
        "description": "Express.js REST API server",
        "files": {
            "server.js": '''/**
 * Express.js server for {project_name}
 */

const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {{
    res.json({{ message: 'Welcome to {project_name} API' }});
}});

app.get('/api/hello', (req, res) => {{
    res.json({{ message: 'Hello from {project_name}!' }});
}});

// Start server
app.listen(PORT, () => {{
    console.log(`Server running on http://localhost:${{PORT}}`);
}});
''',
            "package.json": '''{
    "name": "{project_name_lower}",
    "version": "1.0.0",
    "description": "{project_name} - Express.js API",
    "main": "server.js",
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js"
    },
    "dependencies": {
        "cors": "^2.8.5",
        "express": "^4.18.2"
    },
    "devDependencies": {
        "nodemon": "^3.0.1"
    }
}
''',
            "README.md": '''# {project_name}

An Express.js API created with Valyxo.

## Installation

```bash
npm install
```

## Run

```bash
npm start
# or for development:
npm run dev
```

## API Endpoints

- `GET /` - Welcome message
- `GET /api/hello` - Hello endpoint

## License

MIT
''',
            ".gitignore": '''node_modules/
.env
*.log
'''
        },
        "folders": ["routes", "middleware"]
    },
    
    "valyxoscript": {
        "name": "ValyxoScript Project",
        "description": "ValyxoScript project template",
        "files": {
            "main.vs": '''# {project_name} - ValyxoScript Project
# Created with Valyxo

# Variables
set name = "{project_name}"
set version = "1.0.0"

# Main function
func main() {{
    print "Welcome to " + name
    print "Version: " + version
}}

# Run main
main()
''',
            "README.md": '''# {project_name}

A ValyxoScript project created with Valyxo.

## Run

```bash
valyxo run main.vs
```

## Structure

- `main.vs` - Main entry point
- `lib/` - Library files

## License

MIT
''',
            "lib/utils.vs": '''# Utility functions for {project_name}

func greet(name) {{
    print "Hello, " + name + "!"
}}

func add(a, b) {{
    return a + b
}}
'''
        },
        "folders": ["lib", "tests"]
    },
    
    "html": {
        "name": "Static Website",
        "description": "HTML/CSS/JS static website",
        "files": {
            "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="#" class="logo">{project_name}</a>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <h1>Welcome to {project_name}</h1>
            <p>Your awesome website starts here.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; {year} {project_name}. All rights reserved.</p>
    </footer>
    
    <script src="js/main.js"></script>
</body>
</html>
''',
            "css/style.css": '''* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    line-height: 1.6;
}}

header {{
    padding: 1rem 2rem;
    border-bottom: 1px solid #222;
}}

nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: bold;
    color: #fff;
    text-decoration: none;
}}

nav ul {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

nav a {{
    color: #888;
    text-decoration: none;
}}

nav a:hover {{
    color: #fff;
}}

.hero {{
    text-align: center;
    padding: 8rem 2rem;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

footer {{
    text-align: center;
    padding: 2rem;
    border-top: 1px solid #222;
    color: #666;
}}
''',
            "js/main.js": '''/**
 * {project_name} - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {{
    console.log('{project_name} loaded!');
}});
''',
            "README.md": '''# {project_name}

A static website created with Valyxo.

## Structure

- `index.html` - Main page
- `css/` - Stylesheets
- `js/` - JavaScript files

## License

MIT
'''
        },
        "folders": ["css", "js", "images"]
    },
    
    "cli": {
        "name": "CLI Tool",
        "description": "Command-line tool template",
        "files": {
            "cli.py": '''#!/usr/bin/env python3
"""
{project_name} - Command Line Tool
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="{project_name} - A command-line tool"
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="help",
        help="Command to run"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="{project_name} 1.0.0"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode"
    )
    
    args = parser.parse_args()
    
    if args.command == "help":
        parser.print_help()
    elif args.command == "hello":
        if not args.quiet:
            print("Hello from {project_name}!")
    else:
        print(f"Unknown command: {{args.command}}")
        sys.exit(1)


if __name__ == "__main__":
    main()
''',
            "setup.py": '''from setuptools import setup

setup(
    name="{project_name_lower}",
    version="1.0.0",
    py_modules=["{project_name_lower}"],
    entry_points={{
        "console_scripts": [
            "{project_name_lower}=cli:main",
        ],
    }},
    python_requires=">=3.8",
)
''',
            "README.md": '''# {project_name}

A command-line tool created with Valyxo.

## Installation

```bash
pip install -e .
```

## Usage

```bash
{project_name_lower} hello
{project_name_lower} --help
```

## License

MIT
''',
            ".gitignore": '''__pycache__/
*.egg-info/
dist/
build/
'''
        },
        "folders": []
    }
}


def list_templates() -> List[Dict[str, str]]:
    """List all available templates."""
    return [
        {
            "name": name,
            "description": template["description"]
        }
        for name, template in TEMPLATES.items()
    ]


def create_project(template_name: str, project_name: str, directory: str = None) -> str:
    """Create a new project from template.
    
    Args:
        template_name: Name of the template
        project_name: Name of the new project
        directory: Optional base directory (defaults to current dir)
    
    Returns:
        Path to created project or error message
    """
    if template_name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        return f"✗ Unknown template: {template_name}\nAvailable: {available}"
    
    template = TEMPLATES[template_name]
    
    if directory is None:
        directory = os.getcwd()
    
    project_dir = os.path.join(directory, project_name)
    
    if os.path.exists(project_dir):
        return f"✗ Directory already exists: {project_dir}"
    
    try:
        os.makedirs(project_dir, exist_ok=True)
        
        # Create folders
        for folder in template.get("folders", []):
            os.makedirs(os.path.join(project_dir, folder), exist_ok=True)
        
        # Create files with variable substitution
        year = datetime.now().year
        replacements = {
            "{project_name}": project_name,
            "{project_name_lower}": project_name.lower().replace(" ", "-").replace("_", "-"),
            "{year}": str(year)
        }
        
        for file_path, content in template["files"].items():
            full_path = os.path.join(project_dir, file_path)
            
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Apply replacements
            for key, value in replacements.items():
                content = content.replace(key, value)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return f"✓ Created {template['name']}: {project_dir}"
        
    except Exception as e:
        return f"✗ Failed to create project: {e}"


def get_template_info(template_name: str) -> Optional[Dict[str, Any]]:
    """Get detailed info about a template."""
    if template_name not in TEMPLATES:
        return None
    
    template = TEMPLATES[template_name]
    return {
        "name": template["name"],
        "description": template["description"],
        "files": list(template["files"].keys()),
        "folders": template.get("folders", [])
    }
