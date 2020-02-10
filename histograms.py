import matplotlib.pyplot as plt
import numpy as np
from imgClass import *
import cv2
import sys
sys.setrecursionlimit(10**6)


filename = ["img/LARVAS_1.jpg", "img/LARVAS_2.jpg", "img/LARVAS_3.jpg"]

posArray = [231, 232, 233]

for i in range(len(filename)):
    img = Image(filename[i])
    img.gray.window()
    img.gray.getRelativeThreshold()
    img.gray.show(posArray[i])
    img.gray.showHistogram(posArray[i] + 3)

plt.show()
