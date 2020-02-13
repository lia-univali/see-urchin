import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)


def removeBinaryRelative(filename):
    img = Image(filename)
    img.gray.window()
    thresh = img.gray.getRelativeThreshold()
    img.gray.binary(thresh * 1.1)
    img.gray.invert()
    img.gray.floodFill()
    if(img.gray.image.shape[0] > 1000 and img.gray.image.shape[1] > 1000):
        img.gray.erode()
    return img.gray.image

def removeBinary(filename):
    img = Image(filename)
    img.gray.window()
    img.gray.binary(10)
    img.gray.invert()
    img.gray.close((10, 10))
    img.gray.dilate((15, 15))
    return img.gray.image

filename = ["img/LARVAS_1.jpg", "img/LARVAS_2.jpg", "img/LARVAS_3.jpg"]

first = Img(cv2.imread(filename[0]))
result = Img(cv2.bitwise_and(removeBinary(filename[0]), removeBinaryRelative(filename[0])))
while(result.checkForRemovableObjects()):
    result.removeObjectsBySize(0, 25)
counter = result.markObjects(first.image, [0, 0, 255])
showImage(first.BGRToRGB(), 211)
cv2.imwrite("IMGPESQ_1.png", first.image)

second = Img(cv2.imread(filename[1]))
result = Img(cv2.bitwise_and(removeBinary(filename[1]), removeBinaryRelative(filename[1])))
while(result.checkForRemovableObjects()):
    result.removeObjectsBySize(0, 25)
counter = result.markObjects(second.image, [0, 0, 255])
showImage(second.BGRToRGB(), 223)
cv2.imwrite("IMGPESQ_2.png", second.image)

third = Img(cv2.imread(filename[2]))
result = Img(cv2.bitwise_and(removeBinary(filename[2]), removeBinaryRelative(filename[2])))
while(result.checkForRemovableObjects()):
    result.removeObjectsBySize(0, 25)
counter = result.markObjects(third.image, [0, 0, 255])
showImage(third.BGRToRGB(), 224)
cv2.imwrite("IMGPESQ_3.png", third.image)

plt.show()