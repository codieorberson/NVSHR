from multiprocessing import Process, get_start_method

is_forking = get_start_method() == 'fork'

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

if get_start_method() == "fork":
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
            process = ProcessConstructor(target=callback, args=arguments)
        else:
            process = ProcessConstructor(target=callback)
        self.processes.append(process)
        process.start()

    def on_done(self, callback=None):
        for process in self.processes:
            process.join()
        self.processes = []
        if callback:
            callback()
