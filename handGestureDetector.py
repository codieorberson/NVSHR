from gesture import Gesture

class HandGestureDetector():
    def __init__(self):
        self.fist = Gesture("fist.xml")
        self.palm = Gesture("palm.xml")
        self.fist.set_debug_color((0, 0, 255))
        self.palm.set_debug_color((0, 255, 255))

    def on_fist(self, callback):
        self.fist.on_gesture(callback)

    def on_palm(self, callback):
        self.palm.on_gesture(callback)

    def detect(self, frame):
        self.fist.detect(frame)
        self.palm.detect(frame)
        
    def cycle(self):
        self.fist.cycle()
        self.palm.cycle()
