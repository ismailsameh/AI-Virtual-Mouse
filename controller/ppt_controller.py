import pyautogui
from controller.hand_recognition import Gest
import time

class PPTController:
    # Timestamp to prevent repeated gesture actions in short time
    last_action_time = 0

    @staticmethod
    def handle_ppt_controls(gesture, is_minor_hand):

        # Only allow control via the minor hand (usually left)
        if not is_minor_hand:
            return

        current_time = time.time()
        # Prevent triggering multiple times in less than 1 second
        if current_time - PPTController.last_action_time < 1.0:
            return 

        PPTController.last_action_time = current_time

        # Map gestures to PowerPoint controls
        if gesture == Gest.PINKY:
            pyautogui.press('f5')  # Start presentation

        elif gesture == Gest.FIST:
            pyautogui.press('esc')  # Exit presentation

        elif gesture == Gest.V_GEST:
            pyautogui.press('right')  # Next slide

        elif gesture == Gest.INDEX:
            pyautogui.press('left')  # Previous slide
