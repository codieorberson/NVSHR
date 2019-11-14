#!/usr/local/bin/python3
import sys
sys.path.insert(1, './static_data/')
sys.path.insert(2, './dynamic_data/')
sys.path.insert(3, './modules/')
sys.path.insert(4, './modules/gesture_sequence_detector_modules/')
sys.path.insert(5, './modules/smart_home/')
sys.path.insert(6, './modules/gui/')

from nonVerbalSmartHomeRecognitionSystem import NonVerbalSmartHomeRecognitionSystem

if __name__ == '__main__':
    print("Activating the Non-Verbal Smart Home Recognition system.\n")
    NonVerbalSmartHomeRecognitionSystem()
