import os

class DataManager():
    def __init__(self):
        exists =  os.path.exists("data.txt")
        if not os.path.exists("data.txt"):
            self.file = open("data.txt", 'w+')
            #default EAR on first line:
            self.file.write("0.2\n")
            self.open_eye_threshold = 0.2
            # the number below is just place holders here
            self.low_contrast_value = 0
            self.high_contrast_value = 0
            self.min_time_inc = 0
            self.max_time_inc = 0

        else:
            self.file = open("data.txt", 'r+')
            self.lines = self.file.readlines()
            if len(self.lines) < 1:
                self.file.write("0.2\n")
                self.file.seek(0)
                self.lines = self.file.readlines()
            self.open_eye_threshold = float(self.strip_newline(self.lines[0]))
            # the number below is just place holders here
            self.low_contrast_value = 0
            self.high_contrast_value = 0
            self.min_time_inc = 0
            self.max_time_inc = 0


    def set_open_eye_threshold(self, new_open_eye_threshold):
        self.file.seek(0)
        lines = self.file.readlines()
        lines[0] = self.add_newline(str(new_open_eye_threshold))
        self.file.close()
        os.remove('data.txt')
        self.file = open("data.txt", 'w+')
        self.file.write(''.join(lines))
 
    def get_open_eye_threshold(self):
        return self.open_eye_threshold

    def set_low_contrast(self, new_low_contrast):
        return 0
    
    def get_low_contrast(self):
        return self.low_contrast_value
    
    def set_high_contrast(self, new_high_contrast):
        return 0
    
    def get_high_contrast(self):
        return self.high_contrast_value
    
    def set_min_time_inc(self, new_min_time_inc):
        return 0

    def get_min_time_inc(self):
        return self.min_time_inc

    def set_max_time_inc(self, new_max_time_inc):
        return 0

    def get_max_time_inc(self):
        return self.max_time_inc 

    
    def strip_newline(self, string):
        return string[:-1]

    def add_newline(self, string):
        return string + "\n"
       
    def close(self):
        self.file.close()
