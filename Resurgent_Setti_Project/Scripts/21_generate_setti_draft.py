import json
import os

SOURCE_LOGIC = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\nair_logic.json"
OUTPUT_LOGIC = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Clean_Data\setti_logic_draft.json"

if os.path.exists(SOURCE_LOGIC):
    with open(SOURCE_LOGIC, 'r') as f:
        data = json.load(f)
        
    print("Loaded Nair Logic. Applying Setti transforms...")
    
    # Example Modifications for Setti (Hypothetical - making her faster/stronger)
    # Reducing Attack duration by 10% for snappier feel
    if "actions" in data:
        for key in data["actions"]:
            if "Attack" in key or "Skill" in key:
                original = data["actions"][key]
                new_val = round(original * 0.9, 4)
                data["actions"][key] = new_val
                print(f"  {key}: {original} -> {new_val}")
                
    with open(OUTPUT_LOGIC, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Created Setti Logic Draft: {OUTPUT_LOGIC}")
    
else:
    print("Source Logic not found!")
