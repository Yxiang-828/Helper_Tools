import cv2
import argparse
import os
import numpy as np

def enhance_image_ai(image_path, scale, output_path):
    """Enhance image using AI EDSR model if available, else classical method."""
    # Read image
    print("[1/5] Loading image...")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    print(f"     Image loaded: {image.shape[0]}x{image.shape[1]}")

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "models", f"EDSR_x{scale}.pb")

    # Try AI method first
    if os.path.exists(model_path):
        try:
            print(f"[2/5] Loading EDSR model: {model_path}")
            # Create super resolution object
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            print("[3/5] Reading model weights...")
            sr.readModel(model_path)
            sr.setModel("edsr", scale)
            print(f"[4/5] Upscaling image {scale}x (this may take 15-30 seconds)...")
            # Upscale
            upscaled = sr.upsample(image)
            print(f"     Upscaling complete! New size: {upscaled.shape[0]}x{upscaled.shape[1]}")
        except Exception as e:
            print(f"Failed to run EDSR model: {e}")
            upscaled = enhance_image_classical(image, scale)
    else:
        print(f"EDSR model not found: {model_path}")
        upscaled = enhance_image_classical(image, scale)

    # Save result
    print("[5/5] Saving result...")
    cv2.imwrite(output_path, upscaled)
    print(f"✅ Saved enhanced image to: {output_path}")

def enhance_image_classical(image, scale):
    """Classical image enhancement using CLAHE + good upsampling + unsharp mask."""
    # Resize using Lanczos
    print("[2/4] Resizing image with Lanczos interpolation...")
    height, width = image.shape[:2]
    new_height, new_width = height * scale, width * scale
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    # Convert to LAB color space
    print("[3/4] Applying adaptive contrast enhancement...")
    lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)

    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = lab[:, :, 0]
    lab[:, :, 0] = clahe.apply(l)

    # Convert back to BGR
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Sharpen using unsharp mask
    print("[4/4] Applying sharpening filter...")
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 1.0)
    sharpened = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)

    return sharpened

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance image using EDSR or classical method")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("--scale", type=int, default=4, choices=[2,3,4], help="Upscale factor")
    parser.add_argument("--output", required=True, help="Output image path")

    args = parser.parse_args()

    try:
        enhance_image_ai(args.input, args.scale, args.output)
        print("\n✅ Enhancement completed successfully")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
