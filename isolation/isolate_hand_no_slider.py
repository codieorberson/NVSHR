import cv2
import numpy as np

cap = cv2.VideoCapture(0)

panel = np.zeros([100, 700], np.uint8)


hContrastRed = 0
lContrastRed = 132

hContrastGreen = 0
lContrastGreen = 255

hContrastBlue = 0
lContrastBlue = 255


while True:
    ret, frame = cap.read()


    low_contrast = np.array([hContrastRed, hContrastGreen, hContrastBlue])
    high_contrast = np.array([lContrastRed, lContrastGreen, lContrastBlue])

    mask = cv2.inRange(frame, low_contrast, high_contrast)
    mask_inv = cv2.bitwise_not(mask)

    color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame', gray_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
