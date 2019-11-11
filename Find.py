import matplotlib.pyplot as plt
import numpy as np
import imgClass
import cv2
import sys
sys.setrecursionlimit(10**6)

larvas = imgClass.Image("LARVAS_2.jpg")
larvas.gray.show(221)

larvas.gray.getWindowed()
larvas.gray.windowed.show(222)

larvas.gray.windowed.getBinary(90)
larvas.gray.windowed.binary.invert()
larvas.gray.windowed.binary.show(234)
larvas.gray.windowed.binary.floodFill()

larvas.gray.windowed.binary.show(235)

contours = larvas.gray.windowed.binary.removeObjectsBySize(0, 4000)


larvas.gray.windowed.binary.markObjects(larvas.gray.image)

larvas.gray.windowed.binary.show(236)

larvas.gray.show()


plt.show()