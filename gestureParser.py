class GestureParser():

    def __init__(self):
        self.gesture_pattern_map = {}

    def add_pattern(self, gestures, event):
        self.gesture_pattern_map["".join(gestures)] = event

    def parse(self, gesture_pattern):
        if "".join(gesture_pattern) in self.gesture_pattern_map:
            print("Gesture recognized.")
            self.gesture_pattern_map["".join(gesture_pattern)]()
        else:
            print("Gesture pattern not recognized: " + str(gesture_pattern))
