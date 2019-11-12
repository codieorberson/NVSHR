# Sound Effects by Eric Matyas,  www.soundimage.org
from playsound import playsound
from sys import argv

sound_file = argv[1]
playsound('./static_data/' + argv[1])
