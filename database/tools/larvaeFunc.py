from os import path, makedirs
import numpy as np
from imgClass import *
import cv2

class Larvae:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = []
        self.srcImgIndex = 0
        self.evolStage = "Unknown"

class CSV: 
    def __init__(self, path):
        self.train = open(path + "/train.csv", 'w+')
        self.predict = open(path + "/predict.csv", 'w+')
        self.train.write("image_path,class\n")
        self.predict.write("image_path,class\n")

class LarvaeImage:
    def __init__(self, filename):
        self.image = cv2.imread(filename)
        self.numberOfLarvae = 0
        self.numberOfEggs = 0
        self.numberOfAdults = 0

#---Get Images From Array---#
def getImagesFromArray(array):
    resultArray = []
    for i in range(len(array)):
        resultArray.append(LarvaeImage(array[i]))
    return resultArray

#---Process Larvae Soft---#
def processLarvaeSoft(filename):
    img = Image(filename)
    img.gray.window()
    thresh = img.gray.getRelativeThreshold()
    img.gray.binary(thresh * 1.1)
    img.gray.invert()
    img.gray.floodFill()
    if(img.gray.image.shape[0] > 1000 and img.gray.image.shape[1] > 1000):
        img.gray.erode()
    return img.gray.image

#---Process Larvae Hard---#
def processLarvaeHard(filename):
    img = Image(filename)
    img.gray.window()
    img.gray.binary(10)
    img.gray.invert()
    img.gray.close((10, 10))
    img.gray.dilate((15, 15))
    return img.gray.image

#---saveWithChoice---#
def saveWithChoice(filename, src, csv):
    evolStage = ""
    #-Creates a window showing the image to be saved-#
    cv2.namedWindow("Save?", cv2.WINDOW_NORMAL)
    cv2.imshow("Save?", src)
    cv2.resizeWindow("Save?", 256, 256)
    #-Waits for user input-#
    key = cv2.waitKey(0)
    if(key == 115 or key == 100):
        cv2.imwrite(filename, src)
        #-If "S", saves the picture and classifies it as "Egg"-#
        if(key == 115):
            csv.train.write(f"{filename},1\n")
            evolStage = "Egg"
        #-If "D", saves the picture and classifies it as "Larvae"-#
        else:
            csv.train.write(f"{filename},0\n")
            evolStage = "Larvae"
        csv.predict.write(f"{filename}\n")
    return evolStage

#---getObjectInfo---#
def getLarvaeInfo(binaryImage, srcImage, srcImageFilenameIndex):
    #-Makes an empty array to include the larvaes' info-#
    positions = []
    img = cv2.copyMakeBorder(srcImage, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    contours, hier = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        #-Inserts the position, size, evolutionary stage and image in the array-#
        (x, y, w, h) = cv2.boundingRect(cnt)
        larvaeTemp = Larvae(x, y, w, h)
        larvaeTemp.image = img[y:y+h+100, x:x+w+100]
        larvaeTemp.image = cv2.resize(larvaeTemp.image, (64, 64))
        larvaeTemp.srcImgIndex = srcImageFilenameIndex
        positions.append(larvaeTemp)
    return positions