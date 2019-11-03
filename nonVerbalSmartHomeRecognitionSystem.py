from datetime import datetime

import cv2

from adminCmdManager import AdminCmdManager
from databaseManager import DatabaseManager
from gestureDetector import GestureDetector
from gestureLexer import GestureLexer
from gestureParser import GestureParser
from guiManager import GuiManager
from logger import Logger
from multithreadedPerimeter import MultithreadedPerimeter
from popUp import PopUp
from processManager import ProcessManager
from smartHomeActivator import SmartHomeActivator


class NonVerbalSmartHomeRecognitionSystem():
    def __init__(self):

        # I'm not sure that we need the following code, but it isn't working on
        # muh Linux box so I'm commenting it out right now and just setting the
        # admin value to True.

        # print("Are you an admin?\n 1. Yes\n 2. No")
        # self.admin = input()
        self.pop_up_window = PopUp()
        self.admin = self.pop_up_window.send_verification()
        # self.admin = True

        self.last_timestamp = datetime.utcnow()
        self.logger = Logger()
        self.gesture_detector = GestureDetector()
        self.gesture_lexer = GestureLexer(self.logger)
        self.gesture_parser = GestureParser(self.logger)
        self.gesture_detected = None
        self.AdminSettingsManager = AdminCmdManager()
        # self.AdminSettingsManager.read_from_file()

        self.gesture_detector.on_fist(lambda timestamp: self.gesture_lexer.add("fist", timestamp))
        self.gesture_detector.on_palm(lambda timestamp: self.gesture_lexer.add("palm", timestamp))
        self.gesture_detector.on_blink(lambda timestamp: self.gesture_lexer.add("blink", timestamp))
        
        self.smart_home_activator = SmartHomeActivator()
#    This is a test pattern to find in a gesture sequence. The gesture sequence 
#    being detected as a pattern must be made up of strings which correspond to the
#    strings passed into self.gesture_lexer.add in the anonymous lambdas above.
        self.gesture_parser.add_pattern(['fist', 'palm', 'blink'],
                                        lambda: self.smart_home_activator.activate('lights on', 'Alexa'))
        self.gesture_parser.add_pattern(['palm', 'fist', 'blink'],
                                        lambda: self.smart_home_activator.activate('lights off', 'Alexa'))
        self.gesture_parser.add_pattern(['fist', 'blink', 'palm'],
                                        lambda: self.smart_home_activator.activate('AC on', 'Alexa'))
        self.gesture_parser.add_pattern(['palm', 'blink', 'fist'],
                                        lambda: self.smart_home_activator.activate('AC off', 'Alexa'))

        self.gesture_parser.add_pattern(['fist', 'palm', 'blink'], lambda: self.smart_home_activator.activate('Lights on/off', 'Alexa'))
        self.gesture_parser.add_pattern(['palm', 'fist', 'blink'], lambda: self.smart_home_activator.activate('Smart Plug on/off', 'Alexa'))
        self.gesture_parser.add_pattern(['fist', 'blink', 'palm'], lambda: self.smart_home_activator.activate('Heat on/off', 'Alexa'))
        self.gesture_parser.add_pattern(['palm', 'blink', 'fist'], lambda: self.smart_home_activator.activate('AC on/off', 'Alexa'))
        self.gesture_parser.add_pattern(['palm'], lambda: self.smart_home_activator.activate('STOP', 'Alexa')) 

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

        self.process_manager = ProcessManager()
        self.database_manager = DatabaseManager()

        self.open_eye_threshold = self.database_manager.get_open_eye_threshold()
        self.low_contrast_value = self.database_manager.get_low_contrast()
        self.high_contrast_value = self.database_manager.get_high_contrast()
        self.min_increment = self.database_manager.get_min_time_inc()
        self.max_increment = self.database_manager.get_max_time_inc()

        self.gui_manager = GuiManager(self.cap,
                                      self.set_open_eye_threshold, self.open_eye_threshold,
                                      self.set_low_contrast, self.low_contrast_value,
                                      self.set_high_contrast, self.high_contrast_value,
                                      self.set_min_time_inc, self.min_increment,
                                      self.set_max_time_inc, self.max_increment,
                                      self.gesture_detected, self.admin)

        self.gui_manager.start(self.main_loop, self.on_close)
     
    def main_loop(self):
        ret, frame = self.cap.read()

        timestamp = datetime.utcnow()
        self.fps = str(1/((timestamp - self.last_timestamp).microseconds/1000000))[:4]

#    These multithreaded perimeters are the only objects which hold values that
#    are shared between threads. The frame, for example, is copied for each 
#    core in the processor, and drawing on a frame inside of a child process
#    will not affect the original frame in the parent process. Checking for
#    changes in the values held by multithreaded perimeters is the only way
#    that the code currently communicates from a child process to a parent
#    process (besides returning control via ProcessManager).
        fist_perimeter = MultithreadedPerimeter()
        palm_perimeter = MultithreadedPerimeter()
        left_eye_perimeter = MultithreadedPerimeter()
        right_eye_perimeter = MultithreadedPerimeter()

        # Aggregates gestures into gesture sequences.
        gesture_sequences = self.gesture_lexer.lex(
                timestamp, self.min_increment, self.max_increment)

        # Creates a child process to check for predefined patterns of gestures in the list of gesture sequences
        self.process_manager.add_process(
                self.gesture_parser.parse_patterns, 
                (gesture_sequences, timestamp))

        self.process_manager.add_process(
                self.gesture_detector.detect, (frame, timestamp, self.open_eye_threshold, fist_perimeter,
                palm_perimeter, left_eye_perimeter, right_eye_perimeter))

        self.process_manager.on_done()

        self.gesture_detector.trigger_events(
                timestamp, self.open_eye_threshold, fist_perimeter, 
                palm_perimeter, left_eye_perimeter, right_eye_perimeter)

        # Drawing rectangles around identified gestures and eyes
        for perimeter in [fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter]:
            if perimeter.is_set():
                cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)

        self.gui_manager.set_fps(self.fps)
        self.gui_manager.set_debug_frame(cv2.flip(frame, 1))
        self.last_timestamp = timestamp
        self.gesture_detected = self.gesture_detector.get_gesture_detected()
        self.gui_manager.set_gesture_background(self.gesture_detected)

    def set_open_eye_threshold(self, new_ear_value):
        self.open_eye_threshold = float(new_ear_value)
        self.database_manager.set_open_eye_threshold(self.open_eye_threshold)
        
    def set_low_contrast(self, new_low_contrast):
        self.database_manager.set_low_contrast(int(new_low_contrast))

    def set_high_contrast(self, new_high_contrast):
        self.database_manager.set_high_contrast(int(new_high_contrast))

    def set_min_time_inc(self, new_min_time_inc):
        self.min_increment = int(new_min_time_inc)
        self.database_manager.set_min_time_inc(new_min_time_inc)

    def set_max_time_inc(self, new_max_time_inc):
        self.max_increment = int(new_max_time_inc)
        self.database_manager.set_max_time_inc(new_max_time_inc)

    def on_close(self):
        # Close down OpenCV
        self.cap.release()
        cv2.destroyAllWindows()

        # Close the GUI
        self.gui_manager.destroy_gui()

        # Close log file
        self.logger.close() 
        self.database_manager.close()
