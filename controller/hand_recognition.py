import math
from enum import IntEnum
from google.protobuf.json_format import MessageToDict
import mediapipe as mp

# Enum for different hand gesture identifiers
class Gest(IntEnum):
    FIST = 0
    PINKY = 1
    RING = 2
    MID = 4
    LAST3 = 7
    INDEX = 8
    FIRST2 = 12
    LAST4 = 15
    THUMB = 16
    PALM = 31
    V_GEST = 33
    TWO_FINGER_CLOSED = 34
    PINCH_MAJOR = 35
    PINCH_MINOR = 36

# Enum to label hand as MINOR (left) or MAJOR (right)
class HLabel(IntEnum):
    MINOR = 0  
    MAJOR = 1  

# Class for recognizing gestures from hand landmarks
class HandRecog:

    def __init__(self, hand_label):
        # Initialize hand recognition state
        self.finger = 0
        self.ori_gesture = Gest.PALM
        self.prev_gesture = Gest.PALM
        self.frame_count = 0
        self.hand_result = None
        self.hand_label = hand_label

    def update_hand_result(self, hand_result):
        # Update the detected hand landmark results
        self.hand_result = hand_result

    def get_signed_dist(self, point):
        # Calculate signed Euclidean distance between two landmarks in 2D
        sign = -1
        if self.hand_result.landmark[point[0]].y < self.hand_result.landmark[point[1]].y:
            sign = 1
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist * sign

    def get_dist(self, point):
        # Calculate Euclidean distance between two landmarks in 2D
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist

    def get_dz(self, point):
        # Calculate absolute depth (z-axis) difference between two landmarks
        return abs(self.hand_result.landmark[point[0]].z - self.hand_result.landmark[point[1]].z)

    def set_finger_state(self):
        # Analyze finger states based on landmark positions
        if self.hand_result is None:
            return

        # Indexes for each finger's tip and joint
        points = [[8, 5, 0], [12, 9, 0], [16, 13, 0], [20, 17, 0]]
        self.finger = 0
        self.finger = self.finger | 0 

        for idx, point in enumerate(points):
            dist = self.get_signed_dist(point[:2])
            dist2 = self.get_signed_dist(point[1:])

            try:
                ratio = round(dist / dist2, 1)
            except:
                ratio = round(dist / 0.01, 1)  # Avoid division by zero

            self.finger = self.finger << 1
            if ratio > 0.5:
                self.finger = self.finger | 1  # Mark finger as open

    def get_gesture(self):
        # Determine the gesture based on finger state and landmark distances
        if self.hand_result is None:
            return Gest.PALM

        current_gesture = Gest.PALM

        # Detect pinch gesture
        if self.finger in [Gest.LAST3, Gest.LAST4] and self.get_dist([8, 4]) < 0.05:
            if self.hand_label == HLabel.MINOR:
                current_gesture = Gest.PINCH_MINOR
            else:
                current_gesture = Gest.PINCH_MAJOR

        # Detect V gesture or two fingers closed
        elif Gest.FIRST2 == self.finger:
            point = [[8, 12], [5, 9]]
            dist1 = self.get_dist(point[0])
            dist2 = self.get_dist(point[1])
            ratio = dist1 / dist2

            if ratio > 1.7:
                current_gesture = Gest.V_GEST
            else:
                if self.get_dz([8, 12]) < 0.1:
                    current_gesture = Gest.TWO_FINGER_CLOSED
                else:
                    current_gesture = Gest.MID

        else:
            current_gesture = self.finger  # Map finger pattern to gesture

        # Confirm gesture stability across frames
        if current_gesture == self.prev_gesture:
            self.frame_count += 1
        else:
            self.frame_count = 0

        self.prev_gesture = current_gesture

        # Accept gesture if it remains consistent for multiple frames
        if self.frame_count > 4:
            self.ori_gesture = current_gesture

        return self.ori_gesture
