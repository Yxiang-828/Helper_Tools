import os

BYTES_BUNDLE = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\BytesData\Bytes.unity3d"

def search_string_in_binary(file_path, search_str):
    print(f"Scanning {os.path.basename(file_path)} for '{search_str}'...")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            
        pos = data.find(search_str.encode('utf-8'))
        if pos != -1:
            print(f"FOUND matches at index {pos}")
            # Show context
            start = max(0, pos - 50)
            end = min(len(data), pos + 100)
            print("Context:\n", data[start:end])
        else:
            print("Not found.")
            
    except Exception as e:
        print(e)
        
search_string_in_binary(BYTES_BUNDLE, "C_Nair_Final")
search_string_in_binary(BYTES_BUNDLE, "_CharacterPrefabData_")
