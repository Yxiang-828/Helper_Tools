import os
import UnityPy

DOCUMENT_BUNDLE = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\Document\Document.unity3d"
OUTPUT_TXT = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\document_text_dump.txt"

def extract_document_text(bundle_path):
    print(f"Extracting: {os.path.basename(bundle_path)}")
    
    if not os.path.exists(bundle_path):
        print(f"Not found: {bundle_path}")
        return
        
    env = UnityPy.load(bundle_path)
    
    found_count = 0
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                try:
                    text_content = data.script.decode('utf-8')
                    f.write(f"\n=== FILE: {data.name} ===\n")
                    f.write(text_content)
                    found_count += 1
                except:
                    pass
                    
    print(f"Extracted {found_count} text assets to {OUTPUT_TXT}")

extract_document_text(DOCUMENT_BUNDLE)
