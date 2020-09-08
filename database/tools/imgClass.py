import matplotlib.pyplot as plt
from os import path, makedirs
import numpy as np
import math
import cv2
from time import time

class Img:
    #======================================INIT=======================================
    def __init__(self, img):
        self.image = img

    #============================IMAGE-REPLACING-FUNCTIONS============================
    #Functions that replaces the target image by the transformed one

    #---Binary---#
    def binary(self, limit = 127):
        binary = self.image
        binary[binary >= limit] = 255
        binary[binary < limit] = 0
        self.image = binary

    #---Dilate---#
    def dilate(self, ksize = (3, 3)):
        kernel = np.ones((ksize))
        self.image = cv2.dilate(self.image, kernel)

    #---Flood Fill---#
    def floodFill(self, dstPixel = (0, 0)):
        cv2.floodFill(self.image, np.zeros((self.image.shape[0]+ 2, self.image.shape[1] + 2), dtype='uint8'), (0, 0), 128)
        self.image[self.image < 1] = 255
        self.image[self.image <= 128] = 0

    #---Invert---#
    def invert(self):
        self.image = cv2.bitwise_not(self.image)

    #---Mark Objects---#
    def markObjects(self, dst, color):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            size = max(w, h)
            borderSize = size//2
            cutTop = y - (borderSize * 3 - h)
            cutBottom = cutTop + size * 2 
            cutLeft = x - (borderSize * 3 - w)
            cutRight = cutLeft + size * 2 
            cv2.rectangle(dst, (cutLeft, cutTop), (cutRight, cutBottom), color, 5)

    #---Remove Objects by Size---#
    def removeObjectsBySize(self, minPercentOfNonWhite = 20):
        imgArea = self.image.shape[0]*self.image.shape[1]
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if((cv2.countNonZero(self.image[y:y+h, x:x+w]) < h*w*minPercentOfNonWhite/100) or \
                h > w*4 or \
                w > h*4 or \
                h < self.image.shape[0]*0.035 or \
                w < self.image.shape[1]*0.035):
                self.image[y:y+h, x:x+w] = 0
            elif(w > self.image.shape[1] / 4 or h > self.image.shape[0] / 4):
                cv2.floodFill(self.image, np.zeros((self.image.shape[0]+ 2, self.image.shape[1] + 2), dtype='uint8'), (cnt[0][0][0], cnt[0][0][1]), 0)

    #============================TOOLS============================
    #------------Functions that do not alter the image------------

    #---Check for Removable Objects---#
    def checkForRemovableObjects(self):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgArea = self.image.shape[0]*self.image.shape[1]
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(w > self.image.shape[1] / 4 or h > self.image.shape[0] / 4 or \
                (cv2.countNonZero(self.image[y:y+h, x:x+w]) < h*w*20/100) or \
                h > w*4 or \
                w > h*4 or \
                h < self.image.shape[0]*0.035 or \
                w < self.image.shape[1]*0.035):
                return True
        return False
            
    #---Show---#
    def show(self, title = ""):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, self.image)

class Image:
    def __init__(self, filename):
        try:
            self.original = Img(cv2.cvtColor(cv2.imread(filename), cv2.COLOR_RGB2BGR))
            self.gray = Img(cv2.cvtColor(self.original.image, cv2.COLOR_BGR2GRAY))
        except:
            print("\nAn error has occurred while loading the image.")
            print(" - Check if the image is located in database/input.")
            print(" - Check if the image is named \"0 ([any number]).jpg\".")
            quit()

def removeObjectsSmallerThan(image, size):
    result = np.array(image)
    counter = 0
    contours, hier = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        counter += 1
        (x, y, w, h) = cv2.boundingRect(cnt)
        if(w < size[0] or h < size[1]):
            result[y:y+h, x:x+w] = 0
    return result

def getLargestContour(contourArray):
    largestContour = 0
    for i in range(len(contourArray)):
        if(len(contourArray[i]) > len(contourArray[largestContour])):
            largestContour = i
    return largestContour