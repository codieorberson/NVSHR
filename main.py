import sys
import dlib
from gestureLexer import GestureLexer
from gestureDetector import GestureDetector
from Blink import Blink

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

gesture_detector = GestureDetector(time_increment, is_black_and_white)
gesture_lexer = GestureLexer()

#Note that while these methods have been changed to allow an argument in the
#callback, I've purposefully made it continue working without an argument
#so that it can be tested the way it was before. We can change that later
#once we have some basic tests up.
gesture_detector.on_fist(lambda timestamp: gesture_lexer.lex("fist", timestamp))
gesture_detector.on_palm(lambda timestamp: gesture_lexer.lex("palm", timestamp))
#gestureDetector.on_left_wink(lambda: print("left wink"))
#gestureDetector.on_right_wink(lambda: print("right wink"))

blink_detector = Blink(detector = dlib.get_frontal_face_detector(),
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat'))

#blink_detector.detect()
gesture_detector.start()
