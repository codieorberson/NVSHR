import multiprocessing
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
            self.process = multiprocessing.Process(target=callback, args=arguments)
        else:
            self.process = multiprocessing.Process(target=callback)
            
        self.processes.append(self.process)
        self.process.start()
        if self.process.is_alive():
            self.process.terminate()
        self.process.terminate()
        
    def on_done(self):
        for self.process in self.processes:
            self.process.join()
        self.process.join(.2)
        self.processes = []
        if self.process.is_alive():
            self.process.terminate()
        self.process.terminate()
