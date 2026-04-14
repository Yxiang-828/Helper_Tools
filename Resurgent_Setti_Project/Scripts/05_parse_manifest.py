import json
import os

INPUT_FILE = r"c:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\fileResource.bytes"
OUTPUT_FILE = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\setti_manifest.json"

def parse_manifest():
    if not os.path.exists(INPUT_FILE):
        print("File resource not found")
        return

    # The file might contain binary header, so find first '{'
    with open(INPUT_FILE, 'rb') as f:
        data = f.read()
    
    try:
        start = data.find(b'{')
        if start == -1:
            print("No JSON start found")
            return
            
        json_data = data[start:].decode('utf-8', errors='ignore')
        # Ensure we have valid JSON by trimming end if needed
        # (Naive approach: find last '}')
        end = json_data.rfind('}')
        if end != -1:
            json_data = json_data[:end+1]
            
        parsed = json.loads(json_data)
        
        # Filter for 20790
        setti_files = []
        if 'fileList' in parsed:
            for item in parsed['fileList']:
                if '20790' in str(item):
                    setti_files.append(item)
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(setti_files, f, indent=2)
            
        print(f"Found {len(setti_files)} assets for 20790. Saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse_manifest()
