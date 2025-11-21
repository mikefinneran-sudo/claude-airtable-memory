# Logo Extraction Task

## Current Logo Asset
- **File**: Geometric raccoon mascot with "FRAMNE SIGNAL" text
- **Colors**: Purple, cyan/turquoise, blue gradient
- **Background**: Dark navy (#0a1628 or similar)

## Required Outputs

### 1. Logo Extraction (Immediate)
- [ ] Crop raccoon mascot free of text
- [ ] Remove background (transparent PNG)
- [ ] Export multiple sizes:
  - 512x512 (favicon, app icon)
  - 256x256 (social media)
  - 128x128 (small UI elements)
  - 64x64 (tiny icons)

### 2. Logo Variations
- [ ] **Primary**: Full color on transparent
- [ ] **White**: All white version for dark backgrounds
- [ ] **Black**: All black version for light backgrounds
- [ ] **Monotone Purple**: Single purple color
- [ ] **Monotone Cyan**: Single cyan color

### 3. File Formats Needed
- PNG (transparent) - for web
- SVG (vector) - for scaling
- ICO - for favicon
- ICNS - for Mac app icon (if needed)

## Color Palette (from image)
```
Purple range: #8B5CF6, #A78BFA, #C4B5FD
Cyan range: #67E8F9, #22D3EE, #06B6D4
Blue range: #3B82F6, #2563EB, #1E40AF
Background: #0A1628 (dark navy)
```

## Tools to Use
- **Figma** - Vector editing and export
- **Photoshop/GIMP** - Raster editing if needed
- **ImageMagick** - Batch processing and conversions
- **Online**: remove.bg or similar for quick background removal

## Priority
**HIGH** - Needed before website can be finalized
