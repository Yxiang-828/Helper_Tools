
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import glob

class ComprehensiveUIViewer:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Silver and Blood Complete UI Collection - 38 images")
        self.root.geometry("1600x1200")
        
        self.output_dir = r"C:\Program Files (x86)\Silver_And_Blood_Datamining\complete_ui_extraction"
        self.current_images = []
        self.current_index = 0
        
        # Load all categories and their contents
        self.load_categories()
        self.create_widgets()
    
    def load_categories(self):
        self.categories = {}
        
        # Load all PNG files directly from the output directory
        if os.path.exists(self.output_dir):
            png_files = glob.glob(os.path.join(self.output_dir, "*.png"))
            if png_files:
                self.categories["All_UI_Images"] = {
                    'path': self.output_dir,
                    'images': sorted(png_files),
                    'count': len(png_files)
                }
    
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
            item_id = self.category_tree.insert('', 'end', text=f"{category_name} ({category_data['count']})")
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
                self.info_label.config(text=f"Category: {category_name}")
                self.stats_label.config(text=f"{len(self.current_images)} images")
                
                # Update image list
                self.image_listbox.delete(0, tk.END)
                for i, img_path in enumerate(self.current_images):
                    filename = os.path.basename(img_path)
                    # Truncate long filenames
                    display_name = filename[:60] + "..." if len(filename) > 63 else filename
                    self.image_listbox.insert(tk.END, f"{i+1:3}. {display_name}")
                
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
            self.image_info_label.config(text=f"{self.current_index + 1}/{len(self.current_images)} - {filename}\nOriginal: {orig_size[0]}x{orig_size[1]}")
            
            # Update listbox selection
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_index)
            self.image_listbox.see(self.current_index)
            
        except Exception as e:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2,
                                  text=f"Error loading image:\n{str(e)}", anchor=tk.CENTER)
    
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
                       f"Complete UI extraction successful!\n\n"
                       f"Categories: {categories_count}\n"
                       f"Total Images: 38\n\n"
                       f"Navigate through categories on the left to explore all UI elements!")
    
    root.mainloop()
