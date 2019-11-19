# Sound Effects by Eric Matyas,  www.soundimage.org

from builtins import staticmethod

from playsound import playsound


class Sound:
    def __init__(self):
        pass

    @staticmethod
    def success():
        playsound('Success.wav', False)

    @staticmethod
    def failure():
        playsound('Failure.wav', False)
