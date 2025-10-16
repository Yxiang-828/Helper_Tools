# Unity3D Image Finder
# This script scans all .unity3d files in the Characters folder and logs which files contain images.
# It will print a summary of which files have images and how many.

import os
import UnityPy

# Use relative path based on script location
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))
CHARACTERS_DIR = os.path.join(parent_dir, "extracted_assets", "Characters")
report = []

for filename in os.listdir(CHARACTERS_DIR):
    if filename.endswith(".unity3d"):
        file_path = os.path.join(CHARACTERS_DIR, filename)
        env = UnityPy.load(file_path)
        count = 0
        for obj in env.objects:
            if obj.type.name in ["Texture2D", "Sprite"]:
                try:
                    data = obj.read()
                    img = data.image
                    if img:
                        count += 1
                except Exception:
                    continue
        if count > 0:
            report.append(f"{filename}: {count} images found")
        else:
            report.append(f"{filename}: no images found")

with open(os.path.join(CHARACTERS_DIR, "unity3d_image_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Scan complete. See unity3d_image_report.txt for results.")
