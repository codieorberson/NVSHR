import numpy as np
import datetime
import os

class GestureLexer():
    def __init__(self):

        self.gestures = []
        self.gesture_patterns = []

        #Again, everything related to logging should be moved to a different
        #class. I think a shared instance of that class should be passed to
        #both GestureLexer and GestureParser.
        exists =  os.path.exists("logfile.txt")
        if not os.path.exists("logfile.txt"):
            self.file = open("logfile.txt", 'w+')
            self.file.write("   Date        Time     Command\n")
        else:
            self.file = open("logfile.txt", "a+")
        print("   Date        Time     Command\n")

    def add(self, gesture_name, now):
        gesture_tuple = (now.isoformat()[:10], "    ", now.isoformat()[12:19], "    ", gesture_name ," \n")
        gesture_text=''.join(gesture_tuple)
        print(gesture_text)
        self.file.write(gesture_text)
        self.gestures.append((gesture_name, now.timestamp()))

    def lex(self, now, min_increment, max_increment):
        last_dict = {'fist' : None, 'palm' : None, 'blink' : None, 'left_wink' : None, 'right_wink' : None}

        now = now.timestamp()
        gesture_pattern = []
        for gesture in self.gestures:
            if not last_dict[gesture[0]]:
                last_dict[gesture[0]] = gesture[1]
                gesture_pattern.append(gesture[0])
            elif last_dict[gesture[0]] + min_increment < gesture[1]:
                last_dict[gesture[0]] = gesture[1]
                gesture_pattern.append(gesture[0])

        if len(self.gestures) > 0:
            if float(now) > max_increment + self.gestures[len(self.gestures) - 1][1]:
                if gesture_pattern != []:
                    self.gesture_patterns.append(gesture_pattern)
                    self.gestures = []

        current_patterns = self.gesture_patterns
        self.gesture_patterns = []

        return current_patterns

    def close(self):
        self.file.seek(0)
        self.file.truncate()
        self.file.close()
