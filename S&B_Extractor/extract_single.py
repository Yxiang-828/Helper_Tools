# Extract single Unity3D files to images
import os
import sys
import UnityPy
from PIL import Image

def extract_unity_file(file_path, output_dir):
    """Extract images from a single Unity3D file"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    
    print(f"Processing: {filename}")
    
    extracted_files = []
    
    try:
        # Read and find Unity data
        with open(file_path, 'rb') as f:
            data = f.read()
        
        unity_sig = b'UnityFS'
        offset = data.find(unity_sig)
        
        if offset == -1:
            print(f"No Unity signature found in {filename}")
            return []
        
        # Extract Unity data
        unity_data = data[offset:]
        
        # Save as temp file and process
        temp_path = os.path.join(output_dir, "temp_unity.bundle")
        with open(temp_path, 'wb') as f:
            f.write(unity_data)
        
        env = UnityPy.load(temp_path)
        
        extracted_count = 0
        
        for obj in env.objects:
            if obj.type.name in ['Texture2D', 'Sprite']:
                try:
                    obj_data = obj.read()
                    
                    img = None
                    if hasattr(obj_data, 'image') and obj_data.image:
                        img = obj_data.image
                    
                    if img:
                        # Create safe filename
                        try:
                            obj_name = obj_data.name if hasattr(obj_data, 'name') and obj_data.name else f"{obj.type.name}_{obj.path_id}"
                        except:
                            obj_name = f"{obj.type.name}_{obj.path_id}"
                        
                        safe_name = "".join(c for c in obj_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        if not safe_name or len(safe_name) < 3:
                            safe_name = f"{obj.type.name}_{extracted_count}"
                        
                        final_filename = f"{base_name}_{safe_name}.png"
                        output_path = os.path.join(output_dir, final_filename)
                        
                        img.save(output_path)
                        extracted_files.append(output_path)
                        extracted_count += 1
                        print(f"  Extracted: {final_filename}")
                        
                except Exception as e:
                    continue
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        print(f"Total extracted from {filename}: {extracted_count} images")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
    
    return extracted_files


if __name__ == "__main__":
    # Files to extract
    files = [
        r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\ABResourceSingle\Ani_C_Alene_Base_study.unity3d",
        r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\ABResourceSingle\Ani_C_Alene_Base_councilhall.unity3d"
    ]
    
    output_dir = r"C:\Users\xiang\Helper_Tools\S&B_Extractor\alene_extraction"
    
    all_extracted = []
    
    for file_path in files:
        extracted = extract_unity_file(file_path, output_dir)
        all_extracted.extend(extracted)
    
    print(f"\n{'='*50}")
    print(f"Extraction complete! Total images: {len(all_extracted)}")
    print(f"Output folder: {output_dir}")
    print(f"{'='*50}")
