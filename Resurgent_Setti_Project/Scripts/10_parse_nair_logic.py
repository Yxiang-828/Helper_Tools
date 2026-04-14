import struct
import os

def parse_nair_logic(file_path):
    print(f"Parsing: {os.path.basename(file_path)}")
    
    with open(file_path, 'rb') as f:
        # Read Header
        version = f.read(4)
        print(f"Header/Version: {version.hex()}")
        
        # Read Prefab Name
        try:
            name_len = ord(f.read(1))
            name = f.read(name_len).decode('utf-8')
            print(f"Prefab Name: {name}")
        except:
            print("Failed to read prefab name")
            return

        # Read Count?
        count_bytes = f.read(4)
        count = struct.unpack('<I', count_bytes)[0]
        print(f"Item Count: {count}")
        
        print("\n--- Items ---")
        for i in range(count):
            try:
                # Read String Length
                s_len_byte = f.read(1)
                if not s_len_byte:
                    break
                s_len = ord(s_len_byte)
                
                # Read String
                s_val = f.read(s_len).decode('utf-8')
                
                # Read Float
                f_bytes = f.read(4)
                f_val = struct.unpack('<f', f_bytes)[0]
                
                print(f"{i+1:02d}: {s_val:<25} = {f_val:.4f}")
            except Exception as e:
                print(f"Error parsing item {i}: {e}")
                break

file_path = r"C:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\C_Nair_Final.bytes"
parse_nair_logic(file_path)
