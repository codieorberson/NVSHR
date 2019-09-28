import sys
from gestureDetector import GestureDetector

if len(sys.argv) > 1:
    time_increment = float(sys.argv[1])
else:
    time_increment = 3

gestureDetector = GestureDetector(time_increment)

#Note that while these methods have been changed to allow an argument in the
#callback, I've purposefully made it continue working without an argument
#so that it can be tested the way it was before. We can change that later
#once we have some basic tests up.
gestureDetector.on_fist(lambda timestamp: print("fist @" + str(timestamp)))
gestureDetector.on_palm(lambda timestamp: print("palm @" + str(timestamp)))

gestureDetector.on_left_wink(lambda: print("left wink"))
gestureDetector.on_right_wink(lambda: print("right wink"))

gestureDetector.start()
