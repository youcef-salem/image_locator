import tkinter as tk
from PIL import Image, ImageTk
from utils import Theme

theme = Theme()
styles = theme.tk_styles()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Variables to store original image and references
        self.original_image = None
        self.bg_photo = None
        self.bg_label = None
        self.last_width = None
        self.last_height = None
        
        # Load background image
        try:
            self.original_image = Image.open("assets/photo-location.webp")  
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Create background label
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create button centered in the middle
        button = tk.Button(self, text="Make extractions", 
                          command=lambda: controller.show_frame("uploading"))
        button.config(**styles["primary_button"])
        button.place(relx=0.5, rely=0.5, anchor="center")
        
        # Bind resize event
        self.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        """Update background image only when size actually changes"""
        if self.original_image and (self.last_width != event.width or self.last_height != event.height):
            self.last_width = event.width
            self.last_height = event.height
            
            try:
                resized_image = self.original_image.resize((event.width, event.height))
                self.bg_photo = ImageTk.PhotoImage(resized_image)
                self.bg_label.config(image=self.bg_photo)
                self.bg_label.image = self.bg_photo
            except Exception as e:
                print(f"Error resizing image: {e}")
