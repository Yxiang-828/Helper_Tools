import UnityPy
import os

path = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\dragon2019\assets\BytesData\Bytes.unity3d"

if not os.path.exists(path):
    print("File not found")
    exit()

print(f"Loading {path}...")
env = UnityPy.load(path)

candidates = []
for obj in env.objects:
    if obj.type.name == "TextAsset":
        data = obj.read()
        name = getattr(data, 'm_Name', 'Unknown')
        candidates.append(name)

print(f"Total TextAssets found: {len(candidates)}")

print("\n--- Potential Data Files (Filter: Hero, Skill, Config, Data) ---")
for name in sorted(candidates):
    n = name.lower()
    # Filter for things that look like stats/skills
    if "hero" in n or "skill" in n or "config" in n or "data" in n or "table" in n:
        # Exclude common assets that are likely visual/audio metadata
        if "roleanimator" in n or "movielength" in n or "camera" in n:
            continue
        print(name)
