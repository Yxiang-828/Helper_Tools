import os

def find_id_context(file_path, search_id_str):
    print(f"Searching for {search_id_str} in {os.path.basename(file_path)}")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            
        # Search for ASCII string
        pos = data.find(search_id_str.encode('utf-8'))
        if pos != -1:
            print(f"Found '{search_id_str}' at offset {pos} (0x{pos:X})")
            start = max(0, pos - 64)
            end = min(len(data), pos + 128)
            context = data[start:end]
            
            print(f"--- Context (Hex) ---")
            hex_str = context.hex()
            for i in range(0, len(hex_str), 32):
                 print(hex_str[i:i+32])
                 
            print("\n--- Context (ASCII) ---")
            # printable
            ascii_rep = ""
            for byte_val in context:
                if 32 <= byte_val <= 126:
                    ascii_rep += chr(byte_val)
                else:
                    ascii_rep += "."
            print(ascii_rep)
            
        else:
            print("ID not found as string.")
            
    except Exception as e:
        print(f"Error: {e}")

fp = r"C:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\fileResource.bytes"
find_id_context(fp, "20790")
