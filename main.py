import sys
import dlib
from gestureDetector import GestureDetector
from Blink import Blink

#from smartHomeActivator import SmartHomeActivator
#from commandMapper import CommandMapper


if len(sys.argv) > 1:
    time_increment = float(sys.argv[1])
else:
    time_increment = 3

gestureDetector = GestureDetector(time_increment)

gestureDetector.on_fist(lambda: print("fist"))
gestureDetector.on_palm(lambda: print("palm"))
#gestureDetector.on_left_wink(lambda: print("left wink"))
#gestureDetector.on_right_wink(lambda: print("right wink"))

#blink_detector = Blink(detector = dlib.get_frontal_face_detector(),
    #                 predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat'))

#blink_detector.detect()
gestureDetector.start()
