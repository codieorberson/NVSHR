import cv2
import numpy as np

cap = cv2.VideoCapture(0)

panel = np.zeros([100, 700], np.uint8)
cv2.namedWindow('panel')

def nothing(x):
    pass

cv2.createTrackbar('High Contrast Red', 'panel', 0, 255, nothing)
cv2.createTrackbar('Low Contrast Red', 'panel', 132, 255, nothing) #This one we may have to change

cv2.createTrackbar('High Contrast Green', 'panel', 0, 255, nothing)
cv2.createTrackbar('Low Contrast Green', 'panel', 255, 255, nothing)

cv2.createTrackbar('High Contrast Blue', 'panel', 0, 255, nothing)
cv2.createTrackbar('Low Contrast Blue', 'panel', 255, 255, nothing)

cv2.createTrackbar('North Rows', 'panel', 0, 480, nothing)
cv2.createTrackbar('South Rows', 'panel', 480, 480, nothing)
cv2.createTrackbar('Left Columns', 'panel', 0, 640, nothing)
cv2.createTrackbar('Right Columns', 'panel', 640, 640, nothing)

while True:
    ret, frame = cap.read()

    north_rows = cv2.getTrackbarPos('North Rows', 'panel')
    south_rows = cv2.getTrackbarPos('South Rows', 'panel')
    left_columns = cv2.getTrackbarPos('Left Columns', 'panel')
    right_columns = cv2.getTrackbarPos('Right Columns', 'panel')

    roi = frame[north_rows: south_rows, left_columns: right_columns]

    high_contrast_red = cv2.getTrackbarPos('High Contrast Red', 'panel')
    low_contrast_red = cv2.getTrackbarPos('Low Contrast Red', 'panel')
    high_contrast_green = cv2.getTrackbarPos('High Contrast Green', 'panel')
    low_contrast_green = cv2.getTrackbarPos('Low Contrast Green', 'panel')
    high_contrast_blue = cv2.getTrackbarPos('High Contrast Blue', 'panel')
    low_contrast_blue = cv2.getTrackbarPos('Low Contrast Blue', 'panel')

    low_contrast = np.array([high_contrast_red, high_contrast_green, high_contrast_blue])
    high_contrast = np.array([low_contrast_red, low_contrast_green, low_contrast_blue])

    mask = cv2.inRange(roi, low_contrast, high_contrast)
    mask_inv = cv2.bitwise_not(mask)

    color_frame = cv2.bitwise_and(roi, roi, mask=mask_inv)
    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame', gray_frame)

    #I tried commenting out the panel below, however it still displays when the program is ran
    cv2.imshow('panel', panel)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()