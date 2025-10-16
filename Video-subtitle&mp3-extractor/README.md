# Video Media Extractor

Extract embedded subtitle/closed caption tracks from MP4 and MOV video files.

## ⚠️ IMPORTANT: FFmpeg Required

**This tool requires FFmpeg to be installed on your system.**

### Quick FFmpeg Installation (Windows):

1. **Download FFmpeg:**
   - Go to: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
   - Or official site: https://ffmpeg.org/download.html

2. **Extract the ZIP:**
   - Extract to `C:\ffmpeg\` (create the folder if needed)

3. **Add to PATH:**
   - Search for "Environment Variables" in Windows search
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Test Installation:**
   - Open Command Prompt and run: `ffmpeg -version`
   - Should show FFmpeg version information

### Alternative: Place in Standard Locations

If you don't want to modify PATH, place `ffmpeg.exe` in one of these folders:
- `C:\ffmpeg\bin\ffmpeg.exe`
- `C:\Program Files\FFmpeg\bin\ffmpeg.exe`
- `C:\Program Files (x86)\FFmpeg\bin\ffmpeg.exe`

## Usage

### Method 1: Batch File (Recommended)
```batch
extract_cc.bat "C:\Users\xiang\Downloads\G22_F A1 OP video.MOV"
```

### Method 2: Direct Python
```batch
py cc_extractor.py "C:\Users\xiang\Downloads\G22_F A1 OP video.MOV"
```

### Method 3: Custom Output Directory
```batch
extract_cc.bat "video.mp4" "C:\My Captions"
```

## Output

- **Default Location**: `extracted_captions/` folder in the same directory as the video
- **File Naming**: `{video_name}_{language}_{codec}.srt`
- **Example**: `G22_F_A1_OP_video_eng_mov_text.srt`

## Supported Subtitle Types

- **Embedded Subtitles**: Subtitles embedded in the video file
- **Closed Captions**: CEA-608/708 closed caption data
- **Movie Text**: QuickTime mov_text subtitles
- **Other Formats**: Various subtitle codecs supported by FFmpeg

## Troubleshooting

### "FFmpeg not found" Error
- Install FFmpeg and add to PATH
- Or place `ffmpeg.exe` in a standard location

### "No subtitle tracks found" Message
- Video may not contain embedded subtitles
- Subtitles might be burned into the video (not extractable)
- Try a different video file

### Extraction Fails
- Check video file is not corrupted
- Ensure FFmpeg version supports the subtitle codec
- Try with a different output format

## Technical Details

The extractor uses FFmpeg to:
1. Analyze video streams to find subtitle tracks
2. Extract each subtitle track individually
3. Convert to SRT format for maximum compatibility
4. Preserve timing and language information

## File Structure

```
Video_Media_Extractor/
├── cc_extractor.py      # Main extraction script
├── extract_cc.bat       # Windows batch file
└── README.md           # This documentation
```

## Credits

- **FFmpeg**: Used for video processing and subtitle extraction (https://ffmpeg.org/)