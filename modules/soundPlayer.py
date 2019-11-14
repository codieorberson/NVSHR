from subprocessExecutor import SubprocessExecutor

class SoundPlayer():
    def __init__(self):
       self.subprocess_executor = SubprocessExecutor()

    def speak(self, text):
        self.subprocess_executor.execute('./modules/sound_player/speak.py', text)

    def play_success_sound(self):
        self.__play_file__('success.wav')

    def play_failure_sound(self):
        self.__play_file__('failure.wav')

    def __play_file__(self, file_name):
        self.subprocess_executor.execute('./modules/sound_player/play_file.py', file_name)
