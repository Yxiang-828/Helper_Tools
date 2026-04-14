import os
import shutil

SOURCE_DIR = r"c:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump"
TARGET_DIR = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Resurgent_Setti_Files"

# Files identified as relevant
TARGET_FILES = [
    "C_Nair_Final.bytes",
    "C_Nair_Base.bytes",
    "AVG_Setti.bytes",
    "AVG_Setti_Covenant.bytes",
    "T_Nair_Final.bytes",
    "Nair_Final_Texture2D_-1277136603767831672.png", # Example texture found in list_dir earlier
    "MaxSkill.bytes" # Global skill table
]

def collate():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    print(f"Collating files to {TARGET_DIR}...")
    
    # Copy explicitly named files
    for filename in TARGET_FILES:
        src = os.path.join(SOURCE_DIR, filename)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(TARGET_DIR, filename))
            print(f"Copied {filename}")
        else:
            # Try to find partial matches for textures if strict match fails
            pass

    # Also search for any "Nair" file
    for filename in os.listdir(SOURCE_DIR):
        if "Nair" in filename and filename not in TARGET_FILES:
             src = os.path.join(SOURCE_DIR, filename)
             shutil.copy2(src, os.path.join(TARGET_DIR, filename))
             print(f"Copied related file: {filename}")

if __name__ == "__main__":
    collate()
