import os

def hex_dump(file_path, size=256):
    print(f"--- Hex Dump: {os.path.basename(file_path)} ---")
    try:
        with open(file_path, 'rb') as f:
            data = f.read(size)
        
        # simple hex print
        hex_str = data.hex()
        for i in range(0, len(hex_str), 32):
            chunk = hex_str[i:i+32]
            ascii_rep = ""
            for j in range(0, len(chunk), 2):
                byte_val = int(chunk[j:j+2], 16)
                if 32 <= byte_val <= 126:
                    ascii_rep += chr(byte_val)
                else:
                    ascii_rep += "."
            print(f"{chunk} | {ascii_rep}")
            
    except Exception as e:
        print(f"Error reading file: {e}")

files_to_check = [
    r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Resurgent_Setti_Files\C_Nair_Final.bytes",
    r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Resurgent_Setti_Files\MaxSkill.bytes"
]

for fp in files_to_check:
    hex_dump(fp)
    print("\n")
