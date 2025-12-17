# Valyxo Desktop - Quick Start

Get Valyxo running on your PC as a native desktop application in 5 minutes.

## Option 1: Download Pre-built (Fastest)

1. **Download**: Get latest installer from releases page
   - Windows: `Valyxo-0.41.0.exe`
   - macOS: `Valyxo-0.41.0.dmg`
   - Linux: `Valyxo-0.41.0.AppImage`

2. **Install**: Run the installer

3. **Launch**: Find in applications menu or desktop

✓ Done! App will automatically start the backend.

---

## Option 2: Run from Source (Developers)

### Prerequisites

```bash
# Install Node.js (if not already installed)
# Download from: https://nodejs.org/ (LTS version)

# Verify installation
node --version
npm --version
```

### Step 1: Setup

```bash
# Navigate to desktop directory
cd desktop

# Install dependencies
npm install
```

### Step 2: Run Development

```bash
npm run dev
```

App will:
1. Start backend API on port 5000
2. Open Electron window
3. Load web interface
4. Show DevTools

### Step 3: Build (Optional)

```bash
# Build installer for your platform
npm run build

# Build specific platform
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux
```

Installers appear in `dist/` folder.

---

## First Launch

When you run Valyxo for the first time:

1. **Initializing** — Backend server starts (5-10 seconds)
2. **Loading UI** — Web interface loads
3. **Welcome** — Dashboard appears

Click "Create Project" to start building!

---

## Key Features

### System Tray

Right-click the Valyxo icon in system tray:
- Show/Hide window
- Quick navigation
- Exit app

### Main Menu

- **File** → Exit
- **View** → Reload, Zoom, DevTools
- **Tools** → API Docs, Server Health, Metrics
- **Help** → About, Documentation

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Q | Quit |
| Ctrl+R | Reload |
| Ctrl+I | DevTools |
| F11 | Fullscreen |

---

## Troubleshooting

### App won't start

**Solution 1**: Wait longer (first launch takes 10-15 seconds)

**Solution 2**: Check port 5000
```bash
# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000
```

Kill any process using port 5000 and try again.

**Solution 3**: Delete database and restart
```bash
# Windows
rmdir /s %APPDATA%\Valyxo

# Mac
rm -rf ~/Library/Application\ Support/Valyxo

# Linux
rm -rf ~/.config/Valyxo
```

### Blank window

- Wait 5 seconds for backend
- Press Ctrl+R to reload
- Close and reopen app

### High memory usage

- Close unused projects
- Restart the app
- Check for memory leaks in DevTools

### Backend server errors

Check logs:
- Windows: `%APPDATA%\Valyxo\logs\error.log`
- Mac: `~/Library/Application Support/Valyxo/logs/error.log`
- Linux: `~/.config/Valyxo/logs/error.log`

---

## Common Tasks

### Create a Project

1. Click "Projects" in sidebar
2. Click "New Project"
3. Enter name and description
4. Click "Create"

### Write a Script

1. Open project
2. Click "New Script"
3. Enter script name
4. Write ValyxoScript code
5. Click "Run" to execute

### Check API Docs

1. Click "Tools" → "API Documentation"
2. Swagger UI opens in new tab
3. Try out endpoints

### View Performance Metrics

1. Click "Tools" → "Metrics"
2. See requests, errors, memory usage
3. Cache statistics

---

## File Locations

### Windows
```
%APPDATA%\Valyxo\
├── valyxo.db
└── logs\
    ├── combined.log
    └── error.log
```

### macOS
```
~/Library/Application Support/Valyxo/
├── valyxo.db
└── logs/
    ├── combined.log
    └── error.log
```

### Linux
```
~/.config/Valyxo/
├── valyxo.db
└── logs/
    ├── combined.log
    └── error.log
```

---

## Command Line (Development)

```bash
cd desktop

# Development with auto-reload
npm run dev

# Production mode
npm run start

# Build installer
npm run build

# Build for specific platform
npm run build:win
npm run build:mac
npm run build:linux
```

---

## Next Steps

1. **Create Project** — Build your first project
2. **Write Script** — Create a ValyxoScript
3. **Explore API** — Check API documentation
4. **Read Docs** — Learn more features
5. **Join Community** — Share your projects

---

## Useful Links

- **Full Documentation**: `README.md`
- **Build Instructions**: `BUILD.md`
- **Backend API**: `../server/README.md`
- **ValyxoScript Guide**: `../README.md`

---

## Support

- **Issue**: Open GitHub issue
- **Question**: Check documentation
- **Bug**: Report with logs attached
- **Feature**: Request on discussions

---

## Version Info

- **Valyxo Version**: 0.41.0
- **Electron Version**: 27.0.0
- **Node.js**: 16+

Launch the app now: `npm run dev` or click the installer!

✨ Enjoy Valyxo!
