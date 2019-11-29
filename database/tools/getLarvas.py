import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)

def removeBinary(filename, threshold, showPos):
    img = Image(filename)
    img.gray.getWindowed()
    img.gray.windowed.getBinary(threshold)
    img.gray.windowed.binary.invert()
    img.gray.windowed.binary.floodFill()
    img.gray.windowed.binary.removeObjectsBySize(0, 100)
    img.gray.windowed.binary.show(showPos)
    return Img(img.gray.windowed.binary.image)

filename = "../LARVAS_4.jpg"

original = cv2.imread(filename)

showImage(cv2.imread(filename), 311)
sum1 = removeBinary(filename, 150, 323)
sum2 = removeBinary(filename, 80, 324)
result = Img(cv2.add(sum1.image, sum2.image))
result.show(313)
plt.show()

result.writeObjects(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), "grayscaleImg")

plt.show()