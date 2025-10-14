#!/usr/bin/env python3
"""
Closed Caption Extractor for MP4/MOV Videos
Extracts embedded subtitle tracks from video files and saves them as SRT/VTT files
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class CCExtractor:
    def __init__(self):
        self.ffmpeg_path = self.find_ffmpeg()

    def find_ffmpeg(self):
        """Find FFmpeg executable"""
        # Try common FFmpeg locations
        common_paths = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\FFmpeg\bin\ffmpeg.exe",
            "ffmpeg"  # In PATH
        ]

        for path in common_paths:
            try:
                result = subprocess.run([path, "-version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✓ Found FFmpeg: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                continue

        return None

    def get_subtitle_tracks(self, video_path):
        """Get information about subtitle tracks in the video"""
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg and add it to your PATH.")

        cmd = [
            self.ffmpeg_path, "-i", video_path,
            "-f", "ffmetadata", "-"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while analyzing video file")

        # Also try to get stream information
        cmd_streams = [self.ffmpeg_path, "-i", video_path]
        try:
            result_streams = subprocess.run(cmd_streams, capture_output=True, text=True, timeout=30)
            stderr_output = result_streams.stderr
        except subprocess.TimeoutExpired:
            stderr_output = ""

        # Parse subtitle streams from stderr
        subtitle_tracks = []
        lines = stderr_output.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()
            if 'Subtitle:' in line or 'Stream #' in line and 'Subtitle' in line:
                # Extract stream index and codec info
                if 'Stream #' in line:
                    try:
                        # Parse stream info like: "Stream #0:3(eng): Subtitle: mov_text (tx3g / 0x67337874), 0 kb/s (default)"
                        stream_part = line.split('Stream #')[1].split(':')[0:2]
                        stream_index = f"0:{stream_part[1]}" if len(stream_part) > 1 else "unknown"

                        # Look for language in parentheses
                        lang_start = line.find('(')
                        lang_end = line.find(')')
                        language = "unknown"
                        if lang_start != -1 and lang_end != -1 and lang_end > lang_start:
                            language = line[lang_start+1:lang_end]

                        # Look for codec info
                        codec = "unknown"
                        if 'Subtitle:' in line:
                            codec_part = line.split('Subtitle:')[1].split(',')[0].strip()
                            codec = codec_part

                        subtitle_tracks.append({
                            'index': stream_index,
                            'language': language,
                            'codec': codec,
                            'description': line
                        })
                    except:
                        continue

        return subtitle_tracks

    def extract_subtitles(self, video_path, track_index, output_path, format='srt'):
        """Extract subtitles from a specific track"""
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg and add it to your PATH.")

        cmd = [
            self.ffmpeg_path, "-i", video_path,
            "-map", f"0:{track_index}",
            "-f", format,
            output_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return True
            else:
                print(f"FFmpeg error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("Timeout while extracting subtitles")
            return False

    def extract_all_subtitles(self, video_path, output_dir=None):
        """Extract all subtitle tracks from a video file"""
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Set output directory
        if output_dir is None:
            output_dir = video_path.parent / "extracted_captions"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(exist_ok=True)

        print(f"🔍 Analyzing video: {video_path.name}")

        # Get subtitle tracks
        subtitle_tracks = self.get_subtitle_tracks(str(video_path))

        if not subtitle_tracks:
            print("❌ No subtitle tracks found in this video")
            return []

        print(f"📋 Found {len(subtitle_tracks)} subtitle track(s):")
        for i, track in enumerate(subtitle_tracks, 1):
            print(f"  {i}. Stream {track['index']} - {track['language']} ({track['codec']})")

        extracted_files = []

        # Extract each subtitle track
        for track in subtitle_tracks:
            stream_index = track['index'].split(':')[-1]  # Get just the number part
            language = track['language'] or 'unknown'
            codec = track['codec'].replace('/', '_').replace(' ', '_')

            # Generate output filename
            base_name = video_path.stem
            output_filename = f"{base_name}_{language}_{codec}.srt"
            output_path = output_dir / output_filename

            print(f"\n📝 Extracting track {track['index']} ({language})...")

            if self.extract_subtitles(str(video_path), stream_index, str(output_path)):
                print(f"✅ Saved: {output_path.name}")
                extracted_files.append(str(output_path))
            else:
                print(f"❌ Failed to extract track {track['index']}")

        return extracted_files

def main():
    print("🎬 Closed Caption Extractor for MP4/MOV Videos")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("Usage: python cc_extractor.py <video_file> [output_directory]")
        print("Example: python cc_extractor.py video.mp4")
        print("Example: python cc_extractor.py video.mp4 ./captions")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        extractor = CCExtractor()

        if not extractor.ffmpeg_path:
            print("❌ FFmpeg not found!")
            print("Please install FFmpeg and add it to your PATH, or place ffmpeg.exe in:")
            print("  - C:\\ffmpeg\\bin\\")
            print("  - C:\\Program Files\\FFmpeg\\bin\\")
            print("Download from: https://ffmpeg.org/download.html")
            sys.exit(1)

        extracted_files = extractor.extract_all_subtitles(video_path, output_dir)

        if extracted_files:
            print(f"\n✅ Extraction complete! {len(extracted_files)} subtitle file(s) created:")
            for file in extracted_files:
                print(f"  📄 {file}")
        else:
            print("\n❌ No subtitles were extracted")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()