import numpy as np
from imgClass import *
import matplotlib.pyplot as plt
import cv2

'''
u were
 - getting an image
 - coloring a circle black in the center
 - doing a floodfill with black in the center
 - doing a bitwise with the contour pic to get the furthest borders

good luck!
'''


for i in range(50):
    image = Image(f"../oneHundred/img/{i}.png")
    image.gray.window()sda
    image.gray.binary(30)
    image.gray.invert()
    image.gray.removeObjectsSmallerThan((15, 15))
    contours, hier = cv2.findContours(image.gray.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largestContour = getLargestContour(contours)
    image.gray.show(222)
    (x,y),radius = cv2.minEnclosingCircle(contours[largestContour])
    center = (int(x),int(y))

    image.gray.laplacian()
    circleImage = cv2.circle(np.array(image.gray.image), center, int(radius), 0, -1)
    #cv2.namedWindow("a", cv2.WINDOW_NORMAL); cv2.resizeWindow("a",  256, 256); cv2.imshow("a", circleImage); cv2.waitKey(); cv2.destroyAllWindows()

    circleImage = Img(circleImage)
    image.gray.show(221)
    circleImage.show(212)
    plt.show()