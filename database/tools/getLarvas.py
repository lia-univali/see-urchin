import numpy as np
from imgClass import *
import cv2
from os import path, makedirs
import sys
sys.setrecursionlimit(10**6)

def removeBinary(filename, threshold):
    img = Image(filename)
    img = img.gray.getWindowed()
    img = img.getBinary(threshold)
    img.invert()
    img.floodFill()
    while(img.checkForRemovableObjects()):
        img.removeObjectsBySize()
    return img.image

filename = ["../../LARVAS_1.jpg", 
            "../../LARVAS_2.jpg",
            "../../LARVAS_3.jpg",
            "../../LARVAS_4.jpg"]

pathName = path.dirname(path.realpath(__file__)) + "/" + input("Type the path in which the images will be saved: ")

if not path.exists(pathName):
    makedirs(pathName)
counter = 0
csvFile = open(pathName + "/train.csv", 'w+')
csvFile.write("image_path,class\n")
for name in filename:
    print(f"Loading {name}...")
    original = cv2.imread(name)
    result = Img(cv2.add(removeBinary(name, 50), removeBinary(name, 25)))
    counter = result.writeEachObject(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), csvFile, pathName, counter)
    cv2.destroyAllWindows()
    print(f"from {name}.")