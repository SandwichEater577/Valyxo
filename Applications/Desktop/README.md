# Valyxo Desktop Application

Complete standalone desktop application for Windows, Mac, and Linux. Built with Electron and powered by the Valyxo backend API.

## Features

- **Native Desktop Application** — Runs as a standalone app like Discord or VS Code
- **Embedded Backend** — No need to run a separate server
- **System Tray Integration** — Quick access from system tray
- **Auto-Updates** — Keep your app up-to-date
- **Cross-Platform** — Windows, macOS, Linux support
- **Professional UI** — Modern interface with dark theme

## Installation

### Pre-built Installers

Download the latest release:
- **Windows**: `Valyxo-0.41.0.exe` or `Valyxo-0.41.0-portable.exe`
- **macOS**: `Valyxo-0.41.0.dmg`
- **Linux**: `Valyxo-0.41.0.AppImage` or `valyxo_0.41.0_amd64.deb`

### Windows Installation

1. Download `Valyxo-0.41.0.exe`
2. Double-click to run installer
3. Follow installation wizard
4. App will launch automatically

**Portable Version**: Download `Valyxo-0.41.0-portable.exe` to run without installation

### macOS Installation

1. Download `Valyxo-0.41.0.dmg`
2. Open the DMG file
3. Drag Valyxo to Applications folder
4. Launch from Applications

### Linux Installation

**AppImage** (Universal):
```bash
chmod +x Valyxo-0.41.0.AppImage
./Valyxo-0.41.0.AppImage
```

**Debian/Ubuntu**:
```bash
sudo dpkg -i valyxo_0.41.0_amd64.deb
valyxo  # Launch from terminal or applications menu
```

## Development

### Prerequisites

- Node.js 16+
- npm or yarn

### Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Install backend dependencies:
   ```bash
   cd ../server
   npm install
   cd ../desktop
   ```

### Development Mode

Start the development server:
```bash
npm run dev
```

This will:
1. Start the backend API server
2. Open the Electron app
3. Enable hot reload

### Building

#### Windows
```bash
npm run build:win
```

Outputs:
- `dist/Valyxo-0.41.0.exe` — Installer
- `dist/Valyxo-0.41.0-portable.exe` — Portable executable

#### macOS
```bash
npm run build:mac
```

Outputs:
- `dist/Valyxo-0.41.0.dmg` — Disk image
- `dist/Valyxo-0.41.0-mac.zip` — Compressed

#### Linux
```bash
npm run build:linux
```

Outputs:
- `dist/Valyxo-0.41.0.AppImage` — AppImage
- `dist/valyxo_0.41.0_amd64.deb` — Debian package

#### All Platforms
```bash
npm run build
```

## Project Structure

```
desktop/
├── src/
│   ├── main.js              # Main Electron process
│   ├── preload.js           # Security layer
│   ├── titlebar.js          # Custom titlebar
│   └── setup.js             # Windows installer setup
├── assets/
│   ├── icon.png             # App icon (256x256)
│   └── icon-small.png       # Tray icon (16x16)
├── package.json             # Dependencies and build config
├── README.md                # This file
└── BUILD.md                 # Build instructions
```

## Features Guide

### System Tray

Right-click the Valyxo icon in system tray to:
- Show/Hide main window
- Quick access to Dashboard
- Open Projects
- View API Docs
- Access Settings
- Exit app

Double-click tray icon to toggle window visibility

### Menu Bar

**File Menu**
- Exit — Close the application

**Edit Menu**
- Standard editing options (Undo, Redo, Cut, Copy, Paste)

**View Menu**
- Reload — Refresh the interface
- Developer Tools — Open DevTools (development only)
- Zoom controls
- Full screen toggle

**Tools Menu**
- API Documentation — Open Swagger UI
- Server Health — Check backend status
- Metrics — View performance metrics

**Help Menu**
- About Valyxo — View version info
- Documentation — Access full docs

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Q | Quit application |
| Ctrl+R | Reload |
| Ctrl+Shift+I | DevTools (dev only) |
| Ctrl+0 | Reset zoom |
| Ctrl++ | Zoom in |
| Ctrl+- | Zoom out |
| F11 | Toggle fullscreen |

## Data Storage

All data is stored in your user directory:

**Windows**: `C:\Users\<YourUsername>\AppData\Roaming\Valyxo\`
**macOS**: `~/Library/Application Support/Valyxo/`
**Linux**: `~/.config/Valyxo/`

Database location: `<user-data>/valyxo.db`

## Backend Integration

The app automatically:
1. Starts the embedded backend server
2. Waits for server to be ready (max 15 seconds)
3. Opens the web interface
4. Stops the server when app closes

Backend runs on `http://localhost:5000` (internal)

### Logs

Check backend logs in user data directory:
- `logs/combined.log` — All logs
- `logs/error.log` — Errors only

## Troubleshooting

### App Won't Start

1. Check if port 5000 is in use:
   ```bash
   netstat -ano | findstr :5000  # Windows
   lsof -i :5000                 # Mac/Linux
   ```

2. Kill any process on port 5000

3. Delete database and restart:
   ```bash
   rm ~/AppData/Roaming/Valyxo/valyxo.db  # Windows
   rm ~/Library/Application\ Support/Valyxo/valyxo.db  # Mac
   ```

### Backend Not Starting

1. Check logs in `logs/combined.log`
2. Verify Node.js is bundled correctly
3. Try portable version (includes all dependencies)

### Blank Window

1. Wait 5 seconds for backend to start
2. Try refreshing: Ctrl+R
3. Check if localhost:5000 is accessible

### High Memory Usage

- Close unused tabs/projects
- Restart the application
- Check for background processes

## Performance

### Typical Performance

- **Startup Time**: 3-5 seconds
- **Memory Usage**: 150-250MB
- **CPU Usage**: <5% idle
- **Disk Usage**: ~400MB installed

### Tips for Best Performance

1. Close unused projects
2. Clear browser cache periodically
3. Restart app if memory usage grows
4. Close API docs when not needed

## Security

- **Database**: Encrypted SQLite
- **Passwords**: Hashed with bcryptjs
- **API**: JWT authentication
- **Data**: Stored locally by default
- **Updates**: Signed and verified

## Updates

The app checks for updates on startup. If an update is available:

1. A notification will appear
2. Click "Update" to download and install
3. App will restart with new version

Updates are downloaded in background and installed when you restart.

## Uninstallation

### Windows

1. Open Control Panel → Programs → Programs and Features
2. Find "Valyxo"
3. Click "Uninstall"
4. App data will be preserved in AppData

### macOS

1. Open Applications folder
2. Find "Valyxo"
3. Drag to Trash

### Linux

**AppImage**: Simply delete the file

**Debian/Ubuntu**:
```bash
sudo apt remove valyxo
```

## Development Commands

```bash
npm run start          # Run production build
npm run dev            # Development with hot reload
npm run build          # Build all platforms
npm run build:win      # Build Windows only
npm run build:mac      # Build macOS only
npm run build:linux    # Build Linux only
npm run pack           # Pack without publishing
npm run dist           # Publish to dist/
```

## Building Installers

### Windows Installer (.exe)

The installer includes:
- Auto-start on login
- System integration
- Quick uninstall
- Start menu shortcuts
- Desktop shortcuts

### macOS App (.dmg)

Includes:
- Code signing
- Notarization (for Big Sur+)
- Drag-to-install
- Auto-launch

### Linux AppImage

Includes:
- Single executable
- No dependencies required
- Portable across distros

## Contributing

To contribute:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Make changes
4. Test thoroughly
5. Commit changes
6. Push to branch
7. Open Pull Request

## License

MIT License - See LICENSE file

## Support

- **Documentation**: https://github.com/valyxo/docs
- **Issues**: https://github.com/valyxo/issues
- **Discussions**: https://github.com/valyxo/discussions
- **Email**: support@valyxo.dev

## Changelog

### v0.41.0 (Initial Release)

**Features:**
- Desktop application with embedded backend
- System tray integration
- Custom titlebar and menu
- Windows, macOS, Linux support
- Auto-update system
- Project and script management
- Real-time metrics
- API documentation access

**Known Issues:**
- First launch may take 10-15 seconds
- WebSocket features not yet implemented
- Some animations disabled on Linux

**Future Updates:**
- Real-time collaboration
- Offline mode
- Plugin system
- Custom themes

---

**Version**: 0.41.0  
**Status**: Stable Release ✓  
**Last Updated**: 2024-01-16
