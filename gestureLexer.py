import numpy as np
import datetime
import os

class GestureLexer():
    def __init__(self):
        exists = os.path.getsize("logfile.txt")
        if exists > 0:
            self.file=open("logfile.txt", 'a')

        else:
            self.file=open("logfile.txt", 'a+')
            self.file.write("   Date        Time     Command\n")
            print("   Date        Time     Command\n")

    def lex(self, gesture_name, now):
        gesture_tuple = (now.isoformat()[:10], "    ", now.isoformat()[12:19], "    ", gesture_name ," \n")
        gesture_text=''.join(gesture_tuple)
        self.file.write(gesture_text)
        print(gesture_text)

    def close(self):
        self.file.close()
