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

        self.fist_perimeter = MultithreadedPerimeter()
        self.palm_perimeter = MultithreadedPerimeter() 
        self.left_eye_perimeter = MultithreadedPerimeter()
        self.right_eye_perimeter = MultithreadedPerimeter()
 
        self.perimeters = [
            self.fist_perimeter, 
            self.palm_perimeter, 
            self.left_eye_perimeter, 
            self.right_eye_perimeter
        ]

        self.gesture_events = []
        self.gestures_detected = []

    def on_gesture(self, callback):
        self.gesture_events.append(callback)

    def get_gestures_detected(self):
        return self.gestures_detected

    def detect(self, frame, timestamp, open_eye_threshold, palm_low_contrast, palm_high_contrast):
        current_frame = frame
        self.__reset_perimeters__()

        self.process_manager.add_process(
                self.hand_gesture_detector.detect, (current_frame, palm_low_contrast, palm_high_contrast, self.fist_perimeter, self.palm_perimeter))

        self.blink_detector.detect(current_frame, self.left_eye_perimeter, self.right_eye_perimeter)

        self.process_manager.on_done()
        self.__trigger_events__(timestamp, open_eye_threshold)
        return self.__draw_rectangles__(frame)

    def __trigger_events__(self, timestamp, open_eye_threshold):
        self.gestures_detected = []

        if self.fist_perimeter.is_set():
            self.gestures_detected.append("fist")

        if self.palm_perimeter.is_set():
            self.gestures_detected.append("palm")
        
        if self.left_eye_perimeter.is_set() and self.right_eye_perimeter.is_set():
            if open_eye_threshold / 100 > (self.left_eye_perimeter.get_ratio() + self.right_eye_perimeter.get_ratio()) / 2:
                self.gestures_detected.append("blink")

        for gesture_name in self.gestures_detected:
            for event in self.gesture_events:
                event(gesture_name, timestamp)

    def __draw_rectangles__(self, frame):
        for perimeter in self.perimeters:
            if perimeter.is_set():
                cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)
                
        return frame

    def __reset_perimeters__(self):
        for perimeter in self.perimeters:
            perimeter.set((0, 0, 0, 0))
