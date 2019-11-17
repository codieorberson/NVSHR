import multiprocessing
from multiprocessing import Process
import platform

class SynchronousProcess():
    def __init__(self, target = None, args = None):
        if args:
            target(*args)
        else:
            target()

    def start(self):
        pass

    def join(self):
        pass


if platform.system() == 'Linux':
    #On Linux, we use multiprocessing.
    ProcessConstructor = Process
else:
    #On Windows, we use the previously defined kludge.
    ProcessConstructor = SynchronousProcess

class ProcessManager():
    def __init__(self):
        self.processes = []

    def add_process(self, callback, arguments=None):
        if arguments:
            if not isinstance(arguments, tuple):
                arguments = (arguments, )
            self.process = ProcessConstructor(target=callback, args=arguments)
        else:
            self.process = ProcessConstructor(target=callback)
            
        self.processes.append(self.process)
        self.process.start()
        

    def on_done(self, callback=None):
        for self.process in self.processes:
            self.process.join()
        self.processes = []
        if callback:
            callback()
