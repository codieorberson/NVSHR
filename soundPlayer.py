# Sound Effects by Eric Matyas,  www.soundimage.org
from playsound import playsound

class SoundPlayer():
    def play_success_sound(self):
        self.__play_file__('Success.wav')

    def play_failure_sound(self):
        self.__play_file__('Failure.wav')

    def __play_file__(self, file_name):
        playsound(file_name, False)
