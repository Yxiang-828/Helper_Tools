import UnityPy
import os

# Path to the file
file_path = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\dragon2019\assets\lua\logic.unity3d"

try:
    # Load the environment
    env = UnityPy.load(file_path)
    print(f"Loaded env: {env}")
    
    # Try different ways to access objects
    print(f"Enc.objects count: {len(list(env.objects))}")
    
    for obj in env.objects:
        print(f"Obj: {obj.type.name}")

    if len(list(env.objects)) == 0:
        print("No objects found in root. Checking files...")
        for name, file in env.files.items():
            print(f"File: {name} - Type: {type(file)}")

            
except Exception as e:
    print(f"Error: {e}")
