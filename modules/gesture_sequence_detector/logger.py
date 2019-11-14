import os

_file_name = "./dynamic_data/logfile.txt"

class Logger():
    def __init__(self):
        exists = os.path.exists(_file_name)
        if not exists:
            self.file = open(_file_name, 'w+')
            self.file.write("   Date        Time     Command\n")
            print("   Date        Time     Command\n")
        else:
            self.file = open(_file_name, "a+")
            
    def log(self, output):
        self.__init__()
        self.file.write(output)
        print(output) 

    def log_fist(self, now):
        self.__log_gesture__('fist', now)

    def log_palm(self, now):
        self.__log_gesture__('palm', now)

    def log_blink(self, now):
        self.__log_gesture__('blink', now)

    def __log_gesture__(self, gesture_name, now):
        self.log(''.join((now.isoformat()[:10], "    ", now.isoformat()[12:19], 
                "    ", gesture_name ," \n")))

    def log_gesture_sequence(self, gesture_sequence, now, was_recognised):
        if was_recognised:
            ending = "] recognised"
        else:
            ending = "] not recognised"

        self.__log_gesture__("pattern: [" + ', '.join(gesture_sequence) + ending, now)

    def close(self):
        self.file.seek(0)
        self.file.close()
        os.remove(_file_name)
