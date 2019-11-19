import cv2
from datetime import datetime
from databaseManager import DatabaseManager
from gestureDetector import GestureDetector
from gestureLexer import GestureLexer
from gestureParser import GestureParser
from guiManager import GuiManager
from logger import Logger
from processManager import ProcessManager
from smartHomeActivator import SmartHomeActivator

class NonVerbalSmartHomeRecognitionSystem():
    def __init__(self):
        self.__set_up_helpers__()
        self.__set_up_gestures__()
        self.__set_up_commands__()
        self.__set_up_camera__()
        self.__set_up_configuration__()
        self.__set_up_gui__()

    def main_loop(self):
        ret, frame = self.cap.read()
        timestamp = datetime.utcnow()

        # Aggregates gestures into gesture sequences.
        gesture_sequences = self.gesture_lexer.lex(
            timestamp, self.minimum_time_increment, self.maximum_time_increment)

        # Creates a child process to check for predefined patterns of gestures in the list of gesture sequences
        self.process_manager.add_process(
                self.gesture_parser.parse_patterns, 
                (gesture_sequences, timestamp))

        frame = self.gesture_detector.detect(frame, timestamp, self.open_eye_threshold)

        self.process_manager.on_done()

        self.gui_manager.set_debug_frame(cv2.flip(frame, 1))
        self.gesture_detected = self.gesture_detector.get_gesture_detected()
        self.gui_manager.set_gesture_background(self.gesture_detected)

        new_log_line = self.logger.get_output()
        if self.gesture_detected != None:
            self.gui_manager.update_log_text(new_log_line)

        self.update_commands()

    def set_open_eye_threshold(self, new_ear_value):
        self.open_eye_threshold = float(new_ear_value)
        self.database_manager.set_open_eye_threshold(self.open_eye_threshold)
        
    def set_low_contrast(self, new_low_contrast):
        self.database_manager.set_low_contrast(int(new_low_contrast))

    def set_high_contrast(self, new_high_contrast):
        self.database_manager.set_high_contrast(int(new_high_contrast))

    def set_minimum_time_increment(self, new_minimum_time_increment):
        self.minimum_time_increment = int(new_minimum_time_increment)
        self.database_manager.set_minimum_time_increment(new_minimum_time_increment)

    def set_maximum_time_increment(self, new_maximum_time_increment):
        self.maximum_time_increment = int(new_maximum_time_increment)
        self.database_manager.set_maximum_time_increment(new_maximum_time_increment)

    def add_command(self, gesture_sequence, command_text, device_name):
        self.gesture_parser.add_pattern(gesture_sequence)
        self.database_manager.set_command(gesture_sequence, command_text, device_name)
        commands = self.database_manager.get_commands()
        self.smart_home_activator.set_commands(commands)

    def update_commands(self):
        for command_map in self.database_manager.get_commands():
            self.add_command(command_map['gesture_sequence'],
                             command_map['command_text'],
                             command_map['device_name'])

    def on_close(self):
        # Close down OpenCV
        self.cap.release()
        cv2.destroyAllWindows()

        # Close the GUI
        self.gui_manager.destroy_gui()

        # Close log file
        self.logger.close()

    def __set_up_pop_up__(self):
        self.pop_up_window = PopUp()
        self.is_admin = self.pop_up_window.send_verification()

    def __set_up_helpers__(self):
        self.is_admin = True
        self.database_manager = DatabaseManager()
        self.logger = Logger()
        self.smart_home_activator = SmartHomeActivator()
        self.gesture_detector = GestureDetector()
        self.gesture_lexer = GestureLexer()
        self.gesture_parser = GestureParser()
        self.gesture_detected = None
        self.process_manager = ProcessManager()

        self.smart_home_activator.set_commands(self.database_manager.get_commands())

    def __set_up_gestures__(self):
        self.gesture_detector.on_gesture(self.gesture_lexer.add)
        self.gesture_detector.on_gesture(self.database_manager.set_gesture)
        self.gesture_detector.on_gesture(self.logger.log_gesture)

    def __set_up_commands__(self):
        self.gesture_parser.on_gesture_sequence(self.logger.log_gesture_sequence)
        self.gesture_parser.on_gesture_sequence(
            lambda gesture_sequence, timestamp, was_recognised: self.smart_home_activator.activate(gesture_sequence,
                                                                                                   was_recognised))
        self.update_commands()

    def __set_up_camera__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    def __set_up_configuration__(self):
        self.open_eye_threshold = self.database_manager.get_open_eye_threshold()
        self.low_contrast_value = self.database_manager.get_low_contrast()
        self.high_contrast_value = self.database_manager.get_high_contrast()
        self.minimum_time_increment = self.database_manager.get_minimum_time_increment()
        self.maximum_time_increment = self.database_manager.get_maximum_time_increment()

    def __set_up_gui__(self):
        self.gui_manager = GuiManager(self.cap, self.database_manager, self.is_admin)
        self.__set_up_gui_values__()
        self.__set_up_gui_watchers__()
        self.gui_manager.start(self.main_loop, self.on_close)

    def __set_up_gui_values__(self):
        self.gui_manager.set_initial_ear(self.open_eye_threshold)
        self.gui_manager.set_initial_low_contrast(self.low_contrast_value)
        self.gui_manager.set_initial_high_contrast(self.high_contrast_value)
        self.gui_manager.set_initial_minimum_time_increment(self.minimum_time_increment)
        self.gui_manager.set_initial_maximum_time_increment(self.maximum_time_increment)

    def __set_up_gui_watchers__(self):
        self.gui_manager.on_ear_change(self.set_open_eye_threshold)
        self.gui_manager.on_low_contrast_change(self.set_low_contrast)
        self.gui_manager.on_high_contrast_change(self.set_high_contrast)
        self.gui_manager.on_minimum_time_increment_change(self.set_minimum_time_increment)
        self.gui_manager.on_maximum_time_increment_change(self.set_maximum_time_increment)
        self.gui_manager.on_new_command(self.add_command)
