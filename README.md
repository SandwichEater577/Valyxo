<p align="center">
  <img src="https://raw.githubusercontent.com/SandwichEater577/NovaHub/main/NovaLogo.png" width="200">
</p>
⭐ NovaHub — Terminal OS + Scripting Language + AI Toolkit

A lightweight terminal-based development environment featuring:
✔ A virtual OS
✔ The NovaScript programming language
✔ Integrated AI assistant (NovaGPT)
✔ File system, editor, job manager, manpages, and more.

🏷️ Badges
![Version](https://img.shields.io/github/v/release/SandwichEater577/NovaHub)
![Downloads](https://img.shields.io/github/downloads/SandwichEater577/NovaHub/total)
![License](https://img.shields.io/github/license/SandwichEater577/NovaHub)
![MadeWith](https://img.shields.io/badge/Made%20with-Python%203.13-blue)


(Replace this block in your README with the actual badge links if GitHub doesn’t auto-render them.)

🚀 About NovaHub

NovaHub is a fully custom terminal environment and scripting platform, designed to feel like a mix of:

Linux terminal

A lightweight OS

Custom scripting language (NovaScript)

AI development assistant (NovaGPT)

Virtual file system with projects, tools, and job control

All inside one Python-powered application.

It includes:

A full virtual filesystem under ~/NovaHubDocuments

A working nano-style text editor

A robust man page system

Background job execution (run file.ns &)

Auto-suggestions

A modular architecture for future tools (NovaStore, NovaTools, etc.)

NovaHub is built for developers, learners, and anyone who wants their own customizable terminal OS.

📦 Download
👉 Download the latest NovaHub.exe:

➡ https://github.com/SandwichEater577/NovaHub/releases/latest

No Python required.
Just download and run.

🧰 Features
🌐 NovaHub Shell

A minimalistic terminal OS with:

mkdir, ls, cd, cat, grep

nano editor

man documentation system

run foreground / run file & background execution

jobs and kill

Settings system (colors, suggestions, etc.)

Auto-correct suggestions for commands

🧪 NovaScript Language

NovaHub’s custom programming language.

Supports:

Variables (set x = 5)

Expressions (x + 2)

Strings ("Hello")

Printing (print x)

One-line conditional logic:

if [x < 10] then [print x] else [print "big"]


Comments (# this is a comment)

Integrated AI helper inside NovaScript:

N@"create a function that calculates velocity"

🤖 NovaGPT

AI chat system inside NovaHub.

Two modes:

NovaHub → NovaGPT:
Ask questions, brainstorm ideas, get help.

NovaScript → NovaGPT (code only):
N@"write code" generates NovaScript code automatically.

(Currently simulated; optional real API support planned.)

📝 Nano Editor

A file editor built into NovaHub.

No line numbers (clean & minimal)

Saves automatically on exit

Can create new files with language extension selection

Used mainly for NovaScript development

📚 Manpage System

Like Linux:

man NovaHub
man NovaScript
man nano
man mkdir
man lang
man command


Pages include:

COMMAND

HOW TO USE

EXAMPLE

DESCRIPTION

LANGUAGE

NOTES

WARNINGS

SEE ALSO

With a full pager:
SPACE = next page, ENTER = next line, q = quit

🛠️ Installation
Option A — Run the Windows EXE

Download the latest release:
👉 https://github.com/SandwichEater577/NovaHub/releases/latest

Run:

NovaHub.exe


Done!
NovaHub creates the directory:

C:\Users\<you>\NovaHubDocuments

Option B — Run from source (requires Python 3.11+)

Clone the repo:

git clone https://github.com/SandwichEater577/NovaHub.git
cd NovaHub/src
python NovaHub.py

🔤 Hello World in NovaScript

Create a file:

nano Hello.ns


Write:

set msg = "Hello World"
print msg
exit


Run it:

run Hello.ns


Output:

Hello World

🧪 Example Commands
NovaHub=> mkdir Projects
NovaHub=> cd Projects
NovaHub=> nano main.ns
NovaHub=> run main.ns
NovaHub=> run server.ns &
NovaHub=> jobs
NovaHub=> kill 1
NovaHub=> man NovaScript

🌱 Roadmap (Upcoming Versions)
v0.4

NovaScript loops (for, while)

Functions

File import system

NovaGPT real API support (optional)

Improved nano editing commands

v0.5

Plugin system (NovaTools)

NovaHub Store (novapkg)

Themes for terminal

FS permissions

1.0

Stable NovaScript compiler

Package manager

Editor improvements

Real AI-assisted development

Automatic updates

🤝 Contributing

PRs welcome!
Please open an issue first to discuss features or bugs.

📜 License

MIT License — free to use, modify, and distribute.

🙌 Credits

Created by SandwichEater577
Built with ❤️ in Python.
