import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)

def removeBinary(filename, threshold):
    img = Image(filename)
    img.gray.getWindowed()
    img.gray.windowed.getBinary(threshold)
    img.gray.windowed.binary.invert()
    img.gray.windowed.binary.floodFill()
    img.gray.windowed.binary.removeObjectsBySize(0, 4000)
    return Img(img.gray.windowed.binary.image)

filename = "../../LARVAS_1.jpg"

original = cv2.imread(filename)

sum1 = removeBinary(filename, 80)
sum2 = removeBinary(filename, 40)
result = Img(cv2.add(sum1.image, sum2.image))

result.writeObjects(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), "../regular/img", 0)
print(f"from {filename}.")
plt.show()