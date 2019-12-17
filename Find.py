import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)

def removeBinary(filename, threshold, showPos):
    img = Image(filename)
    img.gray.window()
    img.gray.binary(threshold)
    img.gray.invert()
    img.gray.floodFill()
    if(img.gray.image.shape[0] > 1000 and img.gray.image.shape[1] > 1000):
        img.gray.erode()
    while(img.gray.checkForRemovableObjects()):
        img.gray.removeObjectsBySize()
    img.gray.show(showPos)
    return img.gray.image


filename = ["LARVAS_1.jpg", "LARVAS_2.jpg", "LARVAS_3.jpg", "LARVAS_4.jpg"]

for i in range(len(filename)):
    original = cv2.imread(filename[i])
    showImage(cv2.imread(filename[i]), 311)
    result = Img(cv2.add(removeBinary(filename[i], 50, 323), removeBinary(filename[i], 20, 324)))
    result.show(313)
    plt.show()

    showImage(original, 121)
    counter = result.markObjects(original, [255, 0, 0])
    showImage(original, 122)

    #plt.show()
    print(f"There are {counter} larvae in {filename[i]}")
