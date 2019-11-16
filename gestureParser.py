from smartHomeActivator import SmartHomeActivator

class GestureParser():
    def __init__(self, logger, database_manager):
        self.logger = logger
        self.gesture_pattern_map = {}
        self.smart_Home_Activator = SmartHomeActivator(database_manager)

    def add_pattern(self, gestures, event):
        self.gesture_pattern_map["".join(gestures)] = event

    # Takes in a list of lists of gestures and matches them to any patterns under add_pattern
    # Then sends confirm or failure noise, and logs the sequence in logger.
    def parse_pattern(self, gesture_sequence, now):
        joined_gesture_sequence = "".join(gesture_sequence)
        was_recognized = bool(
            joined_gesture_sequence in self.gesture_pattern_map)
        self.logger.log_gesture_sequence(gesture_sequence, now, was_recognized)

        if was_recognized: 
            self.gesture_pattern_map[joined_gesture_sequence]()

        self.smart_Home_Activator.activate(gesture_sequence, was_recognized)

    def parse_patterns(self, gesture_patterns, now):
        for gesture_pattern in gesture_patterns:
            self.parse_pattern(gesture_pattern, now)

