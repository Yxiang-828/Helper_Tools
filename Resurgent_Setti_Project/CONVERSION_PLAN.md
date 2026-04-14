# Resurgent Setti: Conversion Profile

## Source Data (Nair)
- **ID**: `20050`
- **Logic File**: `C_Nair_Final.bytes` (Extracted & Converted)
- **Skill Data**: `MaxSkill.bytes` (Extracted & Converted)
- **State Scripts**: `20050_C_Nair_*.unity3d` (Verified UnityFS)

## Target Data (Setti)
- **Target ID**: `20790` (To Be Confirmed)
- **Prefab Name**: `_CharacterPrefabData_` (Preserved)

## Action Plan
1. **Logic Conversion**: 
   - [x] Extract Nair Logic
   - [ ] Generate `Setti_Logic.json` with updated IDs? (Logic seems ID-agnostic, mostly timings)
   - [ ] Repack to `C_Setti_Final.bytes`

2. **Skill Conversion**:
   - [x] Extract MaxSkill 
   - [ ] Process floats for Setti's balance (Damage tuning)
   - [ ] Repack to `MaxSkill_Setti.bytes`

3. **Asset Cloning**:
   - [ ] Clone `20050_*.unity3d` bundles to `20790_*.unity3d`
   - [ ] Hex-edit internal names if necessary (e.g., if "Nair" is hardcoded inside the asset names)

## Status
Ready to generate prototype files.
