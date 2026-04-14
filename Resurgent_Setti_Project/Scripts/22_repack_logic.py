import struct
import json
import os

SOURCE_JSON = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\setti_logic_draft.json"
OUTPUT_BYTES = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\C_Setti_Final.bytes"

def repack_logic(json_path, output_path):
    print(f"Repacking {os.path.basename(json_path)} -> {os.path.basename(output_path)}")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    with open(output_path, 'wb') as f:
        # 1. Header (Standard 02 00 00 00)
        f.write(struct.pack('<I', 2))
        
        # 2. Prefab Tag
        tag = data.get("_meta_tag", "_CharacterPrefabData_")
        f.write(struct.pack('B', len(tag)))
        f.write(tag.encode('utf-8'))
        
        # 3. Count
        actions = data.get("actions", {})
        count = len(actions)
        f.write(struct.pack('<I', count))
        
        # 4. Items (Alphabetical sort is usually safer for consistency, though dictionary order 'should' be fine)
        # We will iterate the dict directly
        for key, val in actions.items():
            # Key String
            f.write(struct.pack('B', len(key)))
            f.write(key.encode('utf-8'))
            
            # Value Float
            f.write(struct.pack('<f', val))
            
    print("Repack complete.")

repack_logic(SOURCE_JSON, OUTPUT_BYTES)
