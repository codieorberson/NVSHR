#!/usr/local/bin/python3
import sys

paths = [
        './static_data/',
        './dynamic_data/',
        './modules/',
        './modules/data_manager/',
        './modules/gesture_sequence_detector/',
        './modules/gesture_sequence_detector/gesture_detector/',
        './modules/smart_home_activator/',
        './modules/sound_player/',
        './modules/gui_manager/'
        ]

for i in range(0, len(paths)):
    sys.path.insert(i + 1, paths[i])

from nonVerbalSmartHomeRecognitionSystem import NonVerbalSmartHomeRecognitionSystem

if __name__ == '__main__':
    print("Activating the Non-Verbal Smart Home Recognition system.\n")
    NonVerbalSmartHomeRecognitionSystem()
