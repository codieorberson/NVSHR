import time

class Timer():
    def __init__(self, time_increment):
       self.last_time = time.time()
       self.time_increment = time_increment
       self.callback = None

    def set_time(self, new_time_increment):
        self.time_increment = new_time_increment

    def on_time(self, callback):
        self.callback = callback

    def check_time(self):
        current_time = time.time()
        if self.last_time + self.time_increment <= current_time:
            self.callback()
            self.last_time = current_time
