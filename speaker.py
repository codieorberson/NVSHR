from subprocessExecutor import SubprocessExecutor

class Speaker():
    def __init__(self):
        self.subprocess_executor = SubprocessExecutor()

    def speak(self, command_text):
        self.subprocess_executor.execute('speak.py', command_text)
