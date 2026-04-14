import os
import struct
import re

FILE_PATH = r"c:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump\fileResource.bytes"
OUTPUT_PATH = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\file_resource_dump.txt"

def extract_strings(data):
    # Find sequence of printable characters length >= 4
    # Including common text characters
    pattern = rb'[ -~]{4,}'
    return [match.group().decode('utf-8', errors='ignore') for match in re.finditer(pattern, data)]

def extract_floats(data):
    floats = []
    # Iterate 4 bytes at a time
    for i in range(0, len(data) - 4, 4):
        try:
            val = struct.unpack('<f', data[i:i+4])[0]
            # Filter reasonable float values for game stats (e.g., 0.1 to 10000.0) or specific exact mechanics
            if (abs(val) > 0.001 and abs(val) < 100000.0) or val == 0.0:
                floats.append((i, val))
        except:
            pass
    return floats

def main():
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

    with open(FILE_PATH, 'rb') as f:
        data = f.read()

    strings = extract_strings(data)
    floats = extract_floats(data)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("=== STRINGS ===\n")
        for s in strings:
            f.write(f"{s}\n")
        
        f.write("\n=== FLOATS (Offset: Value) ===\n")
        for offset, val in floats:
            f.write(f"{offset}: {val}\n")

    print(f"Dumped {len(strings)} strings and {len(floats)} floats to {OUTPUT_PATH}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open(r"c:\Users\xiang\Helper_Tools\debug_error.txt", "w") as f:
            f.write(str(e))
