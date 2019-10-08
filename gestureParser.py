class GestureParser():

    def __init__(self, logger):
        self.logger = logger
        self.gesture_pattern_map = {}

    def add_pattern(self, gestures, event):
        self.gesture_pattern_map["".join(gestures)] = event

    def parse_pattern(self, gesture_sequence, now):
        joined_gesture_sequence = "".join(gesture_sequence)
        was_recognised = bool(joined_gesture_sequence in self.gesture_pattern_map)
        '''
        if was_recognised:
            self.gesture_paatern_map[joined_gesture_sequence]()

        if joined_gesture_sequence in self.gesture_pattern_map:
            self.logger.log("Gesture sequence recognised:")
            self.gesture_pattern_map[joined_gesture_sequence]()
        else:
            self.logger.log("Gesture sequence not recognized:")
        '''
        self.logger.log_gesture_sequence(gesture_sequence, now, was_recognised)

    def parse_patterns(self, gesture_patterns, now):
        for gesture_pattern in gesture_patterns:
            self.parse_pattern(gesture_pattern, now)
