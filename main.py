#!/usr/local/bin/python3
import sys
sys.path.insert(1, './modules/')
sys.path.insert(2, './modules/gui/')
sys.path.insert(3, './static_data/')
sys.path.insert(4, './dynamic_data/')

from nonVerbalSmartHomeRecognitionSystem import NonVerbalSmartHomeRecognitionSystem

if __name__ == '__main__':
    print("Activating the Non-Verbal Smart Home Recognition system.\n")
    NonVerbalSmartHomeRecognitionSystem()
