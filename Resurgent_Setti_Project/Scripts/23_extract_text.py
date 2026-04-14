import os
import UnityPy
import json

# Target Bundles
PATH_JA = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\LanResObj\LanResObj.unity3d"
PATH_EN = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\LanResObj\LanResObj_en_add.unity3d"

OUTPUT_TXT = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\raw_text_dump.txt"

def extract_text(bundle_path, label):
    print(f"--- Extracting {label} ---")
    if not os.path.exists(bundle_path):
        print(f"Missing: {bundle_path}")
        return

    env = UnityPy.load(bundle_path)
    
    found_any = False
    
    with open(OUTPUT_TXT, 'a', encoding='utf-8') as f:
        f.write(f"\n=== SOURCE: {label} ===\n")
        
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                # Try to decode as text
                try:
                    text_content = data.script.decode('utf-8')
                    # Naively filter for Nair/Setti keywords or IDs to keep it readable, 
                    # OR just dump everything for grep. Let's dump everything first to analyze format.
                    f.write(f"\n--- File: {data.name} ---\n")
                    f.write(text_content)
                    found_any = True
                except:
                    f.write(f"\n--- File: {data.name} (Binary/Fail) ---\n")

    if found_any:
        print("Text assets found and dumped.")
    else:
        print("No readable TextAssets found.")

# Clear previous
if os.path.exists(OUTPUT_TXT):
    os.remove(OUTPUT_TXT)

# Extract default (likely CN/JP base) and EN add-on
extract_text(PATH_JA, "Base_Lang")
extract_text(PATH_EN, "EN_Add")
