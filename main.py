import tkinter as tk
from tkinter import filedialog, messagebox
from utils.theme import Theme
from PIL import Image, ImageTk
import os

# Initialize theme
theme = Theme()
styles = theme.tk_styles()
main_dimension = "700x500"

# Create root window
root = tk.Tk()
root.title("Image Location Extractor")
root.geometry(main_dimension)

# Dictionary to store frames
frames = {}

class MainApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Variables to store original image and references
        self.original_image = None
        self.bg_photo = None
        self.bg_label = None
        
        # Load and set background image
        try:
            self.original_image = Image.open("assets/photo-location.webp")  
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Create background label
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create button centered in the middle
        button = tk.Button(self, text="Make extractions", 
                          command=lambda: controller.show_frame(UploadingPage))
        button.config(**styles["primary_button"])
        button.place(relx=0.5, rely=0.5, anchor="center")
        
        # Bind resize event
        self.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        if self.original_image:
            resized_image = self.original_image.resize((event.width, event.height))
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            self.bg_label.config(image=self.bg_photo)
            self.bg_label.image = self.bg_photo


class UploadingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=theme.background)
        
        self.uploaded_image_path = None
        
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
                               command=lambda: controller.show_frame(MainApp))
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
                photo = ImageTk.PhotoImage(preview_image)
                self.preview_label.config(image=photo)
                self.preview_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")


class AppController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Image Location Extractor")
        self.geometry(main_dimension)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (MainApp, UploadingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainApp)
    
    def show_frame(self, cont):
        """Show a frame for the given page"""
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = AppController()
    app.mainloop()

