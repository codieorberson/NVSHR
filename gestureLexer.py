import numpy as np
import datetime
import os

class GestureLexer():
    def __init__(self):
        self.gestures = []
        self.gesture_patterns = []

    def add(self, gesture_name, now):
        self.gestures.append((gesture_name, now.timestamp()))

    #Iterates over list of gestures in proper order. If a timestamp is less than current time - set max increment,
    #that gesture sequence is added to list of all sequences.
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
