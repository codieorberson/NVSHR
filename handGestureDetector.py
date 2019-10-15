from processManager import ProcessManager
from gesture import Gesture


class HandGestureDetector():
    def __init__(self):
        self.process_manager = ProcessManager()
        self.fist = Gesture("fist.xml")
        self.palm = Gesture("palm.xml")
        self.fist.set_debug_color((0, 0, 255))
        self.palm.set_debug_color((0, 255, 255))

    def detect(self, frame, has_made_fist, has_made_palm):
        self.process_manager.add_process(
                self.fist.detect, (frame, has_made_fist))
        self.process_manager.add_process(
                self.palm.detect, (frame, has_made_palm))
        self.process_manager.on_done()
