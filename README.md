
# AI Virtual Mouse using Computer Vision

## Description

This is a graduation project that demonstrates an AI-powered virtual mouse system using real-time hand gesture recognition. It allows users to control mouse actions, type using a virtual keyboard, and manage presentation slides—all without physical contact.

The system is built with Python and integrates computer vision, GUI programming, and automation to create a practical example of human-computer interaction through artificial intelligence.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [License](#license)
- [Contact](#contact)

---

## Installation


1. (Optional) Create a virtual environment:

   python -m venv venv
   venv\Scripts\activate   # For Windows


2. Install the required dependencies:

   pip install -r requirements.txt


---

## Usage

1. Make sure your webcam is connected.
2. Run the main script:

   python main.py

3. Use predefined hand gestures to control the mouse, type, or manage slides.
4. Access the Help button in the application to view available gestures.

---

## Features

- Real-time mouse control with hand gestures
- Left and right mouse click using pinching gestures
- On-screen virtual keyboard (supports English and Arabic)
- Presentation control: next/previous slide, drawing, and exit
- Pause/Resume detection
- Settings saving and gesture customization
- Gesture usage logging
- Packaged executable with splash screen and custom icon

---

## Technologies Used

- Python 3.8+
- OpenCV
- MediaPipe
- Tkinter
- PyAutoGUI
- Pyperclip

---

## Project Structure

```
THEPROJECT(FINAL)/
│
├── controller/                  # Core control modules
│   ├── __init__.py              # Package initializer
│   ├── config.py                # Configuration and settings
│   ├── gesture_controller.py    # Main gesture-to-action mapping
│   ├── hand_recognition.py      # Hand tracking and landmark detection
│   ├── language.py              # Language switching logic
│   ├── ppt_controller.py        # Presentation control functions
│   ├── system_control.py        # Pause/Resume and system-level actions
│   └── virtual_keyboard.py      # On-screen keyboard functionality
│
├── app.py                       # Entry point for running via app interface
├── main.py                      # Main application launcher
├── settings.json                # Saved user settings
├── requirements.txt             # Required Python packages
├── splash.png                   # Splash screen image
├── linkedin.png                 # Profile/logo asset
├── venv/                        # Virtual environment directory
└── README.md                    # Project documentation
```

---

## License

This project is developed for academic purposes . Commercial use or distribution is prohibited without written permission.

---

## Contact

**Name:** Eng.Esmail Sameh EL-Hariri  
**Supervisor:** Dr.Eid Emari
**University:** Faculty of Computer Science, Arab Open University - Egypt 
**Academic Year:** 2024/2025
