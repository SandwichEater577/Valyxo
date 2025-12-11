# NovaHub - D-Edition

A terminal-based developer environment with NovaScript language interpreter, NovaGPT assistant, and background job management.

## Features

- **Virtual Filesystem**: Isolated environment under `~/NovaHubDocuments`
- **NovaScript**: Lightweight scripting language with variables, expressions, and control flow
- **NovaGPT**: Simulated AI assistant for development queries
- **nano Editor**: NovaScript-based file editor with line management
- **Job Control**: Run scripts in background with thread-based job management
- **Man Pages**: Built-in documentation system with pager
- **Language Detection**: Support for NovaScript, JavaScript, Python, and Java
- **Autosuggest**: Smart command suggestions using difflib
- **Settings**: Persistent configuration stored in JSON

## Requirements

- Python 3.11 or newer
- No external dependencies (uses only Python standard library)

## Quick Start

1. **Run NovaHub**:
   ```bash
   python3 src/NovaHub.py
   ```

2. **Create a folder**:
   ```
   NovaHub=~==> mkdir myproject
   ```

3. **Navigate to folder**:
   ```
   NovaHub=~==> cd myproject
   ```

4. **Create a NovaScript file**:
   ```
   NovaHub=~/myproject==> nano main.ns
   ```

5. **Write NovaScript code**:
   ```
   set message = "Hello NovaHub"
   print message
   ```
   (Type `exit` to save and leave)

6. **Run the script**:
   ```
   NovaHub=~/myproject==> run main.ns
   ```

## NovaScript Syntax

### Variables and Expressions

```
set x = 10
set y = 20
set sum = x + y
print sum
```

### Printing Values

```
set greeting = "Hello"
print greeting
print "World"
```

### Conditional Logic

```
set age = 25
if [age >= 18] then [print "Adult"] else [print "Minor"]
```

### Operators

- **Arithmetic**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Boolean**: `and`, `or`, `not`

### Built-in Commands

- `set <name> = <expression>` - Assign variable
- `print <value>` - Print to console
- `if [condition] then [command] else [command]` - Conditional execution
- `vars` - List all variables
- `exit` - Exit interpreter
- `help` - Show help

## Commands

### File Operations

- **mkdir** - Create folder or file
  ```
  mkdir projects
  mkdir "main.ns" --ns
  ```
- **ls** - List directory contents
  ```
  ls
  ls projects
  ```
- **cd** - Change directory
  ```
  cd projects
  cd ..
  ```
- **cat** - Display file contents
  ```
  cat main.ns
  ```
- **grep** - Search in files (regex supported)
  ```
  grep "pattern" main.ns
  ```

### Code Editing & Execution

- **nano** - Edit NovaScript files
  ```
  nano main.ns
  ```
  - `show` - Display buffer
  - `delete <line#>` - Remove line
  - `replace <line#> <text>` - Replace line
  - `insert <line#> <text>` - Insert line
  - `save` - Save without exiting
  - `exit` - Save and exit
  - `quit` - Exit without saving

- **run** - Execute NovaScript
  ```
  run main.ns       # Foreground
  run worker.ns &   # Background
  ```

### Job Management

- **jobs** - List running jobs
  ```
  jobs
  ```
- **kill** - Terminate job
  ```
  kill 1
  ```

### Documentation & Settings

- **man** - Read manuals
  ```
  man NovaScript
  man nano
  man command
  ```
- **settings** - Configure preferences
  ```
  settings              # Show all
  settings toggle suggestions
  ```

### Modes

- **enter NovaScript** - Interactive interpreter
  ```
  enter NovaScript
  NovaScript=> set x = 42
  NovaScript=> print x
  ```

- **enter NovaGPT** - Chat with simulated AI
  ```
  enter NovaGPT
  NovaGPT=> Nova@"How do I create a variable?"
  ```

## Man System

The man system provides built-in documentation for all commands:

```
man NovaHub
man NovaScript
man nano
man run
man settings
```

**Navigation**:
- **SPACE** - Next page
- **ENTER** - Next line
- **q** - Quit pager

## Background Jobs

Run long-running scripts in the background:

```
run long_task.ns &   # Start job in background
jobs                 # Monitor progress
kill 1               # Terminate job
```

Background jobs:
- Run in separate threads
- Can be monitored with `jobs`
- Cannot accept interactive input
- Must be terminated with `kill <id>`

## File Structure

```
NovaHubDocuments/
├── Projects/
│   └── Main/
├── System/
│   └── man/
└── Config/
    └── config.json
```

## nano Editor

The nano editor is NovaScript-specific:

1. **Create/edit file**:
   ```
   nano myfile
   ```

2. **Type commands** (not executed, just stored):
   ```
   set x = 1
   print x
   ```

3. **Line management**:
   - Add lines by typing
   - `show` - See all lines
   - `delete 1` - Remove line 1
   - `replace 1 "new text"` - Update line

4. **Save & exit**:
   - `exit` - Save
   - `quit` - Discard changes

## Language Detection

Supported file extensions:

- `.ns` - NovaScript
- `.js` - JavaScript
- `.py` - Python
- `.java` - Java

When creating files without extension, you'll be prompted to choose a language.

## Settings

Configuration is stored in `~/NovaHubDocuments/Config/config.json`:

```json
{
  "suggestions": true,
  "colors": true,
  "start_cwd": "~/Projects/Main",
  "remember_language": false
}
```

**Available settings**:
- `suggestions` - Enable command autosuggest
- `colors` - Enable colored output
- `start_cwd` - Initial working directory

Toggle settings:
```
settings toggle suggestions
```

## Examples

See `examples/HelloWorld/main.ns` for a simple NovaScript program.

## License

MIT License - See LICENSE file for details

## Project Structure

```
NovaHub/
├── src/
│   └── NovaHub.py          # Main application
├── docs/
│   └── manpages/           # Documentation files
├── examples/
│   └── HelloWorld/
│       └── main.ns         # Example script
├── .gitignore
├── LICENSE
└── README.md
```

## Development

NovaHub D-Edition is a single-file Python application designed for:
- Easy deployment
- No external dependencies
- Cross-platform compatibility
- Quick learning of scripting concepts

All functionality is contained within `src/NovaHub.py`.
