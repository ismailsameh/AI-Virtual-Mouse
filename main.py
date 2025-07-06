import tkinter as tk
from PIL import Image, ImageTk
import time
import ttkbootstrap as ttk
from app import App

def show_splash():
    # Create and display the splash screen window
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)  # Remove window borders
    splash_root.geometry("340x512+500+200")  # Set splash window size and position

    image = Image.open("splash.png")
    image = image.resize((340, 512))
    img = ImageTk.PhotoImage(image)

    label = tk.Label(splash_root, image=img)
    label.image = img  # Keep a reference to prevent garbage collection
    label.pack()

    splash_root.after(2500, splash_root.destroy)  # Close splash after 2.5 seconds
    splash_root.mainloop()

def start_main_app():
    # Start the main application after splash screen
    try:
        root = ttk.Window(themename="darkly")  # Use themed window
        App(root)  # Launch main app
        root.mainloop()
    except Exception as e:
        print("App launch error:", e)  # Handle any initialization errors

if __name__ == "__main__":
    # Entry point: show splash then launch main app
    show_splash()
    start_main_app()
