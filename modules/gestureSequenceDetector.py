from gestureDetector import GestureDetector
from gestureLexer import GestureLexer
from gestureParser import GestureParser
from guiManager import GuiManager
from processManager import ProcessManager

class GestureSequenceDetector():
    def __init__(self, logger, database_manager):
        self.__set_up_helpers__(logger, database_manager)
        self.__set_up_gestures__()

    def set_open_eye_threshold(self, new_ear_value):
        self.open_eye_threshold = float(new_ear_value)
        
    def set_low_contrast(self, new_low_contrast):
        self.low_contrast = int(new_low_contrast)

    def set_high_contrast(self, new_high_contrast):
        self.low_contrast = int(new_high_contrast)

    def set_min_time_inc(self, new_min_time_inc):
        self.min_increment = int(new_min_time_inc)

    def set_max_time_inc(self, new_max_time_inc):
        self.max_increment = int(new_max_time_inc)
     
    def on_fist(self, callback):
        self.gesture_detector.on_fist(callback)

    def on_palm(self, callback):
        self.gesture_detector.on_palm(callback)

    def on_blink(self, callback):
        self.gesture_detector.on_blink(callback)


    def get_gesture_detected(self):
        return self.gesture_detector.get_gesture_detected()

    def detect(self, frame, timestamp, open_eye_threshold, minimum_time_increment, maximum_time_increment):
        gesture_sequences = self.gesture_lexer.lex(
                timestamp, minimum_time_increment, maximum_time_increment)

        self.process_manager.add_process(
                self.gesture_parser.parse_patterns, 
                (gesture_sequences, timestamp))

        frame = self.gesture_detector.detect(frame, timestamp, open_eye_threshold)
        self.process_manager.on_done()

        return frame

    def on_gesture_sequence(self, gesture_sequence, callback):
        self.gesture_parser.add_pattern(gesture_sequence, callback)

    def on_recognised_gesture_sequence(self, callback):
        self.gesture_parser.on_recognised_pattern(callback)

    def on_unrecognised_gesture_sequence(self, callback):
        self.gesture_parser.on_unrecognised_pattern(callback)

    def __set_up_helpers__(self, logger, database_manager):
        self.process_manager = ProcessManager()
        self.gesture_detector = GestureDetector()
        self.gesture_lexer = GestureLexer(logger, database_manager)
        self.gesture_parser = GestureParser()

    def __set_up_gestures__(self):
        self.gesture_detector.on_fist(self.gesture_lexer.add_fist)
        self.gesture_detector.on_palm(self.gesture_lexer.add_palm)
        self.gesture_detector.on_blink(self.gesture_lexer.add_blink)
