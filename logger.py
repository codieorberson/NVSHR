import os

class Logger():
    def __init__(self):
        exists =  os.path.exists("logfile.txt")
        if not os.path.exists("logfile.txt"):
            self.file = open("logfile.txt", 'w+')
            self.file.write("   Date        Time     Command\n")
        else:
            self.file = open("logfile.txt", "a+")
        print("   Date        Time     Command\n")

    def log(self, output):
       self.file.write(output)
       print(output) 

    def log_gesture(self, gesture_name, now):
        self.log(''.join((now.isoformat()[:10], "    ", now.isoformat()[12:19], 
                "    ", gesture_name ," \n")))

    def log_gesture_sequence(self, gesture_sequence):
        #This method should probably be radically different.
        log(''.join(gesture_sequence))

    def close(self):
        self.file.seek(0)
        self.file.truncate()
        self.file.close()
