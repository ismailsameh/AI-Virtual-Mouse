import json
import os

# File name for storing configuration settings
CONFIG_FILE = "settings.json"

# Default configuration settings used if no config file exists
DEFAULT_CONFIG = {
    "language": "EN",  # Default language set to English
    "gestures": {
        "move_cursor": "V_GEST",     # Gesture assigned to move the cursor
        "left_click": "MID",         # Gesture assigned for left click
        "right_click": "INDEX",      # Gesture assigned for right click
        "scroll": "PINCH_MINOR",     # Gesture assigned for scrolling
        "volume": "PINCH_MAJOR"      # Gesture assigned for volume control
    }
}

def load_config():
    """
    Loads configuration from file if it exists.
    Falls back to default configuration if the file is missing or unreadable.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)  # Load configuration from JSON file
        except Exception as e:
            print("Error loading config:", e)  # Print error if loading fails
    save_config(DEFAULT_CONFIG.copy())  # Save default config if file not found or error occurs
    return DEFAULT_CONFIG.copy()        # Return a copy of the default configuration

def save_config(config):
    """
    Saves the provided configuration dictionary to the config file.
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)  # Write config to JSON file with indentation
    except Exception as e:
        print("Error saving config:", e)  # Print error if saving fails
