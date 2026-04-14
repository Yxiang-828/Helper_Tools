import os
DIR = r"c:\Users\xiang\Helper_Tools\S&B_Extractor\BytesData_Dump"
FILE = os.path.join(DIR, "C_Nair_Final.bytes")

with open(r"c:\Users\xiang\Helper_Tools\debug_log.txt", "w") as f:
    f.write(f"Checking {DIR}\n")
    if os.path.exists(DIR):
        f.write("Directory exists\n")
        files = os.listdir(DIR)
        f.write(f"Found {len(files)} files\n")
        if "C_Nair_Final.bytes" in files:
            f.write("File found in list\n")
    else:
        f.write("Directory DOES NOT exist\n")

    if os.path.exists(FILE):
        f.write("File Check: OK\n")
    else:
        f.write("File Check: MISSING\n")
