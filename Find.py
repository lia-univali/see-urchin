import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)

def removeBinary(filename, threshold, showPos):
    img = Image(filename)
    img.gray.getWindowed()
    img.gray.windowed.blur((5, 5))
    img.gray.windowed.getBinary(threshold)
    img.gray.windowed.binary.invert()
    img.gray.windowed.binary.floodFill()
    img.gray.windowed.binary.removeObjectsBySize(0, 4000)
    img.gray.windowed.binary.show(showPos)
    return Img(img.gray.windowed.binary.image)

filename = "LARVAS_1.jpg"

original = cv2.imread(filename)

showImage(cv2.imread(filename), 311)
sum1 = removeBinary(filename, 80, 323)
sum2 = removeBinary(filename, 40, 324)
result = Img(cv2.add(sum1.image, sum2.image))
result.show(313)
plt.show()

showImage(original, 121)
result.markObjects(original, [255, 0, 0])
showImage(original, 122)


plt.show()