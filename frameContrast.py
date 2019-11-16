import cv2
import numpy as np

class FrameContrast():
    
    def set_frame_contrast(self, redContrast, greenContrast, blueContrast):
        return np.array([redContrast, greenContrast, blueContrast])

    def update_low_contrast(self, redContrast):
        self.low_contrast = self.set_frame_contrast(int(redContrast), 0, 0)
        return(self.low_contrast)

    def update_high_contrast(self, redContrast):
        self.high_contrast = self.set_frame_contrast(int(redContrast), 255, 255)
        return(self.high_contrast)

    def changing_palm_frame(self, frame, palm_low_contrast, palm_high_contrast):
        self.update_low_contrast(palm_low_contrast)
        self.update_high_contrast(palm_high_contrast)
        mask = cv2.inRange(frame, self.low_contrast, self.high_contrast)
        mask_inv = cv2.bitwise_not(mask)
        color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
        contrast_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Palm Detection', contrast_frame) #Uncomment this out if you want to see the different level contrast frame
        return contrast_frame

    