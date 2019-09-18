# NVSHR

Pass an argument into main.py to set the number of seconds between ticks (default is 3).

Everything is sketchy and broken right now, but it does run. Logs "tick" every tick, "fist" if it detected a fist in the last tick, "palm" if it detected a palm with spread out fingers in the last tick, and "wink" if it detected exactly one eye at any point during the last tick. It's WAAAAY too trigger-happy about claiming to see winks, since the eye detection in general is still sketch.

GestureDetector has a bunch of repeating code in it, and we obvious need to abstract that stuff out into a separate class called Gesture.
