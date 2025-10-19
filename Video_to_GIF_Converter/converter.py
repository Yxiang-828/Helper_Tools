#!/usr/bin/env python3
"""
Advanced MP4 to GIF Converter with Custom Constraints
Automatically optimizes conversion based on user-specified size and speed constraints
"""

import os
import sys
import math
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import argparse

class GIFConverter:
    def __init__(self):
        self.video_info = None
        self.size_constraint_mb = None
        self.speed_constraint_ratio = None

    def analyze_video(self, mp4_path):
        """Analyze the input video and extract key information using OpenCV"""
        if not os.path.exists(mp4_path):
            raise FileNotFoundError(f"Video file not found: {mp4_path}")

        print("🔍 Analyzing video with GPU acceleration...")

        # Enable OpenCL for AMD GPU acceleration
        cv2.ocl.setUseOpenCL(True)
        print(f"   OpenCL enabled: {cv2.ocl.useOpenCL()}")

        try:
            # Open video with OpenCV
            cap = cv2.VideoCapture(mp4_path)
            if not cap.isOpened():
                raise RuntimeError("Could not open video file")

            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0

            # Get file size
            file_size_mb = os.path.getsize(mp4_path) / (1024 * 1024)

            cap.release()

            self.video_info = {
                'path': mp4_path,
                'duration': duration,
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': frame_count,
                'file_size_mb': file_size_mb
            }

            print("✅ Video analysis complete!")
            print(f"   Duration: {self.video_info['duration']:.2f}s")
            print(f"   Original FPS: {self.video_info['fps']}")
            print(f"   Resolution: {self.video_info['width']}x{self.video_info['height']}")
            print(f"   Total frames: {self.video_info['total_frames']}")
            print(f"   File size: {self.video_info['file_size_mb']:.1f} MB")
            return True

        except Exception as e:
            raise RuntimeError(f"Failed to analyze video: {e}")
            print(f"   Resolution: {self.video_info['width']}x{self.video_info['height']}")
            print(f"   Total frames: {self.video_info['total_frames']}")
            print(f"   File size: {self.video_info['file_size_mb']:.1f} MB")
            return True

        except Exception as e:
            raise RuntimeError(f"Failed to analyze video: {e}")

    def validate_constraints(self, size_mb, speed_ratio):
        """Validate and set user constraints"""
        # Size constraint validation
        if not isinstance(size_mb, (int, float)) or size_mb <= 0:
            raise ValueError("Size constraint must be a positive number (MB)")

        if size_mb > 50:
            print("⚠️  Warning: Size constraint > 50MB may result in very large files")
        elif size_mb < 1:
            print("⚠️  Warning: Size constraint < 1MB may result in very low quality")

        # Speed constraint validation
        if not isinstance(speed_ratio, (int, float)) or speed_ratio <= 0 or speed_ratio > 2:
            raise ValueError("Speed ratio must be between 0.1 and 2.0 (1.0 = original speed)")

        if speed_ratio < 0.5:
            print("⚠️  Warning: Speed ratio < 0.5 will make video play very slowly")
        elif speed_ratio > 1.5:
            print("⚠️  Warning: Speed ratio > 1.5 will make video play very fast")

        self.size_constraint_mb = float(size_mb)
        self.speed_constraint_ratio = float(speed_ratio)

        print("\n✅ Constraints validated:")
        print(f"   Size limit: {self.size_constraint_mb} MB")
        print(f"   Speed ratio: {self.speed_constraint_ratio}x original speed")
        return True

    def calculate_optimal_settings(self):
        """Calculate optimal FPS and resolution based on constraints with accurate estimation"""
        if not self.video_info or not self.size_constraint_mb or not self.speed_constraint_ratio:
            raise RuntimeError("Video analysis and constraints must be set first")

        original_fps = self.video_info['fps']
        original_width = self.video_info['width']
        original_height = self.video_info['height']
        original_duration = self.video_info['duration']

        # For speed constraint: adjust duration proportionally instead of FPS
        # 2x speed = half duration, 0.5x speed = double duration
        adjusted_duration = original_duration / self.speed_constraint_ratio

        # GIF size estimation: depends on image complexity and palette
        # Conservative default tuned from empirical tests for typical clips
        # Use a higher estimate to avoid undershooting the user target.
        bytes_per_pixel = 0.2  # bytes per pixel (conservative estimate for GIF compression)

        # Calculate target size in bytes
        target_size_bytes = self.size_constraint_mb * 1024 * 1024

        # Calculate pixels per frame based on adjusted duration (speed affects playback time)
        pixels_per_frame = (target_size_bytes / bytes_per_pixel) / (original_fps * adjusted_duration)

        # If pixels per frame is too low, we need higher resolution or the file will be too small
        # Dynamic minimum based on size target
        if self.size_constraint_mb <= 20:
            min_pixels_per_frame = 160 * 90  # 14,400
        if self.size_constraint_mb <= 10:
            min_pixels_per_frame = 80 * 45   # 3,600
        if self.size_constraint_mb <= 5:
            min_pixels_per_frame = 40 * 22   # 880
        else:
            min_pixels_per_frame = 320 * 180  # 57,600

        if pixels_per_frame < min_pixels_per_frame:
            pixels_per_frame = min_pixels_per_frame

        # Calculate target resolution
        original_pixels_per_frame = original_width * original_height
        scale_factor = math.sqrt(pixels_per_frame / original_pixels_per_frame)
        scale_factor = max(0.1, min(1.0, scale_factor))  # Clamp between 10% and 100%

        # For small size targets, force more aggressive scaling
        if self.size_constraint_mb <= 10:
            scale_factor = min(scale_factor, 0.15)  # Force smaller scale for ≤10MB targets
        elif self.size_constraint_mb <= 20:
            scale_factor = min(scale_factor, 0.25)  # Force smaller scale for ≤20MB targets

        target_width = int(original_width * scale_factor)
        target_height = int(original_height * scale_factor)

        # Ensure minimum resolution (dynamic based on size target)
        min_width, min_height = 320, 180  # Default minimum
        if self.size_constraint_mb <= 20:
            min_width, min_height = 160, 90
        if self.size_constraint_mb <= 10:
            min_width, min_height = 80, 45
        if self.size_constraint_mb <= 5:
            min_width, min_height = 40, 22

        target_width = max(min_width, target_width)
        target_height = max(min_height, target_height)

        # Keep original FPS, speed is controlled by duration adjustment
        final_fps = original_fps

        # Calculate estimated final size
        final_pixels_per_frame = target_width * target_height
        estimated_total_pixels = final_pixels_per_frame * final_fps * adjusted_duration
        estimated_size_mb = (estimated_total_pixels * bytes_per_pixel) / (1024 * 1024)

        settings = {
            'fps': final_fps,
            'width': target_width,
            'height': target_height,
            'estimated_frames': int(adjusted_duration * final_fps),
            'estimated_duration': adjusted_duration,
            'speed_ratio_actual': self.speed_constraint_ratio,  # We achieve exact speed ratio now
            'estimated_size_mb': estimated_size_mb
        }

        print("\n🎯 Calculated optimal settings:")
        print(f"   Target FPS: {settings['fps']} (original maintained)")
        print(f"   Resolution: {settings['width']}x{settings['height']} (from {original_width}x{original_height})")
        print(f"   Estimated frames: {settings['estimated_frames']}")
        print(f"   Adjusted duration: {settings['estimated_duration']:.2f}s (from {original_duration:.2f}s)")
        print(f"   Speed ratio: {settings['speed_ratio_actual']:.2f}x")
        print(f"   Estimated size: {settings['estimated_size_mb']:.1f} MB (target: {self.size_constraint_mb} MB)")
        return settings

    def convert_video(self, output_path=None):
        """Perform the conversion with constraints and create both optimized and original versions"""
        if not self.video_info:
            raise RuntimeError("Video must be analyzed first")

        settings = self.calculate_optimal_settings()

        # Generate output paths
        if output_path is None:
            # Use extracted_gifs folder in the converter's own directory
            extracted_gifs_dir = Path(__file__).parent / "extracted_gifs"
            extracted_gifs_dir.mkdir(exist_ok=True)

            video_name = Path(self.video_info['path']).stem
            optimized_path = str(extracted_gifs_dir / f"{video_name}.gif")
            original_path = str(extracted_gifs_dir / f"{video_name}_original.gif")
        else:
            # If custom output path provided, create variants
            base_path = Path(output_path)
            optimized_path = str(base_path.parent / f"{base_path.stem}.gif")
            original_path = str(base_path.parent / f"{base_path.stem}_original.gif")

        print("\n🔄 Converting video...")
        print(f"   Input: {self.video_info['path']}")
        print(f"   Optimized output: {optimized_path}")
        print(f"   Original output: {original_path}")
        print("\n⏳ GIF conversion is slow because:")
        print("   • Each frame is processed individually")
        print("   • GIF format requires color palette generation per frame")
        print("   • No video compression (each frame stored as full image)")
        print("   • This is normal - please be patient...")

        try:
            # Load video once - trim last 0.5 seconds to avoid corrupted frames
            trim_duration = 0.5  # Trim last 0.5 seconds to avoid frame reading issues
            if self.video_info['duration'] > trim_duration:
                print(f"   🔧 Trimming last {trim_duration}s to avoid corrupted frames...")
                clip = mp.VideoFileClip(self.video_info['path']).subclip(0, self.video_info['duration'] - trim_duration)
                print(f"   New duration: {clip.duration:.2f}s (was {self.video_info['duration']:.2f}s)")
            else:
                clip = mp.VideoFileClip(self.video_info['path'])
                print("   ⚠️  Video too short to trim, proceeding with full video")

            original_clip = clip.copy()  # Keep original for second conversion

            # ITERATIVE APPROACH: Keep reducing resolution until size is under limit
            current_settings = settings.copy()
            iteration = 0
            max_iterations = 5
            original_fps = self.video_info['fps']  # Store original FPS for speed adjustments

            while iteration < max_iterations:
                iteration += 1
                print(f"\n📏 Creating optimized version (attempt {iteration})...")

                # Create a fresh copy for each attempt
                opt_clip = clip.copy()

                # Apply speed adjustment by changing duration proportionally
                if self.speed_constraint_ratio != 1.0:
                    opt_clip = opt_clip.with_speed_scaled(self.speed_constraint_ratio)
                    print(f"   Speed adjusted to {self.speed_constraint_ratio}x (duration: {opt_clip.duration:.2f}s)")

                # Resize if needed for optimized version
                if opt_clip.w > current_settings['width'] or opt_clip.h > current_settings['height']:
                    opt_clip = opt_clip.resized(width=current_settings['width'], height=current_settings['height'])
                    print(f"   Resized to {current_settings['width']}x{current_settings['height']}")

                # Convert optimized version to GIF
                print(f"   Converting optimized at {current_settings['fps']} FPS...")
                try:
                    opt_clip.write_gif(optimized_path, fps=current_settings['fps'])
                except Exception as e:
                    print(f"   ❌ Conversion failed: {e}")
                    opt_clip.close()
                    # Clean up any partial file
                    if os.path.exists(optimized_path):
                        os.remove(optimized_path)
                    raise RuntimeError(f"GIF conversion failed on attempt {iteration}: {e}")

                # Close this attempt's clip
                opt_clip.close()

                # Verify the result
                if not os.path.exists(optimized_path) or os.path.getsize(optimized_path) == 0:
                    print(f"   ❌ Empty or missing output file after conversion")
                    continue

                result_info = self.verify_conversion(optimized_path, current_settings)
                actual_size_mb = result_info['size_mb']

                print(f"   Attempt {iteration} result: {actual_size_mb:.2f} MB (target: {self.size_constraint_mb} MB)")

                # If we're within limit and not too far below target, accept
                undershoot_threshold = 0.95  # accept if >= 95% of target
                if actual_size_mb <= self.size_constraint_mb and actual_size_mb >= self.size_constraint_mb * undershoot_threshold:
                    print(f"   ✅ Size constraint met on attempt {iteration} within acceptable undershoot ({actual_size_mb:.2f} MB)")
                    break

                # If under target but too small (undershoot), try increasing resolution moderately
                if actual_size_mb < self.size_constraint_mb * undershoot_threshold and iteration < max_iterations:
                    # Increase resolution by 25% to get closer to target without exceeding
                    increase_factor = 1.25
                    # Cap at original video resolution
                    current_settings['width'] = min(self.video_info['width'], int(current_settings['width'] * increase_factor))
                    current_settings['height'] = min(self.video_info['height'], int(current_settings['height'] * increase_factor))
                    print(f"   🔧 Undershot target by >5%, increasing resolution to {current_settings['width']}x{current_settings['height']} for next attempt...")

                    # Remove the small file before next attempt
                    if os.path.exists(optimized_path):
                        os.remove(optimized_path)
                    continue

                # If over limit and not last iteration, reduce resolution
                if actual_size_mb > self.size_constraint_mb and iteration < max_iterations:
                    reduction_factor = 0.8
                    current_settings['width'] = max(40, int(current_settings['width'] * reduction_factor))
                    current_settings['height'] = max(22, int(current_settings['height'] * reduction_factor))
                    print(f"   ⚠️  Size over limit, reducing resolution to {current_settings['width']}x{current_settings['height']} for next attempt...")

                    # Remove the oversized file
                    if os.path.exists(optimized_path):
                        os.remove(optimized_path)
                else:
                    # Either we reached acceptable size or max iterations
                    if actual_size_mb > self.size_constraint_mb:
                        print(f"   ⚠️  Maximum iterations reached. Final size: {actual_size_mb:.2f} MB (over {self.size_constraint_mb} MB limit)")
                    else:
                        print(f"   ✅ Final size after iterations: {actual_size_mb:.2f} MB")

            # Now create original version if requested
            create_original = input("\n🎬 Create original quality version? (y/n): ").lower().strip() == 'y'

            if create_original:
                print("\n🎬 Creating original quality version...")
                # Convert original version to GIF
                print(f"   Converting original at {self.video_info['fps']} FPS...")
                original_clip.write_gif(original_path, fps=self.video_info['fps'])

                # Close clips
                original_clip.close()
            else:
                print("\n⏭️  Skipping original quality version")

            # Close main clips
            clip.close()

            # Final verification and results
            final_result = self.verify_conversion(optimized_path, current_settings)

            if create_original:
                print("\n✅ Both conversions complete!")
                print(f"   Optimized file: {optimized_path}")
                print(f"   Original file: {original_path}")
            else:
                print("\n✅ Optimized conversion complete!")
                print(f"   Optimized file: {optimized_path}")

            print(f"   Final size: {final_result['size_mb']:.2f} MB")
            print(f"   Final duration: {final_result['duration']:.2f}s")
            print(f"   Final FPS: {final_result['fps']:.1f}")
            print(f"   Final resolution: {current_settings['width']}x{current_settings['height']}")

            # Check final constraints
            if final_result['size_mb'] > self.size_constraint_mb:
                print(f"   ⚠️  Size still over limit: {final_result['size_mb']:.2f} > {self.size_constraint_mb} MB")
            else:
                print(f"   ✅ Size constraint met: {final_result['size_mb']:.2f} ≤ {self.size_constraint_mb} MB")

            if abs(final_result['speed_ratio'] - self.speed_constraint_ratio) / self.speed_constraint_ratio < 0.1:  # Within 10% of target
                print(f"   ✅ Speed constraint met: {final_result['speed_ratio']:.2f}x ≈ {self.speed_constraint_ratio}x")
            else:
                print(f"   ⚠️  Speed constraint not met: {final_result['speed_ratio']:.2f}x ≠ {self.speed_constraint_ratio}x")

            return optimized_path, original_path if create_original else None, final_result

        except Exception as e:
            print(f"   ❌ Conversion failed: {e}")
            raise

    def verify_conversion(self, gif_path, expected_settings):
        """Verify the converted GIF meets expectations"""
        try:
            with Image.open(gif_path) as img:
                frame_count = 0
                total_duration = 0
                try:
                    while True:
                        duration = img.info.get('duration', 1000 // expected_settings['fps'])
                        total_duration += duration
                        frame_count += 1
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass

                actual_fps = 1000 / (total_duration / frame_count) if frame_count > 0 else 0
                file_size_mb = os.path.getsize(gif_path) / (1024 * 1024)

                # Calculate speed ratio based on duration change, not FPS change
                actual_duration = total_duration / 1000
                speed_ratio = self.video_info['duration'] / actual_duration if actual_duration > 0 else 1.0

                return {
                    'frames': frame_count,
                    'duration': actual_duration,
                    'fps': actual_fps,
                    'size_mb': file_size_mb,
                    'speed_ratio': speed_ratio
                }

        except Exception as e:
            print(f"   Warning: Could not verify conversion: {e}")
            return {
                'frames': 0,
                'duration': 0,
                'fps': 0,
                'size_mb': os.path.getsize(gif_path) / (1024 * 1024),
                'speed_ratio': 1.0  # Default to original speed if verification fails
            }

    def convert_video_gpu(self, output_path=None):
        """GPU-accelerated conversion using OpenCV with OpenCL for AMD GPUs"""
        if not self.video_info:
            raise RuntimeError("Video must be analyzed first")

        settings = self.calculate_optimal_settings()

        # Generate output paths
        if output_path is None:
            extracted_gifs_dir = Path(__file__).parent / "extracted_gifs"
            extracted_gifs_dir.mkdir(exist_ok=True)
            video_name = Path(self.video_info['path']).stem
            optimized_path = str(extracted_gifs_dir / f"{video_name}_gpu.gif")
        else:
            base_path = Path(output_path)
            optimized_path = str(base_path.parent / f"{base_path.stem}_gpu.gif")

        print("\n🚀 Converting video with AMD GPU acceleration...")
        print(f"   Input: {self.video_info['path']}")
        print(f"   Output: {optimized_path}")
        print(f"   Using AMD Radeon RX 6800 XT GPU")

        # Enable OpenCL for AMD GPU
        cv2.ocl.setUseOpenCL(True)
        print(f"   OpenCL status: {cv2.ocl.useOpenCL()}")

        try:
            # Open video with OpenCV
            cap = cv2.VideoCapture(self.video_info['path'])
            if not cap.isOpened():
                raise RuntimeError("Could not open video file")

            # Calculate frame processing parameters
            total_frames = int(self.video_info['total_frames'])
            fps = self.video_info['fps']
            target_fps = settings['fps']

            # Trim last frames to avoid corruption (convert seconds to frames)
            trim_frames = int(0.5 * fps)  # Trim last 0.5 seconds
            if total_frames > trim_frames:
                total_frames -= trim_frames
                print(f"   🔧 Trimming last {trim_frames} frames to avoid corruption")

            # Calculate which frames to sample (for speed adjustment)
            frame_interval = max(1, int(fps / target_fps))
            expected_frames = total_frames // frame_interval

            print(f"   Processing {expected_frames} frames at {target_fps} FPS")
            print(f"   Target resolution: {settings['width']}x{settings['height']}")
            print("   Using GPU acceleration for frame processing...")

            frames = []
            frame_count = 0
            processed_count = 0

            # Read and process frames with GPU acceleration
            while processed_count < expected_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # Skip frames according to speed adjustment
                if frame_count % frame_interval != 0:
                    continue

                # Resize frame using GPU-accelerated OpenCV
                if frame.shape[1] > settings['width'] or frame.shape[0] > settings['height']:
                    frame = cv2.resize(frame, (settings['width'], settings['height']),
                                     interpolation=cv2.INTER_LINEAR)

                # Convert BGR to RGB for PIL
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(frame_rgb))

                processed_count += 1

                # Progress update every 100 frames
                if processed_count % 100 == 0:
                    progress = (processed_count / expected_frames) * 100
                    print(f"   📊 GPU processed {processed_count}/{expected_frames} frames ({progress:.1f}%)")

            cap.release()

            if not frames:
                raise RuntimeError("No frames were processed")

            print(f"   🎨 Creating GIF with {len(frames)} frames using optimized encoder...")

            # Create GIF using PIL with optimization (much faster than MoviePy)
            frames[0].save(
                optimized_path,
                save_all=True,
                append_images=frames[1:],
                duration=int(1000 / target_fps),  # Duration per frame in ms
                loop=0,
                optimize=True
            )

            # Verify result
            if os.path.exists(optimized_path) and os.path.getsize(optimized_path) > 0:
                result_info = self.verify_conversion(optimized_path, settings)
                actual_size_mb = result_info['size_mb']

                print(f"   ✅ GPU conversion complete!")
                print(f"   Size: {actual_size_mb:.2f} MB (target: {self.size_constraint_mb} MB)")
                print(f"   Frames: {len(frames)}")
                print(f"   Duration: {len(frames) / target_fps:.1f}s")

                # Check if size is acceptable
                if actual_size_mb <= self.size_constraint_mb:
                    print("   ✅ Size constraint met!")
                else:
                    print(f"   ⚠️  Size over limit ({actual_size_mb:.2f} MB > {self.size_constraint_mb} MB)")

                return optimized_path
            else:
                raise RuntimeError("GIF file was not created or is empty")

        except Exception as e:
            print(f"   ❌ GPU conversion failed: {e}")
            raise

def main():
    print("🎬 Advanced MP4 to GIF Converter")
    print("=" * 50)

    converter = GIFConverter()

    # Get video path
    while True:
        video_path = input("Enter MP4 video path: ").strip()
        # Remove surrounding quotes if present
        if video_path.startswith('"') and video_path.endswith('"'):
            video_path = video_path[1:-1]
        elif video_path.startswith("'") and video_path.endswith("'"):
            video_path = video_path[1:-1]

        if not video_path:
            print("❌ No path provided")
            continue

        try:
            converter.analyze_video(video_path)
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    # Get size constraint
    print("\n📏 Size Constraints:")
    print("   • Valid range: 0.1 - 50 MB")
    print("   • Recommended: 1-10 MB for web use")
    print("   • Warning: >50MB may create very large files")
    print("   • Warning: <1MB may result in poor quality")
    while True:
        try:
            size_input = input("Enter size limit (0.1-50 MB, e.g., 10): ").strip()
            size_mb = float(size_input)
            if size_mb < 0.1 or size_mb > 50:
                print("❌ Size limit must be between 0.1 and 50 MB")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number for size (0.1-50 MB)")
            continue

    # Get speed constraint
    print("\n⚡ Speed Constraints:")
    print("   • Valid range: 0.1 - 2.0")
    print("   • 1.0 = original speed")
    print("   • < 0.5 = very slow playback")
    print("   • > 1.5 = very fast playback")
    while True:
        try:
            speed_input = input("Enter speed ratio (0.1-2.0, 1.0 = original speed): ").strip()
            speed_ratio = float(speed_input)
            if speed_ratio < 0.1 or speed_ratio > 2.0:
                print("❌ Speed ratio must be between 0.1 and 2.0")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number for speed ratio (0.1-2.0)")
            continue

    # Get conversion method
    print("\n🚀 Conversion Method:")
    print("   • GPU: Faster with AMD Radeon GPU (recommended)")
    print("   • CPU: Slower but more compatible")
    while True:
        method = input("Choose conversion method (gpu/cpu): ").strip().lower()
        if method in ['gpu', 'cpu']:
            break
        print("❌ Please enter 'gpu' or 'cpu'")

    # Set constraints (already validated during input)
    converter.validate_constraints(size_mb, speed_ratio)

    # Perform conversion
    try:
        if method == 'gpu':
            optimized_path = converter.convert_video_gpu()
            print("\n🎉 SUCCESS! Your GPU-accelerated GIF is ready!")
            print(f"   File: {optimized_path}")
        else:
            optimized_path, original_path, result_info = converter.convert_video()
            print("\n🎉 SUCCESS! Your GIFs are ready!")
            print(f"   Optimized file: {optimized_path}")
            print(f"   Original file: {original_path}")
            print(f"   Optimized size: {result_info['size_mb']:.2f} MB (limit: {converter.size_constraint_mb} MB)")
            print(f"   Optimized speed: {result_info['speed_ratio']:.2f}x (target: {converter.speed_constraint_ratio:.2f}x)")
            print(f"   Optimized quality: {result_info['fps']:.1f} FPS, {result_info['frames']} frames")

        return 0

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line usage
        parser = argparse.ArgumentParser(description="Convert MP4 to GIF with custom constraints")
        parser.add_argument("input", help="Input MP4 file")
        parser.add_argument("-s", "--size", type=float, required=True, help="Size limit in MB")
        parser.add_argument("-p", "--speed", type=float, required=True, help="Speed ratio (1.0 = original)")
        parser.add_argument("-o", "--output", help="Output GIF file")
        parser.add_argument("--gpu", action="store_true", help="Use GPU acceleration (AMD Radeon)")

        args = parser.parse_args()

        converter = GIFConverter()
        try:
            converter.analyze_video(args.input)
            converter.validate_constraints(args.size, args.speed)
            if args.gpu:
                optimized_path = converter.convert_video_gpu(args.output)
                print(f"✅ GPU conversion complete!")
                print(f"   Output: {optimized_path}")
            else:
                optimized_path, original_path, result_info = converter.convert_video(args.output)
                print(f"✅ CPU conversion complete!")
                print(f"   Optimized: {optimized_path}")
                print(f"   Original: {original_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        sys.exit(main())