# Comprehensive Silver and Blood UI Image Extractor
# Extracts and organizes ALL UI images from both regular and HQ UI folders
# Now with duplicate checking and new_extractions tracking

import os
import UnityPy
from PIL import Image
import glob
import shutil
import re
from datetime import datetime

def categorize_ui_file(filename):
    """Categorize UI files based on their naming patterns"""
    filename_lower = filename.lower()
    
    # Character-related UI
    if any(pattern in filename_lower for pattern in ['atlas_acappella', 'atlas_agares', 'atlas_aiona', 'atlas_albert', 
                                                     'atlas_ami', 'atlas_bella', 'atlas_cain', 'atlas_cecia',
                                                     'atlas_clive', 'atlas_dalcar', 'atlas_empousa', 'atlas_fanny',
                                                     'atlas_friedrich', 'atlas_garlic', 'atlas_gilrain', 'atlas_goldland',
                                                     'atlas_hati', 'atlas_lamia', 'atlas_noah', 'atlas_piera', 'atlas_ressa',
                                                     'atlas_selena', 'atlas_stella', 'atlas_tris', 'atlas_yggdrasill',
                                                     '_angry', '_base', '_happy', '_sad', '_shock', '_covenant', '_base003']):
        return "Characters"
    
    # Battle-related UI
    elif any(pattern in filename_lower for pattern in ['atlas_battle', 'atlas_boss', 'form_battle', 'battle_']):
        return "Battle"
    
    # Activity and Event UI
    elif any(pattern in filename_lower for pattern in ['atlas_activity', 'form_activity', 'activity_']):
        return "Activities"
    
    # Gacha and summoning UI
    elif any(pattern in filename_lower for pattern in ['atlas_gacha', 'atlas_attract', 'form_gacha', 'gacha_']):
        return "Gacha"
    
    # Guild-related UI
    elif any(pattern in filename_lower for pattern in ['atlas_guild', 'form_guild', 'guild_']):
        return "Guild"
    
    # Hero management UI
    elif any(pattern in filename_lower for pattern in ['atlas_hero', 'form_hero', 'hero_', 'atlas_equipment', 'atlas_skill']):
        return "Heroes"
    
    # Shop and Mall UI
    elif any(pattern in filename_lower for pattern in ['atlas_mall', 'atlas_shop', 'form_mall', 'shop_', 'recharge']):
        return "Shop"
    
    # PvP and ranking UI
    elif any(pattern in filename_lower for pattern in ['atlas_pvp', 'atlas_rank', 'form_pvp', 'pvp_', 'rank_']):
        return "PvP"
    
    # Castle and exploration UI
    elif any(pattern in filename_lower for pattern in ['atlas_castle', 'atlas_level', 'atlas_tower', 'form_castle', 'castle_', 'level_', 'tower_']):
        return "Exploration"
    
    # Main UI and common elements
    elif any(pattern in filename_lower for pattern in ['atlas_common', 'atlas_hall', 'atlas_main', 'form_hall', 'common_', 'main_']):
        return "Main_UI"
    
    # Dialog and story UI
    elif any(pattern in filename_lower for pattern in ['atlas_dialogue', 'form_dialogue', 'dialogue_', 'plot_']):
        return "Dialogue"
    
    # Legacy and special modes
    elif any(pattern in filename_lower for pattern in ['atlas_legacy', 'atlas_rogue', 'atlas_simulation', 'legacy_', 'rogue_']):
        return "Special_Modes"
    
    # Login and system UI
    elif any(pattern in filename_lower for pattern in ['atlas_login', 'form_login', 'login_', 'loading_', 'title_']):
        return "System"
    
    # Items and equipment
    elif any(pattern in filename_lower for pattern in ['atlas_item', 'atlas_equip', 'item_', 'equip_']):
        return "Items"
    
    # Miscellaneous UI elements
    elif any(pattern in filename_lower for pattern in ['atlas_bg', 'atlas_font', 'atlas_tab', 'bg_', 'ui_']):
        return "UI_Elements"
    
    else:
        return "Other"

def extract_ui_images(source_dir, output_base_dir, folder_name, new_extractions_dir, timestamp_folder):
    """Extract images from a UI source directory with duplicate checking"""
    print(f"\n=== Processing {folder_name} ===")
    
    unity_files = glob.glob(os.path.join(source_dir, "*.unity3d"))
    total_files = len(unity_files)
    
    print(f"Found {total_files} Unity3D files")
    
    category_stats = {}
    total_extracted = 0
    new_files_count = 0
    skipped_files_count = 0
    
    for i, file_path in enumerate(unity_files, 1):
        filename = os.path.basename(file_path)
        
        # No categorization - dump everything directly into main folders
        category_output_dir = output_base_dir
        category_new_dir = os.path.join(new_extractions_dir, timestamp_folder)
        os.makedirs(category_output_dir, exist_ok=True)
        os.makedirs(category_new_dir, exist_ok=True)
        
        if "All_UI" not in category_stats:
            category_stats["All_UI"] = {"files": 0, "images": 0, "new_images": 0, "skipped": 0}
        
        try:
            # Read and find Unity data
            with open(file_path, 'rb') as f:
                data = f.read()
            
            unity_sig = b'UnityFS'
            offset = data.find(unity_sig)
            
            if offset == -1:
                print(f"  [{i}/{total_files}] ✗ {filename} - No Unity signature")
                continue
            
            # Extract Unity data
            unity_data = data[offset:]
            
            # Save as temp file and process
            temp_path = os.path.join(category_output_dir, "temp_unity.bundle")
            with open(temp_path, 'wb') as f:
                f.write(unity_data)
            
            env = UnityPy.load(temp_path)
            
            extracted_count = 0
            new_count = 0
            skipped_count = 0
            base_name = os.path.splitext(filename)[0]
            
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
                            output_path = os.path.join(category_output_dir, final_filename)
                            new_output_path = os.path.join(category_new_dir, final_filename)
                            
                            # Check if file already exists in complete_ui_extraction
                            if os.path.exists(output_path):
                                skipped_count += 1
                                continue
                            
                            # Save to both locations if it's new
                            img.save(output_path)
                            img.save(new_output_path)
                            extracted_count += 1
                            new_count += 1
                            
                    except Exception as e:
                        continue
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            category_stats["All_UI"]["files"] += 1
            category_stats["All_UI"]["images"] += extracted_count
            category_stats["All_UI"]["new_images"] += new_count
            category_stats["All_UI"]["skipped"] += skipped_count
            total_extracted += extracted_count
            new_files_count += new_count
            skipped_files_count += skipped_count
            
            if extracted_count > 0:
                print(f"  [{i}/{total_files}] ✓ {filename} ({new_count} new, {skipped_count} skipped)")
            else:
                print(f"  [{i}/{total_files}] - {filename} (all {skipped_count} already exist)")
            
        except Exception as e:
            print(f"  [{i}/{total_files}] ✗ {filename} - Error: {e}")
            continue
    
    print(f"\n{folder_name} Summary:")
    print("-" * 50)
    for category, stats in sorted(category_stats.items()):
        print(f"{category}: {stats['files']} files, {stats['new_images']} new, {stats['skipped']} skipped")
    print(f"TOTAL: {new_files_count} new images, {skipped_files_count} skipped")
    
    return total_extracted, new_files_count, category_stats

def main():
    # Define source directories
    ui_dir = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\UI"
    hq_ui_dir = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\HQ\UI"
    
    # Define output directories dynamically based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "complete_ui_extraction")
    new_extractions_dir = os.path.join(script_dir, "new_extractions")
    
    # Create timestamp for this extraction run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp_folder = f"extraction_{timestamp}"
    
    print("=== COMPREHENSIVE SILVER AND BLOOD UI EXTRACTION ===")
    print(f"Output directory: {output_dir}")
    print(f"New extractions: {new_extractions_dir}\\{timestamp_folder}")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(new_extractions_dir, exist_ok=True)
    
    total_images = 0
    total_new_images = 0
    all_category_stats = {}
    
    # Extract from regular UI folder
    if os.path.exists(ui_dir):
        ui_total, ui_new, ui_stats = extract_ui_images(ui_dir, output_dir, "Standard_UI", new_extractions_dir, timestamp_folder)
        total_images += ui_total
        total_new_images += ui_new
        
        for category, stats in ui_stats.items():
            if category not in all_category_stats:
                all_category_stats[category] = {"files": 0, "images": 0, "new_images": 0, "skipped": 0}
            all_category_stats[category]["files"] += stats["files"]
            all_category_stats[category]["images"] += stats["images"]
            all_category_stats[category]["new_images"] += stats["new_images"]
            all_category_stats[category]["skipped"] += stats["skipped"]
    
    # Extract from HQ UI folder
    if os.path.exists(hq_ui_dir):
        hq_total, hq_new, hq_stats = extract_ui_images(hq_ui_dir, output_dir, "HQ_UI", new_extractions_dir, timestamp_folder)
        total_images += hq_total
        total_new_images += hq_new
        
        for category, stats in hq_stats.items():
            if category not in all_category_stats:
                all_category_stats[category] = {"files": 0, "images": 0, "new_images": 0, "skipped": 0}
            all_category_stats[category]["files"] += stats["files"]
            all_category_stats[category]["images"] += stats["images"]
            all_category_stats[category]["new_images"] += stats["new_images"]
            all_category_stats[category]["skipped"] += stats["skipped"]
    
    print("\n" + "="*80)
    print("FINAL EXTRACTION SUMMARY")
    print("="*80)
    
    for category, stats in sorted(all_category_stats.items()):
        print(f"{category:20}: {stats['new_images']:4} new, {stats['skipped']:4} skipped, {stats['images']:4} total")
    
    print("-" * 80)
    total_skipped = sum(s['skipped'] for s in all_category_stats.values())
    print(f"{'GRAND TOTAL':20}: {total_new_images:4} new, {total_skipped:4} skipped, {total_images:4} total")
    
    # Create extraction report
    report_path = os.path.join(new_extractions_dir, timestamp_folder, "extraction_report.txt")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Silver and Blood UI Extraction Report\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"=" * 50 + "\n\n")
        f.write(f"NEW IMAGES EXTRACTED: {total_new_images}\n")
        f.write(f"IMAGES SKIPPED: {total_skipped}\n")
        f.write(f"TOTAL PROCESSED: {total_images}\n\n")
        f.write("Per Category Breakdown:\n")
        f.write("-" * 30 + "\n")
        for category, stats in sorted(all_category_stats.items()):
            f.write(f"{category}: {stats['new_images']} new, {stats['skipped']} skipped\n")
    
    print(f"\n📁 Complete UI images: {output_dir}")
    print(f"📂 New extractions: {new_extractions_dir}\\{timestamp_folder}")
    print(f"📄 Report saved: {report_path}")
    
    if total_new_images > 0:
        print(f"\n🎉 {total_new_images} NEW IMAGES FOUND AND EXTRACTED!")
        # Open the new extractions folder to show what's new
        os.startfile(os.path.join(new_extractions_dir, timestamp_folder))
    else:
        print(f"\n✅ NO NEW IMAGES - All {total_skipped} images already exist in complete collection")
        # Still open the complete collection
        os.startfile(output_dir)
    
    # Create a comprehensive UI viewer only if there are images
    if total_images > 0:
        create_comprehensive_ui_viewer(output_dir, total_images, all_category_stats)

def create_comprehensive_ui_viewer(output_dir, total_images, category_stats):
    """Create a comprehensive UI image viewer"""
    viewer_code = f'''
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import glob

class ComprehensiveUIViewer:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Silver and Blood Complete UI Collection - {total_images} images")
        self.root.geometry("1600x1200")
        
        self.output_dir = r"{output_dir}"
        self.current_images = []
        self.current_index = 0
        
        # Load all categories and their contents
        self.load_categories()
        self.create_widgets()
    
    def load_categories(self):
        self.categories = {{}}
        
        # Load all PNG files directly from the output directory
        if os.path.exists(self.output_dir):
            png_files = glob.glob(os.path.join(self.output_dir, "*.png"))
            if png_files:
                self.categories["All_UI_Images"] = {{
                    'path': self.output_dir,
                    'images': sorted(png_files),
                    'count': len(png_files)
                }}
    
    def create_widgets(self):
        # Create main layout
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Categories
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="UI Categories:", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0,5))
        
        # Category tree
        self.category_tree = ttk.Treeview(left_frame, height=25)
        self.category_tree.pack(fill=tk.BOTH, expand=True, pady=(0,5))
        self.category_tree.bind('<<TreeviewSelect>>', self.on_category_select)
        
        # Populate categories
        for category_name, category_data in sorted(self.categories.items()):
            item_id = self.category_tree.insert('', 'end', text=f"{{category_name}} ({{category_data['count']}})")
            self.category_tree.set(item_id, '#1', category_name)
        
        # Right panel - Image display
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=4)
        
        # Image info panel
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill=tk.X, pady=(0,5))
        
        self.info_label = ttk.Label(info_frame, text="Select a category to view UI images", font=("Arial", 12))
        self.info_label.pack(side=tk.LEFT)
        
        self.stats_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.stats_label.pack(side=tk.RIGHT)
        
        # Image display area
        self.image_frame = ttk.Frame(right_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0,5))
        
        # Canvas for image with scrollbars
        canvas_frame = ttk.Frame(self.image_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="<< Previous", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Next >>", command=self.next_image).pack(side=tk.LEFT, padx=5)
        
        self.image_info_label = ttk.Label(control_frame, text="", font=("Arial", 9))
        self.image_info_label.pack(side=tk.RIGHT, padx=10)
        
        # Image list
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.X, pady=(5,0))
        
        ttk.Label(list_frame, text="Images in category:").pack(anchor=tk.W)
        
        # Image listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.X, pady=2)
        
        self.image_listbox = tk.Listbox(list_container, height=6, font=("Arial", 8))
        list_scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=list_scrollbar.set)
        
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
    
    def on_category_select(self, event):
        selection = self.category_tree.selection()
        if selection:
            item = selection[0]
            category_name = self.category_tree.set(item, '#1')
            
            if category_name in self.categories:
                category_data = self.categories[category_name]
                self.current_images = category_data['images']
                self.current_index = 0
                
                # Update info
                self.info_label.config(text=f"Category: {{category_name}}")
                self.stats_label.config(text=f"{{len(self.current_images)}} images")
                
                # Update image list
                self.image_listbox.delete(0, tk.END)
                for i, img_path in enumerate(self.current_images):
                    filename = os.path.basename(img_path)
                    # Truncate long filenames
                    display_name = filename[:60] + "..." if len(filename) > 63 else filename
                    self.image_listbox.insert(tk.END, f"{{i+1:3}}. {{display_name}}")
                
                if self.current_images:
                    self.load_current_image()
    
    def on_image_select(self, event):
        selection = self.image_listbox.curselection()
        if selection and self.current_images:
            self.current_index = selection[0]
            self.load_current_image()
    
    def load_current_image(self):
        if not self.current_images:
            return
        
        try:
            img_path = self.current_images[self.current_index]
            filename = os.path.basename(img_path)
            
            img = Image.open(img_path)
            orig_size = img.size
            
            # Scale image to fit canvas while maintaining aspect ratio
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                scale_factor = min(canvas_width / img.width, canvas_height / img.height, 1.0)
                if scale_factor < 1:
                    new_width = int(img.width * scale_factor)
                    new_height = int(img.height * scale_factor)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Display image on canvas
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            
            # Center the image
            x = (self.canvas.winfo_width() - img.width) // 2
            y = (self.canvas.winfo_height() - img.height) // 2
            self.canvas.create_image(max(x, 0), max(y, 0), anchor=tk.NW, image=self.photo)
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Update info labels
            self.image_info_label.config(text=f"{{self.current_index + 1}}/{{len(self.current_images)}} - {{filename}}\\nOriginal: {{orig_size[0]}}x{{orig_size[1]}}")
            
            # Update listbox selection
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_index)
            self.image_listbox.see(self.current_index)
            
        except Exception as e:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2,
                                  text=f"Error loading image:\\n{{str(e)}}", anchor=tk.CENTER)
    
    def prev_image(self):
        if self.current_images:
            self.current_index = (self.current_index - 1) % len(self.current_images)
            self.load_current_image()
    
    def next_image(self):
        if self.current_images:
            self.current_index = (self.current_index + 1) % len(self.current_images)
            self.load_current_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ComprehensiveUIViewer(root)
    
    # Bind keyboard shortcuts
    root.bind('<Left>', lambda e: app.prev_image())
    root.bind('<Right>', lambda e: app.next_image())
    root.focus_set()
    
    # Show welcome message
    categories_count = len(app.categories)
    messagebox.showinfo("Silver and Blood UI Collection", 
                       f"Complete UI extraction successful!\\n\\n"
                       f"Categories: {{categories_count}}\\n"
                       f"Total Images: {total_images}\\n\\n"
                       f"Navigate through categories on the left to explore all UI elements!")
    
    root.mainloop()
'''
    
    viewer_path = os.path.join(output_dir, "comprehensive_ui_viewer.py")
    with open(viewer_path, 'w', encoding='utf-8') as f:
        f.write(viewer_code)
    
    print(f"\\n📱 Comprehensive UI viewer created: {viewer_path}")
    
    # Launch the viewer
    try:
        import subprocess
        subprocess.Popen([
            r"C:/Users/xiang/AppData/Local/Programs/Python/Python313/python.exe",
            viewer_path
        ])
        print("🚀 UI viewer launched!")
    except:
        print("📝 Run the comprehensive_ui_viewer.py file to browse all UI images")

if __name__ == "__main__":
    main()
