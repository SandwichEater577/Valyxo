# Building Valyxo Desktop Application

Complete guide for building Valyxo for Windows, macOS, and Linux.

## Prerequisites

- **Node.js**: 16.x or higher
- **npm**: 7.x or higher
- **Git**: Latest version

### Platform-Specific Requirements

**Windows:**
- Windows 7 or higher
- Visual Studio Build Tools 2015+ (for native modules)

**macOS:**
- macOS 10.13 or higher
- Xcode Command Line Tools
- Apple Developer Account (for code signing)

**Linux:**
- Ubuntu 12.04 or higher (or equivalent)
- Build essentials: `sudo apt-get install build-essential`

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/valyxo/valyxo.git
cd valyxo
```

### 2. Install Dependencies

```bash
# Install backend dependencies
cd server
npm install
cd ../

# Install desktop dependencies
cd desktop
npm install
cd ../
```

### 3. Build Backend

```bash
cd server
npm run build  # Or create distribution
cd ../
```

## Building for Windows

### Quick Build

```bash
cd desktop
npm run build:win
```

Outputs:
- `dist/Valyxo-0.41.0.exe` — NSIS Installer
- `dist/Valyxo-0.41.0-portable.exe` — Portable executable

### Customizing Windows Build

Edit `package.json` build config:

```json
"win": {
  "target": [
    { "target": "nsis", "arch": ["x64"] },
    { "target": "portable", "arch": ["x64"] }
  ]
}
```

### Code Signing (Optional)

For production builds, add certificate:

```json
"win": {
  "certificateFile": "path/to/cert.pfx",
  "certificatePassword": "password"
}
```

### Building for Different Architectures

```bash
# 32-bit
npm run build:win -- --ia32

# 64-bit (default)
npm run build:win

# Both architectures
npm run build:win -- --x64 --ia32
```

## Building for macOS

### Prerequisites

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install create-dmg
npm install -g create-dmg
```

### Build

```bash
cd desktop
npm run build:mac
```

Outputs:
- `dist/Valyxo-0.41.0.dmg` — Disk Image
- `dist/Valyxo-0.41.0-mac.zip` — ZIP archive

### Code Signing

For notarization (required for Big Sur+):

1. Get Apple Developer Certificate
2. Configure in `package.json`:

```json
"mac": {
  "certificateFile": "path/to/cert.p12",
  "certificatePassword": "password",
  "identity": "Your Name (ABCDE12345)"
}
```

3. Build and notarize:

```bash
npm run build:mac
# Apple will email you when ready
```

### Universal Binary (Intel + Apple Silicon)

```bash
npm run build:mac -- --universal
```

## Building for Linux

### Prerequisites

```bash
# Debian/Ubuntu
sudo apt-get install build-essential libxss1 libgconf-2-4

# Fedora/RHEL
sudo dnf install gcc g++ make libxss1 libgconf2
```

### Build

```bash
cd desktop
npm run build:linux
```

Outputs:
- `dist/Valyxo-0.41.0.AppImage` — AppImage
- `dist/valyxo_0.41.0_amd64.deb` — Debian package

### AppImage Configuration

Edit `package.json`:

```json
"linux": {
  "target": ["AppImage", "deb"],
  "category": "Development"
}
```

### Creating DEB Package

```bash
npm run build:linux -- --deb
```

Customize in `package.json`:

```json
"deb": {
  "depends": ["libxss1", "libgconf-2-4"],
  "maintainer": "Valyxo <support@valyxo.dev>"
}
```

## Multi-Platform Build

### Build All Platforms

```bash
cd desktop
npm run dist
```

This builds:
- Windows: .exe installer + portable
- macOS: .dmg + .zip
- Linux: AppImage + .deb

### Build Specific Combinations

```bash
# Windows only
npm run build:win

# macOS only
npm run build:mac

# Linux only
npm run build:linux

# Windows + Linux
npm run build -- --win --linux
```

## Development Build

### Development Mode with Hot Reload

```bash
cd desktop
npm run dev
```

This:
1. Starts backend server
2. Opens Electron with DevTools
3. Auto-reloads on code changes

### Production Mode Testing

```bash
npm run start
```

## Packaging Options

### NSIS Installer (Windows)

Highly customizable Windows installer.

Configuration in `package.json`:

```json
"nsis": {
  "oneClick": false,
  "allowToChangeInstallationDirectory": true,
  "createDesktopShortcut": true,
  "createStartMenuShortcut": true,
  "shortcutName": "Valyxo"
}
```

### Portable Executable (Windows)

Single `.exe` file, no installation required.

### DMG (macOS)

Disk image with drag-to-install.

### AppImage (Linux)

Single executable that runs on all Linux distros.

### DEB Package (Linux)

Standard Debian/Ubuntu package with:
- APT integration
- Dependency management
- Uninstall support

## Signing and Notarization

### Windows Code Signing

```bash
# Create certificate
signtool sign /f cert.pfx /p password dist/Valyxo-0.41.0.exe
```

### macOS Notarization

```bash
# Submit for notarization
xcrun altool --notarize-app --file dist/Valyxo-0.41.0.dmg \
  --primary-bundle-id com.valyxo.app \
  -u apple-id@example.com -p @keychain:notarization
```

## Distribution

### GitHub Releases

1. Create release on GitHub
2. Upload built files:
   ```bash
   dist/Valyxo-0.41.0.exe
   dist/Valyxo-0.41.0-portable.exe
   dist/Valyxo-0.41.0.dmg
   dist/Valyxo-0.41.0.AppImage
   dist/valyxo_0.41.0_amd64.deb
   ```

### Auto-Update Server

Configure in `main.js`:

```javascript
autoUpdater.setFeedURL({
  provider: 'github',
  owner: 'valyxo',
  repo: 'valyxo'
});
```

## Troubleshooting

### Build Fails on Windows

```bash
# Clear cache
rm -r dist
rm -r node_modules
npm install

# Try again
npm run build:win
```

### macOS Code Signing Issues

```bash
# List available certificates
security find-identity -v -p codesigning

# Remove quarantine attribute
xattr -rd com.apple.quarantine /Applications/Valyxo.app
```

### Linux AppImage Issues

```bash
# Make executable
chmod +x dist/Valyxo-0.41.0.AppImage

# Run with debug
./dist/Valyxo-0.41.0.AppImage --verbose --no-sandbox
```

### Port 5000 Already in Use

The build script will fail if the backend port is busy.

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

## Size Optimization

### Reducing Bundle Size

Current size: ~300MB (with Node.js runtime)

Options:
- Use `asar` archive format (default)
- Remove dev dependencies
- Tree-shake unused code
- Compress native modules

### Configuration

```json
"build": {
  "asar": true,
  "files": [
    "src/**/*",
    "assets/**/*"
  ]
}
```

## Performance

### Build Times

Typical build times:
- Windows: 1-2 minutes
- macOS: 2-3 minutes
- Linux: 1-2 minutes
- All platforms: 5-10 minutes

### Improving Build Speed

1. Use SSD for faster I/O
2. Increase Node memory:
   ```bash
   NODE_OPTIONS=--max-old-space-size=4096 npm run build
   ```
3. Build single platform at a time
4. Cache dependencies

## CI/CD Integration

### GitHub Actions

Example workflow:

```yaml
name: Build
on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: 16
      - run: npm install
      - run: npm run build
      - uses: actions/upload-artifact@v2
        with:
          name: dist-${{ matrix.os }}
          path: desktop/dist/
```

## Security Checklist

- [ ] Code signing certificate obtained
- [ ] Notarization setup for macOS
- [ ] Update server configured
- [ ] Dependencies audited
- [ ] Security headers enabled
- [ ] CORS configured
- [ ] Database encrypted
- [ ] Logs sanitized

## Release Checklist

Before release:

- [ ] Update version in `package.json`
- [ ] Update `CHANGELOG.md`
- [ ] Test on all platforms
- [ ] Run security audit
- [ ] Build all platforms
- [ ] Sign all binaries
- [ ] Create GitHub release
- [ ] Publish release notes
- [ ] Update documentation

## Next Steps

1. Build test version: `npm run build`
2. Test on target platform
3. Collect feedback
4. Fix issues
5. Create release build
6. Publish to app stores (optional)

## Support

- **Build Issues**: Check `TROUBLESHOOTING.md`
- **Questions**: Open GitHub issue
- **Contributions**: Submit PR

---

**Last Updated**: 2024-01-16  
**Valyxo Version**: 0.41.0  
**Electron Version**: 27.0.0
