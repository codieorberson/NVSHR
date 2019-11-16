import cv2
import imutils
import numpy as np
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gesture import Gesture
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector

class GestureDetector():
    def __init__(self):
        # Next value not being used right now, but may be in the near future.
        # self.is_black_and_white = False

        self.process_manager = ProcessManager()
        self.hand_gesture_detector = HandGestureDetector()
        self.blink_detector = BlinkDetector()

        self.fist_event = None
        self.palm_event = None
        self.blink_event = None
        self.gesture_detected = None

    def on_fist(self, callback):
        self.fist_event = callback

    def on_palm(self, callback):
        self.palm_event = callback

    def on_blink(self, callback):
        self.blink_event = callback

    def get_gesture_detected(self):
        return self.gesture_detected

    # Method is to be run in separate thread
    def detect(self, frame, palm_low_contrast_frame, palm_high_contrast_frame, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter):

        current_frame = frame

        # Creating two grandchild processes (relative to main.py)
        # First (hand_gesture) will create two more sub-processes while blink will not
        self.process_manager.add_process(
                self.hand_gesture_detector.detect, (current_frame, palm_low_contrast_frame, palm_high_contrast_frame, fist_perimeter, palm_perimeter))
        self.process_manager.add_process(
                self.blink_detector.detect, (current_frame, left_eye_perimeter, right_eye_perimeter))

        # Wait for children to yield control back to this process
        self.process_manager.on_done()

    def trigger_events(self, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter):

        self.gesture_detected = None
        if fist_perimeter.is_set():
            self.gesture_detected = "fist"
            self.fist_event(timestamp)

        if palm_perimeter.is_set():
            self.gesture_detected = "palm"
            self.palm_event(timestamp)
        
        if left_eye_perimeter.is_set() and right_eye_perimeter.is_set():
            if open_eye_threshold / 100 > (left_eye_perimeter.get_ratio() + right_eye_perimeter.get_ratio()) / 2:
                self.gesture_detected = "blink"
                self.blink_event(timestamp)

                self.blink_event(timestamp)