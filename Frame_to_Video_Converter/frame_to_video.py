#!/usr/bin/env python3
"""
Frame to Video/GIF Converter
Combines image frames from a folder into MP4 or GIF files with GPU acceleration
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import argparse

class FrameConverter:
    def __init__(self):
        self.frame_files = []
        self.fps = 30  # Default FPS

    def find_frames(self, folder_path):
        """Find all image files in the folder and sort them"""
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        # Common image extensions
        extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']

        self.frame_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in extensions):
                self.frame_files.append(os.path.join(folder_path, file))

        if not self.frame_files:
            raise ValueError(f"No image files found in {folder_path}")

        # Sort frames by filename (assuming numbered sequence)
        self.frame_files.sort()

        print(f"✅ Found {len(self.frame_files)} frames:")
        print(f"   First frame: {os.path.basename(self.frame_files[0])}")
        print(f"   Last frame: {os.path.basename(self.frame_files[-1])}")

        return self.frame_files

    def create_mp4_gpu(self, output_path, fps=30):
        """Create MP4 using OpenCV with GPU acceleration"""
        if not self.frame_files:
            raise RuntimeError("No frames loaded. Call find_frames() first.")

        print(f"\n🎬 Creating MP4 with GPU acceleration...")
        print(f"   Output: {output_path}")
        print(f"   FPS: {fps}")
        print(f"   Frames: {len(self.frame_files)}")

        # Enable OpenCL for AMD GPU
        cv2.ocl.setUseOpenCL(True)
        print(f"   OpenCL enabled: {cv2.ocl.useOpenCL()}")

        # Read first frame to get dimensions
        first_frame = cv2.imread(self.frame_files[0])
        if first_frame is None:
            raise ValueError(f"Could not read first frame: {self.frame_files[0]}")

        height, width = first_frame.shape[:2]
        print(f"   Resolution: {width}x{height}")

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        if not out.isOpened():
            raise RuntimeError("Could not create video writer")

        frame_count = 0
        for frame_path in self.frame_files:
            frame = cv2.imread(frame_path)
            if frame is None:
                print(f"   ⚠️  Skipping unreadable frame: {os.path.basename(frame_path)}")
                continue

            # Ensure frame has correct dimensions
            if frame.shape[:2] != (height, width):
                frame = cv2.resize(frame, (width, height))

            out.write(frame)
            frame_count += 1

            # Progress update
            if frame_count % 50 == 0:
                progress = (frame_count / len(self.frame_files)) * 100
                print(f"   📊 Processed {frame_count}/{len(self.frame_files)} frames ({progress:.1f}%)")

        out.release()
        print(f"   ✅ MP4 created successfully! ({frame_count} frames)")

        # Verify file
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"   📁 File size: {size_mb:.2f} MB")
            return output_path
        else:
            raise RuntimeError("MP4 file was not created properly")

    def create_gif(self, output_path, fps=30):
        """Create GIF using PIL (CPU-based but optimized)"""
        if not self.frame_files:
            raise RuntimeError("No frames loaded. Call find_frames() first.")

        print(f"\n🎨 Creating GIF...")
        print(f"   Output: {output_path}")
        print(f"   FPS: {fps}")
        print(f"   Frames: {len(self.frame_files)}")

        frames = []
        frame_count = 0

        for frame_path in self.frame_files:
            try:
                img = Image.open(frame_path)
                frames.append(img.copy())
                img.close()
                frame_count += 1

                # Progress update
                if frame_count % 50 == 0:
                    progress = (frame_count / len(self.frame_files)) * 100
                    print(f"   📊 Loaded {frame_count}/{len(self.frame_files)} frames ({progress:.1f}%)")

            except Exception as e:
                print(f"   ⚠️  Skipping unreadable frame: {os.path.basename(frame_path)} ({e})")
                continue

        if not frames:
            raise RuntimeError("No valid frames could be loaded")

        print(f"   🎨 Saving GIF with {len(frames)} frames...")

        # Calculate duration per frame in milliseconds
        duration_ms = int(1000 / fps)

        # Save as GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0,
            optimize=True
        )

        print(f"   ✅ GIF created successfully! ({len(frames)} frames)")

        # Verify file
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"   📁 File size: {size_mb:.2f} MB")
            return output_path
        else:
            raise RuntimeError("GIF file was not created properly")

def main():
    print("🎬 Frame to Video/GIF Converter")
    print("=" * 40)
    print("Combines image frames into MP4 or GIF files")
    print("Supports PNG, JPG, JPEG, BMP, TIFF formats")
    print()

    converter = FrameConverter()

    # Get input folder
    while True:
        folder_path = input("Enter frames folder path: ").strip()
        # Remove surrounding quotes if present
        if folder_path.startswith('"') and folder_path.endswith('"'):
            folder_path = folder_path[1:-1]
        elif folder_path.startswith("'") and folder_path.endswith("'"):
            folder_path = folder_path[1:-1]

        if not folder_path:
            print("❌ No path provided")
            continue

        try:
            converter.find_frames(folder_path)
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    # Get output format
    while True:
        format_choice = input("Output format (mp4/gif): ").strip().lower()
        if format_choice in ['mp4', 'gif']:
            break
        print("❌ Please enter 'mp4' or 'gif'")

    # Get timing mode
    print("\n⏱️  Timing Options:")
    print("   • FPS: Frames per second (e.g., 30 FPS = fast playback)")
    print("   • Duration: Milliseconds per frame (e.g., 100ms = slow playback)")
    while True:
        timing_mode = input("Choose timing mode (fps/duration): ").strip().lower()
        if timing_mode in ['fps', 'duration']:
            break
        print("❌ Please enter 'fps' or 'duration'")

    # Get timing value based on mode
    if timing_mode == 'fps':
        print("\n⚡ FPS Mode:")
        print("   • 24 FPS: Cinematic, smooth playback")
        print("   • 30 FPS: Standard video, good for most content")
        print("   • 60 FPS: Very smooth, larger file size")
        print("   • Lower FPS: Slower playback, smaller files")
        while True:
            try:
                fps_input = input("FPS (1-120, default 30): ").strip()
                fps = int(fps_input) if fps_input else 30
                if fps < 1 or fps > 120:
                    print("❌ FPS must be between 1 and 120")
                    continue
                duration_ms = int(1000 / fps)
                break
            except ValueError:
                print("❌ Please enter a valid number for FPS")
                continue
    else:
        print("\n⏱️  Duration Mode:")
        print("   • 100-200ms: Slow, detailed viewing")
        print("   • 50-100ms: Moderate speed")
        print("   • 20-50ms: Fast, video-like")
        print("   • <20ms: Very fast, may appear as video")
        while True:
            try:
                duration_input = input("Duration per frame in milliseconds (default 100): ").strip()
                duration_ms = int(duration_input) if duration_input else 100
                if duration_ms < 10 or duration_ms > 5000:
                    print("❌ Duration must be between 10 and 5000 milliseconds")
                    continue
                fps = int(1000 / duration_ms)
                break
            except ValueError:
                print("❌ Please enter a valid number for duration")
                continue

    # Show timing summary and tips
    total_duration = (len(converter.frame_files) * duration_ms) / 1000
    print(f"\n📊 Timing Summary:")
    print(f"   Mode: {timing_mode.upper()}")
    print(f"   FPS: {fps}")
    print(f"   Duration per frame: {duration_ms}ms")
    print(f"   Total frames: {len(converter.frame_files)}")
    print(f"   Estimated duration: {total_duration:.1f}s")

    # Provide tips based on timing
    print(f"\n💡 Timing Tips:")
    if duration_ms >= 200:
        print("   • SLOW: Perfect for presentations, tutorials, or detailed viewing")
        print("   • Result: Each frame clearly visible, good for educational content")
    elif duration_ms >= 100:
        print("   • MODERATE: Good balance of speed and visibility")
        print("   • Result: Smooth slideshow feel, suitable for most content")
    elif duration_ms >= 50:
        print("   • FAST: Quick transitions, video-like feel")
        print("   • Result: Good for animations or time-lapse effects")
    else:
        print("   • VERY FAST: Almost video-like playback")
        print("   • Result: May appear as smooth video, good for high-frame-rate content")

    if fps >= 60:
        print("   • HIGH FPS: Very smooth playback, larger file sizes")
    elif fps >= 30:
        print("   • STANDARD FPS: Compatible with most video players")
    elif fps >= 24:
        print("   • CINEMATIC FPS: Film-like quality")
    else:
        print("   • LOW FPS: Creates stop-motion or slideshow effect")

    # Generate output path (in output directory)
    folder_name = Path(folder_path).name
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    if format_choice == 'mp4':
        output_path = str(output_dir / f"{folder_name}.mp4")
    else:
        output_path = str(output_dir / f"{folder_name}.gif")

    # Confirm overwrite if file exists
    if os.path.exists(output_path):
        overwrite = input(f"Output file exists: {os.path.basename(output_path)}. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("❌ Operation cancelled")
            return 1

    # Perform conversion
    try:
        if format_choice == 'mp4':
            result_path = converter.create_mp4_gpu(output_path, fps)
        else:
            result_path = converter.create_gif(output_path, fps)

        print("\n🎉 SUCCESS!")
        print(f"   Output: {result_path}")
        print(f"   Format: {format_choice.upper()}")
        print(f"   FPS: {fps}")
        print(f"   Duration per frame: {duration_ms}ms")
        print(f"   Frames: {len(converter.frame_files)}")
        print(f"   Total duration: {total_duration:.1f}s")

        return 0

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line usage
        parser = argparse.ArgumentParser(description="Convert image frames to video/GIF")
        parser.add_argument("input", help="Input folder containing frames")
        parser.add_argument("-f", "--format", choices=['mp4', 'gif'], required=True, help="Output format")
        parser.add_argument("-o", "--output", help="Output file path")
        parser.add_argument("-fps", "--fps", type=int, help="Frames per second (alternative to --duration)")
        parser.add_argument("-d", "--duration", type=int, help="Duration per frame in milliseconds (alternative to --fps)")

        args = parser.parse_args()

        # Validate timing arguments
        if args.fps and args.duration:
            parser.error("Cannot specify both --fps and --duration. Choose one.")
        elif not args.fps and not args.duration:
            args.fps = 30  # Default to 30 FPS

        # Convert timing to consistent format
        if args.fps:
            fps = args.fps
            duration_ms = int(1000 / fps)
        else:
            duration_ms = args.duration
            fps = int(1000 / duration_ms)

        converter = FrameConverter()
        try:
            converter.find_frames(args.input)

            if args.output:
                output_path = args.output
            else:
                folder_name = Path(args.input).name
                ext = 'mp4' if args.format == 'mp4' else 'gif'
                # Output to output directory
                output_dir = Path(__file__).parent / "output"
                output_dir.mkdir(exist_ok=True)
                output_path = str(output_dir / f"{folder_name}.{ext}")

            if args.format == 'mp4':
                result_path = converter.create_mp4_gpu(output_path, fps)
            else:
                result_path = converter.create_gif(output_path, fps)

            print(f"✅ Conversion complete: {result_path}")
            print(f"   FPS: {fps}, Duration per frame: {duration_ms}ms")

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        sys.exit(main())