try:
    from rembg import remove
    from PIL import Image
    import os
    import sys
except ImportError as e:
    print("Error: Required libraries not found.")
    print(f"Details: {e}")
    print("Please install required packages using: pip install rembg pillow")
    sys.exit(1)

def process_images():
    input_dir = "input"
    output_dir = "output"
    
    # Ensure directories exist
    if not os.path.exists(input_dir):
        print(f"Creating input directory: {input_dir}")
        os.makedirs(input_dir)
        print("Please place images in the 'input' folder and run again.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of image files
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]
    
    if not files:
        print("No image files found in 'input' folder.")
        return

    print(f"Found {len(files)} images to process...")
    
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        # Create output filename (always png for transparency)
        output_filename = os.path.splitext(filename)[0] + "_nobg.png"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"Processing: {filename} -> {output_filename}")
        
        try:
            with open(input_path, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input_data = i.read()
                    output_data = remove(input_data)
                    o.write(output_data)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

    print("\nProcessing complete! Check 'output' folder.")

if __name__ == "__main__":
    # Change working directory to script location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    process_images()
