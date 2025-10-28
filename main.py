import tkinter as tk
from tkinter import PhotoImage
from theme import Theme
from PIL import Image, ImageTk

# Initialize theme
theme = Theme()
styles = theme.tk_styles()
main_dimension = "700x500"

# Create root window
root = tk.Tk()
root.title("Hello, Tkinter!")
root.geometry(main_dimension)

# Variables to store original image and references
original_image = None
bg_photo = None
bg_label = None

# Load and set background image
try:
    original_image = Image.open("assets/photo-location.webp")  
except Exception as e:
    print(f"Error loading image: {e}")

# Create background label
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create button centered in the middle
button = tk.Button(root, text="Hello in the Location extractor")
button.config(**styles["primary_button"])
button.place(relx=0.5, rely=0.5, anchor="center")

# Function to update background image on window resize
def on_window_resize(event):
    global bg_photo
    if original_image:
        resized_image = original_image.resize((event.width, event.height))
        bg_photo = ImageTk.PhotoImage(resized_image)
        bg_label.config(image=bg_photo)
        bg_label.image = bg_photo

# Bind the resize event
root.bind("<Configure>", on_window_resize)

root.mainloop()

