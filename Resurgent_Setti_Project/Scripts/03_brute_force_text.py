import os
import re

INPUT_DIR = r"c:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump"
OUTPUT_FILE = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\master_string_dump.txt"

def extract_strings_from_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            # Find printable strings > 4 chars
            # We use a broad pattern: sequence of non-control bytes
            pattern = rb'[\x20-\x7E]{4,}' 
            ascii_matches = [m.group().decode('ascii', errors='ignore') for m in re.finditer(pattern, data)]
            
            # Also try utf-8 full decode for regions
            # logic: decode whole file as utf-8, split by non-printable
            try:
                text = data.decode('utf-8', errors='ignore')
                # Split by control chars (anything < 32)
                utf8_matches = [s for s in re.split(r'[\x00-\x1F]+', text) if len(s) >= 4]
            except:
                utf8_matches = []
                
            return set(ascii_matches + utf8_matches)
    except Exception as e:
        return set()

def main():
    print(f"Scanning {INPUT_DIR}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for filename in sorted(os.listdir(INPUT_DIR)):
            if not filename.endswith(".bytes"):
                continue
                
            file_path = os.path.join(INPUT_DIR, filename)
            strings = extract_strings_from_file(file_path)
            
            if strings:
                out.write(f"=== {filename} ===\n")
                for s in sorted(strings):
                    # Filter out noise (only symbols, etc)
                    if any(c.isalnum() for c in s):
                        out.write(f"{s}\n")
                out.write("\n")

    print(f"Dump complete to {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open(r"c:\Users\xiang\Helper_Tools\BruteForceError.txt", "w") as f:
            f.write(str(e))
