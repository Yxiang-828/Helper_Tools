import os

def find_int_context(file_path, val):
    print(f"Searching for int {val} in {os.path.basename(file_path)}")
    target = val.to_bytes(4, byteorder='little')
    print(f"Target bytes: {target.hex()}")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            
        pos = data.find(target)
        if pos != -1:
            print(f"Found at offset {pos} (0x{pos:X})")
            start = max(0, pos - 64)
            end = min(len(data), pos + 128)
            context = data[start:end]
            
            print(f"--- Context (Hex) ---")
            hex_str = context.hex()
            for i in range(0, len(hex_str), 32):
                 print(hex_str[i:i+32])
                 
            print("\n--- Context (ASCII) ---")
            ascii_rep = ""
            for byte_val in context:
                if 32 <= byte_val <= 126:
                    ascii_rep += chr(byte_val)
                else:
                    ascii_rep += "."
            print(ascii_rep)
            
        else:
            print("ID not found as int32.")
            
    except Exception as e:
        print(f"Error: {e}")

fp = r"C:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\fileResource.bytes"
find_int_context(fp, 20790)
