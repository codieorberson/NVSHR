from subprocess import Popen

class SubprocessExecutor():
    def __init__(self):
        self.subprocess_maps = []

    def execute(self, file_name, argument, callback = None):
        self.__clean_up_subprocesses__()
        self.subprocess_maps.append({
                'process' : Popen(['python3', file_name, argument]),
                'callback' : callback
                })

    def __clean_up_subprocesses__(self):
        running_subprocess_maps = []
        for subprocess_map in self.subprocess_maps:
            if subprocess_map['process'].poll() == None:
                running_subprocess_maps.append(subprocess_map)
            else:
                subprocess_map['process'].terminate()
                if subprocess_map['callback']:
                    subprocess_map['callback']()
        self.subprocess_maps = running_subprocess_maps
