import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import webbrowser
from PIL import Image, ImageTk
from controller.gesture_controller import GestureController
from controller.language import Language
from controller.config import load_config, save_config
from ttkbootstrap.widgets import Combobox
from controller.virtual_keyboard import VirtualKeyboard

class App:
    def __init__(self, root):
        # Initialize main application window
        self.root = root

        # Load language and config settings
        self.config = load_config()
        self.current_lang = self.config.get("language", "EN")
        if not hasattr(Language, self.current_lang):
            self.current_lang = "EN"
        self.lang_dict = getattr(Language, self.current_lang)

        # Set window properties
        self.root.title(self.lang_dict["title"])
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # Initialize control state
        self.controller_instance = None
        self.is_running = False

        # Title label
        self.label = ttk.Label(root, text=self.lang_dict["title"], font=("Helvetica", 16, "bold"))
        self.label.pack(pady=(20, 10))

        # Description label
        self.description = ttk.Label(root, text=self.lang_dict["description"],
            font=("Arial", 10), wraplength=300, justify="center")
        self.description.pack(pady=(0, 10))

        # Control buttons frame
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)

        # Start/Pause/Resume button
        self.start_pause_btn = ttk.Button(button_frame, text=self.lang_dict["start"],
            command=self.toggle_start_pause, bootstyle="success-outline")
        self.start_pause_btn.pack(side=LEFT, padx=5, ipadx=10, ipady=5)

        # Exit button
        self.exit_btn = ttk.Button(button_frame, text=self.lang_dict["exit"],
            command=self.exit_app, bootstyle="danger")
        self.exit_btn.pack(side=RIGHT, padx=5, ipadx=10, ipady=5)

        # Virtual keyboard toggle button
        self.keyboard_btn = ttk.Button(root, text=self.lang_dict["keyboard"],
            command=self.open_keyboard, bootstyle="primary")
        self.keyboard_btn.pack(pady=5, ipadx=10, ipady=5)

        # Note under keyboard button
        self.keyboard_note = ttk.Label(root, text=self.lang_dict["keyboard_note"],
            font=("Arial", 8), foreground="gray")
        self.keyboard_note.pack(pady=(0, 5))

        # Help button
        self.help_btn = ttk.Button(root, text=self.lang_dict["help"],
            command=self.show_help, bootstyle="info-outline")
        self.help_btn.pack(pady=5, ipadx=10, ipady=5)
        self.root.bind("<F1>", lambda event: self.show_help())

        # Language selection dropdown
        ttk.Label(root, text="Language:", font=("Arial", 10)).pack(pady=(10, 0))
        self.language_var = ttk.StringVar()
        self.lang_menu = Combobox(
            root,
            textvariable=self.language_var,
            values=["English (EN)", "Arabic (AR)", "French (FR)", "Spanish (ES)", "German (DE)"],
            bootstyle="secondary",
            state="readonly"
        )
        self.lang_menu.pack(pady=5, ipadx=10, ipady=5)
        self.lang_menu.bind("<<ComboboxSelected>>", lambda e: self.set_language(self.language_var.get().split()[-1].strip("()")))
        self.language_var.set(f"{self.get_lang_name(self.current_lang)} ({self.current_lang})")

        # Status label
        self.status_label = ttk.Label(root, text=self.lang_dict["status_idle"],
                                    font=("Arial", 10), foreground="gray")
        self.status_label.pack(pady=(10, 0))

        # Footer with LinkedIn icon and name
        footer_frame = ttk.Frame(root)
        footer_frame.pack(pady=(0, 5))

        linkedin_img = Image.open("linkedin.png")
        linkedin_img = linkedin_img.resize((40, 40))
        linkedin_icon = ImageTk.PhotoImage(linkedin_img)

        icon_label = ttk.Label(footer_frame, image=linkedin_icon, cursor="hand2")
        icon_label.image = linkedin_icon
        icon_label.pack(side=LEFT, padx=(0, 5))

        name_label = ttk.Label(footer_frame, text="BY Esmail Sameh El-Hariri", font=("Arial", 9, "italic"), foreground="#AAAAAA", cursor="hand2")
        name_label.pack(side=LEFT)

        # LinkedIn link on click
        def open_link(event):
            webbrowser.open_new("https://www.linkedin.com/in/esmail-elhariri/")

        icon_label.bind("<Button-1>", open_link)
        name_label.bind("<Button-1>", open_link)

    def toggle_start_pause(self):
        # Toggle between start, pause, and resume states
        if not self.controller_instance:
            self.controller_instance = GestureController(self.root)
            self.is_running = True
            self.start_pause_btn.config(text=self.lang_dict["pause"], bootstyle="warning")
            self.status_label.config(text=self.lang_dict["status_running"], foreground="green")
        else:
            if self.is_running:
                self.controller_instance.running = False
                self.is_running = False
                self.start_pause_btn.config(text=self.lang_dict["resume"], bootstyle="success-outline")
                self.status_label.config(text=self.lang_dict["status_paused"], foreground="orange")
            else:
                self.controller_instance.running = True
                self.is_running = True
                self.controller_instance.update()
                self.start_pause_btn.config(text=self.lang_dict["pause"], bootstyle="warning")
                self.status_label.config(text=self.lang_dict["status_running"], foreground="green")

    def exit_app(self):
        # Gracefully stop the app and exit
        if self.controller_instance:
            self.controller_instance.stop()
        self.root.destroy()
        os._exit(0)

    def open_keyboard(self):
        # Show the virtual keyboard
        if not self.controller_instance:
            self.controller_instance = GestureController(self.root)
            self.controller_instance.running = False
        self.controller_instance.virtual_keyboard.show()

    def set_language(self, lang_code):
        # Update app language and save to config
        self.current_lang = lang_code
        self.config["language"] = lang_code
        save_config(self.config)
        self.lang_dict = getattr(Language, self.current_lang)
        self.update_ui_language()

    def update_ui_language(self):
        # Refresh all UI texts based on current language
        self.root.title(self.lang_dict["title"])
        self.label.config(text=self.lang_dict["title"])
        self.description.config(text=self.lang_dict["description"])
        self.start_pause_btn.config(text=self.lang_dict["start"])
        self.exit_btn.config(text=self.lang_dict["exit"])
        self.keyboard_btn.config(text=self.lang_dict["keyboard"])
        self.help_btn.config(text=self.lang_dict["help"])
        self.status_label.config(text=self.lang_dict["status_idle"])
        self.language_var.set(f"{self.get_lang_name(self.current_lang)} ({self.current_lang})")
        self.keyboard_note.config(text=self.lang_dict["keyboard_note"])

    def show_help(self):
        # Show help window with usage instructions
        help_win = ttk.Toplevel(self.root)
        help_win.title(self.lang_dict["help_title"])
        help_win.geometry("500x500")

        help_text = ttk.Text(help_win, wrap="word", font=("Arial", 11))
        help_text.pack(padx=10, pady=10, expand=True, fill="both")

        help_text.insert("1.0", self.lang_dict.get("help_content", "").strip())
        help_text.config(state="disabled")

    def get_lang_name(self, code):
        # Map language code to readable name
        return {
            "EN": "English",
            "AR": "Arabic",
            "FR": "French",
            "ES": "Spanish",
            "DE": "German"
        }.get(code, "Unknown")
