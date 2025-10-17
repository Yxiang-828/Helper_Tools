# Helper Tools Collection

**Personal CLI tools for advanced developers. Fast, offline media processing. Not for casual users.**

## Why Helper Tools?

I built this for myself and fellow developers who understand code. These are power-user tools that assume programming knowledge and command-line comfort. Not beginner-friendly - designed for those who can read and modify source code.

- Fast: CLI tools that process in seconds
- Offline: No internet required after setup
- No Ads: Pure functionality
- CLI: Command-line interfaces for automation
- Focused: Each tool does one thing well
- Minimal: Few dependencies

**Rule**: If it requires a browser or takes >30 seconds to set up, it's not included.

## Contents

- [Audio to Text Transcriber](#audio-to-text-transcriber)
- [Video to GIF Converter](#video-to-gif-converter)
- [Video Subtitle & MP3 Extractor](#video-subtitle--mp3-extractor)
- [AMD GPU Image Upscaler](#amd-gpu-image-upscaler)
- [AMD GPU Video Upscaler](#amd-gpu-video-upscaler)
- [File Scanner](#file-scanner)
- [Git Auto-Push](#git-auto-push)
- [Unity Image Extractor](#unity-image-extractor)

## Available Tools

### Audio to Text Transcriber
Convert audio files to text transcripts using OpenAI Whisper

Turns MP3, WAV, M4A into searchable text. Works offline after model download.

```bash
mp3-to-txt.bat "path\to\audio.mp3"
```

Features:
- Multiple AI models (tiny to large)
- GPU acceleration (3-5x faster)
- 99+ languages
- Batch processing

Setup: `pip install openai-whisper torch`

[Full Documentation](Audio_to_Text_Transcriber/README.md)

---

### Video to GIF Converter
Convert MP4 videos to optimized GIFs with size/speed constraints

Creates GIFs with exact file size and playback speed limits.

```bash
mp4togif.bat
```

Features:
- Size constraint optimization
- Speed ratio control
- Automatic resolution adjustment
- Interactive interface

Setup: `pip install moviepy pillow`

[Full Documentation](Video_to_GIF_Converter/README.md)

---

### Video Subtitle & MP3 Extractor
Extracts subtitles AND MP3 audio from videos.

What it does:
- Extracts embedded subtitle tracks as SRT files
- Always extracts audio as MP3
- Produces both outputs when subtitles exist
- Produces MP3 audio when no subtitles exist

```bash
extract_cc.bat "path\to\video.mp4"
```

Setup: FFmpeg required

[Full Documentation](Video-subtitle&mp3-extractor/README.md)

---

### AMD GPU Image Upscaler
AI-powered image enhancement with AMD GPU acceleration

Upscales and sharpens images using Real-ESRGAN and EDSR models.

```bash
image_upscaler.bat
```

Features:
- Real-ESRGAN and EDSR models
- 2x, 3x, 4x scaling
- AMD GPU optimized
- Vulkan acceleration

Setup: Models download automatically

[Full Documentation](image_upscaler/README.md)

---

### AMD GPU Video Upscaler
AI-powered video enhancement with AMD GPU acceleration

Upscales videos using Real-ESRGAN AI or fast FFmpeg methods, optimized for AMD GPUs.

```bash
video_upscaler.bat
```

Features:
- Real-ESRGAN AI upscaling (frame-by-frame)
- FFmpeg hardware encoding with AMD VCE
- 2x, 3x, 4x scaling
- MP4 and GIF output
- Automatic CPU fallback for high resolution
- Audio preservation

Setup: FFmpeg and Real-ESRGAN Vulkan required

[Full Documentation](video_upscaler/README.md)

---

### File Scanner
Find and remove large files to reclaim disk space - 10-50x faster than standard Windows tools

Built for Windows storage optimization. Rapidly identifies the largest files consuming your disk space, generates interactive deletion scripts with safety confirmations. Employs min-heap algorithms and .NET Framework APIs to scan entire drives in minutes. Scans 469,385 files in 151 seconds (3,107 files/sec) with O(M log K) time complexity.

```bash
.\file_scanner.ps1 -FileType video -TopCount 50
.\file_scanner.ps1 -CustomExtensions @('.exe', '.dll')
.\file_scanner.ps1 -RootPath "D:\Games" -FileType game
```

Core Features:
- Scan entire C:\ drive in 2-3 minutes (vs 40+ minutes with Windows Explorer)
- Interactive deletion script with safety confirmations (preview files, type YES to confirm)
- Identify top N largest files instantly for storage reclamation
- 9 preset file type categories (media, video, audio, document, archive, code, game, all)
- Custom extension support for specialized file hunting
- Real-time progress reporting (files/second throughput)
- UTF-8 output supporting international filenames

Storage Optimization:
- Find forgotten large video recordings taking gigabytes
- Identify duplicate downloads in multiple locations
- Locate old game installations and assets
- Discover build artifacts from development projects
- Clean up temporary files and caches

Technical Specifications:
- Time Complexity: O(M log K) where M = total files, K = top count
- Space Complexity: O(K + D) where D = directory count
- Memory Footprint: <1MB for typical scans
- Throughput: 3,000-8,800 files/second depending on I/O patterns

Performance Comparison vs Get-ChildItem:
- Full C:\ scan: 151s vs 2,500s+ (16x faster)
- Memory usage: <1MB vs 50MB+ (50x reduction)

Primary Use Cases:
- **Free up disk space**: Find and delete large files consuming storage
- **Storage auditing**: Identify what's taking up space on your drives
- **Pre-cleanup analysis**: Review largest files before manual deletion
- **Game management**: Locate large game installations and decide what to uninstall
- **Development cleanup**: Find build artifacts, node_modules, compiled binaries
- **Media library cleanup**: Identify large videos, photos, music files for archiving

Why This Tool Exists:
Windows Explorer is painfully slow for finding large files across entire drives. This tool was built to solve that specific problem - quickly scan massive filesystems, identify storage hogs, and safely remove them with interactive confirmation. No GUI bloat, no waiting 40 minutes for Windows Search to index.

Technical Architecture (for developers):
- Direct .NET System.IO.Directory.EnumerateFiles() API integration
- Min-heap implemented via SortedSet<T> with custom comparator (O(log K) insertion)
- Queue<string> for explicit BFS control flow (prevents stack overflow)
- Extension pre-filtering reduces FileInfo allocation by 85% (29.9s saved)
- Path exclusions for system directories (Windows, Program Files)

Setup: PowerShell 5.1+, .NET Framework 4.5+ (bundled with Windows 8+)

[Full Technical Documentation](File_Scanner/README.md)

---

### Git Auto-Push
Fast git workflow without commit hassle

Auto-commits and pushes all changes with timestamps for tracking. Skip the commit message drama.

```bash
pushgit.bat
# or with custom message:
pushgit.bat "my changes"
```

Features:
- Automatic timestamp tracking
- One-command push workflow
- No staging required
- Maintains change history

Setup: Git repository required

### Unity Image Extractor
Extract images from Unity3D bundle files

Scans Unity game files for embedded textures and sprites, extracts them as PNG images.

```bash
extract_unity.bat "path\to\unity3d_file_or_directory"
```

Features:
- Extracts Texture2D and Sprite assets
- Recursive directory scanning
- PNG output format
- Preserves source organization

Setup: `pip install UnityPy Pillow`

## Where Do My Files Go?

Each tool saves outputs in predictable locations:

- Audio Transcripts → `Audio_to_Text_Transcriber/output_transcripts/`
- GIFs → `Video_to_GIF_Converter/extracted_gifs/`
- Subtitles → `Video-subtitle&mp3-extractor/extracted_captions/`
- MP3 Audio → `Video-subtitle&mp3-extractor/extracted_audio/`
- Upscaled Images → `image_upscaler/output/`
- Unity Images → `Unity_Image_Extractor/extracted_images/`

All outputs include the original filename with descriptive suffixes.

---

## Quick Start

1. Clone or download this repository
2. Pick your tool from the list above
3. Install dependencies (most tools need `pip install`)
4. Run the batch file
5. Specify your input files

## System Requirements

- OS: Windows 10/11
- Python: 3.7+
- Hardware: Modern CPU/GPU recommended
- Storage: 2-5GB for AI models

## Design Philosophy

### Speed First
Every tool is optimized for performance. Results in seconds, not minutes.

### Offline by Default
No internet required for core functionality. AI models download once and work forever.

### CLI Superiority
Command-line interfaces enable automation, scripting, and integration.

### Minimal Dependencies
Each tool uses as few external libraries as possible.

### Cross-Platform Ready
While currently Windows-focused, all tools are designed to work on Linux/Mac with minimal changes.

## Personal Project

This is a personal collection of tools I built for my own development workflow. Not accepting external contributions or feature requests. Use at your own risk - these tools are designed for advanced developers who can troubleshoot and modify code.

## License

All tools are provided as-is for personal use only. No warranties, no support. Each tool may have its own license - check individual READMEs.

---

Built for me. By me. For developers like me.</content>
<parameter name="filePath">c:\Program Files (x86)\helper_tools\README.md