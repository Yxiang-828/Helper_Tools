import os
import UnityPy

# Paths
GAME_DATA_ROOT = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets"
BYTES_BUNDLE = os.path.join(GAME_DATA_ROOT, "BytesData", "Bytes.unity3d")
OUTPUT_DIR = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Original_Extraction"

def inspect_bundle(bundle_path):
    if not os.path.exists(bundle_path):
        return

    print(f"Loading bundle: {os.path.basename(bundle_path)}")
    try:
        env = UnityPy.load(bundle_path)
        for obj in env.objects:
            print(f" - Found Object: {obj.type.name}")

    except Exception as e:
        print(f"Error reading {bundle_path}: {e}")

# Inspect just ONE to see what type it actually is
sample_bundle = os.path.join(GAME_DATA_ROOT, "BytesData", "StateScript", "20050_C_Nair_Attack.unity3d")
inspect_bundle(sample_bundle)

print("\n--- Checking Bytes.unity3d ---")
inspect_bundle(BYTES_BUNDLE)
