import sys
from gestureLexer import GestureLexer
from gestureDetector import GestureDetector
from blinkDetector import BlinkDetector

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
gesture_detector.on_fist(lambda timestamp: gesture_lexer.lex("fist", timestamp))
gesture_detector.on_palm(lambda timestamp: gesture_lexer.lex("palm", timestamp))

gesture_detector.on_blink(lambda timestamp: gesture_lexer.lex("blink", timestamp))
gesture_detector.on_left_wink(lambda timestamp: gesture_lexer.lex("left wink", timestamp))
gesture_detector.on_right_wink(lambda timestamp: gesture_lexer.lex("right wink", timestamp))

gesture_detector.start(0.2)
