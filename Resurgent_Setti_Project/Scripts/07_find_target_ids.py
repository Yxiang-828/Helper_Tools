INPUT_FILE = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Reference_Data\setti_file_list.txt"

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = ["20790", "20050", "2079", "2005", "setti", "nair"]

print("Scanning for targets...")
for line in lines:
    for t in targets:
        if t in line.lower():
            print(f"MATCH {t}: {line.strip()}")
