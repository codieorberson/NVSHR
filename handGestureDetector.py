from gesture import Gesture

class HandGestureDetector():
    def __init__(self, fist_perimeter, palm_perimeter):
        self.fist = Gesture("fist.xml", fist_perimeter)
        self.palm = Gesture("palm.xml", palm_perimeter)

    def set_fist_low_contrast(self, low_contrast):
        self.fist.set_low_contrast(low_contrast)

    def set_fist_high_contrast(self, high_contrast):
        self.fist.set_high_contrast(high_contrast)

    def toggle_fist_contrast(self, should_be_on):
        self.fist.toggle_contrast(should_be_on)

    def set_palm_low_contrast(self, low_contrast):
        self.palm.set_low_contrast(low_contrast)

    def set_palm_high_contrast(self, high_contrast):
        self.palm.set_high_contrast(high_contrast)

    def toggle_palm_contrast(self, should_be_on):
        self.palm.toggle_contrast(should_be_on)

    def turn_off_palm_contrast(self):
        self.palm.turn_off_contrast()

    def set_view_filter(self, view_filter_name):
        self.view_filter_name = view_filter_name
        
    def detect(self, frame):
        fist_frame = self.fist.detect(frame)
        palm_frame = self.palm.detect(frame)

        if self.view_filter_name == 'fist':
            return self.fist_frame
        elif self.view_filter_name == 'palm':
            return self.palm_frame
        else:
            return frame
