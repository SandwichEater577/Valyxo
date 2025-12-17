# 🚀 Valyxo — Complete Developer Ecosystem

**🖥️ Running Valyxo (Desktop App)**

Valyxo is available as a **native desktop application** for all major operating systems.
No terminal or programming knowledge is required to run the app.

### Supported Platforms
- 🪟 **Windows** — Portable App
- 🐧 **Linux** — AppImage
- 🍎 **macOS** — Native `.app`

The desktop app automatically starts:
- the backend API
- the database
- the web interface

Everything runs silently in the background.


> **Valyxo** = Terminal CLI + Desktop Apps + Web Platform + AI Assistant

```
     ██    ██  █████  ██       █████  ██   ██  ██████  
     ██    ██ ██   ██ ██      ██   ██  ██ ██  ██    ██ 
     ██    ██ ███████ ██      ███████   ███   ██    ██ 
     ██    ██ ██   ██ ██      ██   ██   ██    ██    ██ 
      ██████  ██   ██ ███████ ██   ██   ██     ██████  
                                                        
         Version 0.41 | Powered by Zencoder AI
```

## 📋 Table of Contents

1. [What is Valyxo](#what-is-valyxo)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Components](#components)
   - [ValyxoHub](#valyxohub-terminal-cli)
   - [ValyxoScript](#valyxoscript)
   - [ValyxoGPT](#valyxogpt)
   - [ValyxoApp](#valyxoapp-desktop-applications)
5. [Web Platform](#web-platform)
6. [Installation](#installation)
7. [Quick Start](#quick-start)
8. [Security](#security)
9. [Roadmap](#roadmap)
10. [Documentation](#documentation)
11. [Contributing](#contributing)
12. [License](#license)

---

## 🎯 What is Valyxo

**Valyxo** is a comprehensive developer ecosystem designed for modern software development. It combines a powerful terminal interface, intelligent scripting language, AI assistance, and web platform into one unified system.

| Component | Type | Description |
|-----------|------|-------------|
| **ValyxoHub** | Terminal CLI | Professional development environment |
| **ValyxoApp** | Desktop Applications | Graphical interface with multi-language support |
| **ValyxoGPT** | AI Assistant | Intelligent coding companion |
| **ValyxoScript** | Programming Language | Lightweight, intuitive scripting |
| **Web Platform** | Full Stack | Collaboration and management hub |

---

## 🌟 Key Features

- ✅ **Modern Architecture** — Modular, scalable, and extensible design
- ✅ **Terminal-First** — Full power for developers in CLI
- ✅ **AI-Powered** — Integrated Zencoder AI for intelligent assistance
- ✅ **Cross-Platform** — Linux, Windows, macOS support
- ✅ **Open Source** — Transparent development, community-driven
- ✅ **Secure** — Password hashing, input validation, data protection
- ✅ **Multi-Language** — Support for ValyxoScript, JavaScript, Python, Java
- ✅ **Project Management** — Built-in tools for file operations and job management

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   VALYXO ECOSYSTEM                      │
└─────────────────────────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼─────┐        ┌────▼─────┐      ┌─────▼─────┐
    │ TERMINAL │        │  DESKTOP │      │    WEB    │
    │(ValyxoHub)        │(ValyxoApp)      │(Platform) │
    └──────────┘        └──────────┘      └───────────┘
         │                  │                  │
         ├──────────────────┼──────────────────┤
         │                  │                  │
    ┌────▼──────────────────▼──────────────────▼─┐
    │           VALYXO CORE                      │
    │  ┌─────────────────────────────────────┐   │
    │  │ - Filesystem Operations             │   │
    │  │ - ValyxoScript Runtime              │   │
    │  │ - Job Management                    │   │
    │  │ - Manual System                     │   │
    │  │ - Color Theming                     │   │
    │  └─────────────────────────────────────┘   │
    └────┬──────────────────────────────┬────┘
         │                              │
    ┌────▼───────────────────────┬─────▼────┐
    │                            │          │
┌───▼──────┐                   ┌─────▼───┐ ┌────▼─────┐
│ValyxoGPT │                   │ Zencoder│ │ Database  │
│(AI Core) │                   │   API   │ └──────────┘
└──────────┘                   └─────────┘
```

### Three Core Layers

#### 1️⃣ **ValyxoHub** — Terminal CLI
- Professional console application for developers
- Full-featured code editing and execution
- Multi-language support (ValyxoScript, JavaScript, Python, Java)
- Integrated AI Assistant in terminal
- Project management and file operations

#### 2️⃣ **ValyxoApp** — Desktop Applications
- Graphical user interface for enhanced workflow
- Project visualization and management
- Integration with ValyxoHub
- Implementations: Java (JavaFX), C# (.NET/MAUI), C++ (Qt), JavaScript (Electron)
- Complements terminal, doesn't replace it

#### 3️⃣ **Web Platform** — Full Stack Ecosystem
- Frontend: HTML5 + CSS3 + JavaScript
- Backend: Node.js + Express (REST API)
- Database: PostgreSQL/SQLite
- Features: Authentication, Dashboard, Collaboration, AI Chat

---

## 🔧 Components

### **ValyxoHub** (Terminal)

Launch the terminal environment:

```bash
python src/Valyxo.py
```

**Available Commands:**
- `mkdir <path>` — Create directories
- `ls [path]` — List files
- `cd <path>` — Change directory
- `cat <file>` — Display file contents
- `grep <pattern>` — Search files
- `nano <file>` — Edit files
- `run <file>` — Execute script
- `jobs` — List running processes
- `kill <pid>` — Terminate process
- `enter ValyxoScript` — Enter ValyxoScript interpreter
- `enter ValyxoGPT` — Chat with AI assistant
- `theme [list|set]` — Manage themes
- `man <command>` — View documentation

### **ValyxoScript** (v0.41 Enhanced)

Lightweight scripting language designed for simplicity and power. v0.41 includes a full runtime with safe evaluation, control flow, and function support.

```valyxoscript
set x = 10
set y = 20
set z = x + y
print z

if [z > 20] then [print "Greater!"] else [print "Smaller!"]

for i in 1 to 5 {
  print i
}

while [x < 30] {
  set x = x + 5
  print x
}

func add(a, b) {
  print a + b
}

add(3, 4)
```

**Core Features (v0.41):**
- **Variable Management**: `set x = value` with type inference
- **Expressions**: Safe mathematical evaluation (2+3, x*10, etc.)
- **Conditionals**: `if [condition] then [cmd] else [cmd]`
- **Loops**: 
  - `for i in start to end { ... }` — Counted iteration
  - `while [condition] { ... }` — Conditional loops
  - Infinite loop protection with MAX_ITERATIONS
- **Functions**: `func name(params) { body }` with parameter passing
- **Output**: `print x`, `print "text"`, `print x + 10`
- **Safety**: AST validation, no arbitrary code execution
- **Variable Inspection**: `vars` command to list all variables

**Runtime Implementation:**
- `ValyxoScriptRuntime` class: Full interpreter
- `safe_eval()`: Secure expression evaluation
- Block stack: Nested control flow support
- Function registry: Reusable code blocks
- Error handling: Informative error messages

### **ValyxoGPT**

AI-powered assistant integrated in terminal:

```bash
> enter ValyxoGPT
> How do I define a function in ValyxoScript?
AI: In ValyxoScript, use the 'func' keyword: func add(a, b) { ... }
```

**Capabilities:**
- Code explanation and assistance
- Debugging support
- Best practices recommendations
- Multi-turn conversations
- Context-aware responses

### **ValyxoApp** — Desktop Applications

Multi-language desktop implementations:

- **Java** — JavaFX/Swing UI
- **C#** — .NET/WPF/MAUI
- **C++** — Qt framework
- **JavaScript** — Electron/Tauri

Each provides:
- Project management interface
- ValyxoScript editor and runner
- Log viewer
- ASCII map visualization
- Direct ValyxoHub integration

---

## 🌐 Web Platform

Complete web-based ecosystem:

**Frontend:**
- Responsive HTML5 + CSS3 interface
- Interactive JavaScript components
- Feed/card-based design
- Real-time updates

**Backend:**
- RESTful API with Express.js
- User authentication and authorization
- Project management
- Collaboration tools

**Features:**
- User registration and login
- Dashboard and profile management
- Project workspace
- API documentation
- Blog and changelog
- Community features

---

## 📦 Installation

### Requirements
- Python 3.8+
- Git
- npm (for web platform)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/valyxo.git
cd valyxo
```

### Step 2: Install Dependencies

```bash
# Terminal CLI
pip install -r requirements.txt

# Web platform (optional)
cd website
npm install
```

### Step 3: Launch

```bash
python src/Valyxo.py
```

---

## 🎮 Quick Start

### Launch ValyxoHub

```bash
python src/Valyxo.py
```

You should see:
```
Welcome to Valyxo v0.41 (Zencoder Integrated)
valyxo:~>
```

### Basic Workflow

```bash
# Create a project
mkdir Projects/MyProject
cd Projects/MyProject

# Create a script file
nano script.vs

# Add ValyxoScript code
set name = "Valyxo"
print name

# Run it
run script.vs

# Get help
man valyxohub
```

### ValyxoScript Examples

**Example 1: Basic Variables and Math**
```valyxoscript
set x = 10
set y = 20
set sum = x + y
print sum
```

**Example 2: Loops**
```valyxoscript
for i in 1 to 5 {
  print i
}

set count = 0
while [count < 3] {
  print count
  set count = count + 1
}
```

**Example 3: Functions**
```valyxoscript
func multiply(a, b) {
  print a * b
}

multiply(4, 5)
```

**Example 4: Conditionals**
```valyxoscript
set score = 85
if [score >= 80] then [print "Passed!"] else [print "Try again"]
```

---

## 🔒 Security

Valyxo is built with security as a core principle:

- ✅ **Password Hashing** — bcrypt/argon2
- ✅ **Input Validation** — Sanitization of all user inputs
- ✅ **HTTPS** — Encrypted communication
- ✅ **Secure Secrets** — Environment variables, no plaintext
- ✅ **SQL Injection Protection** — Parameterized queries
- ✅ **CSRF Protection** — Token validation
- ✅ **XSS Prevention** — Output escaping

See [SECURITY_AUDIT.md](./SECURITY_AUDIT.md) for detailed analysis.

---

## 🗺️ Roadmap

### ✅ v0.41 (Current)
- [x] Modular Valyxo core architecture with type hints
- [x] ValyxoHub terminal with full commands
- [x] ValyxoScript full runtime implementation
  - [x] Variable management and expressions
  - [x] Control flow (if/else, for, while)
  - [x] Function definitions and calls
  - [x] Infinite loop protection
  - [x] Safe AST-based evaluation
- [x] ASCII art and branding system
- [x] Zencoder AI integration
- [x] Web platform skeleton (23 HTML pages)
- [x] Security improvements
- [x] Version standardization (0.41)

### 🔄 v0.42 (Planned)
- [ ] ValyxoApp desktop applications (Java, C#, C++, Electron)
- [ ] Extended ValyxoScript features
- [ ] Plugin system for extensions
- [ ] Performance optimization
- [ ] Advanced web platform features
- [ ] Collaboration tools

### 📅 v0.43+ (Future)
- [ ] Web IDE (VS Code-like)
- [ ] Mobile application
- [ ] Cloud storage integration
- [ ] Team collaboration platform
- [ ] Advanced analytics

---

## 📂 Project Structure

```
valyxo/
├── src/
│   ├── Valyxo.py                 (Entry point)
│   ├── valyxo/
│   │   ├── core/                 (Core modules)
│   │   │   ├── branding.py       (ASCII art & banners)
│   │   │   ├── colors.py         (Color theming)
│   │   │   ├── constants.py      (Configuration)
│   │   │   ├── filesystem.py     (File operations)
│   │   │   ├── gpt.py            (AI integration)
│   │   │   ├── jobs.py           (Job management)
│   │   │   ├── man.py            (Manual system)
│   │   │   └── utils.py          (Utilities)
│   │   ├── script.py             (ValyxoScript runtime)
│   │   ├── shell/                (Shell interface)
│   │   └── editor/               (Text editor)
├── website/
│   ├── css/                      (Stylesheets)
│   ├── index.html                (Homepage)
│   └── [23 component pages]
├── docs/
│   ├── MANUALS.md                (User manual)
│   └── manpages/                 (Command help)
├── tests/                        (Test suite)
├── examples/                     (Example projects)
├── README.md                     (This file)
├── LICENSE                       (MIT License)
└── requirements.txt              (Python dependencies)
```

---

## 📚 Documentation

Comprehensive documentation available:

- **[VALYXO_ARCHITECTURE.md](./VALYXO_ARCHITECTURE.md)** — Detailed architecture
- **[VALYXO_QUICK_START.md](./VALYXO_QUICK_START.md)** — Quick reference guide
- **[SECURITY_AUDIT.md](./SECURITY_AUDIT.md)** — Security analysis
- **[docs/MANUALS.md](./docs/MANUALS.md)** — User manual
- **[ASCII_MAP_VALYXO.md](./ASCII_MAP_VALYXO.md)** — System visualization

---

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Make your changes and commit: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a Pull Request

**Contributing Guidelines:**
- Follow existing code style
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

---

## 📄 License

Valyxo is licensed under the **MIT License with commercial restrictions**.

See [LICENSE](./LICENSE) for details.

---

## 📞 Contact & Community

- 🐙 GitHub: [github.com/valyxo](https://github.com)
- 📧 Email: contact@valyxo.dev
- 🌐 Website: https://valyxo.dev
- 💬 Discord: (Community server)

---

## 🌟 Acknowledgments

We thank:
- **Zencoder AI** — for AI integration
- **Open Source Community** — for inspiration and tools
- **All Contributors** — for making Valyxo possible

---

**Valyxo v0.41** — The Complete Developer Ecosystem

_Built by developers, for developers._

```
Made with ❤️ for the global developer community
```
