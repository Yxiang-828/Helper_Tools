#!/usr/bin/env python3
"""
Efficient Video Upscaler for AMD GPU on Windows
Uses batch processing with Real-ESRGAN + FFmpeg
Preserves audio and uses AMD hardware encoding
"""

import subprocess
import argparse
import shutil
from pathlib import Path
import tempfile
import os
import sys
import time

def check_ffmpeg():
    """Check if FFmpeg is available."""
    if not shutil.which('ffmpeg'):
        print("FFmpeg not found!")
        print("   Download from: https://www.gyan.dev/ffmpeg/builds/")
        print("   Extract and add to PATH, or place in script directory")
        return False
    return True

def get_video_info(video_path):
    """Get video metadata."""
    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-hide_banner'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        stderr = result.stderr

        import re
        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})', stderr)
        fps_match = re.search(r'(\d+(?:\.\d+)?) fps', stderr)
        resolution_match = re.search(r'(\d{3,4})x(\d{3,4})', stderr)

        info = {}
        if duration_match:
            h, m, s = map(int, duration_match.groups())
            info['duration_sec'] = h * 3600 + m * 60 + s
        if fps_match:
            info['fps'] = float(fps_match.group(1))
        if resolution_match:
            info['width'] = int(resolution_match.group(1))
            info['height'] = int(resolution_match.group(2))

        return info
    except:
        return {}

def upscale_video_ffmpeg(video_path, output_path, scale):
    """
    Fast upscaling using FFmpeg with AMD GPU encoder.
    Good quality, very fast, preserves audio.
    """
    print("Method: FFmpeg + AMD VCE Hardware Encoding")
    print("   Quality: Good (Lanczos interpolation)")
    print("   Speed: Very Fast (2-5 min for 1080p)")
    print()

    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vf', f'scale=iw*{scale}:ih*{scale}:flags=lanczos',
        '-c:v', 'h264_amf',
        '-quality', 'quality',
        '-rc', 'cqp',
        '-qp_i', '18',
        '-qp_p', '18',
        '-c:a', 'copy',
        '-y',
        str(output_path)
    ]

    print("Running FFmpeg...\n")

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

    import re
    progress_pattern = re.compile(r'frame=\s*(\d+)')

    for line in process.stderr:
        match = progress_pattern.search(line)
        if match:
            current_frame = int(match.group(1))
            if current_frame % 10 == 0:
                print(f"Processed {current_frame} frames...", end="\r", flush=True)

    process.wait()
    print(" " * 50 + "\r", end="", flush=True)  # Clear line

    if process.returncode == 0:
        print("FFmpeg completed successfully!")
        return True
    else:
        print("\nAMD encoder failed, trying CPU encoder...")
        cmd[cmd.index('h264_amf')] = 'libx264'
        cmd.remove('-quality')
        cmd.remove('quality')
        cmd.remove('-rc')
        cmd.remove('cqp')
        cmd.remove('-qp_i')
        cmd.remove('18')
        cmd.remove('-qp_p')
        cmd.remove('18')
        cmd.insert(cmd.index('libx264') + 1, '-preset')
        cmd.insert(cmd.index('libx264') + 2, 'fast')  # Changed from 'slow' to 'fast' for better speed
        cmd.insert(cmd.index('libx264') + 3, '-crf')
        cmd.insert(cmd.index('libx264') + 4, '18')

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

        for line in process.stderr:
            match = progress_pattern.search(line)
            if match:
                current_frame = int(match.group(1))
                if current_frame % 10 == 0:
                    print(f"Processed {current_frame} frames...", end="\r", flush=True)

        process.wait()
        print(" " * 50 + "\r", end="", flush=True)  # Clear line

        if process.returncode == 0:
            print("FFmpeg completed successfully with CPU encoder!")
            return True
        else:
            return False

def extract_frames_only(video_path, output_dir):
    """
    Simple frame extraction - no upscaling, just save frames to output folder
    """
    print("Extracting frames only (no upscaling)...")

    # Create output directory
    frames_dir = output_dir / f"{video_path.stem}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving frames to: {frames_dir}")

    # Extract frames
    extract_cmd = [
        'ffmpeg', '-i', str(video_path),
        '-qscale:v', '1',
        str(frames_dir / 'frame_%06d.png'),
        '-hide_banner', '-loglevel', 'error'
    ]

    subprocess.run(extract_cmd, check=True)

    frame_count = len(list(frames_dir.glob('*.png')))
    print(f"✓ Extracted {frame_count} frames to {frames_dir}")

    return frames_dir
    """
    High-quality upscaling using Real-ESRGAN AI anime model.
    Processes each frame individually with large tiles to prevent artifacts.
    """
    print("Method: Real-ESRGAN AI Model (Vulkan GPU)")
    print("   Quality: Excellent (AI upscaling)")
    print("   Speed: Frame-by-frame processing")
    print()

    realesrgan_exe = script_dir / "realesrgan-windows" / "realesrgan-ncnn-vulkan.exe"
    if not realesrgan_exe.exists():
        print(f"Real-ESRGAN not found: {realesrgan_exe}")
        print("   Download from: https://github.com/xinntao/Real-ESRGAN/releases")
        print("   Extract to: realesrgan-windows/")
        return False

    # Test if Real-ESRGAN executable exists and is accessible
    print("Testing Real-ESRGAN...")
    if not os.access(str(realesrgan_exe), os.X_OK):
        print(f"   ✗ Real-ESRGAN not executable!")
        return False
    print("   ✓ Real-ESRGAN is accessible\n")

    # Create persistent output directory for frames (don't use temp)
    script_dir = Path(__file__).parent
    persistent_frames_dir = script_dir / "output" / f"{video_path.stem}_frames_x{scale}"
    persistent_frames_dir.mkdir(parents=True, exist_ok=True)

    print(f"   💾 Saving frames to: {persistent_frames_dir}")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        frames_dir = temp_path / "frames"
        frames_dir.mkdir()

        # Get FPS for reassembly
        info = get_video_info(video_path)
        fps = info.get('fps', 30)
        duration = info.get('duration_sec', 0)

        print("Step 1: Extracting frames...")
        extract_cmd = [
            'ffmpeg', '-i', str(video_path),
            '-qscale:v', '1',
            str(frames_dir / 'frame_%06d.png'),
            '-hide_banner', '-loglevel', 'error'
        ]
        subprocess.run(extract_cmd, check=True)

        frame_count = len(list(frames_dir.glob('*.png')))
        print(f"   ✓ Extracted {frame_count} frames\n")

        # Process frames one by one with progress display
        print("Step 2: Upscaling frames with Real-ESRGAN...")
        print("   Processing each frame individually for reliable progress tracking")
        print("   💾 Frames saved persistently - can resume if interrupted\n")

        frame_files = sorted(frames_dir.glob('*.png'))
        total_frames = len(frame_files)
        print(f"   Found {total_frames} frames to process")

        start_time = time.time()
        processed_count = 0

        for i, frame_file in enumerate(frame_files, 1):
            upscaled_file = persistent_frames_dir / frame_file.name

            # Skip if already processed
            if upscaled_file.exists():
                processed_count += 1
                continue

            # Show progress
            progress = f"Processing frame {i}/{total_frames} ({i/total_frames*100:.1f}%)"
            print(f"\r{progress}", end="", flush=True)

            # Process single frame with Real-ESRGAN
            upscale_cmd = [
                str(realesrgan_exe),
                '-i', str(frame_file),
                '-o', str(upscaled_file),
                '-s', str(scale),
                '-n', 'realesrgan-x4plus',  # Use regular model instead of anime
                '-m', str(realesrgan_exe.parent / 'models'),
                '-t', '512',  # Smaller tile that might fit in VRAM
            ]

            # Try running Real-ESRGAN
            result = subprocess.run(upscale_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                stderr = result.stderr or result.stdout or ''
                print(f"\n   ✗ Failed to upscale {frame_file.name}: {stderr}")
                return False
            else:
                processed_count += 1

            # Verify the frame was actually created
            if not upscaled_file.exists():
                print(f"\n   ✗ Upscaled frame not found: {upscaled_file}")
                return False

        elapsed = time.time() - start_time
        print(f"\n   ✓ Successfully processed {processed_count}/{total_frames} frames\n")

        # Verify upscaled frames exist and have correct dimensions
        print("Step 2.5: Verifying upscaled frames...")
        upscaled_files = list(persistent_frames_dir.glob('*.png'))
        if len(upscaled_files) != processed_count:
            print(f"   ✗ Expected {processed_count} upscaled frames, found {len(upscaled_files)}")
            return False

        # Check dimensions of first frame
        try:
            import cv2
            first_frame = cv2.imread(str(upscaled_files[0]))
            if first_frame is None:
                print("   ✗ Could not read upscaled frame")
                return False
            h, w = first_frame.shape[:2]
            expected_w, expected_h = 1514 * scale, 848 * scale
            if w != expected_w or h != expected_h:
                print(f"   ✗ Frame dimensions wrong: {w}x{h}, expected {expected_w}x{expected_h}")
                return False

            # Check file sizes
            total_size = sum(f.stat().st_size for f in upscaled_files)
            avg_size = total_size / len(upscaled_files)
            print(f"   ✓ Verified {len(upscaled_files)} frames at {w}x{h}")
            print(f"   ✓ Total frame size: {total_size/1024/1024:.1f} MB, avg: {avg_size/1024:.0f} KB per frame\n")
        except ImportError:
            print("   ⚠ Could not verify frame dimensions (OpenCV not available)\n")
        except Exception as e:
            print(f"   ✗ Error verifying frames: {e}\n")
            return False
        print("Step 3: Reassembling video with audio...")

        # Debug: Check frame pattern
        frame_pattern = persistent_frames_dir / 'frame_%06d.png'
        print(f"   Looking for frames: {frame_pattern}")
        test_frames = list(persistent_frames_dir.glob('frame_*.png'))
        print(f"   Found {len(test_frames)} frame files")
        if test_frames:
            print(f"   Sample frame: {test_frames[0].name}")

        reassemble_cmd = [
            'ffmpeg',
            '-framerate', str(fps),
            '-i', str(persistent_frames_dir / 'frame_%06d.png'),
            '-i', str(video_path),
            '-map', '0:v',
            '-map', '1:a?',
            '-c:v', 'h264_amf',
            '-quality', 'quality',
            '-rc', 'cqp',
            '-qp_i', '18',
            '-qp_p', '18',
            '-c:a', 'copy',
            '-shortest',
            '-y',
            str(output_path),
            '-hide_banner'
        ]

        try:
            result = subprocess.run(reassemble_cmd, capture_output=True, text=True, timeout=300)  # 5 minute timeout
            if result.returncode != 0:
                print(f"   AMD encoder failed: {result.stderr}")
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("   AMD encoder failed, using CPU encoder...")
            # Create fresh CPU encoding command
            cpu_cmd = [
                'ffmpeg',
                '-framerate', str(fps),
                '-i', str(persistent_frames_dir / 'frame_%06d.png'),
                '-i', str(video_path),
                '-map', '0:v',
                '-map', '1:a?',
                '-c:v', 'libx264',
                '-preset', 'slow',
                '-crf', '18',
                '-c:a', 'copy',
                '-shortest',
                '-y',
                str(output_path),
                '-hide_banner'
            ]
            try:
                result = subprocess.run(cpu_cmd, capture_output=True, text=True, timeout=600)
                if result.returncode != 0:
                    print(f"   CPU encoder also failed: {result.stderr}")
                    return False
            except subprocess.TimeoutExpired:
                print("   ✗ CPU encoding timed out after 10 minutes")
                return False

        print("   ✓ Video reassembled with audio\n")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Efficient Video Upscaler for AMD GPU on Windows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Methods:
  ffmpeg     = Fast (Lanczos), uses AMD VCE, good quality, preserves audio
  realesrgan = AI anime upscaling, processes each frame individually with progress tracking

Examples:
  py video_upscaler.py video.mp4 --method ffmpeg --scale 4
  py video_upscaler.py video.mp4 --method realesrgan --scale 4 --format gif
  py video_upscaler.py video.mp4 --method extract
  py video_upscaler.py video.mp4 --method process_existing --format mp4
"""
    )

    parser.add_argument('input', help='Input video file')
    parser.add_argument('--output', help='Output file path (optional, auto-generated if not specified)')
    parser.add_argument('--scale', type=int, default=4, choices=[2,3,4],
                       help='Upscale factor (default: 4)')
    parser.add_argument('--method', choices=['ffmpeg', 'realesrgan', 'extract', 'process_existing'], default='realesrgan',
                       help='Upscaling method, extract for frame extraction only, process_existing for upscaling already extracted frames')
    parser.add_argument('--format', choices=['mp4', 'gif'], default='mp4',
                       help='Output format (default: mp4)')

    args = parser.parse_args()

    if not check_ffmpeg():
        sys.exit(1)

    video_path = Path(args.input)
    if not video_path.exists():
        print(f"Video not found: {video_path}")
        sys.exit(1)

    script_dir = Path(__file__).parent
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)

    if args.output:
        output_path = Path(args.output)
    else:
        suffix = 'ai' if args.method == 'realesrgan' else 'fast'
        extension = args.format
        output_path = output_dir / f"{video_path.stem}_upscaled_x{args.scale}_{suffix}.{extension}"

    print(f"\n{'='*70}")
    print("AMD GPU Video Upscaler")
    print(f"{'='*70}")
    print(f"Input: {video_path.name}")

    info = get_video_info(video_path)
    if info:
        if 'width' in info and 'height' in info:
            print(f"Resolution: {info['width']}x{info['height']} → {info['width']*args.scale}x{info['height']*args.scale}")
        if 'fps' in info:
            print(f"FPS: {info['fps']:.2f}")
        if 'duration_sec' in info:
            mins = info['duration_sec'] // 60
            secs = info['duration_sec'] % 60
            print(f"Duration: {mins}m {secs}s")

    print(f"Scale: {args.scale}x")
    print(f"Output: {output_path.name}")
    print(f"{'='*70}\n")

    try:
        if args.method == 'extract':
            success = extract_frames_only(video_path, output_dir)
        elif args.method == 'process_existing':
            success = process_existing_frames(script_dir, args.scale, video_path, output_path, args.format)
        elif args.method == 'ffmpeg':
            success = upscale_video_ffmpeg(video_path, output_path, args.scale)
        else:
            success = upscale_video_realesrgan(video_path, output_path, args.scale, script_dir, args.format)

        if args.method == 'extract':
            print(f"{'='*70}")
            print("✓ FRAME EXTRACTION COMPLETE!")
            print(f"{'='*70}")
            print(f"Frames saved to: {output_dir / f'{video_path.stem}_frames'}")

            # Ask about cleanup for extracted frames
            cleanup_frames(script_dir)

            print(f"{'='*70}\n")
        elif args.method == 'process_existing':
            if success:
                print(f"{'='*70}")
                print("✓ FRAME UPSCALING COMPLETE!")
                print(f"{'='*70}")
                print(f"Upscaled frames saved to output folder")

                # Ask about cleanup
                cleanup_frames(script_dir)

                print(f"{'='*70}\n")
        elif success and output_path.exists():
            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"{'='*70}")
            print("✓ SUCCESS!")
            print(f"{'='*70}")
            print(f"Output: {output_path}")
            print(f"Size: {size_mb:.1f} MB")
            print(f"{'='*70}\n")

            # Ask about cleanup for realesrgan method
            if args.method == 'realesrgan':
                cleanup_frames(script_dir)
        else:
            print("\n✗ Video processing failed")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n✗ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def upscale_video_realesrgan(video_path, output_path, scale, script_dir, output_format='mp4'):
    """
    Full Real-ESRGAN workflow: extract frames → upscale → reassemble
    """
    print("Method: Real-ESRGAN (AI Upscaling)")
    print("   Extracting frames → AI upscaling each frame → Reassembling video")
    print()

    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Step 1: Extract frames
    frames_dir = output_dir / f"{video_path.stem}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    print(f"Step 1: Extracting frames to {frames_dir}")

    extract_cmd = [
        'ffmpeg', '-i', str(video_path),
        '-qscale:v', '1',
        str(frames_dir / 'frame_%06d.png'),
        '-hide_banner', '-loglevel', 'error'
    ]

    result = subprocess.run(extract_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Frame extraction failed: {result.stderr}")
        return False

    frame_count = len(list(frames_dir.glob('*.png')))
    print(f"✓ Extracted {frame_count} frames")

    # Step 2: Upscale frames
    upscaled_dir = output_dir / f"{frames_dir.name}_upscaled_x{scale}"
    upscaled_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nStep 2: Upscaling {frame_count} frames to {upscaled_dir}")

    realesrgan_exe = script_dir / "realesrgan-windows" / "realesrgan-ncnn-vulkan.exe"
    if not realesrgan_exe.exists():
        print(f"Real-ESRGAN not found: {realesrgan_exe}")
        print("   Download from: https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan")
        print("   Extract to: realesrgan-windows/")
        return False

    frame_files = sorted(frames_dir.glob('*.png'))
    processed_count = 0

    for i, frame_file in enumerate(frame_files, 1):
        upscaled_file = upscaled_dir / frame_file.name

        # Skip if already processed
        if upscaled_file.exists():
            processed_count += 1
            continue

        # Use anime model for better quality
        model_name = f'realesr-animevideov3-x{scale}'

        upscale_cmd = [
            str(realesrgan_exe),
            '-i', str(frame_file),
            '-o', str(upscaled_file),
            '-n', model_name,
            '-m', str(realesrgan_exe.parent / 'models'),
            '-s', str(scale),
            '-f', 'png'
        ]

        result = subprocess.run(upscale_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            processed_count += 1
            progress = f"Processed {processed_count}/{frame_count} frames ({processed_count/frame_count*100:.1f}%)"
            print(f"\r{progress}", end="", flush=True)
        else:
            print(f"\nFailed to upscale {frame_file.name}: {result.stderr}")

    print(f"\n✓ Successfully processed {processed_count}/{frame_count} frames")

    # Step 3: Reassemble
    if processed_count == frame_count:
        print("\nStep 3: Reassembling video...")
        return reassemble_video_from_frames(upscaled_dir, video_path, output_path, script_dir, output_format)

    return processed_count > 0
    """
    Process already extracted frames in the output folder - simple Real-ESRGAN per frame
    """
    print("Method: Process Existing Frames")
    print("   Running Real-ESRGAN on each PNG frame individually")
    print()

    output_dir = script_dir / "output"
    frames_dirs = list(output_dir.glob("*_frames"))

    if not frames_dirs:
        print("No frame directories found in output folder")
        return False

    frames_dir = frames_dirs[0]  # Use the first one found
    print(f"Found frames in: {frames_dir}")

    # Create upscaled directory
    upscaled_dir = output_dir / f"{frames_dir.name}_upscaled_x{scale}"
    upscaled_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving upscaled frames to: {upscaled_dir}")

    realesrgan_exe = script_dir / "realesrgan-windows" / "realesrgan-ncnn-vulkan.exe"
    if not realesrgan_exe.exists():
        print(f"Real-ESRGAN not found: {realesrgan_exe}")
        return False

    frame_files = sorted(frames_dir.glob('*.png'))
    total_frames = len(frame_files)
    print(f"Found {total_frames} frames to upscale")

    processed_count = 0

    for i, frame_file in enumerate(frame_files, 1):
        upscaled_file = upscaled_dir / frame_file.name

        # Skip if already processed
        if upscaled_file.exists():
            processed_count += 1
            continue

        progress = f"Processing frame {i}/{total_frames} ({i/total_frames*100:.1f}%)"
        print(f"\r{progress}", end="", flush=True)

        # Simple Real-ESRGAN command - exactly like single image upscaler
        upscale_cmd = [
            str(realesrgan_exe),
            '-i', str(frame_file),
            '-o', str(upscaled_file),
            '-s', str(scale),
            '-n', 'realesr-animevideov3-x2',  # Correct anime model for x2
            '-m', str(realesrgan_exe.parent / 'models'),
            '-f', 'png'
        ]

        result = subprocess.run(upscale_cmd, capture_output=True, text=True)

        if result.returncode == 0 and upscaled_file.exists():
            processed_count += 1
        else:
            print(f"\nFailed to upscale {frame_file.name}: {result.stderr}")
            continue

    print(f"\n✓ Successfully processed {processed_count}/{total_frames} frames")

    # Now reassemble into video
    if processed_count == total_frames:
        print("\nReassembling video from upscaled frames...")
        return reassemble_video_from_frames(upscaled_dir, video_path, output_path, script_dir, output_format)

    return processed_count > 0

def cleanup_frames(script_dir):
    """
    Ask user if they want to keep the frame folders and clean up if not
    """
    output_dir = script_dir / "output"
    frame_dirs = list(output_dir.glob("*_frames*"))

    if not frame_dirs:
        return

    print("\nFrame folders found:")
    for i, d in enumerate(frame_dirs, 1):
        size_mb = sum(f.stat().st_size for f in d.glob("*.png")) / 1024 / 1024
        print(f"  {i}. {d.name} ({size_mb:.1f} MB)")

    print(f"\nThese folders contain the extracted and upscaled frames.")
    print(f"They take up significant disk space but can be useful for debugging.")

    while True:
        response = input("\nDo you want to keep these frame folders? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("Keeping frame folders.")
            break
        elif response in ['n', 'no']:
            print("Deleting frame folders to save disk space...")
            for frame_dir in frame_dirs:
                try:
                    import shutil
                    shutil.rmtree(frame_dir)
                    print(f"  ✓ Deleted {frame_dir.name}")
                except Exception as e:
                    print(f"  ✗ Failed to delete {frame_dir.name}: {e}")
            print("Cleanup complete.")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def reassemble_video_from_frames(frames_dir, original_video, output_path, script_dir, output_format='mp4'):
    """
    Reassemble upscaled frames back into video with original audio, or create GIF
    """
    # Get video info
    info = get_video_info(original_video)
    fps = info.get('fps', 30)

    # Determine scale from frames_dir name
    import re
    scale_match = re.search(r'_x(\d+)', frames_dir.name)
    scale = int(scale_match.group(1)) if scale_match else 4

    width = info.get('width', 1920) * scale
    height = info.get('height', 1080) * scale

    if width > 4000 or height > 2000:
        qp = '24'
        preset = 'ultrafast'
        crf = 28
    else:
        qp = '18'
        preset = 'fast'
        crf = 18

    if output_format == 'gif':
        print(f"Creating GIF at {fps} FPS...")
        try:
            import moviepy
            ImageSequenceClip = moviepy.ImageSequenceClip
            import glob

            # Get all frame files
            frame_pattern = str(frames_dir / 'frame_*.png')
            frame_files = sorted(glob.glob(frame_pattern))

            if not frame_files:
                print("No frame files found for GIF creation")
                return False

            # Create GIF clip
            clip = ImageSequenceClip(frame_files, fps=fps)

            # Write GIF
            clip.write_gif(str(output_path), fps=fps)

            print("✓ GIF created successfully!")
            return True

        except ImportError:
            print("MoviePy not available for GIF creation. Install with: pip install moviepy")
            return False
        except Exception as e:
            print(f"GIF creation failed: {e}")
            return False

    # MP4 reassembly
    print(f"Reassembling MP4 at {fps} FPS...")

    # For high resolutions, skip AMD encoding as it may fail
    use_amd = not (width > 4000 or height > 2000)
    if use_amd:
        encoder = 'h264_amf'
        extra_args = ['-quality', 'quality', '-rc', 'cqp', '-qp_i', qp, '-qp_p', qp]
    else:
        encoder = 'libx264'
        extra_args = ['-preset', preset, '-crf', str(crf)]

    # FFmpeg command to create video from frames
    reassemble_cmd = [
        'ffmpeg',
        '-framerate', str(fps),
        '-i', str(frames_dir / 'frame_%06d.png'),
        '-i', str(original_video),  # Original video for audio
        '-map', '0:v',  # Video from frames
        '-map', '1:a?',  # Audio from original (optional)
        '-c:v', encoder,
    ] + extra_args + [
        '-c:a', 'copy',  # Copy audio
        '-shortest',
        '-y',
        str(output_path),
        '-hide_banner'
    ]

    try:
        result = subprocess.run(reassemble_cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            if use_amd:
                print("✓ Video reassembled with AMD encoding!")
            else:
                print("✓ Video reassembled with CPU encoding!")
            return True
        else:
            if use_amd:
                print(f"AMD encoder failed: {result.stderr}")
                # Try CPU encoding
                print("Trying CPU encoding...")
                cpu_cmd = reassemble_cmd.copy()
                cpu_cmd[cpu_cmd.index('h264_amf')] = 'libx264'
                cpu_cmd.remove('-quality')
                cpu_cmd.remove('quality')
                cpu_cmd.remove('-rc')
                cpu_cmd.remove('cqp')
                cpu_cmd.remove('-qp_i')
                cpu_cmd.remove(qp)
                cpu_cmd.remove('-qp_p')
                cpu_cmd.remove(qp)
                cpu_cmd.insert(cpu_cmd.index('libx264') + 1, '-preset')
                cpu_cmd.insert(cpu_cmd.index('libx264') + 2, preset)
                cpu_cmd.insert(cpu_cmd.index('libx264') + 3, '-crf')
                cpu_cmd.insert(cpu_cmd.index('libx264') + 4, str(crf))

                result = subprocess.run(cpu_cmd, capture_output=True, text=True, timeout=600)
                if result.returncode == 0:
                    print("✓ Video reassembled with CPU encoding!")
                    return True
                else:
                    print(f"CPU encoding also failed: {result.stderr}")
                    return False
            else:
                print(f"CPU encoding failed: {result.stderr}")
                return False
    except subprocess.TimeoutExpired:
        print("✗ Video reassembly timed out")
        return False

def cleanup_frames(script_dir, force_delete=False):
    """
    Ask user if they want to keep the frame folders and clean up if not
    """
    output_dir = script_dir / "output"
    frame_dirs = list(output_dir.glob("*_frames*"))

    if not frame_dirs:
        return

    if force_delete:
        print("Deleting frame folders to save disk space...")
        for frame_dir in frame_dirs:
            try:
                import shutil
                shutil.rmtree(frame_dir)
                print(f"  ✓ Deleted {frame_dir.name}")
            except Exception as e:
                print(f"  ✗ Failed to delete {frame_dir.name}: {e}")
        print("Cleanup complete.")
        return

    print("\nFrame folders found:")
    for i, d in enumerate(frame_dirs, 1):
        size_mb = sum(f.stat().st_size for f in d.glob("*.png")) / 1024 / 1024
        print(f"  {i}. {d.name} ({size_mb:.1f} MB)")

    print(f"\nThese folders contain the extracted and upscaled frames.")
    print(f"They take up significant disk space but can be useful for debugging.")

    while True:
        response = input("\nDo you want to keep these frame folders? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("Keeping frame folders.")
            break
        elif response in ['n', 'no']:
            print("Deleting frame folders to save disk space...")
            for frame_dir in frame_dirs:
                try:
                    import shutil
                    shutil.rmtree(frame_dir)
                    print(f"  ✓ Deleted {frame_dir.name}")
                except Exception as e:
                    print(f"  ✗ Failed to delete {frame_dir.name}: {e}")
            print("Cleanup complete.")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")

if __name__ == '__main__':
    main()
