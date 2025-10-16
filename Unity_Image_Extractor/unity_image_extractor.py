# Unity Image Extractor
# Extracts images from Unity3D bundle files and converts them to PNG
# Works with any Unity game files containing Texture2D or Sprite assets

import os
import sys
import UnityPy
from PIL import Image
import glob
import argparse
from pathlib import Path
from datetime import datetime

class UnityImageExtractor:
    def __init__(self, output_dir=None):
        # Follow guidelines: ALWAYS create outputs in the specific helper's subfolder
        script_dir = Path(__file__).parent
        if output_dir is None or output_dir == "extracted_images":
            self.output_dir = str(script_dir / "extracted_images")
        else:
            self.output_dir = output_dir
        self.stats = {"files_processed": 0, "images_extracted": 0, "errors": 0}

    def extract_from_unity_file(self, file_path, output_subdir=None):
        """Extract images from a single Unity3D file"""
        try:
            # Read the file
            with open(file_path, 'rb') as f:
                data = f.read()

            # Find Unity signature
            unity_sig = b'UnityFS'
            offset = data.find(unity_sig)

            if offset == -1:
                print(f"✗ {os.path.basename(file_path)} - No Unity signature found")
                self.stats["errors"] += 1
                return 0

            # Extract Unity data
            unity_data = data[offset:]

            # Create output directory
            base_name = Path(file_path).stem
            if output_subdir:
                output_path = Path(self.output_dir) / output_subdir / base_name
            else:
                output_path = Path(self.output_dir) / base_name

            output_path.mkdir(parents=True, exist_ok=True)

            # Save temp bundle and load with UnityPy
            temp_path = output_path / "temp_unity.bundle"
            with open(temp_path, 'wb') as f:
                f.write(unity_data)

            env = UnityPy.load(str(temp_path))

            extracted_count = 0

            # Process all objects
            for obj in env.objects:
                if obj.type.name in ['Texture2D', 'Sprite']:
                    try:
                        obj_data = obj.read()

                        img = None
                        if hasattr(obj_data, 'image') and obj_data.image:
                            img = obj_data.image

                        if img:
                            # Create safe filename
                            obj_name = getattr(obj_data, 'name', None) or f"{obj.type.name}_{obj.path_id}"
                            safe_name = "".join(c for c in obj_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                            if not safe_name or len(safe_name) < 3:
                                safe_name = f"{obj.type.name}_{extracted_count}"

                            filename = f"{safe_name}.png"
                            output_file = output_path / filename

                            # Save the image
                            img.save(str(output_file))
                            extracted_count += 1

                    except Exception as e:
                        continue

            # Clean up temp file
            try:
                temp_path.unlink()
            except:
                pass

            self.stats["files_processed"] += 1
            self.stats["images_extracted"] += extracted_count

            if extracted_count > 0:
                print(f"✓ {os.path.basename(file_path)} - {extracted_count} images extracted")
            else:
                print(f"- {os.path.basename(file_path)} - No images found")

            return extracted_count

        except Exception as e:
            print(f"✗ {os.path.basename(file_path)} - Error: {e}")
            self.stats["errors"] += 1
            return 0

    def extract_from_directory(self, source_dir, recursive=True):
        """Extract images from all Unity3D files in a directory"""
        source_path = Path(source_dir)

        if not source_path.exists():
            print(f"Error: Source directory {source_dir} does not exist")
            return

        # Find all .unity3d files
        if recursive:
            pattern = "**/*.unity3d"
        else:
            pattern = "*.unity3d"

        unity_files = list(source_path.glob(pattern))

        if not unity_files:
            print(f"No .unity3d files found in {source_dir}")
            return

        print(f"Found {len(unity_files)} Unity3D files")

        # Create output directory
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        total_extracted = 0

        for file_path in unity_files:
            # Create relative output subdir based on source structure
            if recursive and file_path.parent != source_path:
                relative_path = file_path.parent.relative_to(source_path)
                extracted = self.extract_from_unity_file(str(file_path), str(relative_path))
            else:
                extracted = self.extract_from_unity_file(str(file_path))

            total_extracted += extracted

        print("\n=== EXTRACTION COMPLETE ===")
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Images extracted: {self.stats['images_extracted']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Output directory: {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Extract images from Unity3D files")
    parser.add_argument("source", help="Unity3D file or directory containing Unity3D files")
    parser.add_argument("-o", "--output", default="extracted_images",
                       help="Output directory (default: extracted_images)")
    parser.add_argument("-r", "--recursive", action="store_true",
                       help="Recursively search subdirectories")
    parser.add_argument("--no-recursive", action="store_true",
                       help="Don't recursively search subdirectories")

    args = parser.parse_args()

    # Determine recursive behavior
    recursive = args.recursive or not args.no_recursive

    extractor = UnityImageExtractor(args.output)

    source_path = Path(args.source)

    if source_path.is_file():
        if source_path.suffix.lower() == '.unity3d':
            print(f"Extracting from single file: {args.source}")
            extractor.extract_from_unity_file(args.source)
        else:
            print("Error: File must have .unity3d extension")
            sys.exit(1)
    elif source_path.is_dir():
        print(f"Extracting from directory: {args.source}")
        extractor.extract_from_directory(args.source, recursive)
    else:
        print(f"Error: {args.source} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main()