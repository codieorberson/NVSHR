class GestureParser():
    def __init__(self):
        self.gesture_pattern_map = {}
        self.recognised_pattern_events = []
        self.unrecognised_pattern_events = []

    def add_pattern(self, gestures, event):
        self.gesture_pattern_map["".join(gestures)] = event
        
    def on_recognised_pattern(self, event):
        self.recognised_pattern_events.append(event)

    def on_unrecognised_pattern(self, event):
        self.unrecognised_pattern_events.append(event)

    def __get_key__(self, gestures):
        key = "".join(gestures)
        if not key in self.gesture_pattern_map.keys():
            self.gesture_pattern_map[key] = {main_event: None, events: []}

        return key

    #Takes in a list of lists of gestures and matches them to any patterns under add_pattern
    #Then sends confirm or failure noise, and logs the sequence in logger.
    def parse_pattern(self, gesture_sequence, now):
        joined_gesture_sequence = "".join(gesture_sequence)

        if joined_gesture_sequence in self.gesture_pattern_map:
            self.gesture_pattern_map[joined_gesture_sequence](now)
            for event in self.recognised_pattern_events:
                event(gesture_sequence, now)
        else:
            for event in self.unrecognised_pattern_events:
                event(gesture_sequence, now)

    def parse_patterns(self, gesture_patterns, now):
        for gesture_pattern in gesture_patterns:
            self.parse_pattern(gesture_pattern, now)
