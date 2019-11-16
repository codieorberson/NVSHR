from sound import Sound

class SoundPlayer():
    def __init__(self):
        self.sound = Sound()

    def play_success_sound(self):
        self.sound.from_file('Success.wav')

    def play_failure_sound(self):
        self.sound.from_file('Failure.wav')
