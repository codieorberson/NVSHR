import sys
from gestureDetector_hand_gesture_only import GestureDetector
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

gestureDetector.start()
