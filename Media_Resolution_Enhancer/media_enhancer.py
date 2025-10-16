#!/usr/bin/env python3
"""
Media Resolution Enhancer
Enhances resolution of images and videos using AI (Real-ESRGAN) and classical methods.
"""

import sys
import argparse
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import subprocess

# Try to import AI libraries, fallback to classical if not available
try:
    import cv2
    # Check if DNN super resolution is available
    dnn = cv2.dnn_superres
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("AI enhancement not available. Using classical method.")

def enhance_image_ai(image_path, scale_factor=2, output_path=None):
    """
    Enhance image resolution using OpenCV DNN Super Resolution.

    Args:
        image_path (str): Path to input image
        scale_factor (int): Upscaling factor (2, 3, 4)
        output_path (str): Output path (optional)

    Returns:
        str: Path to enhanced image
    """
    if not AI_AVAILABLE:
        print("AI not available, using classical method...")
        return enhance_image_classical(image_path, scale_factor, output_path)

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Set output path
    if output_path is None:
        output_dir = Path(__file__).parent / "enhanced_media"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_enhanced_ai{image_path.suffix}"
    else:
        output_path = Path(output_path)

    print(f"AI Enhancing image: {image_path.name}")
    print(f"Scale factor: {scale_factor}x")

    # Initialize DNN super resolution
    sr = cv2.dnn_superres.DnnSuperResImpl_create()

    # Select model based on scale factor
    model_path = Path(__file__).parent / "models"
    model_path.mkdir(exist_ok=True)

    if scale_factor == 2:
        model_file = model_path / "EDSR_x2.pb"
        algorithm = "edsr"
    elif scale_factor == 3:
        model_file = model_path / "EDSR_x3.pb"
        algorithm = "edsr"
    elif scale_factor == 4:
        model_file = model_path / "EDSR_x4.pb"
        algorithm = "edsr"
    else:
        model_file = model_path / "EDSR_x2.pb"
        algorithm = "edsr"

    # Check if model exists, download if needed
    if not model_file.exists():
        print(f"Model {model_file.name} not found in {model_path}")
        print("AI models need to be downloaded. Falling back to classical method...")
        return enhance_image_classical(str(image_path), scale_factor, str(output_path))

    # Read and enhance image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    try:
        # Load model
        sr.readModel(str(model_file))
        sr.setModel(algorithm, scale_factor)

        # Upscale image
        result = sr.upsample(img)

        # Save enhanced image
        cv2.imwrite(str(output_path), result)
        print(f"AI Enhanced image saved: {output_path}")

    except Exception as e:
        print(f"AI enhancement failed: {e}")
        print("Falling back to classical method...")
        return enhance_image_classical(str(image_path), scale_factor, str(output_path))

    return str(output_path)

def enhance_image_classical(image_path, scale_factor=2, output_path=None):
    """
    Classical enhancement method (improved version).
    """
    image_path = Path(image_path)
    if output_path is None:
        output_dir = Path(__file__).parent / "enhanced_media"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_enhanced{image_path.suffix}"

    print("Using improved classical enhancement method...")

    # Read image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = img.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    print(f"Original size: {width}x{height}")
    print(f"Enhanced size: {new_width}x{new_height}")

    # Improved classical approach - gentler processing
    enhanced = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # Convert to LAB for color-preserving enhancement
    enhanced_lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(enhanced_lab)

    # Gentle CLAHE with larger tiles and lower clip limit
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(16, 16))
    l = clahe.apply(l)

    # Merge back
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Light sharpening (reduced kernel)
    kernel = np.array([[-0.5,-0.5,-0.5],
                      [-0.5, 5,-0.5],
                      [-0.5,-0.5,-0.5]])
    enhanced = cv2.filter2D(enhanced, -1, kernel)

    # Save
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
        output_path = output_dir / f"{video_path.stem}_enhanced{scale_factor}x{video_path.suffix}"
    else:
        output_path = Path(output_path)

    print(f"Enhancing video: {video_path.name}")
    print(f"Scale factor: {scale_factor}x")

    # Create temp directory for frames
    temp_dir = Path(__file__).parent / "temp_frames"
    temp_dir.mkdir(exist_ok=True)

    try:
        # Extract frames using FFmpeg with upscaling
        print("Extracting and upscaling frames...")
        cmd = [
            r"C:\ffmpeg\bin\ffmpeg.exe", "-i", str(video_path),
            "-vf", f"scale=iw*{scale_factor}:ih*{scale_factor}:flags=bicubic",
            "-q:v", "2",
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

        # For video, we'll use the upscaled frames directly (AI enhancement would be too slow for video)
        # In a full implementation, you could enhance each frame with AI, but that's very time-consuming

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
    parser.add_argument("--scale", type=int, default=2, choices=[2, 3, 4],
                       help="Upscaling factor (default: 2)")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--method", choices=["ai", "classical"], default="ai",
                       help="Enhancement method (default: ai)")

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
            if args.method == "ai":
                result_path = enhance_image_ai(args.input_file, args.scale, args.output)
            else:
                result_path = enhance_image_classical(args.input_file, args.scale, args.output)
        elif ext in video_extensions:
            result_path = enhance_video(args.input_file, args.scale, args.output)
        else:
            print(f"Error: Unsupported file type: {ext}", file=sys.stderr)
            print("Supported: Images - PNG, JPG, BMP, TIFF, GIF", file=sys.stderr)
            print("Supported: Videos - MP4, MOV, AVI, MKV, WebM, FLV", file=sys.stderr)
            sys.exit(1)

        print(f"\n✅ Enhancement complete!")
        print(f"Output: {result_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()