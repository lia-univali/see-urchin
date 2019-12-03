import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)

def removeBinary(filename, threshold):
    img = Image(filename)
    img.gray.show(221)
    img.gray.getWindowed()
    img.gray.windowed.show(222)
    img.gray.windowed.getBinary(threshold)
    img.gray.windowed.binary.invert()
    img.gray.windowed.binary.show(223)
    img.gray.windowed.binary.floodFill()
    while(img.gray.windowed.binary.checkForRemovableObjects()):
        img.gray.windowed.binary.removeObjectsBySize()
    img.gray.windowed.binary.show(224)
    plt.show()
    return Img(img.gray.windowed.binary.image)

filename = "../../LARVAS_4.jpg"

original = cv2.imread(filename)

sum1 = removeBinary(filename, 50)
sum2 = removeBinary(filename, 25)
result = Img(cv2.add(sum1.image, sum2.image))

result.writeEachObject(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), "niggabean", 0)
print(f"from {filename}.")
plt.show()