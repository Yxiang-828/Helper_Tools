# Background Remover

A simple tool to remove backgrounds from images in bulk using AI.

## Features

- **Automatic Removal**: Uses the `rembg` library for high-quality background removal.
- **Bulk Processing**: Processes all images in the `input` folder at once.
- **Output Handling**: Saves results to `output` folder with `_nobg` suffix.
- **Supports**: PNG, JPG, JPEG, BMP, WEBP.
- **Transparent Output**: All output images are saved as PNG with transparency.

## Quick Start

### Windows (Recommended)
1. Place images in the `Background_Remover/input` folder.
2. Run `remove_bg.bat` from the root directory.

### Manual Setup
If you prefer to run the script manually:

1. Install dependencies:
   ```bash
   pip install rembg pillow
   ```
2. Run the script:
   ```bash
   python Background_Remover/background_remover.py
   ```

## Requirements

- Python 3.7+
- `rembg`
- `Pillow` (PIL)

## Notes

- The first run might take a moment to download the necessary AI models.
- Ensure you have a stable internet connection for the first run.
