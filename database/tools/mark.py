import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)

def removeBinaryRelative(filename, showPos):
    img = Image(filename)
    img.gray.window()
    thresh = img.gray.getRelativeThreshold()
    img.gray.binary(thresh * 1.1)
    img.gray.invert()
    img.gray.floodFill()
    if(img.gray.image.shape[0] > 1000 and img.gray.image.shape[1] > 1000):
        img.gray.erode()
    img.gray.show(showPos)
    return img.gray.image

def removeBinary(filename, showPos):
    img = Image(filename)
    img.gray.window()
    img.gray.binary(10)
    img.gray.invert()
    img.gray.close((10, 10))
    img.gray.dilate((15, 15))
    img.gray.show(showPos)
    return img.gray.image


filename = ["../../img/LARVAS_1.jpg", "../../img/LARVAS_2.jpg", "../../img/LARVAS_3.jpg"]

posArray = [231, 232, 233]

for i in range(len(filename)):

    original = Img(cv2.imread(filename[i]))
    showImage(original.BGRToRGB(), 311)
    result = Img(cv2.bitwise_and(removeBinary(filename[i], 323), removeBinaryRelative(filename[i], 324)))
    while(result.checkForRemovableObjects()):
        result.removeObjectsBySize(0, 25)
    result.show(313)
    plt.show()

    original = Image(filename[i])
    original.gray.window()
    showImage(original.gray.grayToBGR(), 121)
    positions = result.markObjects(original.original.image, [255, 0, 0])
    showImage(original.original.image, 122)
    plt.show()

    print("\n------------------------------------")
    print(f"Encountered {len(positions)} larvae in {filename[i]}.")
    for j in range(len(positions)):
        print(f"#{j+1}: {positions[j].x} x {positions[j].y}")

plt.show()
