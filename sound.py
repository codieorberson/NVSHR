from playsound import playsound


class Sound:
    @staticmethod
    def success():
        playsound('Success.wav')

    @staticmethod
    def failure():
        playsound('Failure.wav')
