# Sound Effects by Eric Matyas,  www.soundimage.org
from playsound import playsound

class Sound:
    def __init__(self):
        pass

    def from_file(self, file_name):
        playsound(file_name)
