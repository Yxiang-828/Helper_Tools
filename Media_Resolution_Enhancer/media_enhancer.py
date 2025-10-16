#!/usr/bin/env python3
"""
Media Resolution Enhancer
Enhances resolution of images and videos using advanced algorithms.
"""

import sys
import argparse
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageFilter
import subprocess

def enhance_image(image_path, scale_factor=2, output_path=None):
    """
    Enhance image resolution using multiple techniques.

    Args:
        image_path (str): Path to input image
        scale_factor (float): Upscaling factor (1.5, 2, 3, 4)
        output_path (str): Output path (optional)

    Returns:
        str: Path to enhanced image
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Set output path
    if output_path is None:
        output_dir = Path(__file__).parent / "enhanced_media"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_enhanced{image_path.suffix}"
    else:
        output_path = Path(output_path)

    print(f"Enhancing image: {image_path.name}")
    print(f"Scale factor: {scale_factor}x")

    # Read image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = img.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    print(f"Original size: {width}x{height}")
    print(f"Enhanced size: {new_width}x{new_height}")

    # Step 1: Bicubic interpolation for initial upscaling
    enhanced = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # Step 2: Convert to LAB color space for better processing
    enhanced_lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(enhanced_lab)

    # Step 3: Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # Step 4: Merge channels back
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Step 5: Sharpen the image
    kernel = np.array([[-1,-1,-1],
                      [-1, 9,-1],
                      [-1,-1,-1]])
    enhanced = cv2.filter2D(enhanced, -1, kernel)

    # Step 6: Reduce noise while preserving edges
    enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)

    # Save enhanced image
    cv2.imwrite(str(output_path), enhanced)
    print(f"Enhanced image saved: {output_path}")

    return str(output_path)

def enhance_video(video_path, scale_factor=2, output_path=None):
    """
    Enhance video resolution by processing each frame.

    Args:
        video_path (str): Path to input video
        scale_factor (float): Upscaling factor
        output_path (str): Output path (optional)

    Returns:
        str: Path to enhanced video
    """
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Set output path
    if output_path is None:
        output_dir = Path(__file__).parent / "enhanced_media"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{video_path.stem}_enhanced{video_path.suffix}"
    else:
        output_path = Path(output_path)

    print(f"Enhancing video: {video_path.name}")
    print(f"Scale factor: {scale_factor}x")

    # Create temp directory for frames
    temp_dir = Path(__file__).parent / "temp_frames"
    temp_dir.mkdir(exist_ok=True)

    try:
        # Extract frames using FFmpeg
        print("Extracting frames...")
        cmd = [
            r"C:\ffmpeg\bin\ffmpeg.exe", "-i", str(video_path),
            "-vf", f"scale=iw*{scale_factor}:ih*{scale_factor}:flags=bicubic",
            "-q:v", "2",  # High quality
            str(temp_dir / "frame_%04d.png")
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg frame extraction failed: {result.stderr}")

        # Get frame count
        frames = list(temp_dir.glob("frame_*.png"))
        if not frames:
            raise RuntimeError("No frames extracted")

        print(f"Extracted {len(frames)} frames")

        # Process each frame for additional enhancement
        print("Enhancing frames...")
        for i, frame_path in enumerate(sorted(frames)):
            if i % 10 == 0:  # Progress update every 10 frames
                print(f"Processing frame {i+1}/{len(frames)}")

            # Read frame
            img = cv2.imread(str(frame_path))

            # Apply additional enhancement
            # Convert to LAB and apply CLAHE
            img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(img_lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            img_lab = cv2.merge([l, a, b])
            img = cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)

            # Sharpen
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernel)

            # Overwrite the frame
            cv2.imwrite(str(frame_path), img)

        # Reassemble video using FFmpeg
        print("Reassembling video...")
        cmd = [
            r"C:\ffmpeg\bin\ffmpeg.exe", "-framerate", "30", "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "slow", "-crf", "20",
            "-c:a", "copy", str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg video assembly failed: {result.stderr}")

        print(f"Enhanced video saved: {output_path}")

    finally:
        # Clean up temp frames
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    return str(output_path)

def main():
    parser = argparse.ArgumentParser(description="Enhance resolution of images and videos")
    parser.add_argument("input_file", help="Path to input media file (image or video)")
    parser.add_argument("--scale", type=float, default=2.0,
                       choices=[1.5, 2.0, 3.0, 4.0],
                       help="Upscaling factor (default: 2.0)")
    parser.add_argument("--output", help="Output file path (optional)")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Determine file type
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif'}
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'}

    ext = input_path.suffix.lower()

    try:
        if ext in image_extensions:
            result_path = enhance_image(args.input_file, args.scale, args.output)
        elif ext in video_extensions:
            result_path = enhance_video(args.input_file, args.scale, args.output)
        else:
            print(f"Error: Unsupported file type: {ext}", file=sys.stderr)
            print("Supported: Images - PNG, JPG, BMP, TIFF", file=sys.stderr)
            print("Supported: Videos - MP4, MOV, AVI, MKV, WebM, FLV", file=sys.stderr)
            sys.exit(1)

        print(f"\n✅ Enhancement complete!")
        print(f"Output: {result_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()