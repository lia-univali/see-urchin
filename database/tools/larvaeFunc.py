from os import path, makedirs
import numpy as np
from imgClass import *
import cv2
from time import time

class Larvae:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.length = 0
        self.evolStage = "Unknown"
        self.image = []
        self.image6464 = []
        self.binaryImage = []
        self.srcImgIndex = 0

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
        self.larvaes = []

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
'''
def processLarvae(filename):
    img = Image(filename)
    #img.gray.window()
    img.gray.windowIfNecessary(30, 200)
    img.gray.image = np.array(255*(img.gray.image/255)**2, dtype='uint8')
    
    #img.gray.show(131)
    
    #img2 = Img(np.array(img.gray.image))
    img.gray.binary(25)

    #thresh = img.gray.getRelativeThreshold()
    #print(thresh)
    #img.gray.binary(thresh)
    img.gray.invert()
    
    img.gray.show(132)
    
    #img.gray.close((10, 10))
    #img.gray.dilate((10, 10))

    #img2.show(232)
    #img2.invert()
    #img2.show(235)
    #if(img2.image.shape[0] > 1000 and img2.image.shape[1] > 1000):
    #    img2.erode()
    #img2.show(233)
    #return Img(cv2.bitwise_and(img.gray.image, img2.image))
    return Img(img.gray.image)
'''

def processLarvae(filename):
    img = Image(filename)
    nW = img.gray.image.shape[0] // 50
    nH = img.gray.image.shape[1] // 50
    img.gray.image = np.array(img.gray.image[nH:img.gray.image.shape[0] - nH, nW:img.gray.image.shape[1] - nW])
    #img.gray.window(50, 200)
    img.gray.image = np.array(255*(img.gray.image/255)**2, dtype='uint8')
    img.gray.show(131)
    img.gray.binary(25)
    img.gray.invert()
    img.gray.show(132)
    img.gray.image = cv2.copyMakeBorder(img.gray.image, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=0)
    return Img(img.gray.image)


def getLarvaeLength(binaryImage):
    contours, hier = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    (x,y), radius = cv2.minEnclosingCircle(contours[getLargestContour(contours)])
    return int(2*radius)

def getInfoFromContour(contour, binaryImage, srcImage, srcImageFilenameIndex):
    (x, y, w, h) = cv2.boundingRect(contour)
    nW, nH = w//2, h//2
    img = cv2.copyMakeBorder(srcImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    binImg = cv2.copyMakeBorder(binaryImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    larvaeTemp = Larvae(x, y, w, h)
    larvaeTemp.image = np.array(img[y:y+h+nH*2, x:x+w+nW*2])
    larvaeTemp.image6464 = img[y:y+h+nH*2, x:x+w+nW*2]
    larvaeTemp.image6464 = np.array(cv2.resize(larvaeTemp.image6464, (64, 64)))
    larvaeTemp.binaryImage = np.array(binImg[y:y+h+nH*2, x:x+w+nW*2])
    larvaeTemp.srcImgIndex = srcImageFilenameIndex
    binaryImageFiltered = removeObjectsSmallerThan(larvaeTemp.binaryImage, (int(larvaeTemp.binaryImage.shape[1]) // 3, int(larvaeTemp.binaryImage.shape[0]) // 3))
    larvaeTemp.length = getLarvaeLength(binaryImageFiltered)
    return larvaeTemp

def getObjectInfo(contours, binaryImage, srcImage, imageArrayIndex):
    larvaeArray = []
    for cnt in contours:
        larvaeArray += [getInfoFromContour(cnt, binaryImage, srcImage, imageArrayIndex)]
    larvaeCounter = 0
    eggCounter = 0
    for i in range(len(larvaeArray)):
        larvaeArray[i].evolStage = classifyLarvae(larvaeArray[i].binaryImage)
    return larvaeArray, larvaeCounter, eggCounter

def classifyLarvae(image):
    currentImage = Img(image)
    circleArray = cv2.HoughCircles(currentImage.image, cv2.HOUGH_GRADIENT, 1, 64, param1=80, param2=20, minRadius=10, maxRadius=42)
    currentImage.window()
    currentImage.binary(currentImage.getRelativeThreshold())
    currentImage.invert()
    #-Checking roundness and size to indentify the evolutionary stage-#
    if(not(circleArray is None) and (22 < circleArray[0, 0, 0] < 44) and (22 < circleArray[0, 0, 1] < 44) and cv2.countNonZero(currentImage.image) < 1100):
        return "Egg"
    else: 
        return "Larvae"
    if circleArray is None:
        return "Unknown"

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
    contours, hier = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        #-Inserts the position, size, evolutionary stage and image in the array-#
        (x, y, w, h) = cv2.boundingRect(cnt)
        nW, nH = w//2, h//2
        img = cv2.copyMakeBorder(srcImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        binImg = cv2.copyMakeBorder(binaryImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        larvaeTemp = Larvae(x, y, w, h)
        larvaeTemp.image = np.array(img[y:y+h+nH*2, x:x+w+nW*2])
        larvaeTemp.image6464 = img[y:y+h+nH*2, x:x+w+nW*2]
        larvaeTemp.image6464 = np.array(cv2.resize(larvaeTemp.image6464, (64, 64)))

        larvaeTemp.binaryImage = np.array(binImg[y:y+h+nH*2, x:x+w+nW*2])

        larvaeTemp.srcImgIndex = srcImageFilenameIndex
        positions.append(larvaeTemp)
    return positions