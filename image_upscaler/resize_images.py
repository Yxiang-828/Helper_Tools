import cv2
import os
from pathlib import Path

def get_image_dimensions(image_path):
    """Get image dimensions."""
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    height, width = img.shape[:2]
    return width, height

def resize_image_to_match(input_path, reference_path, output_path):
    """Resize input image to match the dimensions of reference image."""
    # Get reference dimensions
    ref_dims = get_image_dimensions(reference_path)
    if ref_dims is None:
        print(f"Failed to load reference image: {reference_path}")
        return

    ref_width, ref_height = ref_dims

    # Load input image
    img = cv2.imread(str(input_path))
    if img is None:
        print(f"Failed to load input image: {input_path}")
        return

    # Resize to match reference dimensions
    resized = cv2.resize(img, (ref_width, ref_height), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(str(output_path), resized)
    print(f"Resized {input_path.name} to match {reference_path.name}: {ref_width}x{ref_height}")

def main():
    base_dir = Path(__file__).parent

    # Resize samples to match their upscaled versions
    samples_dir = base_dir / "samples"
    output_dir = base_dir / "output"
    resized_samples_dir = base_dir / "resized_samples"
    resized_samples_dir.mkdir(exist_ok=True)

    # Process each original sample - resize to 256x256 squares
    for sample_file in samples_dir.glob("*"):
        if sample_file.is_file() and sample_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            output_path = resized_samples_dir / sample_file.name
            resize_image_to_square(sample_file, output_path)

    # Resize outputs to squares (from resized_output directory)
    resized_output_dir = base_dir / "resized_output"
    resized_output_dir.mkdir(exist_ok=True)

    # Clear existing resized_output and copy from output, then resize
    for item in resized_output_dir.glob("*"):
        item.unlink()

    # Copy all output files to resized_output first
    for img_file in output_dir.glob("*"):
        if img_file.is_file():
            import shutil
            shutil.copy2(img_file, resized_output_dir / img_file.name)

    # Now resize all files in resized_output to squares
    for img_file in resized_output_dir.glob("*.png"):
        temp_path = resized_output_dir / f"temp_{img_file.name}"
        resize_image_to_square(img_file, temp_path)
        temp_path.replace(img_file)  # Replace original with resized

    for img_file in resized_output_dir.glob("*.jpg"):
        temp_path = resized_output_dir / f"temp_{img_file.name}"
        resize_image_to_square(img_file, temp_path)
        temp_path.replace(img_file)  # Replace original with resized

def resize_image_to_square(input_path, output_path, size=256):
    """Resize image to exact square dimensions with white padding."""
    img = cv2.imread(str(input_path))
    if img is None:
        print(f"Failed to load {input_path}")
        return

    height, width = img.shape[:2]

    # Calculate scaling factor to fit within square
    scale = size / max(width, height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Ensure minimum size of 1 pixel
    new_width = max(1, new_width)
    new_height = max(1, new_height)

    # Resize image
    resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    # Create exact square canvas with white padding
    top_pad = (size - new_height) // 2
    bottom_pad = size - new_height - top_pad
    left_pad = (size - new_width) // 2
    right_pad = size - new_width - left_pad

    square_img = cv2.copyMakeBorder(
        resized,
        top=top_pad,
        bottom=bottom_pad,
        left=left_pad,
        right=right_pad,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]  # White padding
    )

    # Ensure exact dimensions
    square_img = cv2.resize(square_img, (size, size), interpolation=cv2.INTER_LANCZOS4)

    cv2.imwrite(str(output_path), square_img)
    print(f"Resized {input_path.name} to exact {size}x{size} square")

if __name__ == "__main__":
    main()