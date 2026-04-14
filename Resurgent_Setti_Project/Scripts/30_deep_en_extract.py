import os
import UnityPy

# Correct path based on DIR
FILE_PATH = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\Document\AddLanguageEN.unity3d"
OUTPUT_TXT = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\en_add_dump.txt"

def extract_manual(bundle_path):
    print(f"Reading: {bundle_path}")
    env = UnityPy.load(bundle_path)
    
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        count = 0 
        for obj in env.objects:
            # Check EVERYTHING that has data
            if obj.type.name in ["TextAsset", "Shader", "MonoBehaviour"]:
                try:
                    data = obj.read()
                    if hasattr(data, "script"):
                        content = data.script
                        # Try decode
                        try:
                            text = content.decode('utf-8')
                            f.write(f"\n[{obj.type.name}] {data.name}\n")
                            f.write(text)
                            count += 1
                        except:
                            pass
                except:
                    pass
        print(f"Items found: {count}")

extract_manual(FILE_PATH)
