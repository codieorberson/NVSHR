from gesture import Gesture

class HandGestureDetector():
    def __init__(self):
        self.has_made_left_wink = False
        self.has_made_right_wink = False

        self.left_wink_callback = None
        self.right_wink_callback = None

        face_cascade = cv2.CascadeClassifier('face.xml')
        eye_cascade = cv2.CascadeClassifier('eye.xml')

#        self.left_wink = Gesture("eye.xml")
#        self.right_wink = Gesture("eye.xml")
#        self.fist.set_debug_color((0, 0, 255))
#        self.palm.set_debug_color((0, 255, 255))

    def on_left_wink(self, callback):
        self.left_wink_callback = callback

    def on_right_wink(self, callback):
        self.right_wink_callback = callback

    def detect(self, frame):
        self.fist.detect(frame)
        self.palm.detect(frame)
        
    def cycle(self):

        if self.has_made_left_wink and self.left_wink_callback:
            self.left_wink_callback()
            self.has_made_left_wink = False

        if self.has_made_right_wink and self.right_wink_callback:
            self.right_wink_callback()
            self.has_made_right_wink = False
