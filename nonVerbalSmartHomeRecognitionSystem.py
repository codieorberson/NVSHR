import sys
import cv2
import platform
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

        frame = self.rescale_frame(frame, 56, 47) #Rescaling frame with these numbers to fit it in the GUI debug tab
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
    
    def rescale_frame(self, frame, width_frame_percent, height_frame_percent):
        if self.valid_webcam:
            width = int(frame.shape[1] * width_frame_percent/100)
            height = int(frame.shape[0] * height_frame_percent/100)
            dim = (width, height)
            return cv2.resize(frame, dim, interpolation= cv2.INTER_AREA)
        else:
            return frame

    def set_open_eye_threshold(self, new_ear_value):
        self.open_eye_threshold = float(new_ear_value)
        self.database_manager.set_open_eye_threshold(self.open_eye_threshold)

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

        # Close log file.
        self.logger.close()

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
        self.valid_webcam = None

        self.smart_home_activator.set_commands(self.database_manager.get_commands())

    def __set_up_gestures__(self):
        self.gesture_detector.on_gesture(self.gesture_lexer.add)
        self.gesture_detector.on_gesture(self.database_manager.set_gesture)
        self.gesture_detector.on_gesture(self.logger.log_gesture)

    def __set_up_commands__(self):
        self.gesture_parser.on_gesture_sequence(self.logger.log_gesture_sequence)
        self.gesture_parser.on_gesture_sequence(lambda gesture_sequence, timestamp, was_recognised:
                                                self.database_manager.set_gesture_sequence(gesture_sequence,
                                                                                           timestamp, was_recognised))
        self.gesture_parser.on_gesture_sequence(
            lambda gesture_sequence, timestamp, was_recognised: self.smart_home_activator.activate(gesture_sequence,
                                                                                                   was_recognised))
        self.update_commands()

    def __check_camera_resolution__(self):
        ret, frame = self.cap.read()
        if((frame.shape[1]) >= 1280) and ((frame.shape[0]) >=720):
            self.valid_webcam = True
            return True
        else:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
            self.valid_webcam = False
            return False
        
    def __set_up_camera__(self): 
        if platform.system() == 'Windows':
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.cap=cv2.VideoCapture(0) #Not sure if this line or the one two above does the job for Linux
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def __set_up_configuration__(self):
        self.open_eye_threshold = self.database_manager.get_open_eye_threshold()
        self.minimum_time_increment = self.database_manager.get_minimum_time_increment()
        self.maximum_time_increment = self.database_manager.get_maximum_time_increment()

    def __set_up_gui__(self):
        self.gui_manager = GuiManager(self.cap, self.database_manager, self.is_admin, self.__check_camera_resolution__())
        self.__set_up_gui_values__()
        self.__set_up_gui_watchers__()
        self.gui_manager.start(self.main_loop, self.on_close)

    def __set_up_gui_values__(self):
        self.gui_manager.set_initial_ear(self.open_eye_threshold)
        self.gui_manager.set_initial_minimum_time_increment(self.minimum_time_increment)
        self.gui_manager.set_initial_maximum_time_increment(self.maximum_time_increment)

    def __set_up_gui_watchers__(self):
        self.gui_manager.on_ear_change(self.set_open_eye_threshold)
        self.gui_manager.on_minimum_time_increment_change(self.set_minimum_time_increment)
        self.gui_manager.on_maximum_time_increment_change(self.set_maximum_time_increment)
        self.gui_manager.on_new_command(self.add_command)
