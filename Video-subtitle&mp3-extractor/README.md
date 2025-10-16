# Video Subtitle & MP3 Extractor

Extract subtitles from videos, or if none exist, extract MP3 audio.

## What It Does

- Checks video for embedded subtitle tracks
- If subtitles exist: extracts them as SRT files to extracted_captions/
- If no subtitles: extracts audio as MP3 to extracted_audio/
- Always produces output - never fails empty

## Usage

```bash
extract_cc.bat "path\to\video.mp4"
```

## Requirements

FFmpeg installed and accessible.

Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
Extract to C:\ffmpeg\bin\ or add to PATH.

## What Happens

- Always extracts MP3 audio to extracted_audio/
- If subtitles exist: also extracts SRT files to extracted_captions/
- Produces at least MP3 output, plus subtitles if available