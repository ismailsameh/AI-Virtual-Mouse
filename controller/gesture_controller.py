import cv2
import time
import numpy as np
import PIL.Image, PIL.ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controller.hand_recognition import HandRecog, HLabel, Gest
from controller.system_control import Controller
from controller.virtual_keyboard import VirtualKeyboard
from controller.ppt_controller import PPTController
from google.protobuf.json_format import MessageToDict
import mediapipe as mp
import pyautogui

class GestureController:
    # Static variables to hold hand recognition results
    hr_major = None
    hr_minor = None
    dom_hand = True

    def __init__(self, root):
        # Initialize main camera window and its components
        self.root = root
        self.window = ttk.Toplevel(root)
        self.window.title("Camera")
        self.window.geometry("320x180")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.window.attributes("-topmost", True)

        # Frame for displaying video feed
        display_frame = ttk.Frame(self.window)
        display_frame.pack(padx=10, pady=10)

        self.label = ttk.Label(display_frame)
        self.label.pack()

        # Frame for showing status
        control_frame = ttk.Frame(self.window)
        control_frame.pack(padx=10, pady=5, fill="x")

        self.status_label = ttk.Label(control_frame, text="Status: Idle", font=("Arial", 10), foreground="white")
        #self.status_label.pack(side="right", pady=5, padx=5)

        # Initialize virtual keyboard
        self.virtual_keyboard = VirtualKeyboard(self.root)

        # Initialize webcam feed
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.running = True
        Controller.current_status = "Idle"

        # Initialize hand recognition modules
        self.handmajor = HandRecog(HLabel.MAJOR)
        self.handminor = HandRecog(HLabel.MINOR)

        # Initialize Mediapipe hand detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1,
                                        min_detection_confidence=0.7,
                                        min_tracking_confidence=0.7)

        self.prev_time = time.time()
        self.update()  # Start updating the camera feed

    def disable_close(self):
        # Prevent closing the camera window
        pass

    def update(self):
        # Recursively updates the camera feed and processes gestures
        if not self.running:
            return

        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame, 1)  # Flip for mirror view
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            small_rgb = cv2.resize(rgb, (160, 120))
            results = self.hands.process(small_rgb)

            if results.multi_hand_landmarks:
                self.classify_hands(results)
                self.handmajor.update_hand_result(GestureController.hr_major)
                self.handminor.update_hand_result(GestureController.hr_minor)

                self.handmajor.set_finger_state()
                self.handminor.set_finger_state()
                gest_minor = self.handminor.get_gesture()
                gest_major = self.handmajor.get_gesture()                

                # Handle PowerPoint-specific gestures from the minor hand
                PPTController.handle_ppt_controls(gest_minor, is_minor_hand=True)

                # Handle gestures for system control
                if gest_minor == Gest.PINCH_MINOR:
                    Controller.handle_controls(gest_minor, self.handminor.hand_result)
                    self.update_status(gest_minor, hand="left")  
                else:
                    Controller.handle_controls(gest_major, self.handmajor.hand_result)
                    self.update_status(gest_major, hand="right")  

                    if gest_minor != Gest.PALM:
                        self.update_status(gest_minor)
                    else:
                        self.update_status(gest_major)

            else:
                # No hands detected
                Controller.prev_hand = None
                self.status_label.config(text="Status: No Hand Detected", foreground="yellow")

            # Update GUI with current frame
            img = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.root.after(10, self.update)  # Schedule the next frame update

    def update_status(self, gesture, hand="right"):
        # Update the status label based on recognized gesture

        if gesture is None:
            return

        status_map = {
            Gest.FIST: "Mouse Drag",
            Gest.PINKY: "Pinky Finger",
            Gest.RING: "Ring Finger",
            Gest.MID: "Left Click",
            Gest.INDEX: "Right Click",
            Gest.THUMB: "Thumb",
            Gest.PALM: "Palm Open",
            Gest.V_GEST: "Move Cursor" if hand == "right" else "Next Slide",
            Gest.TWO_FINGER_CLOSED: "Double Click",
            Gest.PINCH_MAJOR: "Volume/Brightness Control",
            Gest.PINCH_MINOR: "Scroll Control" if hand == "left" else "Unknown Gesture",
            Gest.LAST3: "Draw Mode (3 Fingers Left)",
        }

        try:
            status_text = status_map.get(gesture, "Unknown Gesture")
            self.status_label.config(text=f"Status: {status_text}", foreground="lightgreen")
        except Exception as e:
            print("⚠️ Failed to update status:", e)

    def stop(self):
        # Gracefully stop the camera and release resources
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        self.hands.close()
        self.virtual_keyboard.close()
        self.window.destroy()

    @staticmethod
    def classify_hands(results):
        # Identify which hand is left and which is right
        left, right = None, None
        try:
            handedness_dict = MessageToDict(results.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[0]
            else:
                left = results.multi_hand_landmarks[0]
        except:
            pass

        try:
            handedness_dict = MessageToDict(results.multi_handedness[1])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[1]
            else:
                left = results.multi_hand_landmarks[1]
        except:
            pass

        GestureController.hr_major = right
        GestureController.hr_minor = left
