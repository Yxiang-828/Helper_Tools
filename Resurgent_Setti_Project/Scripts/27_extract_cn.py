import os
import UnityPy

FILE_PATH = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\Document\AllLanguageCNTraditional.unity3d"
OUTPUT_TXT = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\cn_text_dump.txt"

def extract(bundle_path):
    print(f"Extracting: {os.path.basename(bundle_path)}")
    env = UnityPy.load(bundle_path)
    
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                try:
                    f.write(f"\n=== {data.name} ===\n")
                    f.write(data.script.decode('utf-8'))
                except:
                    pass
    print("Done.")

extract(FILE_PATH)
