<div align="center">

```
██╗   ██╗ █████╗ ██╗  ██╗   ██╗██╗  ██╗ ██████╗
██║   ██║██╔══██╗██║  ╚██╗ ██╔╝╚██╗██╔╝██╔═══██╗
██║   ██║███████║██║   ╚████╔╝  ╚███╔╝ ██║   ██║
╚██╗ ██╔╝██╔══██║██║    ╚██╔╝   ██╔██╗ ██║   ██║
 ╚████╔╝ ██║  ██║███████╗██║   ██╔╝ ██╗╚██████╔╝
  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝ ╚═════╝
```

### The Modern Developer Platform

[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg?style=for-the-badge)](https://github.com/SandwichEater577/Valyxo)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Rust](https://img.shields.io/badge/Rust-Native-orange.svg?style=for-the-badge&logo=rust&logoColor=white)](https://rust-lang.org)
[![Go](https://img.shields.io/badge/Go-Backend-00ADD8.svg?style=for-the-badge&logo=go&logoColor=white)](https://go.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-Web-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)

**[Website](https://valyxo.dev)** · **[Documentation](docs/)** · **[Download](https://github.com/SandwichEater577/Valyxo/releases)** · **[Report Bug](https://github.com/SandwichEater577/Valyxo/issues)**

---

_A blazing-fast, extensible developer shell with native performance and modern aesthetics._

</div>

<br>

## ✨ What is Valyxo?

Valyxo is a **complete developer platform** that reimagines the terminal experience. Built from the ground up with performance and extensibility in mind, it combines:

- 🐍 **Python CLI** — Powerful, extensible command shell
- 🦀 **Rust Native Modules** — Lightning-fast file operations and git
- 🌐 **Go Backend** — Scalable REST API for cloud features
- 🖥️ **Tauri Desktop** — Native cross-platform desktop app
- 🌍 **Web Terminal** — Try Valyxo directly in your browser

<br>

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/SandwichEater577/Valyxo.git
cd Valyxo

# Run the CLI
python Source/Valyxo.py
```

That's it. You're now in the Valyxo shell.

```
┌─────────────────────────────────────────────────────┐
│  $ valyxo                                           │
│  ✓ Welcome to Valyxo v0.6.0                        │
│  ✓ Type 'help' for commands                        │
│                                                     │
│  valyxo > init my-project                          │
│  ✓ Project created successfully                    │
│                                                     │
│  valyxo > run                                      │
│  → Starting development server...                  │
│  ✓ Ready at http://localhost:3000                  │
└─────────────────────────────────────────────────────┘
```

<br>

## 🎯 Features

<table>
<tr>
<td width="50%">

### 🔥 Performance

- **Native Rust modules** for file I/O
- Sub-millisecond command parsing
- Async job execution
- Memory-efficient design

</td>
<td width="50%">

### 🎨 Developer Experience

- Beautiful syntax highlighting
- Smart autocomplete
- Custom themes & keybindings
- Built-in GPT integration

</td>
</tr>
<tr>
<td width="50%">

### 📦 Extensibility

- Plugin system
- Custom scripts (`.vxs` files)
- Package manager
- Template engine

</td>
<td width="50%">

### 🔒 Security

- Sandboxed script execution
- Secure credential storage
- JWT authentication
- Rate limiting

</td>
</tr>
</table>

<br>

## 📁 Project Architecture

```
Valyxo/
│
├── Source/                     # 🐍 Python Core
│   ├── Valyxo.py              # Main entry point
│   └── valyxo/
│       ├── core/              # Core modules (colors, filesystem, git, gpt...)
│       ├── script.py          # ValyxoScript runtime
│       └── shell/             # Shell implementation
│
├── Applications/
│   ├── Desktop/               # 🖥️ Tauri Desktop App
│   │   └── src-tauri/         # Rust backend
│   │
│   ├── ServerGo/              # 🌐 Go REST API
│   │   ├── cmd/server/        # Entry point
│   │   └── internal/          # Handlers, middleware, DB
│   │
│   └── Website/               # 🌍 Marketing Site
│       ├── HTML/              # Pages
│       ├── CSS/               # Styling
│       └── TypeScript/        # Logic
│
├── Libraries/
│   └── Native/                # 🦀 Rust Native Addon (NAPI)
│
└── Data/ValyxoDocuments/      # 📂 User data
```

<br>

## 🛠️ Installation

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** (for desktop app)
- **Rust** (for native modules, optional)
- **Go 1.21+** (for backend server, optional)

### Desktop App

```bash
cd Applications/Desktop
npm install
npm run tauri dev
```

### Go Server

```bash
cd Applications/ServerGo
go run cmd/server/main.go
```

### Build Native Modules

```bash
cd Libraries/Native
cargo build --release
```

<br>

## 🔧 Configuration

Valyxo stores configuration in `Data/ValyxoDocuments/Config/`:

```json
{
  "theme": "dark",
  "font": "JetBrains Mono",
  "fontSize": 14,
  "autoComplete": true,
  "plugins": ["git", "docker", "npm"]
}
```

<br>

## 📊 Tech Stack

| Layer        | Technology | Lines of Code |
| ------------ | ---------- | ------------- |
| CLI Core     | Python     | ~7,000        |
| Native Libs  | Rust       | ~4,400        |
| Web Frontend | TypeScript | ~3,300        |
| API Server   | Go         | ~1,700        |
| Website      | HTML/CSS   | ~4,000        |

**Total: ~20,600 lines**

<br>

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<br>

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

<br>

## 👤 Author

**Michał Kostkowski** ([@SandwichEater577](https://github.com/SandwichEater577))

<br>

---

<div align="center">

**[⬆ Back to Top](#)**

Made with ❤️ and lots of ☕

</div>
