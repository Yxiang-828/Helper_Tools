#!/usr/bin/env python3
"""
Audio to Text Converter using OpenAI Whisper
Converts MP3 audio files to text transcripts.
"""

import sys
import argparse
import os
from pathlib import Path
import whisper

# Add ffmpeg to PATH for Whisper
ffmpeg_path = r"C:\ffmpeg\bin"
if ffmpeg_path not in os.environ['PATH']:
    os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']

def audio_to_text(audio_path, model_size="base", output_dir=None, language="en"):
    """
    Convert audio file to text using Whisper.

    Args:
        audio_path (str): Path to the audio file (MP3, WAV, etc.)
        model_size (str): Whisper model size (tiny, base, small, medium, large)
        output_dir (Path): Directory to save the transcript

    Returns:
        str: Path to the generated transcript file
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if output_dir is None:
        output_dir = Path(__file__).parent / "output_transcripts"
    output_dir.mkdir(exist_ok=True)

    # Load Whisper model
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    # Transcribe audio
    print(f"Transcribing: {audio_path.name}")
    if language == "auto":
        result = model.transcribe(str(audio_path))
    else:
        result = model.transcribe(str(audio_path), language=language)

    # Save transcript
    transcript_path = output_dir / f"{audio_path.stem}_transcript.md"
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(f"# Audio Transcript: {audio_path.name}\n\n")
        f.write(f"**File:** {audio_path.name}\n")
        f.write(f"**Model:** {model_size}\n")
        f.write(f"**Language:** {language}\n")
        f.write(f"**Generated:** {Path(__file__).parent.stem} tool\n\n")
        f.write("## Transcript\n\n")
        f.write(str(result["text"]))
        f.write("\n")

    print(f"Transcript saved to: {transcript_path}")
    return str(transcript_path)

def main():
    parser = argparse.ArgumentParser(description="Convert audio files to text using Whisper")
    parser.add_argument("audio_file", help="Path to the audio file (MP3, WAV, etc.)")
    parser.add_argument("--model", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--output-dir", help="Output directory for transcripts")
    parser.add_argument("--language", default="en",
                       choices=["en", "zh", "ja", "es", "fr", "de", "ko", "auto"],
                       help="Language for transcription (default: en, use 'auto' for detection)")

    args = parser.parse_args()

    try:
        transcript_path = audio_to_text(args.audio_file, args.model, args.output_dir, args.language)
        print(f"Success! Transcript: {transcript_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()