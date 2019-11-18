from subprocessExecutor import SubprocessExecutor
from sound import Sound
from platform import system

class SoundPlayer():
    def __init__(self):
        self.subprocess_executor = SubprocessExecutor()
        self.sound = Sound()
        self.is_linux = system() == 'Linux'

    def play_success_sound(self):
        self.__play_file__('Success.wav')

    def play_failure_sound(self):
        self.__play_file__('Failure.wav')

    def __play_file__(self, file_name):
        if self.is_linux:
            self.subprocess_executor.execute('./play_file.py', file_name)
        else:
            self.sound.from_file(file_name)
