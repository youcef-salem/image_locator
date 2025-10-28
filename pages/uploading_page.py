import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils import Theme
from utils.upload_image import ImageUploadManager, add_image_to_list, delete_image_from_list

theme = Theme()
styles = theme.tk_styles()


class UploadingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=theme.background)

        # Initialize image manager
        self.image_manager = ImageUploadManager(thumbnail_size=(150, 150))

        # Title label
        title_label = tk.Label(self, text="Upload Image", 
                               bg=theme.background, fg=theme.text,
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # Upload button
        upload_button = tk.Button(self, text="Select Image", 
                                 command=self.upload_image)
        upload_button.config(**styles["primary_button"])
        upload_button.pack(pady=10)
        
        # Images list container (scrollable)
        list_frame = tk.Frame(self, bg=theme.background)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Create canvas and scrollbar for scrollable list
        self.canvas = tk.Canvas(list_frame, bg=theme.background, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=theme.background)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Back button
        back_button = tk.Button(self, text="Back to Home",
                               command=lambda: controller.show_frame("main"))
        back_button.config(**styles["primary_button"])
        back_button.pack(pady=10)
    
    def upload_image(self):
        """Open file dialog to select an image"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.webp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Add image using manager
                photo_reference = self.image_manager.add_image(file_path)
                
                # Add to display list using imported function
                add_image_to_list(
                    self.scrollable_frame, 
                    file_path, 
                    photo_reference,
                    self.handle_delete,
                    theme
                )
                print(f"Total images: {self.image_manager.get_image_count()}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")
    
    def handle_delete(self, file_path: str, item_frame: tk.Frame):
        """Handle delete button click"""
        delete_image_from_list(self.image_manager, file_path, item_frame)
