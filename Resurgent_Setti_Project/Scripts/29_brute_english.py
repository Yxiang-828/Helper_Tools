import os
import UnityPy
import glob

# Try inspecting the AllLanguageEN / AddLanguageEN bundles instead
SEARCH_PATH = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\Document\*LanguageEN*.unity3d"
OUTPUT_TXT = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\english_dump.txt"

def brute_extract():
     with open(OUTPUT_TXT, 'w', encoding='utf-8') as outfile:
        for file_path in glob.glob(SEARCH_PATH):
            print(f"Scanning: {os.path.basename(file_path)}")
            try:
                env = UnityPy.load(file_path)
                for obj in env.objects:
                    # TextAsset?
                    if obj.type.name == "TextAsset":
                        data = obj.read()
                        try:
                            outfile.write(f"\n<<< FILE: {data.name} >>>\n")
                            outfile.write(data.script.decode('utf-8'))
                        except:
                            pass
            except Exception as e:
                print(f"Failed {file_path}: {e}")

brute_extract()
print("Scan complete.")
