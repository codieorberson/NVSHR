import sys
import cv2
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gestureDetector import GestureDetector
from gestureLexer import GestureLexer
from gestureParser import GestureParser

#from smartHomeActivator import SmartHomeActivator
#from commandMapper import CommandMapper

#The first command line argument determines the minimum time needed between
#identical gestures for them to be considered separate gestures in a pattern.
if len(sys.argv) > 1:
    min_increment = float(sys.argv[1])
else:
    min_increment = 2

#The second command line argument determines the maximum time that can lapse
#without a gesture before gestures are collected into a gesture pattern.
if len(sys.argv) > 2:
    max_increment = float(sys.argv[2])
else:
    max_increment = 5

#The third command line argument determines the EAR at which blinks and winks
#are detected.
if len(sys.argv) > 3:
    open_eye_threshold = float(sys.argv[3])
else:
    open_eye_threshold = 0.2

#The third command line argument determines whether or not a black and white
#filter should be used when detecting gestures. It displays color regardless.
#Any value whatsoever will set this to False, otherwise it defaults to True.
if len(sys.argv) > 2 and not bool(int(sys.argv[2])):
    is_black_and_white = False
else:
    is_black_and_white = True

gesture_detector = GestureDetector()
gesture_lexer = GestureLexer()
gesture_parser = GestureParser()

#Note that while these methods have been changed to allow an argument in the
#callback, I've purposefully made it continue working without an argument
#so that it can be tested the way it was before. We can change that later
#once we have some basic tests up.
gesture_detector.on_fist(lambda timestamp: gesture_lexer.add("fist", timestamp))
gesture_detector.on_palm(lambda timestamp: gesture_lexer.add("palm", timestamp))

gesture_detector.on_blink(lambda timestamp: gesture_lexer.add("blink", timestamp))
gesture_detector.on_left_wink(lambda timestamp: gesture_lexer.add("left_wink", timestamp))
gesture_detector.on_right_wink(lambda timestamp: gesture_lexer.add("right_wink", timestamp))

should_continue = True
cap = cv2.VideoCapture(0)
process_manager = ProcessManager()

while should_continue:

    ret, frame = cap.read()
    timestamp = datetime.now()

    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter() 

    process_manager.add_process(gesture_detector.detect, 
            (frame, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, 
            left_eye_perimeter, right_eye_perimeter))

    process_manager.on_done()

    gesture_detector.trigger_events(timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)

    for gesture_pattern in gesture_lexer.lex(timestamp, min_increment, max_increment):
        gesture_parser.parse(gesture_pattern)

    for perimeter in [fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter]:
        if perimeter.is_set():
            cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)

    cv2.imshow('NVSHR', cv2.flip(frame, 1))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        should_continue = False

cap.release()
cv2.destroyAllWindows()
gesture_lexer.close()
