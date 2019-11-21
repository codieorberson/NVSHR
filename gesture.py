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

    def detect(self, frame, flipped_frame, multithreaded_perimeter, hand_gesture):
        gesture = self.haar_cascade.detectMultiScale(frame, 1.3, 5)
        flipped_gesture = self.haar_cascade.detectMultiScale(flipped_frame, 1.3, 5)
        if self.detection_check(gesture):
            multithreaded_perimeter.set(gesture[0])
        elif self.detection_check(flipped_gesture):
            if hand_gesture == 'fist':
                flipped_gesture = self.detect_flipped_fist(flipped_gesture)
                multithreaded_perimeter.set(flipped_gesture[0])
            elif hand_gesture == 'palm':
                flipped_gesture = self.detect_flipped_palm(flipped_gesture)
                multithreaded_perimeter.set(flipped_gesture[0])

    def detect_flipped_fist(self, flipped_fist):
        flipped_fist[0][0] = 550 - flipped_fist[0][0]
        return(flipped_fist)
    
    def detect_flipped_palm(self, flipped_palm):
        flipped_palm[0][0] = 500 - flipped_palm[0][0]
        return(flipped_palm)
        
