from subprocessExecutor import SubprocessExecutor

class SoundPlayer():
    def __init__(self):
        self.subprocessExecutor = SubprocessExecutor()

    def play_success_sound(self):
        self.__play_file__('Success.wav')

    def play_failure_sound(self):
        self.__play_file__('Failure.wav')

    def __play_file__(self, file_name):
        self.subprocess_executor.execute('./play_file.py', file_name)
