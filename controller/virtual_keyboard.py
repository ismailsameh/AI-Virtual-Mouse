import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pyautogui
import pyperclip
import time
import ctypes

# Language codes for system input language switching
LANG_EN = 0x0409  
LANG_AR = 0x0C01  

class VirtualKeyboard:
    def __init__(self, parent=None):
        # Create a new top-level window for the virtual keyboard
        self.parent = parent
        self.window = ttk.Toplevel() if parent is None else ttk.Toplevel(parent)

        self.window.title("Virtual Keyboard")
        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        # Position the keyboard window at the bottom center of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 900
        window_height = 350
        x_position = (screen_width - window_width) // 2
        y_position = screen_height - window_height - 50
        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # UI colors and language state
        self.active_bg = "#3fa796"
        self.default_bg = "#2d2d44"
        self.text_color = "white"
        self.shift_on = False
        self.language = "EN"
        self.hidden = True

        # Text preview area for typed input
        self.text_preview = ttk.Text(self.window, height=2, width=90, font=("Arial", 12))
        self.text_preview.pack(pady=(10, 0), padx=10)

        # Buttons for actions like Clear, Send, Language Toggle
        control_frame = ttk.Frame(self.window)
        control_frame.pack(pady=5)

        ttk.Button(control_frame, text="Clear", bootstyle="danger",
            command=self.clear_text, width=10).pack(side=LEFT, padx=10)

        ttk.Button(control_frame, text="Send Text", bootstyle="success",
            command=self.send_text, width=10).pack(side=LEFT, padx=10)

        self.lang_btn = ttk.Button(control_frame, text="Lang: EN", bootstyle="info",
            command=self.toggle_language, width=10)
        self.lang_btn.pack(side=LEFT, padx=10)

        # Initialize keyboard layout and hide initially
        self.create_keyboard()
        self.hide()

    def create_keyboard(self):
        # Define English and Arabic layouts
        self.keyboard_frame = ttk.Frame(self.window)
        self.keyboard_frame.pack(pady=10)

        self.layout_en = [
            ["1","2","3","4","5","6","7","8","9","0","-","=","⌫"],
            ["q","w","e","r","t","y","u","i","o","p","[","]","\\"],
            ["a","s","d","f","g","h","j","k","l",";","'","Enter"],
            ["Shift","z","x","c","v","b","n","m",",",".","/","↑"],
            ["Ctrl","Alt","Space","←","↓","→"]
        ]

        self.layout_ar = [
            ["١","٢","٣","٤","٥","٦","٧","٨","٩","٠","-","=","⌫"],
            ["ض","ص","ث","ق","ف","غ","ع","ه","خ","ح","ج","د","\\"],
            ["ش","س","ي","ب","ل","ا","ت","ن","م","ك","ط","Enter"],
            ["Shift","ئ","ء","ؤ","ر","لا","ى","ة","و","ز","ظ","↑"],
            ["Ctrl","Alt","Space","←","↓","→"]
        ]

        self.build_keyboard(self.layout_en)

    def build_keyboard(self, layout):
        # Build keyboard GUI based on selected layout
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()

        self.keys = {}
        for row_keys in layout:
            frame = ttk.Frame(self.keyboard_frame)
            frame.pack(pady=2)

            for key in row_keys:
                width = 4
                if key == "Space":
                    width = 20
                elif key in ["Enter", "Shift", "Ctrl", "Alt", "⌫"]:
                    width = 7

                btn = ttk.Button(frame, text=key,
                                width=width, bootstyle="secondary",
                                command=lambda k=key: self.key_press(k))
                btn.pack(side=LEFT, padx=2, pady=2)
                self.keys[key] = btn

    def key_press(self, key):
        # Handle key press actions
        if key == "Shift":
            self.toggle_shift()
        elif key == "Space":
            self.text_preview.insert("end", " ")
        elif key == "⌫":
            self.text_preview.delete("end-2c", "end")
        elif key == "Enter":
            self.text_preview.insert("end", "\n")
        elif key in ["Ctrl", "Alt", "↑", "←", "↓", "→"]:
            pass
        elif len(key) == 1:
            self.text_preview.insert("end", key.upper() if self.shift_on else key.lower())

    def toggle_shift(self):
        # Toggle shift mode and update key labels
        self.shift_on = not self.shift_on
        for key, btn in self.keys.items():
            if len(key) == 1 and key.isalpha():
                new_text = key.upper() if self.shift_on else key.lower()
                btn.config(text=new_text)

    def toggle_language(self):
        # Switch between English and Arabic layouts
        if self.language == "EN":
            self.language = "AR"
            self.build_keyboard(self.layout_ar)
            self.lang_btn.config(text="Lang: AR")
        else:
            self.language = "EN"
            self.build_keyboard(self.layout_en)
            self.set_input_language(LANG_EN)
            self.lang_btn.config(text="Lang: EN")

    def set_input_language(self, lang_hex):
        # Change system input language using Windows API
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.PostMessageW(hwnd, 0x50, 0, lang_hex)

    def clear_text(self):
        # Clear all text from the preview box
        self.text_preview.delete("1.0", "end")

    def send_text(self):
        # Send the text from the preview to the focused application

        text = self.text_preview.get("1.0", "end").strip()
        if not text:
            return

        self.window.withdraw()  
        time.sleep(0.5)         
        pyperclip.copy(text)
        time.sleep(0.2)

        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)

        self.clear_text()
        self.window.deiconify() 

    def show(self):
        # Show the virtual keyboard window
        self.window.deiconify()
        self.hidden = False

    def hide(self):
        # Hide the virtual keyboard window
        self.window.withdraw()
        self.hidden = True

    def toggle_visibility(self):
        # Toggle between show and hide
        if self.hidden:
            self.show()
        else:
            self.hide()

    def close(self):
        # Close and destroy the window
        self.window.destroy()
