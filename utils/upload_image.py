"""
Image upload and management utilities.
Handles image loading, validation, and storage operations.
"""

import os
import tkinter as tk
from PIL import Image, ImageTk
from typing import Optional, Tuple


class ImageUploadManager:
    """Manages image upload operations and storage."""
    
    def __init__(self, thumbnail_size: Tuple[int, int] = (150, 150)):
        """
        Initialize the ImageUploadManager.
        
        Args:
            thumbnail_size: Tuple of (width, height) for thumbnail images
        """
        self.thumbnail_size = thumbnail_size
        self.uploaded_image_paths: list[str] = []
        self.photo_references: dict[str, ImageTk.PhotoImage] = {}
    
    def add_image(self, file_path: str) -> Optional[ImageTk.PhotoImage]:
        """
        Add an image to the manager and create a thumbnail.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            ImageTk.PhotoImage object if successful, None otherwise
            
        Raises:
            Exception: If image cannot be loaded
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        # Load and create thumbnail
        try:
            image = Image.open(file_path)
            image.thumbnail(self.thumbnail_size)
            photo_reference = ImageTk.PhotoImage(image)
            
            # Store references
            self.uploaded_image_paths.insert(0, file_path)
            self.photo_references[file_path] = photo_reference
            
            return photo_reference
        except Exception as e:
            raise Exception(f"Could not load image: {e}")
    
    def remove_image(self, file_path: str) -> bool:
        """
        Remove an image from the manager.
        
        Args:
            file_path: Path to the image file to remove
            
        Returns:
            True if successful, False if file_path not found
        """
        if file_path in self.uploaded_image_paths:
            self.uploaded_image_paths.remove(file_path)
        
        if file_path in self.photo_references:
            del self.photo_references[file_path]
            return True
        
        return False
    
    def get_photo_reference(self, file_path: str) -> Optional[ImageTk.PhotoImage]:
        """
        Get the photo reference for an image.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            ImageTk.PhotoImage if found, None otherwise
        """
        return self.photo_references.get(file_path)
    
    def get_all_images(self) -> list[str]:
        """Get list of all uploaded image paths (most recent first)."""
        return self.uploaded_image_paths.copy()
    
    def get_image_count(self) -> int:
        """Get total number of uploaded images."""
        return len(self.uploaded_image_paths)
    
    def clear_all(self) -> None:
        """Clear all stored images and references."""
        self.uploaded_image_paths.clear()
        self.photo_references.clear()
    
    @staticmethod
    def get_filename(file_path: str) -> str:
        """Extract filename from file path."""
        return os.path.basename(file_path)


def add_image_to_list(scrollable_frame: tk.Frame, file_path: str, photo_ref, 
                      delete_callback, theme) -> tk.Frame:
   
    # Create container frame for the image item
    item_frame = tk.Frame(scrollable_frame, bg=theme.surface, relief="solid", bd=1)
    item_frame.pack(fill="x", padx=10, pady=5, ipady=5)
    
    # Left side: thumbnail image
    image_label = tk.Label(item_frame, image=photo_ref, bg=theme.surface)
    image_label.image = photo_ref  # Keep a reference
    image_label.pack(side="left", padx=10)
    
    # Middle: filename and info
    filename = ImageUploadManager.get_filename(file_path)
    info_frame = tk.Frame(item_frame, bg=theme.surface)
    info_frame.pack(side="left", fill="x", expand=True, padx=10)
    
    filename_label = tk.Label(info_frame, text=filename, bg=theme.surface, 
                             fg=theme.text, font=("Arial", 10, "bold"), 
                             wraplength=200, justify="left")
    filename_label.pack(anchor="w")
    
    path_label = tk.Label(info_frame, text=file_path, bg=theme.surface, 
                         fg=theme.muted, font=("Arial", 8), 
                         wraplength=200, justify="left")
    path_label.pack(anchor="w")
    
    # Right side: delete button
    delete_button = tk.Button(item_frame, text="Delete", 
                             command=lambda: delete_callback(file_path, item_frame))
    delete_button.config(bg=theme.danger, fg="white", bd=0, padx=10, pady=5)
    delete_button.pack(side="right", padx=10)
    
    return item_frame


def delete_image_from_list(image_manager: ImageUploadManager, file_path: str, 
                           item_frame: tk.Frame) -> None:
    """
    Delete an image from the manager and destroy its UI frame.
    
    Args:
        image_manager: ImageUploadManager instance
        file_path: Path to the image file to delete
        item_frame: The UI frame to destroy
    """
    image_manager.remove_image(file_path)
    item_frame.destroy()
    print(f"Deleted: {ImageUploadManager.get_filename(file_path)}")
    print(f"Total images: {image_manager.get_image_count()}")
