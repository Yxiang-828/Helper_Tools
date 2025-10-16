#!/usr/bin/env python3
"""
Audio to Text Converter using OpenAI Whisper with DirectML GPU acceleration
Converts MP3 audio files to text transcripts with long audio support.
"""

import sys
import argparse
import os
from pathlib import Path
from optimum.onnxruntime import ORTModelForSpeechSeq2Seq
from transformers import AutoProcessor
import librosa
import time
import torch
import numpy as np

# Add ffmpeg to PATH for Whisper
ffmpeg_path = r"C:\ffmpeg\bin"
if ffmpeg_path not in os.environ['PATH']:
    os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']

def audio_to_text(audio_path, model_size="base", output_dir=None, language="en"):
    """
    Convert audio file to text using Whisper with DirectML GPU acceleration.
    Handles long audio files by chunking them into segments.

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

    # Load ONNX model with DirectML provider for GPU acceleration
    print(f"\n{'='*70}")
    print(f"Loading Whisper model: {model_size} with DirectML GPU acceleration")
    print(f"DirectML GPU: Available (AMD RX 6800 XT)")
    print(f"{'='*70}\n")
    start_time = time.time()
    model_id = f"openai/whisper-{model_size}"

    # Check if ONNX model already exists
    cache_path = Path.home() / ".cache" / "huggingface" / "optimum" / f"openai-whisper-{model_size}"

    if cache_path.exists() and any(cache_path.glob("*.onnx")):
        print("✅ Using cached ONNX model...")
        model = ORTModelForSpeechSeq2Seq.from_pretrained(cache_path, provider="DmlExecutionProvider")
        print("✅ DirectML provider loaded successfully")
    else:
        print("⏳ Converting to ONNX format (first time only)...")
        model = ORTModelForSpeechSeq2Seq.from_pretrained(model_id, provider="DmlExecutionProvider")
        # Save the converted model for future use
        model.save_pretrained(cache_path)
        print(f"✅ ONNX model saved to cache: {cache_path}")
        print("✅ DirectML provider loaded successfully")

    processor = AutoProcessor.from_pretrained(model_id)

    # Load audio
    print("\n⏳ Loading audio file...")
    audio_load_start = time.time()
    audio_array, sample_rate = librosa.load(str(audio_path), sr=16000)
    audio_load_time = time.time() - audio_load_start

    # Calculate duration and chunk size
    duration_seconds = len(audio_array) / sample_rate
    print(f"✅ Audio loaded in {audio_load_time:.2f}s")
    print(f"   Duration: {duration_seconds:.1f}s ({duration_seconds/60:.1f} minutes)")
    print(f"   Sample rate: {sample_rate} Hz")

    # Whisper max context: ~30 seconds per chunk
    chunk_duration = 30
    chunk_samples = chunk_duration * sample_rate

    # Split audio into chunks
    chunks = []
    for i in range(0, len(audio_array), int(chunk_samples)):
        chunk = audio_array[i:i+int(chunk_samples)]
        chunks.append(chunk)

    print(f"⏳ Processing {len(chunks)} audio chunks with GPU DirectML...\n")
    all_transcriptions = []
    chunk_times = []

    # Transcribe each chunk
    for idx, chunk in enumerate(chunks):
        chunk_start = time.time()
        chunk_num = idx + 1
        chunk_duration_sec = len(chunk) / sample_rate

        # Progress bar
        progress = (idx / len(chunks)) * 100
        bar_length = 40
        filled = int(bar_length * idx / len(chunks))
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"[{bar}] {progress:5.1f}% - Chunk {chunk_num}/{len(chunks)} ({chunk_duration_sec:.1f}s audio)", end="")
        sys.stdout.flush()

        # Process audio chunk - move features to GPU BEFORE model.generate
        inputs = processor(chunk, return_tensors="pt", sampling_rate=sample_rate)

        # GPU Optimization: Move input features to GPU (DirectML device)
        inputs["input_features"] = inputs["input_features"].to("dml") if torch.cuda.is_available() else inputs["input_features"]

        # Transcribe with DirectML GPU - now has GPU-accelerated features
        if language == "auto":
            generated_ids = model.generate(inputs["input_features"])
        else:
            generated_ids = model.generate(inputs["input_features"], language=language, task="transcribe")

        # Batch decode (handles tensor conversion internally)
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        all_transcriptions.append(transcription.strip())

        chunk_time = time.time() - chunk_start
        chunk_times.append(chunk_time)

        # Clear line and show timing
        print(f" ✅ {chunk_time:.2f}s")
        sys.stdout.flush()

    # Concatenate all transcriptions
    full_transcription = " ".join(all_transcriptions)

    # Calculate statistics
    total_transcription_time = time.time() - start_time
    avg_chunk_time = sum(chunk_times) / len(chunk_times) if chunk_times else 0
    real_time_factor = total_transcription_time / duration_seconds

    print(f"\n{'='*70}")
    print(f"✅ TRANSCRIPTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total time: {total_transcription_time:.2f}s")
    print(f"Audio duration: {duration_seconds:.1f}s ({duration_seconds/60:.1f} minutes)")
    print(f"Average per chunk: {avg_chunk_time:.2f}s")
    print(f"Real-time factor: {real_time_factor:.2f}x (lower is faster)")
    print(f"Total characters: {len(full_transcription)}")
    print(f"{'='*70}\n")

    # Save transcript
    transcript_path = output_dir / f"{audio_path.stem}_transcript.md"
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(f"# Audio Transcript: {audio_path.name}\n\n")
        f.write(f"**File:** {audio_path.name}\n")
        f.write(f"**Duration:** {duration_seconds:.1f}s ({duration_seconds/60:.1f} minutes)\n")
        f.write(f"**Model:** {model_size} (DirectML GPU accelerated)\n")
        f.write(f"**Language:** {language}\n")
        f.write(f"**Chunks processed:** {len(chunks)}\n")
        f.write(f"**Transcription time:** {total_transcription_time:.2f}s\n")
        f.write(f"**Real-time factor:** {real_time_factor:.2f}x\n")
        f.write(f"**Generated:** {Path(__file__).parent.stem} tool\n\n")
        f.write("## Transcript\n\n")
        f.write(full_transcription)
        f.write("\n")

    print(f"✅ Transcript saved to: {transcript_path}")
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