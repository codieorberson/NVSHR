import cv2
import numpy as np

class ContrastManager():
    def __set_frame_contrast__(self, redContrast, greenContrast, blueContrast):
        return np.array([redContrast, greenContrast, blueContrast])

    def set_low_contrast(self, redContrast):
        self.low_contrast = self.__set_frame_contrast__(int(redContrast), 0, 0)
        return(self.low_contrast)

    def set_high_contrast(self, redContrast):
        self.high_contrast = self.__set_frame_contrast__(int(redContrast), 255, 255)
        return(self.high_contrast)

    def toggle_contrast(self, should_be_on):
        self.should_apply_contrast = should_be_on

    def apply_contrast(self, frame):
        if self.should_apply_contrast:
            mask = cv2.inRange(frame, self.low_contrast, self.high_contrast)
            mask_inv = cv2.bitwise_not(mask)
            color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
            contrast_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Palm Detection', contrast_frame) #Uncomment this out if you want to see the different level contrast frame
            return contrast_frame
        else:
            return frame
