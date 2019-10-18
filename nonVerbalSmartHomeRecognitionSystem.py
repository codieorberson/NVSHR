import sys
import cv2
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from guiManager import GuiManager
from logger import Logger
from dataManager import DataManager
from gestureDetector import GestureDetector
from gestureLexer import GestureLexer
from gestureParser import GestureParser
from smartHomeActivator import SmartHomeActivator

class NonVerbalSmartHomeRecognitionSystem():
    def __init__(self):
        self.logger = Logger()
        self.gesture_detector = GestureDetector()
        self.gesture_lexer = GestureLexer(self.logger)
        self.gesture_parser = GestureParser(self.logger)

#The first command line argument determines the minimum time needed between
#     identical gestures for them to be considered separate gestures in a pattern.
        if len(sys.argv) > 1:
            self.min_increment = float(sys.argv[1])
        else:
            self.min_increment = 2
     
#     The second command line argument determines the maximum time that can lapse
#     without a gesture before gestures are collected into a gesture pattern.
        if len(sys.argv) > 2:
            self.max_increment = float(sys.argv[2])
        else:
            self.max_increment = 5
     
#     Add three callbacks to self.gesture_detector. These anonymous functions (also known
#    as lambdas) take a timestamp and tell self.gesture_lexer to record a gesture at
#    that time. The particular sort of gesture passed is indicated by a string.
#    These anonymous functions will not actually pass any values into
#    self.gesture_lexer.add right now, the lambdas will only execute when
#    when self.gesture_detector tells them to.
        self.gesture_detector.on_fist(lambda timestamp: self.gesture_lexer.add("fist", timestamp))
        self.gesture_detector.on_palm(lambda timestamp: self.gesture_lexer.add("palm", timestamp))
        self.gesture_detector.on_blink(lambda timestamp: self.gesture_lexer.add("blink", timestamp))
     
        self.smart_home_activator = SmartHomeActivator()

#    This is a test pattern to find in a gesture sequence. The gesture sequence 
#    being detected as a pattern must be made up of strings which correspond to the
#    strings passed into self.gesture_lexer.add in the anonymous lambdas above.
        self.gesture_parser.add_pattern(['fist', 'palm', 'fist'], lambda: self.smart_home_activator.activate('lights on (not really)', 'Alexa'))
      
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
                
     
#    This process manager is what spawns child processes and returns control to the
#    parent process when they all finish. All of the multithreaded logic is
#    contained in ProcessManager and MultithreadedPerimeter. You'll see a
#    demonstration of them being used together shortly.
        self.process_manager = ProcessManager()
        self.data_manager = DataManager()
        self.open_eye_threshold = self.data_manager.get_open_eye_threshold()
        self.gui_manager = GuiManager(self.cap, self.set_open_eye_threshold, self.open_eye_threshold)
#        self.gui_manager.on_ear_change(lambda x: print(x))#self.set_open_eye_threshold)
        self.gui_manager.start(self.main_loop, self.on_close)
     
    def main_loop(self):
        ret, frame = self.cap.read()
        timestamp = datetime.now()
     
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
     
#     This line aggregates gestures into gesture sequences.
        gesture_sequences = self.gesture_lexer.lex(
                timestamp, self.min_increment, self.max_increment)
     
#     This line creates a child process to check for predefined patterns of
#     gestures in the list of gesture sequences we just aggregated. The child
#     process gets added to the thread pool, but we don't know exactly when it
#     will start executing.
        self.process_manager.add_process(
                self.gesture_parser.parse_patterns, 
                (gesture_sequences, timestamp))
     
#     This line spawns another child process, this time telling self.gesture_detector
#     to find gestures in the current frame. We pass the frame in for detection,
#     but we won't be drawing to it in GestureDetector. GestureDetector will
#     spawn a bunch of child processes of it's own, and those will be passed
#     the MultithreadedPerimeters. Those grandchild (and great-grandchild) 
#     processes will set the values contained in the multithreaded perimeter if
#     they detect the relevant gestures. 
#     (Side note -- if we want to display the frame using the same filters used
#     for detection, we should apply those filters before this point. Currently
#     that is done in GestureDetector, and we display the frame as self.captured.)
        self.process_manager.add_process(
                self.gesture_detector.detect, 
                (frame, timestamp, self.open_eye_threshold, fist_perimeter, 
                palm_perimeter, left_eye_perimeter, right_eye_perimeter))
     
#     The child processes may or may not have started by now. Calling on_done
#     will make the current process cede control until all of the subprocesses
#     are finished executing.
        self.process_manager.on_done()
#     Now we are gauranteed that those subprocesses are finished operating on
#     the MultithreadedPerimeter instances.
     
#     I separated out the callback triggers so that they could be run 
#     synchronously after the subprocess were finished. This allows lots of
#     relatively big and awkward data, like lists of strings and datestamps, to
#     be passed around without worrying about accessing them between cores.
#     As is we're only storing 16 unsigned integers between cores, and adding
#     arrays of strings would be a whole mess. I think it's more efficient to do
#     this bit synchronously, but that doesn't mean I like how it is cureently
#     written. This is where self.gesture_detector actually executes the lambdas that
#     were defined near the beginning of this file, if the perimeters passed are
#     defined (and in the case of the eye perimeters, if they additionally have
#     an average EAR below the threshold value).
        self.gesture_detector.trigger_events(
                timestamp, self.open_eye_threshold, fist_perimeter, 
                palm_perimeter, left_eye_perimeter, right_eye_perimeter)
     
#     Now we're gonna draw all those beautiful rectangles based on the top and
#     bottom corners of those MultithreadedPerimeter instances. 
#     MultithreadedPerimeter's interface returns (x, y) coordinate tuples,
#     because that is what OpenCV wants to draw rectangles based on.
        for perimeter in [fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter]:
        #Currently they're all red, because that was easy. I think we should
        #display eyes below the EAR threshold differently than eyes above that
        #threshold, though. Different hand colors would be good, too. I'm
        #honestly unsure where the EAR check belongs, it would ideally be 
        #implemented in one place. I think there may be a need for some
        #container class that manages two MultithreadedPerimeter instances that
        #represent a pair of eyes.
            if perimeter.is_set():
                cv2.rectangle(frame, perimeter.get_top_corner(), 
                        perimeter.get_bottom_corner(), (0, 0, 255), 2)
     
        #Display the frame, flipping it to look like a mirror. I have way too much
        #trouble orienting my body to get gestures detected without doing this.
        #It's pretty embarassing.
        self.gui_manager.set_debug_frame(cv2.flip(frame, 1))

    def set_open_eye_threshold(self, new_ear_value):
        self.open_eye_threshold = float(new_ear_value) / 100.0
        self.data_manager.set_open_eye_threshold(self.open_eye_threshold)
        
    def on_close(self):
#Close down OpenCV.
        self.cap.release()
        cv2.destroyAllWindows()

# Close the GUI
        self.gui_manager.destroy_gui()
     
# Close log file.
        self.logger.close() 
        self.data_manager.close()
