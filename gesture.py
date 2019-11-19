import cv2
from contrastManager import ContrastManager

class Gesture():
    def __init__(self, haar_cascade_xml, multithreaded_perimeter, 
            detection_check = lambda detected_gestures: len(detected_gestures) > 0, 
            debug_color = (0, 0, 255)):
        self.haar_cascade = cv2.CascadeClassifier(haar_cascade_xml)
        self.multithreaded_perimeter = multithreaded_perimeter
        self.detection_check = detection_check
        self.debug_color = debug_color
        self.contrast_manager = ContrastManager()

    def set_debug_color(self, rgb_tuple):
        self.debug_color = rgb_tuple

    def set_low_contrast(self, low_contrast):
        self.contrast_manager.set_low_contrast(low_contrast)

    def set_high_contrast(self, high_contrast):
        self.contrast_manager.set_high_contrast(high_contrast)

    def toggle_contrast(self, should_be_on):
        self.contrast_manager.toggle_contrast(should_be_on)

    def set_detection_criteria(self, detection_check):
        self.detection_check = detection_check

    def detect(self, frame):
        frame = self.contrast_manager.apply_contrast(frame)
        gestures = self.haar_cascade.detectMultiScale(frame, 1.3, 5)

        if self.detection_check(gestures):
            self.multithreaded_perimeter.set(gestures[0])

        return frame
