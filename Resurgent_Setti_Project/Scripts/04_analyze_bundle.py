import os
import UnityPy

BUNDLE_PATH = r"c:\Users\xiang\Helper_Tools\temp_inspect.bundle"
OUTPUT_DIR = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data"

def extract_bundle():
    if not os.path.exists(BUNDLE_PATH):
        print(f"Bundle not found: {BUNDLE_PATH}")
        return

    print(f"Loading bundle: {BUNDLE_PATH}")
    env = UnityPy.load(BUNDLE_PATH)
    
    extracted = []
    
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            data = obj.read()
            name = getattr(data, "m_Name", "Unknown")
            script = data.script
            
            # Save it
            out_file = os.path.join(OUTPUT_DIR, f"{name}.txt")
            with open(out_file, "wb") as f:
                f.write(script)
            
            extracted.append(name)
            print(f"Extracted TextAsset: {name}")

    if not extracted:
        print("No TextAssets found in bundle.")

if __name__ == "__main__":
    try:
        extract_bundle()
    except Exception as e:
        print(f"Error: {e}")
