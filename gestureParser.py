class GestureParser():
    def __init__(self):
        self.gesture_pattern_map = {}
        self.gesture_sequence_events = []

    def add_pattern(self, gestures):
        self.gesture_pattern_map["".join(gestures)] = True

    def on_gesture_sequence(self, event):
        self.gesture_sequence_events.append(event)

    def parse_pattern(self, gesture_sequence, now):
        joined_gesture_sequence = "".join(gesture_sequence)
        was_recognised = joined_gesture_sequence in self.gesture_pattern_map

        for event in self.gesture_sequence_events:
            event(gesture_sequence, now, was_recognised)

    def parse_patterns(self, gesture_patterns, now):
        for gesture_pattern in gesture_patterns:
            self.parse_pattern(gesture_pattern, now)
