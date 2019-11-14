import cv2
from datetime import datetime
from processManager import ProcessManager
from gestureSequenceDetector import GestureSequenceDetector
from commandManager import CommandManager
from dataManager import DataManager
from logger import Logger
from popUp import PopUp
from guiManager import GuiManager
from smartHomeActivator import SmartHomeActivator
from soundPlayer import SoundPlayer

class NonVerbalSmartHomeRecognitionSystem():
    def __init__(self):
        self.__set_up_helpers__()
        self.__set_up_commands__()    
        self.__set_up_camera__()
        self.__set_up_configuration__()
        self.__set_up_admin_gui__()
        self.__set_up_pop_up__()

    def change_admin_status(self):
        self.gui_manager.start_foreground_process(self.main_loop, self.on_close)
     
    def main_loop(self):
        ret, frame = self.cap.read()

        timestamp = datetime.utcnow()
        self.fps = str(1/((timestamp - self.last_timestamp).microseconds/1000000))[:4]

        frame = self.gesture_sequence_detector.detect(frame, timestamp, self.open_eye_threshold, self.min_increment, self.max_increment)

        self.gui_manager.set_fps(self.fps)
        self.gui_manager.set_debug_frame(cv2.flip(frame, 1))
        self.gui_manager.set_gesture_background(self.gesture_sequence_detector.get_gesture_detected())
        self.last_timestamp = timestamp

    def set_open_eye_threshold(self, new_ear_value):
        self.open_eye_threshold = float(new_ear_value)
        self.data_manager.set_open_eye_threshold(self.open_eye_threshold)
        
    def set_low_contrast(self, new_low_contrast):
        self.data_manager.set_low_contrast(int(new_low_contrast))

    def set_high_contrast(self, new_high_contrast):
        self.data_manager.set_high_contrast(int(new_high_contrast))

    def set_min_time_inc(self, new_min_time_inc):
        self.min_increment = int(new_min_time_inc)
        self.data_manager.set_min_time_inc(new_min_time_inc)

    def set_max_time_inc(self, new_max_time_inc):
        self.max_increment = int(new_max_time_inc)
        self.data_manager.set_max_time_inc(new_max_time_inc)

    def add_command(self, gesture_sequence, command_text, device_name):
#        self.gui_manager.add_command(gesture_sequence, command_text, device_name)
        self.gesture_sequence_detector.on_gesture_sequence(gesture_sequence, 
                self.__bind_smart_home_activation__(command_text, device_name))
        self.data_manager.set_command(gesture_sequence, command_text, device_name)

    def on_close(self):
        # Close down OpenCV
        self.cap.release()
        cv2.destroyAllWindows()

        # Close the GUI
        self.gui_manager.destroy_gui()

        # Close log file
        self.logger.close() 
        self.data_manager.close()

    def __set_up_helpers__(self):
        self.process_manager = ProcessManager()
        self.last_timestamp = datetime.utcnow()
        self.data_manager = DataManager()
        self.logger = Logger()
        self.gesture_sequence_detector = GestureSequenceDetector(self.logger, self.data_manager)
        self.command_manager = CommandManager()
        self.smart_home_activator = SmartHomeActivator()
        self.sound_player = SoundPlayer()

        self.gesture_sequence_detector.on_fist(self.logger.log_fist)
        self.gesture_sequence_detector.on_palm(self.logger.log_palm)
        self.gesture_sequence_detector.on_blink(self.logger.log_blink)

        self.gesture_sequence_detector.on_recognised_gesture_sequence(self.__on_recognised_gesture_sequence__)
        
        self.gesture_sequence_detector.on_unrecognised_gesture_sequence(self.__on_unrecognised_gesture_sequence__)
 
    def __set_up_commands__(self):
        for command_map in self.data_manager.get_commands():
            self.add_command(command_map['gesture_sequence'],
                    command_map['command_text'],
                    command_map['device_name'])

    def __set_up_camera__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    def __set_up_configuration__(self):
        self.open_eye_threshold = self.data_manager.get_open_eye_threshold()
        self.low_contrast_value = self.data_manager.get_low_contrast()
        self.high_contrast_value = self.data_manager.get_high_contrast()
        self.min_increment = self.data_manager.get_min_time_inc()
        self.max_increment = self.data_manager.get_max_time_inc()

    def __set_up_admin_gui__(self):
        self.gui_manager = GuiManager(self.cap, self.command_manager)
        self.__set_up_gui_values__()
        self.__set_up_gui_watchers__()
        self.gui_manager.start_background_process()

    def __set_up_gui_values__(self):
        self.gui_manager.set_initial_ear(self.open_eye_threshold)
        self.gui_manager.set_initial_low_contrast(self.low_contrast_value)
        self.gui_manager.set_initial_high_contrast(self.high_contrast_value)
        self.gui_manager.set_initial_minimum_time_increment(self.min_increment)
        self.gui_manager.set_initial_maximum_time_increment(self.max_increment)

    def __set_up_gui_watchers__(self): 
        self.gui_manager.on_ear_change(self.set_open_eye_threshold)
        self.gui_manager.on_low_contrast_change(self.set_low_contrast)
        self.gui_manager.on_high_contrast_change(self.set_high_contrast)
        self.gui_manager.on_minimum_time_increment_change(self.set_min_time_inc)
        self.gui_manager.on_maximum_time_increment_change(self.set_max_time_inc)
        self.gui_manager.on_new_command(self.add_command)
   
    def __set_up_pop_up__(self):
        self.pop_up_window = PopUp(self.main_loop, self.change_admin_status, self.on_close)
        self.pop_up_window.start()

    def __on_recognised_gesture_sequence__(self, gestures, timestamp):
        self.logger.log_gesture_sequence(gestures, timestamp, True)

    def __on_unrecognised_gesture_sequence__(self, gestures, timestamp):
        self.sound_player.play_failure_sound()
        self.logger.log_gesture_sequence(gestures, timestamp, False)

    def __bind_smart_home_activation__(self, command_text, device_name):
        return lambda now: self.smart_home_activator.activate(command_text, device_name)
