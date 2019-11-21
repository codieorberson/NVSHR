from processManager import ProcessManager
from gesture import Gesture

class HandGestureDetector():
    def __init__(self):
        self.process_manager = ProcessManager()
        self.fist = Gesture("fist.xml")
        self.palm = Gesture("palm.xml")
        
    def detect(self, frame, flipped_frame, has_made_fist, has_made_palm):
        self.process_manager.add_process(
                self.fist.detect_fist, (frame, flipped_frame, has_made_fist))
        self.process_manager.add_process(
                self.palm.detect_palm, (frame, flipped_frame, has_made_palm))
        self.process_manager.on_done()

