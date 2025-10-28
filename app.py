import tkinter as tk
from pages import StartPage, UploadingPage

main_dimension = "700x500"


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
        self.create_frames(container)
        
        self.show_frame("main")
    
    def create_frames(self, container):
        """Create all page frames"""
        frames_config = {
            "main": StartPage,
            "uploading": UploadingPage,
        }
        
        for page_name, page_class in frames_config.items():
            frame = page_class(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, page_name):
        """Show a frame for the given page"""
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = AppController()
    app.mainloop()
