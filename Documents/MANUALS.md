# VALYXO — Manual Pages

## Table of Contents

- [man valyxohub](#man-valyxohub)
- [man valyxoscript](#man-valyxoscript)
- [man valyxogpt](#man-valyxogpt)
- [man valyxoapp](#man-valyxoapp)

---

## man valyxohub

### COMMAND

**valyxohub** — Terminal-based developer environment with AI integration

### HOW TO USE

```bash
valyxohub              # Start ValyxoHub terminal
```

Commands available:
- `mkdir <path>` — Create directories
- `ls [path]` — List files and directories
- `cd <path>` — Change directory
- `cat <file>` — Display file contents
- `grep <pattern> <file>` — Search in files
- `nano <file>` — Edit files with built-in editor
- `run <file>` — Execute ValyxoScript files
- `jobs` — List running jobs
- `kill <pid>` — Terminate a job
- `enter ValyxoScript` — Start ValyxoScript interpreter
- `enter ValyxoGPT` — Chat with AI assistant
- `theme [list|set <name>]` — Manage color themes
- `python` — Launch Python interpreter
- `man <command>` — Display command documentation
- `settings` — Configure ValyxoHub
- `-help` — Show available commands
- `quit` — Exit ValyxoHub

### EXAMPLE

```bash
$ valyxohub
Welcome to Valyxo v0.31 (Zencoder Integrated)
valyxo:~> mkdir Projects/MyApp
valyxo:~> cd Projects/MyApp
valyxo:~/Projects/MyApp> nano main.vs
# Edit file...
valyxo:~/Projects/MyApp> run main.vs
Hello from ValyxoScript!
valyxo:~/Projects/MyApp> quit
```

### DESCRIPTION

ValyxoHub is a powerful terminal-based developer environment designed for modern programmers. It provides:

- **File Management** — Create, edit, and organize projects
- **Script Execution** — Run ValyxoScript and Python code
- **AI Assistant** — Integrate Zencoder AI for code help
- **Job Management** — Run background processes safely
- **Theming System** — Customize terminal appearance
- **Multi-language Support** — Work with ValyxoScript, Python, JavaScript, Java

### WARNINGS

- ⚠️ Always use `nano` or proper editors — direct file manipulation may corrupt projects
- ⚠️ `kill <pid>` terminates processes immediately — save work first
- ⚠️ Long-running jobs can consume resources — monitor with `jobs`
- ⚠️ Do not navigate outside `~/ValyxoDocuments/` — paths are sandboxed for security

### UPDATED IN

v0.31+ (Modular Architecture Release)

### SEE ALSO

- `man valyxoscript`
- `man valyxogpt`
- `man valyxoapp`

---

## man valyxoscript

### COMMAND

**ValyxoScript** — Lightweight scripting language for Valyxo

### HOW TO USE

```bash
# In ValyxoHub terminal
enter ValyxoScript
> your_code_here
```

### EXAMPLE

```valyxoscript
# Variables
set x = 10
set y = 20
set message = "Hello, Valyxo!"

# Printing
print x
print message

# Conditionals
if [x < 15] then [print "Less than 15"] else [print "More or equal"]

# Loops
while [x < 100] {
  set x = x + 10
  print x
}

# Functions
func greet(name) {
  set msg = "Hello, " + name
  print msg
}

greet "World"

# List operations
set list = [1, 2, 3, 4, 5]
for item in list {
  print item
}
```

### DESCRIPTION

ValyxoScript is a simple, Python-like scripting language with:

- **Simple Syntax** — Easy to learn and read
- **Variables** — Dynamic typing with `set`
- **Control Flow** — if/then/else, while, for loops
- **Functions** — Define reusable code blocks
- **Lists & Dicts** — Basic data structures
- **String Operations** — Concatenation and formatting
- **Safe Evaluation** — Uses AST, prevents malicious code
- **Infinite Loop Protection** — Built-in iteration limits

### DATA TYPES

| Type | Example |
|------|---------|
| Integer | `10`, `-5`, `0` |
| Float | `3.14`, `-0.5` |
| String | `"hello"`, `'world'` |
| Boolean | `True`, `False` |
| List | `[1, 2, 3]`, `["a", "b"]` |
| Dict | `{"key": "value"}` |
| None | `None` |

### KEYWORDS

- `set` — Assign variable
- `print` — Output value
- `if` / `then` / `else` — Conditional
- `while` — Loop while condition is true
- `for` `in` — Loop over iterable
- `func` — Define function
- `import` — Import module
- `exit` — Exit interpreter
- `vars` — List all variables

### WARNINGS

- ⚠️ Infinite loops are automatically stopped after 10,000 iterations
- ⚠️ Variables are case-sensitive: `x` ≠ `X`
- ⚠️ Functions must be defined before use
- ⚠️ Unknown functions raise errors — use `vars` to list available

### UPDATED IN

v0.31+ (Zencoder Integration)

### SEE ALSO

- `man valyxohub`
- `man valyxogpt`

---

## man valyxogpt

### COMMAND

**ValyxoGPT** — AI-powered code assistant

### HOW TO USE

```bash
# In ValyxoHub terminal
enter ValyxoGPT
> Ask your question here
```

### EXAMPLE

```bash
$ valyxohub
valyxo:~> enter ValyxoGPT

ValyxoGPT v0.31 (Powered by Zencoder AI)
Type your question or type 'quit' to exit

> How do I define a function in ValyxoScript?
AI: ValyxoScript functions: Use 'func name(params) { body }' to define. 
Call with 'name(args)'. Supports parameters and local scope.

> How do I debug my code?
AI: I can help debug! Describe the issue or share your code, and I'll help 
identify the problem.

> quit
```

### DESCRIPTION

ValyxoGPT is an AI assistant integrated with Zencoder that helps with:

- **Code Generation** — Generate code snippets and functions
- **Bug Fixing** — Debug and troubleshoot issues
- **Code Review** — Suggest improvements
- **Testing** — Generate unit test code
- **Refactoring** — Improve code quality
- **Learning** — Explain programming concepts
- **Multi-turn Conversations** — Context-aware responses (40 message history)

### FEATURES

- ✅ **Multi-turn Conversation** — Maintains context across messages
- ✅ **Zencoder Powered** — Latest AI models and responses
- ✅ **Code-Aware** — Understands ValyxoScript, Python, JavaScript, Java
- ✅ **Fast** — Real-time responses
- ✅ **Contextual** — Remembers conversation history
- ✅ **Helpful** — Professional, accurate answers

### CONVERSATION HISTORY

ValyxoGPT stores up to **40 messages** in conversation history:
- Older messages are automatically removed
- Each conversation session is independent
- Clear history with `clear` command

### WARNINGS

- ⚠️ ValyxoGPT cannot execute code — use `run` command for that
- ⚠️ AI responses are suggestions — always verify code
- ⚠️ API key required — set with `api-key set <your_key>`
- ⚠️ Some features require internet connection

### UPDATED IN

v0.31+ (Zencoder Integration Complete)

### SEE ALSO

- `man valyxohub`
- `man valyxoscript`

---

## man valyxoapp

### COMMAND

**ValyxoApp** — Desktop application for Valyxo (Planned v0.32+)

### HOW TO USE

```bash
valyxoapp                   # Launch desktop application
```

### EXAMPLE

_Feature in development — See v0.32+ releases_

```
[Desktop Window]
┌─────────────────────────────────┐
│  ValyxoApp v0.32                │
├─────────────────────────────────┤
│ [Projects] [Editor] [AI] [Tools]│
│                                 │
│ My Projects:                    │
│ ✓ Project A                     │
│ ✓ Project B                     │
│ ○ New Project                   │
│                                 │
└─────────────────────────────────┘
```

### DESCRIPTION

ValyxoApp is a graphical desktop application for Valyxo featuring:

- **Project Management** — Visual project browser
- **Code Editor** — Syntax highlighting, multi-file editing
- **Terminal Integration** — Embedded ValyxoHub
- **AI Chat** — ValyxoGPT sidebar
- **File Explorer** — Visual file management
- **Theme Support** — Dark/light modes
- **Cross-platform** — Windows, macOS, Linux

### FEATURES (v0.32+)

- ✅ Modern UI with dark theme
- ✅ Multi-document editing
- ✅ Code syntax highlighting
- ✅ Project templates
- ✅ Built-in terminal
- ✅ AI assistant sidebar
- ✅ Extension system (planned)

### REQUIREMENTS

- Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- 4GB RAM minimum
- 256MB disk space
- Stable internet connection (for Zencoder)

### WARNINGS

- ⚠️ ValyxoApp requires ValyxoHub to be installed
- ⚠️ Some features require active internet connection
- ⚠️ Project files must be in `~/ValyxoDocuments/`

### UPDATED IN

v0.32 (Planned) — Desktop application release

### SEE ALSO

- `man valyxohub`
- `man valyxoscript`
- `man valyxogpt`

---

## Version Information

```
Valyxo v0.31 (Modular Architecture)
├── ValyxoHub: Terminal CLI (active)
├── ValyxoScript: Lightweight language (active)
├── ValyxoGPT: AI Assistant (active)
└── ValyxoApp: Desktop Application (v0.32+)
```

## Quick Links

| Component | Type | Status |
|-----------|------|--------|
| **ValyxoHub** | Terminal | ✅ Active |
| **ValyxoScript** | Language | ✅ Active |
| **ValyxoGPT** | AI | ✅ Active |
| **ValyxoApp** | Desktop | 🔄 Planned |
| **Web Platform** | Full Stack | 🔄 In Progress |

---

Last updated: December 2025
Valyxo Documentation v0.31+
