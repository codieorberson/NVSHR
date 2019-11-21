from datetime import datetime


class FramesPerSecondMeter():
    def __init__(self):
        self.timestamp = datetime.utcnow()

    def cycle(self):
        self.last_timestamp = self.timestamp
        self.timestamp = datetime.utcnow()

        return str(1 / ((self.timestamp - self.last_timestamp).microseconds / 1000000))[:4]
