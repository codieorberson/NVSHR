import sys
import cv2
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gestureDetector import GestureDetector
from gestureLexer import GestureLexer


#from smartHomeActivator import SmartHomeActivator
#from commandMapper import CommandMapper

if len(sys.argv) > 1:
    time_increment = float(sys.argv[1])
else:
    time_increment = 3

if len(sys.argv) > 2 and not bool(int(sys.argv[2])):
    is_black_and_white = False
else:
    is_black_and_white = True

if len(sys.argv) > 3 and not bool(int(sys.argv[2])):
    is_blink = False
else:
    is_blink = True

gesture_detector = GestureDetector(time_increment, is_black_and_white)
gesture_lexer = GestureLexer()

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

    open_eye_threshold = 0.2

    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter() 

    process_manager.add_process(gesture_detector.detect, 
            (frame, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, 
            left_eye_perimeter, right_eye_perimeter))

    process_manager.on_done()

    gesture_detector.trigger_events(timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)
    gesture_lexer.lex(timestamp, 2, 5)

    for perimeter in [fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter]:
        if perimeter.is_set():
            cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)

    cv2.imshow('NVSHR', cv2.flip(frame, 1))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        should_continue = False

cap.release()
cv2.destroyAllWindows()
gesture_lexer.close()
