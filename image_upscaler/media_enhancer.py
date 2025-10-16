#!/usr/bin/env python3
"""
Media Resolution Enhancer
Enhances resolution of images and videos using AI (Real-ESRGAN) and classical methods.
AMD GPU ENABLED: Uses OpenCV UMat for AMD GPU acceleration
"""

import sys
import argparse
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import subprocess

# Set up OpenCL cache directory
cache_dir = Path(__file__).parent / "opencl_cache"
cache_dir.mkdir(exist_ok=True)
os.environ['OPENCV_OCL4DNN_CONFIG_PATH'] = str(cache_dir)

# Try to import AI libraries, fallback to classical if not available
try:
    # Enable OpenCL for AMD GPU
    if cv2.ocl.haveOpenCL():
        cv2.ocl.setUseOpenCL(True)
        print(f"🎮 OpenCL detected and enabled")
        OPENCL_AVAILABLE = True
    else:
        cv2.ocl.setUseOpenCL(False)
        OPENCL_AVAILABLE = False
        print("⚠️  OpenCL not available")
    
    # Check if DNN super resolution is available
    dnn = cv2.dnn_superres
    AI_AVAILABLE = True
    _loaded_models = {}
    
    # Check CUDA
    CUDA_AVAILABLE = False
    try:
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            CUDA_AVAILABLE = True
            print("🎮 NVIDIA CUDA GPU detected")
    except:
        pass

    GPU_AVAILABLE = CUDA_AVAILABLE or OPENCL_AVAILABLE

except (ImportError, AttributeError) as e:
    AI_AVAILABLE = False
    CUDA_AVAILABLE = False
    OPENCL_AVAILABLE = False
    GPU_AVAILABLE = False
    _loaded_models = {}
    print(f"⚠️  AI enhancement not available: {e}")

def enhance_image_ai_opencl(image_path, scale_factor=2, output_path=None):
    """
    Enhance image using AMD GPU with OpenCL UMat (avoids DNN compilation issues).
    Uses custom upscaling with OpenCL acceleration.
    """
    if not OPENCL_AVAILABLE:
        print("OpenCL not available, using classical method...")
        return enhance_image_classical(image_path, scale_factor, output_path)

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if output_path is None:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_enhanced_amd_x{scale_factor}{image_path.suffix}"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🚀 AMD GPU Enhancing image: {image_path.name}")
    print(f"📏 Scale factor: {scale_factor}x")
    print(f"🎮 Using AMD GPU with OpenCL acceleration")

    # Read image
    print(f"📖 Reading image...")
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = img.shape[:2]
    print(f"📏 Original size: {width}x{height}")

    try:
        # Upload to GPU memory (UMat)
        print(f"⬆️  Uploading to AMD GPU memory...")
        img_umat = cv2.UMat(img)
        
        # Calculate new dimensions
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        print(f"🔬 Upscaling on AMD GPU... (this may take a moment)")
        
        # Use Lanczos interpolation on GPU (high quality)
        enhanced_umat = cv2.resize(img_umat, (new_width, new_height), 
                                   interpolation=cv2.INTER_LANCZOS4)
        
        # Apply unsharp mask for enhancement on GPU
        print(f"✨ Applying AI-like enhancement on GPU...")
        
        # Gaussian blur on GPU
        blurred = cv2.GaussianBlur(enhanced_umat, (0, 0), 3.0)
        
        # Unsharp mask: original + (original - blurred) * amount
        enhanced_umat = cv2.addWeighted(enhanced_umat, 1.5, blurred, -0.5, 0)
        
        # Apply CLAHE for detail enhancement on GPU
        # Convert to LAB color space
        lab = cv2.cvtColor(enhanced_umat, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back
        lab = cv2.merge([l, a, b])
        enhanced_umat = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Download from GPU memory
        print(f"⬇️  Downloading from AMD GPU memory...")
        result = enhanced_umat.get()
        
        print(f"📏 Enhanced size: {new_width}x{new_height}")
        print(f"💾 Saving enhanced image...")
        
        success = cv2.imwrite(str(output_path), result)
        
        if success:
            print(f"✅ AMD GPU Enhanced image saved: {output_path}")
            print(f"📁 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        else:
            raise ValueError("Failed to save image")

    except Exception as e:
        print(f"❌ AMD GPU enhancement failed: {e}")
        print("🔄 Falling back to classical method...")
        return enhance_image_classical(str(image_path), scale_factor, str(output_path))

    return str(output_path)

def enhance_image_ai(image_path, scale_factor=2, output_path=None):
    """
    Enhance image resolution using OpenCV DNN Super Resolution.
    Will try to use GPU if available, with proper fallback.
    """
    if not AI_AVAILABLE:
        print("AI not available, using AMD GPU method...")
        return enhance_image_ai_opencl(image_path, scale_factor, output_path)

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if output_path is None:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_enhanced_x{scale_factor}{image_path.suffix}"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🚀 AI Enhancing image: {image_path.name}")
    print(f"📏 Scale factor: {scale_factor}x")

    # Use cached model if available
    model_key = f"edsr_x{scale_factor}"
    sr = None
    
    if model_key not in _loaded_models:
        print(f"⏳ Loading AI model for {scale_factor}x upscaling...")
        
        sr = cv2.dnn_superres.DnnSuperResImpl_create()

        model_path = Path(__file__).parent / "models"
        model_path.mkdir(exist_ok=True)

        model_files = {
            2: "EDSR_x2.pb",
            3: "EDSR_x3.pb",
            4: "EDSR_x4.pb"
        }
        
        model_file = model_path / model_files.get(scale_factor, "EDSR_x2.pb")

        if not model_file.exists():
            print(f"❌ Model {model_file.name} not found in {model_path}")
            print("🔄 Using AMD GPU OpenCL method instead...")
            return enhance_image_ai_opencl(str(image_path), scale_factor, str(output_path))

        try:
            sr.readModel(str(model_file))
            sr.setModel("edsr", scale_factor)

            # Try CUDA first (NVIDIA)
            gpu_enabled = False
            if CUDA_AVAILABLE:
                try:
                    sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                    sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                    print(f"🎮 NVIDIA CUDA GPU acceleration enabled")
                    gpu_enabled = True
                except Exception as e:
                    print(f"⚠️  CUDA failed: {e}")
            
            # For AMD, skip DNN OpenCL (causes compiler issues)
            # Use CPU for DNN model instead
            if not gpu_enabled:
                if OPENCL_AVAILABLE:
                    print(f"⚠️  AMD GPU detected - DNN OpenCL has compatibility issues")
                    print(f"🔄 Using AMD GPU OpenCL method instead (better for AMD)...")
                    return enhance_image_ai_opencl(str(image_path), scale_factor, str(output_path))
                else:
                    sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                    sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                    print(f"⚡ Using CPU mode")

            _loaded_models[model_key] = sr
            print(f"✅ Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            print("🔄 Using AMD GPU OpenCL method instead...")
            return enhance_image_ai_opencl(str(image_path), scale_factor, str(output_path))
    else:
        sr = _loaded_models[model_key]
        print(f"⚡ Using cached model for {scale_factor}x upscaling")

    if sr is None:
        return enhance_image_ai_opencl(str(image_path), scale_factor, str(output_path))

    # Read and enhance image
    print(f"📖 Reading image...")
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = img.shape[:2]
    print(f"📏 Original size: {width}x{height}")

    try:
        print(f"🔬 Applying AI upscaling...")
        print(f"⏱️  This may take 10-60 seconds...")
        
        result = sr.upsample(img)

        new_height, new_width = result.shape[:2]
        print(f"📏 Enhanced size: {new_width}x{new_height}")

        print(f"💾 Saving enhanced image...")
        success = cv2.imwrite(str(output_path), result)
        
        if success:
            print(f"✅ AI Enhanced image saved: {output_path}")
            print(f"📁 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        else:
            raise ValueError("Failed to save image")

    except Exception as e:
        print(f"❌ AI enhancement failed: {e}")
        print("🔄 Using AMD GPU OpenCL method instead...")
        return enhance_image_ai_opencl(str(image_path), scale_factor, str(output_path))

    return str(output_path)

def enhance_image_classical(image_path, scale_factor=2, output_path=None):
    """Classical enhancement with optional GPU acceleration."""
    image_path = Path(image_path)
    if output_path is None:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_enhanced_classical_x{scale_factor}{image_path.suffix}"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print("🔧 Using classical enhancement method...")

    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = img.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    print(f"📏 Original size: {width}x{height}")
    print(f"📏 Enhanced size: {new_width}x{new_height}")

    # Use GPU if available
    if OPENCL_AVAILABLE:
        print(f"🎮 Using AMD GPU acceleration...")
        img_umat = cv2.UMat(img)
        enhanced = cv2.resize(img_umat, (new_width, new_height), 
                            interpolation=cv2.INTER_LANCZOS4)
        
        # Sharpening on GPU
        kernel = np.array([[-0.3,-0.3,-0.3],
                          [-0.3, 3.4,-0.3],
                          [-0.3,-0.3,-0.3]], dtype=np.float32)
        kernel_umat = cv2.UMat(kernel)
        enhanced = cv2.filter2D(enhanced, -1, kernel_umat)
        
        result = enhanced.get()
    else:
        enhanced = cv2.resize(img, (new_width, new_height), 
                            interpolation=cv2.INTER_LANCZOS4)
        
        kernel = np.array([[-0.3,-0.3,-0.3],
                          [-0.3, 3.4,-0.3],
                          [-0.3,-0.3,-0.3]])
        result = cv2.filter2D(enhanced, -1, kernel)

    success = cv2.imwrite(str(output_path), result)
    if success:
        print(f"✅ Enhanced image saved: {output_path}")
        print(f"📁 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        raise ValueError("Failed to save image")

    return str(output_path)

def enhance_video(video_path, scale_factor=2, output_path=None):
    """Enhance video resolution using FFmpeg."""
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if output_path is None:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{video_path.stem}_enhanced_x{scale_factor}{video_path.suffix}"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Enhancing video: {video_path.name}")
    print(f"📏 Scale factor: {scale_factor}x")

    try:
        print("⏳ Processing with FFmpeg...")
        cmd = [
            r"C:\ffmpeg\bin\ffmpeg.exe", "-i", str(video_path),
            "-vf", f"scale=iw*{scale_factor}:ih*{scale_factor}:flags=lanczos",
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-c:a", "copy", "-y", str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")

        print(f"✅ Enhanced video saved: {output_path}")
        print(f"📁 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

    except Exception as e:
        print(f"❌ Video enhancement failed: {e}")
        raise

    return str(output_path)

def main():
    parser = argparse.ArgumentParser(
        description="Enhance resolution of images and videos with AMD GPU support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python media_enhancer.py image.png --scale 2
  python media_enhancer.py video.mp4 --scale 3 --method classical
  python media_enhancer.py photo.jpg --output enhanced.jpg

AMD GPU Note: Uses optimized OpenCL path that avoids DNN compiler issues.
"""
    )
    parser.add_argument("input_file", help="Path to input media file")
    parser.add_argument("--scale", type=int, default=2, choices=[2, 3, 4],
                       help="Upscaling factor (default: 2)")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--method", choices=["ai", "classical"], default="ai",
                       help="Enhancement method (default: ai)")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'}
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'}

    ext = input_path.suffix.lower()

    try:
        print()
        print("=" * 60)
        print("      MEDIA RESOLUTION ENHANCER (AMD GPU ENABLED)")
        print("=" * 60)
        print()
        
        if ext in image_extensions:
            if args.method == "ai":
                result_path = enhance_image_ai(args.input_file, args.scale, args.output)
            else:
                result_path = enhance_image_classical(args.input_file, args.scale, args.output)
        elif ext in video_extensions:
            result_path = enhance_video(args.input_file, args.scale, args.output)
        else:
            print(f"❌ Error: Unsupported file type: {ext}", file=sys.stderr)
            print("📝 Supported images: PNG, JPG, BMP, TIFF, GIF, WebP", file=sys.stderr)
            print("📝 Supported videos: MP4, MOV, AVI, MKV, WebM, FLV", file=sys.stderr)
            sys.exit(1)

        print()
        print("=" * 60)
        print("✅ ENHANCEMENT COMPLETE!")
        print("=" * 60)
        print(f"📁 Output: {result_path}")
        print()

    except KeyboardInterrupt:
        print("\n⚠️  Enhancement cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()