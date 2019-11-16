from sound import Sound

class SoundPlayer():
    def __init__(self):
        self.sound = Sound()

    def playSuccessSound(self):
        self.sound.from_file('Success.wav')

    def playFailureSound(self):
        self.sound.from_file('Failure.wav')
