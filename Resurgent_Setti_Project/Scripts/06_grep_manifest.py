INPUT_FILE = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\file_resource_dump.txt"
OUTPUT_FILE = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\setti_file_list.txt"

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

found = []
for line in lines:
    if "unit_20" in line:
        found.append(line.strip())

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for line in found:
        f.write(line + "\n")

print(f"Found {len(found)} lines.")
