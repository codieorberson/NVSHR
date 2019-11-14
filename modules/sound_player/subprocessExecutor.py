from subprocess import Popen

class SubprocessExecutor():
    def __init__(self):
        self.subprocesses = []

    def execute(self, file_name, argument):
        self.__clean_up_subprocesses__()
        self.subprocesses.append(Popen(['python3', file_name, argument]))

    def __clean_up_subprocesses__(self):
        running_subprocesses = []
        for subprocess in self.subprocesses:
            if subprocess.poll() == None:
                running_subprocesses.append(subprocess)
            else:
                subprocess.terminate()
        self.subprocesses = running_subprocesses
