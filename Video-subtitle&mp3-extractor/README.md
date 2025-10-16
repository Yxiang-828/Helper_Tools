# Video Subtitle & Audio Extractor

**Extract embedded subtitles, closed captions, and audio tracks from video files using FFmpeg - perfect for content creators and accessibility work**

Pull out SRT subtitles, VTT captions, and MP3 audio from MP4, MOV, and other video formats. Essential tool for translation, accessibility, content repurposing, and media production.

## ⚡ Key Features

- 🎯 **Multi-Format Support**: SRT, VTT, WebVTT subtitle extraction
- 🔊 **Audio Extraction**: Convert video audio to MP3/WAV
- 🌍 **Language Detection**: Automatic language tagging and organization
- 📁 **Batch Processing**: Process multiple videos automatically
- 🔍 **Smart Detection**: Finds all embedded subtitle tracks
- ⚡ **FFmpeg Powered**: Industry-standard video processing

## Quick Start

```bash
# Extract subtitles (requires FFmpeg)
extract_cc.bat "path\to\video.mp4"
```

## Installation

### FFmpeg Setup (Required)

**This tool requires FFmpeg. Here's the fastest way to install it:**

#### Option 1: Quick Install (Recommended)
1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extract to: `C:\ffmpeg\` (create folder)
3. Add to PATH or place in standard locations

#### Option 2: Manual PATH Setup
1. Download FFmpeg from above
2. Extract ZIP to `C:\ffmpeg\`
3. Open System Properties → Advanced → Environment Variables
4. Find "Path" → Edit → New → Add: `C:\ffmpeg\bin`
5. Restart command prompt

#### Option 3: Standard Locations
Place `ffmpeg.exe` in any of these folders (no PATH needed):
- `C:\ffmpeg\bin\ffmpeg.exe`
- `C:\Program Files\FFmpeg\bin\ffmpeg.exe`
- `C:\Program Files (x86)\FFmpeg\bin\ffmpeg.exe`

**Test Installation:**
```cmd
ffmpeg -version
```
Should show FFmpeg version information.

### Python Dependencies
```bash
pip install pathlib  # Usually pre-installed with Python
```

## Usage Examples

### Extract Subtitles
```cmd
REM Basic subtitle extraction
extract_cc.bat "C:\Videos\movie.mp4"

REM Extract to custom directory
extract_cc.bat "C:\Videos\movie.mp4" "C:\Subtitles"
```

### Batch Processing
```bash
REM Process all MP4 files in directory
for %f in (*.mp4) do extract_cc.bat "%f"
```

## Output Formats

### Subtitles
- **Format**: SRT (SubRip), VTT (WebVTT)
- **Naming**: `{video_name}_{language}_{codec}.srt`
- **Location**: `extracted_captions/` folder
- **Example**: `movie_eng_mov_text.srt`

### Audio
- **Format**: MP3 (default), WAV
- **Naming**: `{video_name}_audio.mp3`
- **Location**: `extracted_audio/` folder
- **Quality**: Original bitrate preserved

## Supported Subtitle Types

| Type | Description | Common In |
|------|-------------|-----------|
| **Embedded** | Subtitles inside video file | MP4, MOV, MKV |
| **Closed Captions** | CEA-608/708 broadcast captions | TV recordings, streams |
| **Movie Text** | QuickTime mov_text format | Apple MOV files |
| **DVD Subtitles** | VOB subtitle tracks | DVD rips |
| **PGS Subtitles** | Blu-ray format | Blu-ray rips |

## Language Support

- **Auto-Detection**: Extracts language codes from video metadata
- **Common Codes**: `eng` (English), `spa` (Spanish), `fra` (French), etc.
- **Multi-Language**: Extracts all available language tracks
- **Organization**: Files named with language codes for easy sorting

## Technical Details

### FFmpeg Commands Used

**Subtitle Extraction:**
```bash
ffmpeg -i "input.mp4" -map 0:s:0 -c:s text "output.srt"
```

**Audio Extraction:**
```bash
ffmpeg -i "input.mp4" -vn -acodec libmp3lame "output.mp3"
```

### Processing Pipeline
1. **Stream Analysis**: FFmpeg probes video for subtitle/audio tracks
2. **Track Identification**: Maps stream indices and metadata
3. **Format Conversion**: Converts to SRT/VTT for subtitles
4. **Quality Preservation**: Maintains original audio quality
5. **Organization**: Saves files with descriptive names

## Troubleshooting

### "FFmpeg not found"
```
Solutions:
1. Install FFmpeg and add to PATH
2. Place ffmpeg.exe in standard locations
3. Check installation: ffmpeg -version
```

### "No subtitle tracks found"
```
Possible causes:
- Video has no embedded subtitles
- Subtitles are burned into video (not extractable)
- Different subtitle format not supported
- Try different video file
```

### "Extraction failed"
```
Solutions:
- Check video file is not corrupted
- Ensure sufficient disk space
- Try with administrator privileges
- Update FFmpeg to latest version
```

### "Audio extraction slow"
```
Tips:
- MP3 is faster than WAV
- Shorter videos process faster
- Close other applications for better performance
```

## Performance Guide

- **Subtitle Extraction**: 10-30 seconds per video
- **Audio Extraction**: 1-5 minutes for long videos
- **Batch Processing**: Sequential processing (one file at a time)
- **Memory Usage**: Low (100-500MB depending on video size)

## Use Cases

- 🎬 **Content Creation**: Extract subtitles for editing/reuse
- 🌍 **Translation**: Get source subtitles for translation work
- ♿ **Accessibility**: Extract captions for accessibility compliance
- 📱 **Social Media**: Create subtitle files for video posts
- 🎵 **Audio Production**: Extract audio for remixing/podcasting
- 📚 **Education**: Create transcripts for educational content
- 🎭 **Media Production**: Separate audio/video components

## Advanced Usage

### Custom FFmpeg Options
```bash
# Extract specific subtitle track
ffmpeg -i "video.mp4" -map 0:s:1 -c:s text "subtitles.srt"

# Extract audio with custom bitrate
ffmpeg -i "video.mp4" -vn -acodec libmp3lame -ab 192k "audio.mp3"
```

### Language Filtering
```bash
# Extract only English subtitles
ffmpeg -i "video.mp4" -map 0:s:m:language:eng -c:s text "english.srt"
```

### Batch Script Customization
Edit `extract_cc.bat` to customize output directories, formats, or add additional processing.

## File Structure

```
Video_Media_Extractor/
├── cc_extractor.py      # Main extraction script
├── extract_cc.bat       # Subtitle extraction batch file
├── extract_audio.bat    # Audio extraction batch file (if exists)
└── README.md           # This documentation
```

## Dependencies

- **FFmpeg**: Core video processing engine
- **Python**: 3.6+ (for script execution)
- **pathlib**: File path handling (built-in)

## Credits

- **FFmpeg**: https://ffmpeg.org/ (Video processing powerhouse)
- **Python Community**: pathlib and subprocess modules

---

**Ready to extract? Install FFmpeg, run `extract_cc.bat`, and start pulling subtitles from videos!** 🎬➡️📝