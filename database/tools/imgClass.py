import matplotlib.pyplot as plt
from os import path, makedirs
import numpy as np
import math
import cv2
from time import time

class Object:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = []
        self.info = ""

class Img:
    #======================================INIT=======================================
    def __init__(self, img):
        self.image = img

    #============================IMAGE-REPLACING-FUNCTIONS============================
    #Functions that replaces the target image by the transformed one

    #---BGRToGray---#
    def BGRToGray(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = image

    #---Binary---#
    def binary(self, limit = 127):
        binary = self.image
        binary[binary >= limit] = 255
        binary[binary < limit] = 0
        self.image = binary

    #---Blur---#
    def blur(self, ksize = (3, 3)):
        self.image = cv2.blur(self.image, ksize)

    #---Canny---#
    def canny(self, minThreshold, maxThreshold):
        canny = cv2.Canny(self.image, minThreshold, maxThreshold)
        self.image = canny

    #---Close---#
    def close(self, ksize = (20, 20), ktype = cv2.MORPH_ELLIPSE):
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, cv2.getStructuringElement(ktype, ksize))

    #---Dilate---#
    def dilate(self, ksize = (3, 3)):
        kernel = np.ones((ksize))
        self.image = cv2.dilate(self.image, kernel)

    #---Erode---#
    def erode(self, ksize = (3, 3)):
        kernel = np.ones((ksize))
        self.image = cv2.erode(self.image, kernel)

    #---Flood Fill---#
    def floodFill(self, dstPixel = (0, 0)):
        cv2.floodFill(self.image, np.zeros((self.image.shape[0]+ 2, self.image.shape[1] + 2), dtype='uint8'), (0, 0), 128)
        self.image[self.image < 1] = 255
        self.image[self.image <= 128] = 0

    #---Gaussian Blur---#
    def gaussBlur(self, ksize = (3, 3), sigma = 3):
        self.image = cv2.GaussianBlur(self.image, ksize, sigma)

    #---GrayToBGR---#
    def grayToBGR(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        self.image = image

    #---Insert Border---#
    def insertBorder(self, top, bottom, left, right, borderType):
        self.image = cv2.copyMakeBorder(self.image, top, bottom, left, right, borderType)
        self.borders = [top, bottom, left, right]

    #---Invert---#
    def invert(self):
        self.image = cv2.bitwise_not(self.image)

    #---Laplacian---#
    def laplacian(self):
        laplacian = cv2.Laplacian(self.image, -1)
        self.image = laplacian

    #---Log---#
    def log(self):
        result = np.zeros(self.image.shape)
        for y in range(result.shape[0]):
            for x in range(result.shape[1]):
                result[y,x] = (255/math.log(256)) * math.log(self.image[y, x] + 1)
        self.image = result.astype('uint8')

    #---Mark Objects---#
    def markObjects(self, dst, color):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(dst, (x - w//3, y - h//3), (x + w + w//3, y + h + h//3), color, 5)

    #---Open---#
    def open(self, ksize = (20, 20), ktype = cv2.MORPH_ELLIPSE):
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)))

    #---Power---#
    def power(self, factor):
        powerImage = (255/255**factor) * (self.image ** factor)
        self.image = powerImage.astype("uint8")

    #---Pyr Down---#
    def pyrDown(self, times = 1):
        for i in range(times):
            self.image = cv2.pyrDown(self.image)

    #---Pyr Up---#
    def pyrUp(self, times = 1):
        for i in range(times):
            self.image = cv2.pyrUp(self.image)

    #---Remove Border---#
    def removeBorder(self):
        img = self.image
        border = self.borders
        self.image = img[border[0]:img.shape[0] - border[1], border[2]:img.shape[1] - border[3]]
        self.borders = [0, 0, 0, 0]

    #---Remove Objects by Size---#
    def removeObjectsBySize(self, areaMin = 0, minPercentOfNonWhite = 20):
        imgArea = self.image.shape[0]*self.image.shape[1]
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(areaMin <= cv2.contourArea(cnt) <= imgArea * 0.001 or \
                (cv2.countNonZero(self.image[y:y+h, x:x+w]) < h*w*minPercentOfNonWhite/100) or \
                h > w*5 or \
                w > h*5 or \
                h < self.image.shape[0]*0.05 or \
                w < self.image.shape[1]*0.05):
                self.image[y:y+h, x:x+w] = 0
            if(w > self.image.shape[1] / 4 or h > self.image.shape[0] / 4):
                cv2.floodFill(self.image, np.zeros((self.image.shape[0]+ 2, self.image.shape[1] + 2), dtype='uint8'), (cnt[0][0][0], cnt[0][0][1]), 0)

    #---Remove Objects Smaller Than---#
    def removeObjectsSmallerThan(self, size):
        result = self.image
        counter = 0
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            counter += 1
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(w < size[0] or h < size[1]):
                result[y:y+h, x:x+w] = 0
                #cv2.rectangle(result, (x, y), (x+w, y+h), 128, 1)
        self.image = result

    #---Sepia---#
    def sepia(self):
        sepia = np.zeros(self.image.shape)
        img = self.image
        sepia[:, :, 1] = img[:, :, 0] * 0.349 + img[:, :, 1] * 0.686 + img[:, :, 2] * 0.168
        sepia[:, :, 2] = img[:, :, 0] * 0.272 + img[:, :, 1] * 0.534 + img[:, :, 2] * 0.131
        sepia[:, :, 0] = img[:, :, 0] * 0.393 + img[:, :, 1] * 0.769 + img[:, :, 2] * 0.189
        sepia[sepia > 255] = 255
        self.image = sepia.astype('uint8')

    #---Sobel---#
    def sobel(self):
        sobel = cv2.add(cv2.Sobel(self.image, -1, 0, 1), cv2.Sobel(self.image, -1, 1, 0))
        self.image = sobel

    #---Window---#
    def window(self, minLimit = np.inf, maxLimit = 0):
        functionTime = time()
        result = np.array(self.image)
        imgArea = (self.image.shape[0] * self.image.shape[1])
        #-Getting an array to store the amount of pixels of each light intensity-#
        intensities = np.histogram(self.image, bins=range(256))
        intensities = np.array(intensities[0])
        minThreshold, maxThreshold = 0, 0

        #-Getting the minimum and the maximum threshold-#
        maximum = max(intensities)
        minimum = min(intensities)
        twoPercentOfPixels = sum(intensities) * 0.02

        for i in range(0, 255):
            if(intensities[i] > twoPercentOfPixels):
                minThreshold = i
                break
            if(i > 0):
                intensities[i + 1] += intensities[i]
                intensities[i] = 0

        for i in range(254, 0, -1):
            if(intensities[i] > twoPercentOfPixels):
                maxThreshold = i
                break
            intensities[i - 1] += intensities[i]
            intensities[i] = 0

        #-Zero now becomes minThreshold and 255 becomes maxThreshold, expanding the light scope-#
        if(minThreshold < minLimit and maxThreshold > maxLimit):
            operation = (255/(maxThreshold - minThreshold))
            result = (self.image.astype('float32') - minThreshold) * operation
            result[result > 255] = 255
            result[result < 0] = 0
        self.image = result.astype('uint8')

    #---Window if Necessary---#
    def windowIfNecessary(self, minLimit, maxLimit):
        functionTime = time()
        result = np.array(self.image)
        imgArea = (self.image.shape[0] * self.image.shape[1])
        #-Getting an array to store the amount of pixels of each light intensity-#
        intensities = np.histogram(self.image, bins=range(256))
        intensities = np.array(intensities[0])
        minThreshold, maxThreshold = 0, 0

        #-Getting the minimum and the maximum threshold-#
        maximum = max(intensities)
        minimum = min(intensities)
        twoPercentOfPixels = sum(intensities) * 0.02

        for i in range(0, 255):
            if(intensities[i] > twoPercentOfPixels):
                minThreshold = i
                break
            if(i > 0):
                intensities[i + 1] += intensities[i]
                intensities[i] = 0

        for i in range(254, 0, -1):
            if(intensities[i] > twoPercentOfPixels):
                maxThreshold = i
                break
            intensities[i - 1] += intensities[i]
            intensities[i] = 0



        #-Zero now becomes minThreshold and 255 becomes maxThreshold, expanding the light scope-#
        if(minThreshold < minLimit and maxThreshold > maxLimit):
            operation = (255/(maxThreshold - minThreshold))
            result = (self.image.astype('float32') - minThreshold) * operation
            result[result > 255] = 255
            result[result < 0] = 0

        self.image = result.astype('uint8')

    #============================TOOLS============================
    #------------Functions that do not alter the image------------

    #---BGRToGray---#
    def BGRToGray(self):
        result = self.image
        return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    #---BGRToRGB---#
    def BGRToRGB(self):
        result = self.image
        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    #---Check for Removable Objects---#
    def checkForRemovableObjects(self, areaMin = 0, sizeMax = 500, minPercentOfNonWhite = 20):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgArea = self.image.shape[0]*self.image.shape[1]
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(areaMin <= cv2.contourArea(cnt) <= imgArea * 0.001 or \
                (w > self.image.shape[1] / 4 or h > self.image.shape[0] / 4) or \
                (cv2.countNonZero(self.image[y:y+h, x:x+w]) < h*w*minPercentOfNonWhite/100) or \
                h > w*5 or \
                w > h*5 or 
                h < self.image.shape[0]*0.05 or \
                w < self.image.shape[1]*0.05):
                return True
        return False

    #-Count Objects-#
    def countObjects(self):
        contours, hier = cv2.cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return len(contours)

    #---Get Binary Threshold Based on Corners---#
    def getBinaryThresholdBasedOnCorners(self):
        sizeX, sizeY = self.image.shape[0], self.image.shape[1]
        topLeftPixel = min(200, int(self.image[0,0]))
        topRightPixel = min(200, int(self.image[0, sizeX-1]))
        bottomLeftPixel = min(200, int(self.image[sizeY-1, 0]))
        bottomRightPixel = min(200, int(self.image[sizeY-1, sizeX-1]))
        thresh = (topLeftPixel + topRightPixel + bottomLeftPixel + bottomRightPixel) // 4
        thresh = (thresh + (self.image[sizeY//2, sizeX//2]//4)) // 2
        return thresh

    #---Get Relative Threshold---#
    def getRelativeThreshold(self):
        imgArea = (self.image.shape[0] * self.image.shape[1])
        #-Getting an array with 256 positions containing the percentage of each light intensity in the image-#
        intensities = np.histogram(self.image, bins=range(256))
        intensities = np.array(intensities[0])
        result = 255
        minimum = min(intensities)
        for i in range(255):
            if(intensities[i] == minimum):
                return i
        
    #---GrayToBGR---#
    def grayToBGR(self):
        result = self.image
        return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    #---Show---#
    def show(self, pos = 111, title = "", effect = None):
        plot = plt.subplot(pos)
        plot.set_title(title)
        plot.set_yticks([])
        plot.set_xticks([])
        plot.imshow(cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR), cmap = effect)

    #---Show Histogram---#
    def showHistogram(self, pos = 111):
        intervals = range(256)
        intensities = np.zeros(256)
        #-Getting an array with 256 positions containing the percentage of each light intensity in the image-#
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                g = self.image[y, x]
                intensities[g] += 100/(self.image.shape[0] * self.image.shape[1])
        plot = plt.subplot(pos)
        plot.set_title("Light intensity in picture")
        plot.set_xlabel("Intensity")
        plot.bar(intervals, intensities, align = "edge", width = 3)

    #---Write Objects---#
    def writeObjects(self, originalImage, csv, pathName, initialCounterValue = 0):
        counter = initialCounterValue
        #-Creating an img/ folder-#
        if not path.exists(pathName + "/img"):
            makedirs(pathName + "/img")
        #-Getting the image's objects' info-#
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            #-Adding borders and cutting the objects from the image-#
            nW, nH = w//5, h//5
            img = cv2.copyMakeBorder(originalImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=255)
            img = img[y:y + h + nH * 2, x:x + w + nW * 2]
            filename = pathName + "/img/" + str(counter) + ".png"
            cv2.imwrite(filename, cv2.resize(img, (64, 64)))
            #-Writing in the csv files-#
            csv.train.write(f"{filename},1\n")
            csv.predict.write(f"{filename}\n")
            counter += 1
        return counter

    #============================GET-FUNCTIONS============================
    #Functions that create a new Img attribute with the transformed image
    
    #---Crop---#
    def crop(self, x, y, w, h):
        result = self.image
        return result[y:y+h, x:x+w]

    #---get Channels---#
    def getChannels(self):
        self.B = Img(self.image[:, :, 0])
        self.G = Img(self.image[:, :, 1])
        self.R = Img(self.image[:, :, 2])

    #---Get Binary BGR---#
    def getBinaryBGR(self, limitB = 1, limitG = 1, limitR = 1):
        binaryB = self.image[:, :, 0]
        binaryB[binaryB >= limitB] = 255
        binaryB[binaryB < limitB] = 0
        self.binaryB = Img(binaryB)

        binaryG = self.image[:, :, 1]
        binaryG[binaryG >= limitG] = 255
        binaryG[binaryG < limitG] = 0
        self.binaryG = Img(binaryG)

        binaryR = self.image[:, :, 2]
        binaryR[binaryR >= limitR] = 255
        binaryR[binaryR < limitR] = 0
        self.binaryR = Img(binaryR)

class Image:
    def __init__(self, filename):
        self.original = Img(cv2.cvtColor(cv2.imread(filename), cv2.COLOR_RGB2BGR))
        self.gray = Img(cv2.cvtColor(self.original.image, cv2.COLOR_BGR2GRAY))

def toBGR(image):
    result = image
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

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

def findFarthestPixels(image):
    pyrDownImage = cv2.resize(image, (image.shape[1] // 5, image.shape[0] // 5))
    contours, hier = cv2.findContours(pyrDownImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largestContour = getLargestContour(contours)
    maxPoint1, maxPoint2, maxLength = findFarthestPixelsTestingProcess(contours, largestContour)
    return tuple(maxPoint1*5), tuple(maxPoint2*5), int(maxLength*5)

def toGray(image):
    result = image
    return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

def showImage(image, pos = 111, title = "", effect = None):
    plot = plt.subplot(pos)
    plot.set_title(title)
    plot.set_yticks([])
    plot.set_xticks([])
    plot.imshow(image, cmap = effect)