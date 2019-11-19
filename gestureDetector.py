import cv2
import imutils
from multithreadedPerimeter import MultithreadedPerimeter
from gesture import Gesture
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector

class GestureDetector():
    def __init__(self):
        self.__set_up_perimeters__()
        self.__set_up_helpers__()
        self.gesture_events = []
        self.gestures_detected = []

    def on_gesture(self, callback):
        self.gesture_events.append(callback)

    def set_palm_low_contrast(self, low_contrast):
        self.hand_gesture_detector.set_palm_low_contrast(low_contrast)

    def set_palm_high_contrast(self, low_contrast):
        self.hand_gesture_detector.set_palm_high_contrast(low_contrast)

    def toggle_palm_contrast(self, should_be_on):
        self.hand_gesture_detector.toggle_palm_contrast(should_be_on)

    def set_fist_low_contrast(self, low_contrast):
        self.hand_gesture_detector.set_fist_low_contrast(low_contrast)

    def set_fist_high_contrast(self, low_contrast):
        self.hand_gesture_detector.set_fist_high_contrast(low_contrast)

    def toggle_fist_contrast(self, should_be_on):
        self.hand_gesture_detector.toggle_fist_contrast(should_be_on)

    def set_open_eye_threshold(self, open_eye_threshold):
        self.open_eye_threshold = open_eye_threshold

    def get_gestures_detected(self):
        return self.gestures_detected

    def set_view_filter(self, view_filter_name):
        self.view_filter_name = view_filter_name
        self.hand_gesture_detector.set_view_filter(view_filter_name)

    def detect(self, frame, timestamp):
        frame_map = {}
        current_frame = frame
        self.__reset_perimeters__()
        hand_frame = self.hand_gesture_detector.detect(current_frame)
        blink_frame = self.blink_detector.detect(current_frame, self.left_eye_perimeter, self.right_eye_perimeter)

        self.__trigger_events__(timestamp)
        if self.view_filter_name == "blink":
            current_frame = blink_frame
        elif self.view_filter_name == 'fist' or self.view_filter_name == 'palm':
            current_frame = hand_frame
        return self.__draw_rectangles__(frame)

    def __trigger_events__(self, timestamp):
        self.gestures_detected = []

        if self.fist_perimeter.is_set():
            self.gestures_detected.append("fist")

        if self.palm_perimeter.is_set():
            self.gestures_detected.append("palm")
        
        if self.left_eye_perimeter.is_set() and self.right_eye_perimeter.is_set():
            if self.open_eye_threshold / 100 > (self.left_eye_perimeter.get_ratio() + self.right_eye_perimeter.get_ratio()) / 2:
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

    def __set_up_perimeters__(self):
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

    def __set_up_helpers__(self):
        self.hand_gesture_detector = HandGestureDetector(self.fist_perimeter, self.palm_perimeter)
        self.blink_detector = BlinkDetector()
