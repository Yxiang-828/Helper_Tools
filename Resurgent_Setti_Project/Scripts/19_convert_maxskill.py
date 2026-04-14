import struct
import os
import json

# Define the source path
SOURCE_PATH = r"C:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\MaxSkill.bytes"
OUTPUT_JSON = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\max_skill.json"

def parse_max_skill(file_path):
    print(f"Reading raw binary: {file_path}")
    data = {}
    
    with open(file_path, 'rb') as f:
        # Header reading - based on previous hex dump scan
        # Dump showed: 01 00 00 00 02 00 00 00 ...
        # This looks like version 1, count 2?
        
        version = struct.unpack('<I', f.read(4))[0]
        count = struct.unpack('<I', f.read(4))[0]
        
        data["version"] = version
        data["entry_count"] = count
        data["entries"] = []
        
        # Following the header, there were many zeros, then some floats like 30 2E 88...
        # Let's read the rest as a stream of floats for now to see patterns
        # or it might be a struct.
        
        # Hex dump showed:
        # 01 00 00 00 (Ver) 
        # 02 00 00 00 (Count)
        # 00 00 00 00 (Padding/Int?)
        # 00 00 00 00
        # 00 00 00 00 (12 bytes of zeros) -> Maybe Vector3(0,0,0)?
        
        # 88 2E 30 41 = 11.0113 ... -> Float?
        # 88 2E 30 41
        
        # Let's dump identified floats to find pattern
        
        raw_rest = f.read()
        
        # Simple parser loop to find non-zero
        floats = []
        for i in range(0, len(raw_rest), 4):
            if i+4 > len(raw_rest): break
            f_val = struct.unpack('<f', raw_rest[i:i+4])[0]
            if abs(f_val) > 0.0001:
                floats.append(f_val)
                
        data["raw_floats"] = floats

    return data

if not os.path.exists(os.path.dirname(OUTPUT_JSON)):
    os.makedirs(os.path.dirname(OUTPUT_JSON))

parsed_data = parse_max_skill(SOURCE_PATH)

if parsed_data:
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(parsed_data, f, indent=4)
    print(f"Converted MaxSkill to JSON: {OUTPUT_JSON}")
    print(json.dumps(parsed_data, indent=2))
