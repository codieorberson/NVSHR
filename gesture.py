import cv2

class Gesture():
    def __init__(self, haar_cascade_xml, 
            detection_check = lambda detected_gestures: len(detected_gestures) > 0, 
            debug_color = (0, 0, 255)):
        self.haar_cascade = cv2.CascadeClassifier(haar_cascade_xml)
        self.detection_check = detection_check
        self.debug_color = debug_color

    def set_debug_color(self, rgb_tuple):
        self.debug_color = rgb_tuple

    def set_detection_criteria(self, detection_check):
        self.detection_check = detection_check

    def detect(self, frame, multithreaded_perimeter):
        gestures = self.haar_cascade.detectMultiScale(frame, 1.3, 5)

        if self.detection_check(gestures):
            multithreaded_perimeter.set(gestures[0])

#            for (x,y,w,h) in gestures:
#                cv2.rectangle(frame, (x,y), (x+w,y+h), self.debug_color, 2)
