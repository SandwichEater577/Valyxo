# Valyxo Desktop - Icon Assets

## Required Icons

### Application Icon (icon.png)
- **Size**: 256x256 pixels
- **Format**: PNG with transparency
- **Usage**: Main app icon (taskbar, app switcher, installer)
- **Path**: `assets/icon.png`

### Tray Icon (icon-small.png)
- **Size**: 16x16 or 32x32 pixels
- **Format**: PNG with transparency
- **Usage**: System tray icon
- **Path**: `assets/icon-small.png`

## How to Create Icons

### Option 1: Use Online Tools

1. Visit: https://www.favicon-generator.org/ or similar
2. Upload your Valyxo logo
3. Download as PNG
4. Resize to required dimensions
5. Save to `assets/`

### Option 2: Using ImageMagick

```bash
# Resize logo to app icon
convert logo.png -resize 256x256 assets/icon.png

# Resize for tray icon
convert logo.png -resize 32x32 assets/icon-small.png
```

### Option 3: Using Python PIL

```python
from PIL import Image

# Create app icon
img = Image.open('logo.png')
img = img.resize((256, 256), Image.Resampling.LANCZOS)
img.save('assets/icon.png')

# Create tray icon
img_small = img.resize((32, 32), Image.Resampling.LANCZOS)
img_small.save('assets/icon-small.png')
```

### Option 4: Using GIMP

1. Open logo in GIMP
2. Image → Scale Image
3. Set size to 256x256
4. File → Export As `assets/icon.png`
5. Repeat for 32x32 tray icon

## Design Guidelines

### Color Palette

Use Valyxo colors:
- Primary: `#7cffb2` (Neon Green)
- Secondary: `#5ed9ff` (Cyan)
- Accent: `#b58cff` (Purple)
- Dark: `#0a0e27` (Dark Blue)

### Style

- Modern, clean design
- Works well at small sizes (32x32)
- Clear on dark background
- Recognizable at a glance

### Best Practices

- Avoid thin lines (hard to see at small sizes)
- Use solid colors or simple gradients
- Ensure contrast with dark background
- Test at actual size in app

## Placeholder Generation

If you don't have an icon yet, generate a temporary one:

```bash
# Using ffmpeg to create a simple icon
ffmpeg -f lavfi -i color=c='#7cffb2':s=256x256 -frames:v 1 assets/icon.png

# Using ImageMagick
convert -size 256x256 xc:'#0a0e27' -fill '#7cffb2' -draw "text 50,128 'V'" assets/icon.png
```

## Icon Formats

### PNG (Recommended)

- ✓ Transparency support
- ✓ Lossless compression
- ✓ Universal compatibility
- ✓ Works on all platforms

### ICO (Windows)

Optional: Create for enhanced Windows support

```bash
convert assets/icon.png assets/icon.ico
```

## macOS Specific

For macOS builds, also create:

**icon.icns**: 
```bash
# Using Python
python3 -c "
from PIL import Image
img = Image.open('assets/icon.png')
img.save('assets/icon.icns')
"
```

## Testing Icons

1. Place icons in `assets/` folder
2. Run: `npm run dev`
3. Check:
   - App icon in taskbar
   - Tray icon in system tray
   - Window title bar icon
   - App switcher display

## File Structure

```
desktop/
└── assets/
    ├── icon.png              # Main app icon (256x256)
    ├── icon-small.png        # Tray icon (32x32)
    ├── icon.icns             # macOS (optional)
    └── icon.ico              # Windows (optional)
```

## Notes

- Icons must be in PNG format for Electron Builder
- Transparency should be preserved
- Test on actual background colors
- Ensure consistency across platforms

## Resources

- **Design Tools**: Figma, Photoshop, GIMP, Paint.NET
- **Icon Generators**: Favicon Generator, Icon8, Iconizer
- **Color Tools**: ColorHexa, Adobe Color Wheel

---

**Current Status**: Placeholder icons needed
**Action**: Add your Valyxo logo to `assets/` folder
