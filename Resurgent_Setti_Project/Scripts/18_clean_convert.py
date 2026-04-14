import struct
import os
import json

# Define the source path - verified to contain the binary logic
SOURCE_PATH = r"C:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\C_Nair_Final.bytes"
OUTPUT_JSON = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\nair_logic.json"

def parse_character_logic(file_path):
    print(f"Reading raw binary: {file_path}")
    logic_data = {}
    
    with open(file_path, 'rb') as f:
        # 1. Header Check
        header_ver = f.read(4)
        if header_ver.hex() != "02000000":
            print(f"!! Unexpected header: {header_ver.hex()}")
            # standard logic seems to be 02 00 00 00
            
        # 2. Prefab Tag
        # Pascal string: 1 byte len + chars
        try:
            tag_len = ord(f.read(1))
            tag_str = f.read(tag_len).decode('utf-8')
            logic_data["_meta_tag"] = tag_str
        except:
            print("Failed to read prefab tag")
            return None
            
        # 3. Item Count
        count = struct.unpack('<I', f.read(4))[0]
        logic_data["action_count"] = count
        logic_data["actions"] = {}
        
        # 4. Parse Items
        for i in range(count):
            # Key String
            key_len = ord(f.read(1))
            key = f.read(key_len).decode('utf-8')
            
            # Value Float
            val = struct.unpack('<f', f.read(4))[0]
            
            logic_data["actions"][key] = val
            
    return logic_data

if not os.path.exists(os.path.dirname(OUTPUT_JSON)):
    os.makedirs(os.path.dirname(OUTPUT_JSON))

data = parse_character_logic(SOURCE_PATH)

if data:
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully converted binary logic to JSON: {OUTPUT_JSON}")
    print(json.dumps(data, indent=2))
else:
    print("Extraction failed.")
