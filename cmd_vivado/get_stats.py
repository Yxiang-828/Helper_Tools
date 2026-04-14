import os
import UnityPy

def list_candidates():
    bundles_to_check = [
        r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\dragon2019\assets\lua\logic.unity3d",
        r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\dragon2019\assets\BytesData\Bytes.unity3d"
    ]

    print("--- Candidate Files for Skill/Stat Data ---")
    candidates = []

    for bpath in bundles_to_check:
        if not os.path.exists(bpath): continue
        print(f"Scanning {os.path.basename(bpath)}...")
        
        env = UnityPy.load(bpath)
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                name = getattr(data, "m_Name", "Unknown")
                
                name_lower = name.lower()
                # Keywords for data tables
                # Be less restrictive
                candidates.append((name, os.path.basename(bpath)))

    candidates.sort()
    for name, source in candidates:
        print(f"{name} ({source})")

if __name__ == "__main__":
    # Check logic.unity3d
    path = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\dragon2019\assets\lua\logic.unity3d"
    
    if os.path.exists(path):
        env = UnityPy.load(path)
        print(f"Loaded {os.path.basename(path)}")
        
        count = 0
        with open("cmd_vivado/logic_file_list.txt", "w", encoding='utf-8') as f:
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    data = obj.read()
                    name = getattr(data, 'm_Name', 'Unknown')
                    f.write(name + "\n")
                    count += 1
        print(f"Wrote {count} names to logic_file_list.txt")
        
        # Also check Bytes.unity3d
        path2 = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\dragon2019\assets\BytesData\Bytes.unity3d"
        env2 = UnityPy.load(path2)
        with open("cmd_vivado/file_list.txt", "w", encoding='utf-8') as f:
            for obj in env2.objects:
                if obj.type.name == "TextAsset":
                    data = obj.read()
                    name = getattr(data, 'm_Name', 'Unknown')
                    f.write(name + "\n")
        print("Wrote file_list.txt")

