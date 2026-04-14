import os
import re

SEARCH_TERMS = ["Stellar Wrath", "Resurgent Setti", "Stellar Legacy", "Star Veil", "Setti", "Nair"]
SEARCH_DIR = r"c:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump"
OUTPUT_FILE = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\search_results.txt"

def search_files():
    print(f"Searching for {SEARCH_TERMS} in {SEARCH_DIR}...")
    
    matches = {}
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(f"Search Results for {SEARCH_TERMS}\n")
        
        for filename in os.listdir(SEARCH_DIR):
            file_path = os.path.join(SEARCH_DIR, filename)
            if not os.path.isfile(file_path):
                continue
                
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    
                # Try decoding as utf-8 and utf-16
                try:
                    text_content = content.decode('utf-8', errors='ignore')
                    
                    found = False
                    for term in SEARCH_TERMS:
                        if term in text_content:
                            outfile.write(f"Found '{term}' in {filename} (UTF-8)\n")
                            found = True
                    
                    if not found:
                        # Try utf-16
                        text_content = content.decode('utf-16', errors='ignore')
                        for term in SEARCH_TERMS:
                            if term in text_content:
                                outfile.write(f"Found '{term}' in {filename} (UTF-16)\n")

                except Exception:
                    pass
                    
            except Exception as e:
                print(f"Could not read {filename}: {e}")

    print("Search complete.")

if __name__ == "__main__":
    search_files()
