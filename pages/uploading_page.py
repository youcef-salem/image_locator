import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.theme import Theme
from PIL import Image, ImageTk

theme = Theme()
styles = theme.tk_styles()


class UploadingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=theme.background)
        
        self.uploaded_image_path = None
        self.photo_reference = None
        
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
        
        # Display image info
        self.info_label = tk.Label(self, text="No image selected",
                                   bg=theme.background, fg=theme.muted)
        self.info_label.pack(pady=10)
        
        # Image preview
        self.preview_label = tk.Label(self, bg=theme.surface)
        self.preview_label.pack(pady=10, padx=20, fill="both", expand=True)
        
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
            self.uploaded_image_path = file_path
            filename = os.path.basename(file_path)
            self.info_label.config(text=f"Selected: {filename}")
            
            # Show preview
            try:
                preview_image = Image.open(file_path)
                preview_image.thumbnail((400, 300))
                self.photo_reference = ImageTk.PhotoImage(preview_image)
                self.preview_label.config(image=self.photo_reference)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")
