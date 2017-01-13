import cv2
import cv
import numpy as np

cap = cv2.VideoCapture('test_videos/match_video.mp4')

while(cap.isOpened()):
    ret, im = cap.read()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    new_im = cv2.bitwise_and(im, im, mask = thresh)

    hsv = cv2.cvtColor(new_im, cv2.COLOR_BGR2HSV)
    lower = np.array([20, 90, 110])
    upper = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('frame', mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # TODO: Transform ball location + size to a flat field

    cv2.drawContours(im, contours, -1, (0, 0, 255), 3)

    #cv2.imshow('frame', im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()