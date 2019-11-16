from processManager import ProcessManager
from gesture import Gesture
from frameContrast import FrameContrast

class HandGestureDetector():
    def __init__(self):
        self.process_manager = ProcessManager()
        self.palm_frame = FrameContrast()
        self.fist = Gesture("fist.xml")
        self.palm = Gesture("palm.xml")
        
    def detect(self, frame, palm_low_contrast_frame, palm_high_contrast_frame, has_made_fist, has_made_palm):
        self.new_palm_frame = self.palm_frame.changing_palm_frame(frame, palm_low_contrast_frame, palm_high_contrast_frame)
        self.process_manager.add_process(
                self.fist.detect, (frame, has_made_fist))
        self.process_manager.add_process(
                self.palm.detect, (self.new_palm_frame, has_made_palm))
        self.process_manager.on_done()

