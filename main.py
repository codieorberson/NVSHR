#!/usr/local/bin/python3
import sys
sys.path.insert(1, './static_data/')
sys.path.insert(2, './dynamic_data/')
sys.path.insert(3, './modules/')
sys.path.insert(4, './modules/gesture_sequence_detector/')
sys.path.insert(5, './modules/smart_home_activator/')
sys.path.insert(6, './modules/gui_manager/')
sys.path.insert(7, './modules/sound_player/')

from nonVerbalSmartHomeRecognitionSystem import NonVerbalSmartHomeRecognitionSystem

if __name__ == '__main__':
    print("Activating the Non-Verbal Smart Home Recognition system.\n")
    NonVerbalSmartHomeRecognitionSystem()
