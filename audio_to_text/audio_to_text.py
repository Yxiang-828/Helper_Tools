#!/usr/bin/env python3
"""
Audio to Text Converter using Speech Recognition
Converts MP3 audio files to text transcripts using Google Speech API.
"""

import sys
import argparse
import os
from pathlib import Path
import speech_recognition as sr
from pydub import AudioSegment

# Add ffmpeg to PATH
ffmpeg_path = r"C:\ffmpeg\bin"
if ffmpeg_path not in os.environ['PATH']:
    os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']

def audio_to_text(audio_path, output_dir=None):
    """
    Convert audio file to text using Speech Recognition.

    Args:
        audio_path (str): Path to the audio file (MP3, WAV, etc.)
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

    # Load audio file
    print(f"Loading audio: {audio_path.name}")
    audio = AudioSegment.from_file(str(audio_path))

    # Convert to WAV for better recognition
    wav_path = output_dir / f"{audio_path.stem}_temp.wav"
    audio.export(str(wav_path), format="wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Split audio into 30-second chunks (Google limit)
    chunk_length_ms = 30 * 1000  # 30 seconds
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    full_text = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")

        # Export chunk to temp WAV
        chunk_wav_path = output_dir / f"{audio_path.stem}_chunk_{i}.wav"
        chunk.export(str(chunk_wav_path), format="wav")

        # Recognize chunk
        with sr.AudioFile(str(chunk_wav_path)) as source:
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)
                full_text.append(text)
            except sr.UnknownValueError:
                print(f"  Chunk {i+1}: Could not understand")
            except sr.RequestError as e:
                print(f"  Chunk {i+1}: API error - {e}")
                break  # Stop on API errors

        # Clean up chunk
        chunk_wav_path.unlink()

    # Clean up temp file
    wav_path.unlink()

    # Combine text
    combined_text = " ".join(full_text)

    # Save transcript
    transcript_path = output_dir / f"{audio_path.stem}_transcript.txt"
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(combined_text)

    print(f"Transcript saved to: {transcript_path}")
    return str(transcript_path)

def main():
    parser = argparse.ArgumentParser(description="Convert audio files to text using Speech Recognition")
    parser.add_argument("audio_file", help="Path to the audio file (MP3, WAV, etc.)")
    parser.add_argument("--output-dir", help="Output directory for transcripts")

    args = parser.parse_args()

    try:
        transcript_path = audio_to_text(args.audio_file, args.output_dir)
        print(f"Success! Transcript: {transcript_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()