from imgClass import *
import numpy as np
import cv2

# 9 or 22

ballImage = cv2.imread("../automaticExample/img/9.png", 0)
imgToShow = cv2.imread("../automaticExample/img/9.png")
#ballImage = cv2.blur(ballImage, (20,20))
circles = cv2.HoughCircles(ballImage, cv2.HOUGH_GRADIENT, 1, 64, param1=50, param2=20, minRadius=10, maxRadius=32)

print(circles)

#circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    cv2.circle(imgToShow,(i[0],i[1]),i[2],(0,255,0),2)
    cv2.circle(imgToShow,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('image', imgToShow)
cv2.waitKey(0)
cv2.destroyAllWindows()


print(circles)