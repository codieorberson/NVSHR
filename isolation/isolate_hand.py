import cv2
import numpy as np

cap = cv2.VideoCapture(0)

panel = np.zeros([100, 700], np.uint8)
cv2.namedWindow('panel')

def nothing(x):
    pass

cv2.createTrackbar('L - h', 'panel', 0, 255, nothing)
cv2.createTrackbar('U - h', 'panel', 132, 255, nothing) #This one we may have to change

cv2.createTrackbar('L - s', 'panel', 0, 255, nothing)
cv2.createTrackbar('U - s', 'panel', 255, 255, nothing)

cv2.createTrackbar('L - v', 'panel', 0, 255, nothing)
cv2.createTrackbar('U - v', 'panel', 255, 255, nothing)

cv2.createTrackbar('S ROWS', 'panel', 0, 480, nothing)
cv2.createTrackbar('E ROWS', 'panel', 480, 480, nothing)
cv2.createTrackbar('S COL', 'panel', 0, 640, nothing)
cv2.createTrackbar('E COL', 'panel', 640, 640, nothing)

while True:
    ret, frame = cap.read()

    s_r = cv2.getTrackbarPos('S ROWS', 'panel')
    e_r = cv2.getTrackbarPos('E ROWS', 'panel')
    s_c = cv2.getTrackbarPos('S COL', 'panel')
    e_c = cv2.getTrackbarPos('E COL', 'panel')

    roi = frame[s_r: e_r, s_c: e_c]

    l_h = cv2.getTrackbarPos('L - h', 'panel')
    u_h = cv2.getTrackbarPos('U - h', 'panel')
    l_s = cv2.getTrackbarPos('L - s', 'panel')
    u_s = cv2.getTrackbarPos('U - s', 'panel')
    l_v = cv2.getTrackbarPos('L - v', 'panel')
    u_v = cv2.getTrackbarPos('U - v', 'panel')

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(roi, lower, upper)
    mask_inv = cv2.bitwise_not(mask)

    grayFrame = cv2.bitwise_and(roi, roi, mask=mask_inv)
    official_grayFrame = cv2.cvtColor(grayFrame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame', official_grayFrame)

    #I tried commenting out the panel below, however it still displays when the program is ran
    cv2.imshow('panel', panel)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()