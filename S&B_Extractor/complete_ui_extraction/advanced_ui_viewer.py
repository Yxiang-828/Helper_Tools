#!/usr/bin/env python3
"""
Advanced Silver and Blood UI Viewer
A powerful, responsive UI viewer with search, zoom, filtering, and optimization features
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import sqlite3
from pathlib import Path
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json

class ImageCache:
    """Efficient image caching system with memory management"""
    
    def __init__(self, max_cache_size=50):
        self.cache = {}
        self.access_order = []
        self.max_size = max_cache_size
        self.thumbnail_cache = {}
        
    def get_image(self, path, size=None):
        """Get image from cache or load it"""
        cache_key = f"{path}_{size}" if size else path
        
        if cache_key in self.cache:
            # Move to end for LRU
            self.access_order.remove(cache_key)
            self.access_order.append(cache_key)
            return self.cache[cache_key]
        
        # Load image
        try:
            img = Image.open(path)
            if size:
                img.thumbnail(size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            
            # Cache management
            self.cache[cache_key] = photo
            self.access_order.append(cache_key)
            
            # Remove oldest if over limit
            while len(self.cache) > self.max_size:
                oldest = self.access_order.pop(0)
                del self.cache[oldest]
            
            return photo
            
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def get_thumbnail(self, path, size=(150, 150)):
        """Get or create thumbnail"""
        if path in self.thumbnail_cache:
            return self.thumbnail_cache[path]
            
        thumb = self.get_image(path, size)
        if thumb:
            self.thumbnail_cache[path] = thumb
        return thumb
    
    def clear(self):
        """Clear all caches"""
        self.cache.clear()
        self.access_order.clear()
        self.thumbnail_cache.clear()

class ImageDatabase:
    """SQLite database for fast image metadata and search"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY,
                    path TEXT UNIQUE,
                    filename TEXT,
                    category TEXT,
                    folder TEXT,
                    size_bytes INTEGER,
                    width INTEGER,
                    height INTEGER,
                    indexed_date TEXT
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_filename ON images(filename)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_category ON images(category)')
            conn.commit()
    
    def index_directory(self, base_path, progress_callback=None):
        """Index all images in directory"""
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        images = []
        
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if Path(file).suffix.lower() in image_extensions:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, base_path)
                    
                    # Extract category and folder from path
                    path_parts = Path(rel_path).parts
                    folder = path_parts[0] if len(path_parts) > 1 else "Root"
                    category = path_parts[1] if len(path_parts) > 2 else "Other"
                    
                    try:
                        stat = os.stat(full_path)
                        # Get image dimensions
                        with Image.open(full_path) as img:
                            width, height = img.size
                        
                        images.append((
                            full_path, file, category, folder,
                            stat.st_size, width, height,
                            time.strftime('%Y-%m-%d %H:%M:%S')
                        ))
                        
                        if progress_callback and len(images) % 100 == 0:
                            progress_callback(len(images))
                            
                    except Exception as e:
                        print(f"Error indexing {full_path}: {e}")
        
        # Bulk insert
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany('''
                INSERT OR REPLACE INTO images 
                (path, filename, category, folder, size_bytes, width, height, indexed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', images)
            conn.commit()
        
        return len(images)
    
    def search_images(self, query="", category="", folder="", limit=1000):
        """Search images with filters"""
        sql = "SELECT * FROM images WHERE 1=1"
        params = []
        
        if query:
            sql += " AND filename LIKE ?"
            params.append(f"%{query}%")
        
        if category and category != "All":
            sql += " AND category = ?"
            params.append(category)
        
        if folder and folder != "All":
            sql += " AND folder = ?"
            params.append(folder)
        
        sql += f" ORDER BY filename LIMIT {limit}"
        
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(sql, params).fetchall()
    
    def get_categories(self):
        """Get all categories"""
        with sqlite3.connect(self.db_path) as conn:
            return [row[0] for row in conn.execute("SELECT DISTINCT category FROM images ORDER BY category").fetchall()]
    
    def get_folders(self):
        """Get all folders"""
        with sqlite3.connect(self.db_path) as conn:
            return [row[0] for row in conn.execute("SELECT DISTINCT folder FROM images ORDER BY folder").fetchall()]
    
    def get_stats(self):
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM images")
            total_images = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT category) FROM images")
            total_categories = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT folder) FROM images")
            total_folders = cursor.fetchone()[0]
            
            return {
                'total_images': total_images,
                'total_categories': total_categories,
                'total_folders': total_folders
            }

class AdvancedUIViewer:
    """Advanced UI Viewer with modern features"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Silver and Blood UI Viewer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize components
        self.cache = ImageCache(max_cache_size=100)
        self.db = None
        self.current_images = []
        self.current_image_index = 0
        self.zoom_level = 1.0
        self.current_image_path = None
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        self.create_styles()
        self.create_interface()
        self.bind_shortcuts()
        
        # Auto-detect UI extraction folder
        self.auto_detect_folder()
    
    def create_styles(self):
        """Create modern dark theme styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles for dark theme
        self.style.configure('Dark.TFrame', background='#2b2b2b')
        self.style.configure('Dark.TLabel', background='#2b2b2b', foreground='white')
        self.style.configure('Dark.TEntry', fieldbackground='#404040', foreground='white', insertcolor='white')
        self.style.configure('Dark.TButton', background='#404040', foreground='white')
        self.style.map('Dark.TButton', background=[('active', '#505050')])
        self.style.configure('Dark.TCombobox', fieldbackground='#404040', foreground='white')
        self.style.configure('Dark.Treeview', background='#404040', foreground='white', fieldbackground='#404040')
        self.style.configure('Dark.Treeview.Heading', background='#505050', foreground='white')
    
    def create_interface(self):
        """Create the main interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.create_toolbar()
        self.create_content_area()
        self.create_status_bar()
    
    def create_toolbar(self):
        """Create the toolbar with search and filters"""
        toolbar = ttk.Frame(self.main_frame, style='Dark.TFrame')
        toolbar.pack(fill='x', pady=(0, 5))
        
        # Folder selection
        ttk.Label(toolbar, text="Folder:", style='Dark.TLabel').pack(side='left', padx=(0, 5))
        self.folder_button = ttk.Button(toolbar, text="Select Folder", command=self.select_folder, style='Dark.TButton')
        self.folder_button.pack(side='left', padx=(0, 10))
        
        # Index button
        self.index_button = ttk.Button(toolbar, text="Index Images", command=self.index_images, style='Dark.TButton')
        self.index_button.pack(side='left', padx=(0, 10))
        
        # Search
        ttk.Label(toolbar, text="Search:", style='Dark.TLabel').pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=20, style='Dark.TEntry')
        search_entry.pack(side='left', padx=(0, 10))
        
        # Category filter
        ttk.Label(toolbar, text="Category:", style='Dark.TLabel').pack(side='left', padx=(0, 5))
        self.category_var = tk.StringVar(value="All")
        self.category_combo = ttk.Combobox(toolbar, textvariable=self.category_var, width=15, style='Dark.TCombobox', state='readonly')
        self.category_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        self.category_combo.pack(side='left', padx=(0, 10))
        
        # Folder filter
        ttk.Label(toolbar, text="Type:", style='Dark.TLabel').pack(side='left', padx=(0, 5))
        self.folder_var = tk.StringVar(value="All")
        self.folder_combo = ttk.Combobox(toolbar, textvariable=self.folder_var, width=15, style='Dark.TCombobox', state='readonly')
        self.folder_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        self.folder_combo.pack(side='left', padx=(0, 10))
        
        # View mode
        ttk.Label(toolbar, text="View:", style='Dark.TLabel').pack(side='left', padx=(0, 5))
        self.view_var = tk.StringVar(value="Grid")
        view_combo = ttk.Combobox(toolbar, textvariable=self.view_var, values=["Grid", "List"], width=8, style='Dark.TCombobox', state='readonly')
        view_combo.bind('<<ComboboxSelected>>', self.switch_view_mode)
        view_combo.pack(side='left', padx=(0, 10))
    
    def create_content_area(self):
        """Create the main content area"""
        # Create paned window for resizable panels
        self.paned = ttk.PanedWindow(self.main_frame, orient='horizontal')
        self.paned.pack(fill='both', expand=True)
        
        self.create_image_browser()
        self.create_image_viewer()
    
    def create_image_browser(self):
        """Create the image browser panel"""
        # Left panel for image list/grid
        browser_frame = ttk.Frame(self.paned, style='Dark.TFrame')
        self.paned.add(browser_frame, weight=1)
        
        # Create notebook for different view modes
        self.browser_notebook = ttk.Notebook(browser_frame)
        self.browser_notebook.pack(fill='both', expand=True)
        
        # Grid view
        self.create_grid_view()
        # List view
        self.create_list_view()
    
    def create_grid_view(self):
        """Create grid view for thumbnails"""
        grid_frame = ttk.Frame(self.browser_notebook, style='Dark.TFrame')
        self.browser_notebook.add(grid_frame, text="Grid")
        
        # Scrollable canvas for grid
        canvas = tk.Canvas(grid_frame, bg='#2b2b2b', highlightthickness=0)
        scrollbar_v = ttk.Scrollbar(grid_frame, orient='vertical', command=canvas.yview)
        scrollbar_h = ttk.Scrollbar(grid_frame, orient='horizontal', command=canvas.xview)
        
        self.grid_frame = ttk.Frame(canvas, style='Dark.TFrame')
        
        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar_v.pack(side='right', fill='y')
        scrollbar_h.pack(side='bottom', fill='x')
        
        self.grid_canvas = canvas
        self.grid_frame.bind('<Configure>', self.on_grid_configure)
    
    def create_list_view(self):
        """Create list view for detailed info"""
        list_frame = ttk.Frame(self.browser_notebook, style='Dark.TFrame')
        self.browser_notebook.add(list_frame, text="List")
        
        # Treeview for list
        columns = ('Name', 'Category', 'Size', 'Dimensions')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Dark.Treeview')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbars for treeview
        tree_scroll_v = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        tree_scroll_h = ttk.Scrollbar(list_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_v.set, xscrollcommand=tree_scroll_h.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        tree_scroll_v.pack(side='right', fill='y')
        tree_scroll_h.pack(side='bottom', fill='x')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_list_select)
    
    def create_image_viewer(self):
        """Create the image viewer panel"""
        viewer_frame = ttk.Frame(self.paned, style='Dark.TFrame')
        self.paned.add(viewer_frame, weight=2)
        
        # Image display area
        self.image_canvas = tk.Canvas(viewer_frame, bg='#1a1a1a', highlightthickness=0)
        
        # Scrollbars for image canvas
        img_scroll_v = ttk.Scrollbar(viewer_frame, orient='vertical', command=self.image_canvas.yview)
        img_scroll_h = ttk.Scrollbar(viewer_frame, orient='horizontal', command=self.image_canvas.xview)
        self.image_canvas.configure(yscrollcommand=img_scroll_v.set, xscrollcommand=img_scroll_h.set)
        
        self.image_canvas.pack(side='left', fill='both', expand=True)
        img_scroll_v.pack(side='right', fill='y')
        img_scroll_h.pack(side='bottom', fill='x')
        
        # Image controls
        controls_frame = ttk.Frame(viewer_frame, style='Dark.TFrame')
        controls_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Fit", command=self.fit_image, style='Dark.TButton').pack(side='left', padx=2)
        ttk.Button(controls_frame, text="100%", command=self.actual_size, style='Dark.TButton').pack(side='left', padx=2)
        ttk.Button(controls_frame, text="Zoom In", command=self.zoom_in, style='Dark.TButton').pack(side='left', padx=2)
        ttk.Button(controls_frame, text="Zoom Out", command=self.zoom_out, style='Dark.TButton').pack(side='left', padx=2)
        
        # Image enhancement controls
        ttk.Separator(controls_frame, orient='vertical').pack(side='left', fill='y', padx=5)
        ttk.Button(controls_frame, text="Sharpen", command=self.sharpen_image, style='Dark.TButton').pack(side='left', padx=2)
        ttk.Button(controls_frame, text="Reset", command=self.reset_enhancements, style='Dark.TButton').pack(side='left', padx=2)
        
        # Navigation
        ttk.Separator(controls_frame, orient='vertical').pack(side='left', fill='y', padx=5)
        ttk.Button(controls_frame, text="Previous", command=self.previous_image, style='Dark.TButton').pack(side='left', padx=2)
        ttk.Button(controls_frame, text="Next", command=self.next_image, style='Dark.TButton').pack(side='left', padx=2)
        
        # Bind mouse events for pan and zoom
        self.image_canvas.bind('<Button-1>', self.start_pan)
        self.image_canvas.bind('<B1-Motion>', self.pan_image)
        self.image_canvas.bind('<MouseWheel>', self.mouse_zoom)
        self.image_canvas.bind('<Button-4>', lambda e: self.mouse_zoom(e))  # Linux
        self.image_canvas.bind('<Button-5>', lambda e: self.mouse_zoom(e))  # Linux
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.status_frame.pack(fill='x', pady=(5, 0))
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, style='Dark.TLabel')
        self.status_label.pack(side='left')
        
        # Progress bar
        self.progress = ttk.Progressbar(self.status_frame, mode='determinate')
        self.progress.pack(side='right', padx=(10, 0))
    
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.select_folder())
        self.root.bind('<Control-f>', lambda e: self.search_var.set(""))
        self.root.bind('<Left>', lambda e: self.previous_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.actual_size())
        self.root.bind('<F11>', self.toggle_fullscreen)
    
    def auto_detect_folder(self):
        """Auto-detect UI extraction folder"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        ui_folder = os.path.join(base_path, "complete_ui_extraction")
        
        if os.path.exists(ui_folder):
            self.current_folder = ui_folder
            self.folder_button.config(text=f"Folder: {os.path.basename(ui_folder)}")
            
            # Check if database exists
            db_path = os.path.join(base_path, "ui_images.db")
            self.db = ImageDatabase(db_path)
            
            # Auto-index if database is empty or old
            stats = self.db.get_stats()
            if stats['total_images'] == 0:
                self.index_images()
            else:
                self.load_filters()
                self.search_images()
    
    def select_folder(self):
        """Select folder to browse"""
        folder = filedialog.askdirectory(title="Select UI Images Folder")
        if folder:
            self.current_folder = folder
            self.folder_button.config(text=f"Folder: {os.path.basename(folder)}")
            
            # Initialize database for this folder
            base_path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_path, "ui_images.db")
            self.db = ImageDatabase(db_path)
            
            # Prompt to index
            result = messagebox.askyesno("Index Images", "Index images in this folder for fast searching?")
            if result:
                self.index_images()
    
    def index_images(self):
        """Index images in the selected folder"""
        if not hasattr(self, 'current_folder') or not self.db:
            messagebox.showwarning("Warning", "Please select a folder first")
            return
        
        def index_worker():
            try:
                self.status_var.set("Indexing images...")
                self.progress.config(mode='indeterminate')
                self.progress.start()
                
                def progress_callback(count):
                    self.status_var.set(f"Indexed {count} images...")
                
                total = self.db.index_directory(self.current_folder, progress_callback)
                
                self.root.after(0, self.on_index_complete, total)
                
            except Exception as e:
                self.root.after(0, self.on_index_error, str(e))
        
        threading.Thread(target=index_worker, daemon=True).start()
    
    def on_index_complete(self, total):
        """Handle index completion"""
        self.progress.stop()
        self.progress.config(mode='determinate')
        self.status_var.set(f"Indexed {total} images")
        
        self.load_filters()
        self.search_images()
    
    def on_index_error(self, error):
        """Handle index error"""
        self.progress.stop()
        self.status_var.set("Indexing failed")
        messagebox.showerror("Error", f"Failed to index images: {error}")
    
    def load_filters(self):
        """Load filter options from database"""
        if not self.db:
            return
        
        categories = ["All"] + self.db.get_categories()
        folders = ["All"] + self.db.get_folders()
        
        self.category_combo.config(values=categories)
        self.folder_combo.config(values=folders)
    
    def search_images(self):
        """Search and display images"""
        if not self.db:
            return
        
        query = self.search_var.get()
        category = self.category_var.get()
        folder = self.folder_var.get()
        
        results = self.db.search_images(query, category, folder)
        self.current_images = results
        
        self.update_displays()
        self.status_var.set(f"Found {len(results)} images")
    
    def update_displays(self):
        """Update both grid and list displays"""
        self.update_grid_view()
        self.update_list_view()
    
    def update_grid_view(self):
        """Update the grid view with thumbnails"""
        # Clear existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        if not self.current_images:
            return
        
        # Calculate grid layout
        grid_width = 4  # Number of columns
        
        def load_thumbnails():
            for i, image_data in enumerate(self.current_images[:100]):  # Limit for performance
                path = image_data[1]  # path is at index 1
                filename = image_data[2]  # filename is at index 2
                
                try:
                    thumbnail = self.cache.get_thumbnail(path)
                    if thumbnail:
                        row = i // grid_width
                        col = i % grid_width
                        
                        # Create thumbnail frame
                        thumb_frame = ttk.Frame(self.grid_frame, style='Dark.TFrame')
                        thumb_frame.grid(row=row, column=col, padx=5, pady=5)
                        
                        # Thumbnail label
                        thumb_label = tk.Label(thumb_frame, image=thumbnail, bg='#2b2b2b', cursor='hand2')
                        thumb_label.pack()
                        thumb_label.bind('<Button-1>', lambda e, idx=i: self.select_image(idx))
                        
                        # Filename label
                        name_label = ttk.Label(thumb_frame, text=filename[:20] + "..." if len(filename) > 20 else filename, 
                                             style='Dark.TLabel', font=('TkDefaultFont', 8))
                        name_label.pack()
                        
                except Exception as e:
                    print(f"Error creating thumbnail for {path}: {e}")
        
        # Load thumbnails in background
        threading.Thread(target=load_thumbnails, daemon=True).start()
    
    def update_list_view(self):
        """Update the list view"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for image_data in self.current_images:
            filename = image_data[2]
            category = image_data[3]
            size_bytes = image_data[5]
            width = image_data[6]
            height = image_data[7]
            
            # Format size
            size_str = f"{size_bytes // 1024}KB" if size_bytes < 1024*1024 else f"{size_bytes // (1024*1024)}MB"
            dimensions_str = f"{width}x{height}"
            
            self.tree.insert('', 'end', values=(filename, category, size_str, dimensions_str))
    
    def select_image(self, index):
        """Select and display an image"""
        if 0 <= index < len(self.current_images):
            self.current_image_index = index
            image_data = self.current_images[index]
            self.current_image_path = image_data[1]
            self.display_image()
    
    def display_image(self):
        """Display the selected image"""
        if not self.current_image_path:
            return
        
        def load_and_display():
            try:
                # Load image
                img = Image.open(self.current_image_path)
                
                # Apply zoom
                if self.zoom_level != 1.0:
                    new_size = (int(img.width * self.zoom_level), int(img.height * self.zoom_level))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                self.current_photo = ImageTk.PhotoImage(img)
                
                # Display on canvas
                self.image_canvas.delete('all')
                self.image_canvas.create_image(0, 0, anchor='nw', image=self.current_photo)
                self.image_canvas.config(scrollregion=self.image_canvas.bbox('all'))
                
            except Exception as e:
                print(f"Error displaying image: {e}")
        
        threading.Thread(target=load_and_display, daemon=True).start()
    
    def fit_image(self):
        """Fit image to canvas"""
        if not self.current_image_path:
            return
        
        try:
            # Get canvas size
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            # Get image size
            with Image.open(self.current_image_path) as img:
                img_width, img_height = img.size
            
            # Calculate zoom to fit
            zoom_x = canvas_width / img_width
            zoom_y = canvas_height / img_height
            self.zoom_level = min(zoom_x, zoom_y, 1.0)  # Don't zoom in beyond 100%
            
            self.display_image()
            
        except Exception as e:
            print(f"Error fitting image: {e}")
    
    def actual_size(self):
        """Display image at actual size"""
        self.zoom_level = 1.0
        self.display_image()
    
    def zoom_in(self):
        """Zoom in"""
        self.zoom_level = min(self.zoom_level * 1.2, 10.0)
        self.display_image()
    
    def zoom_out(self):
        """Zoom out"""
        self.zoom_level = max(self.zoom_level / 1.2, 0.1)
        self.display_image()
    
    def sharpen_image(self):
        """Apply sharpening filter"""
        if not self.current_image_path:
            return
        
        try:
            img = Image.open(self.current_image_path)
            
            # Apply sharpening
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            
            # Apply zoom if needed
            if self.zoom_level != 1.0:
                new_size = (int(img.width * self.zoom_level), int(img.height * self.zoom_level))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            self.current_photo = ImageTk.PhotoImage(img)
            
            # Display
            self.image_canvas.delete('all')
            self.image_canvas.create_image(0, 0, anchor='nw', image=self.current_photo)
            self.image_canvas.config(scrollregion=self.image_canvas.bbox('all'))
            
        except Exception as e:
            print(f"Error sharpening image: {e}")
    
    def reset_enhancements(self):
        """Reset image enhancements"""
        self.display_image()
    
    def previous_image(self):
        """Navigate to previous image"""
        if self.current_images and self.current_image_index > 0:
            self.select_image(self.current_image_index - 1)
    
    def next_image(self):
        """Navigate to next image"""
        if self.current_images and self.current_image_index < len(self.current_images) - 1:
            self.select_image(self.current_image_index + 1)
    
    def start_pan(self, event):
        """Start panning"""
        self.image_canvas.scan_mark(event.x, event.y)
    
    def pan_image(self, event):
        """Pan image"""
        self.image_canvas.scan_dragto(event.x, event.y, gain=1)
    
    def mouse_zoom(self, event):
        """Mouse wheel zoom"""
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def toggle_fullscreen(self, event):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def on_search_change(self, *args):
        """Handle search text change"""
        # Debounce search
        if hasattr(self, '_search_timer'):
            self.root.after_cancel(self._search_timer)
        self._search_timer = self.root.after(300, self.search_images)
    
    def on_filter_change(self, *args):
        """Handle filter change"""
        self.search_images()
    
    def switch_view_mode(self, *args):
        """Switch between grid and list view"""
        mode = self.view_var.get()
        if mode == "Grid":
            self.browser_notebook.select(0)
        else:
            self.browser_notebook.select(1)
    
    def on_grid_configure(self, event):
        """Handle grid frame configuration"""
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox('all'))
    
    def on_list_select(self, event):
        """Handle list selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item['values'][0]
            
            # Find image by filename
            for i, image_data in enumerate(self.current_images):
                if image_data[2] == filename:
                    self.select_image(i)
                    break
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.cache.clear()
        self.executor.shutdown(wait=False)

if __name__ == "__main__":
    app = AdvancedUIViewer()
    app.run()
