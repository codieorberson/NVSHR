# Sound Effects by Eric Matyas,  www.soundimage.org
from playsound import playsound
from sys import argv
from os import path
import os

current_working_directory = path.dirname(os.path.realpath(__file__))
relative_path = "/../../static_data/"
sound_file = argv[1]
full_path = current_working_directory + relative_path + sound_file

playsound(full_path)
