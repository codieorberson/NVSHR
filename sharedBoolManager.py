from multiprocessing import Value
from sharedBool import SharedBool

class SharedBoolManager():
    def __init__(self):
        self.has_made_fist = SharedBool()
        self.has_made_palm = SharedBool()
        self.has_made_blink = SharedBool()
        self.has_made_left_wink = SharedBool()
        self.has_made_right_wink = SharedBool()

    def get_fist(self):
        return self.has_made_fist
 
    def get_palm(self):
        return self.has_made_palm

    def get_blink(self):
        return self.has_made_blink
 
    def get_left_wink(self):
        return self.has_made_left_wink
 
    def get_right_wink(self):
        return self.has_made_right_wink
