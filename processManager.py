from multiprocessing import Process


class ProcessManager():
    def __init__(self):
        self.processes = []

    def add_process(self, callback, arguments=None):
        if arguments:
            if not isinstance(arguments, tuple):
                arguments = (arguments, )
            process = Process(target=callback, args=arguments)
        else:
            process = Process(target=callback)
        self.processes.append(process)
        process.start()

    def on_done(self, callback=None):
        for process in self.processes:
            process.join()
        self.processes = []
        if callback:
            callback()
