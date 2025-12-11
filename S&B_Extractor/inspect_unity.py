# Inspect Unity3D files to see what assets they contain
import os
import UnityPy

def inspect_unity_file(file_path):
    """Inspect a Unity3D file to see what asset types it contains"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    filename = os.path.basename(file_path)
    print(f"\n{'='*60}")
    print(f"Inspecting: {filename}")
    print(f"{'='*60}")
    
    try:
        # Read and find Unity data
        with open(file_path, 'rb') as f:
            data = f.read()
        
        unity_sig = b'UnityFS'
        offset = data.find(unity_sig)
        
        if offset == -1:
            print(f"No Unity signature found")
            return
        
        print(f"Unity signature found at offset: {offset}")
        
        # Extract Unity data
        unity_data = data[offset:]
        
        # Save as temp file and process
        temp_path = "temp_inspect.bundle"
        with open(temp_path, 'wb') as f:
            f.write(unity_data)
        
        env = UnityPy.load(temp_path)
        
        print(f"\nAsset types found:")
        asset_types = {}
        
        for obj in env.objects:
            type_name = obj.type.name
            if type_name not in asset_types:
                asset_types[type_name] = []
            
            # Try to get name
            try:
                obj_data = obj.read()
                name = obj_data.name if hasattr(obj_data, 'name') else f"path_id_{obj.path_id}"
            except:
                name = f"path_id_{obj.path_id}"
            
            asset_types[type_name].append(name)
        
        for type_name, names in sorted(asset_types.items()):
            print(f"\n  {type_name} ({len(names)} objects):")
            for name in names[:10]:  # Show first 10 of each type
                print(f"    - {name}")
            if len(names) > 10:
                print(f"    ... and {len(names) - 10} more")
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    files = [
        r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\ABResourceSingle\Ani_C_Alene_Base_study.unity3d",
        r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\ABResourceSingle\Ani_C_Alene_Base_councilhall.unity3d"
    ]
    
    for file_path in files:
        inspect_unity_file(file_path)
