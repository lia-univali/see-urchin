import matplotlib.pyplot as plt
from os import path, makedirs
import numpy as np
import math
import cv2

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
    def binary(self, limit = 1):
        binary = self.image
        binary[binary >= limit] = 255
        binary[binary < limit] = 0
        self.image = binary

    #---Blur---#
    def blur(self, ksize = (3, 3)):
        self.image = cv2.blur(self.image, ksize)

    #---Canny---#
    def canny(self, min, max):
        canny = cv2.Canny(self.image, min, max)
        self.image = canny

    #---Close---#
    def close(self, ksize = (20, 20), ktype = cv2.MORPH_ELLIPSE):
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)))

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
            cv2.rectangle(dst, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 5)
        return len(contours)

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
            if(h > w*1.5):
                cv2.line(self.image, (x, y + (h//2)), (x+w, y + (h//2)), (0, 0, 0), 1)
            elif(w > h*1.5):
                cv2.line(self.image, (x + (w//2), y), (x + (w//2), y + h), (0, 0, 0), 1)
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(areaMin <= cv2.contourArea(cnt) <= imgArea * 0.001271 or (w > self.image.shape[1] / 4 or h > self.image.shape[0] / 4) or (cv2.countNonZero(self.image[y:y+h, x:x+w]) < h*w*minPercentOfNonWhite/100)):
                self.image[y:y+h, x:x+w] = 0

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
    def window(self):
        imgArea = self.image.shape[0] * self.image.shape[1]
        intensities = np.zeros(256)
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                g = self.image[y, x]
                intensities[g] += 100/imgArea
        minThreshold, maxThreshold = 0, 0

        for i in range(255, 0, -1):
            maxThreshold = intensities[i]
            if maxThreshold > 2:
                maxThreshold = i
                break
            intensities[i - 1] += intensities[i]
            intensities[i] = 0

        for i in range(255):
            minThreshold = intensities[i]
            if minThreshold > 2:
                minThreshold = i
                break
            intensities[i + 1] += intensities[i]
            intensities[i] = 0

        result = np.zeros(self.image.shape)
        result = (self.image.astype('float32') - minThreshold) * (255/(maxThreshold - minThreshold))
        result[result > 255] = 255
        result[result < 0] = 0
        self.image = result.astype('uint8')

    #============================TOOLS============================
    #Functions that do not alter the image

    #---Check for Removable Objects---#
    def checkForRemovableObjects(self, areaMin = 0, sizeMax = 500, minPercentOfNonWhite = 20):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgArea = self.image.shape[0]*self.image.shape[1]
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(h > w*1.5):
                return True
            elif(w > h*1.5):
                return True
            elif(areaMin <= cv2.contourArea(cnt) <= imgArea * 0.001271 or (w > self.image.shape[1] / 4 or h > self.image.shape[0] / 4) or (cv2.countNonZero(self.image[y:y+h, x:x+w]) < h*w*minPercentOfNonWhite/100)):
                return True
        return False

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
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                g = self.image[y, x]
                intensities[g] += 100/(self.image.shape[0] * self.image.shape[1])
        plot = plt.subplot(pos)
        plot.set_title("Light intensity in picture")
        plot.set_xlabel("Intensity")
        plot.bar(intervals, intensities, align = "edge", width = 0.3)

    #---Write Each Object---#
    def writeEachObject(self, originalImage, csvFileTrain, csvFilePredict, pathName, initialValue = 0):
        initialCounterValue = initialValue
        counter = initialCounterValue
        if not path.exists(pathName + "/img"):
            makedirs(pathName + "/img")

        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            nW = w//5
            nH = h//5
            img = cv2.copyMakeBorder(originalImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=255)
            img = img[y:y + h + nH * 2, x:x + w + nW * 2]
            filename = pathName + "/img/" + str(counter) + ".png"
            cv2.namedWindow(f"Save?")
            cv2.resizeWindow(f"Save?", 256, 256)
            cv2.imshow(f"Save?", img)
            key = cv2.waitKey(0)
            if(key == 115 or key == 100):
                cv2.imwrite(filename, cv2.resize(img, (64, 64)))
                print(f"Saved {filename};")
                counter += 1
                if(key == 115):
                    csvFileTrain.write(f"{filename},1\n")
                else:
                    csvFileTrain.write(f"{filename},0\n")
                csvFilePredict.write(f"{filename}\n")
            else:
                print("---Did not save picture---")
        print(f"Successfully saved {counter - initialCounterValue} images ", end="")
        return counter

    #---Write Objects---#
    def writeObjects(self, originalImage, path = "", initialValue = 0):
        initialCounterValue = initialValue
        counter = initialCounterValue
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            nW = w//5
            nH = h//5
            img = cv2.copyMakeBorder(originalImage, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=255)
            img = img[y:y + h + nH * 2, x:x + w + nW * 2]
            filename = path + "/" + str(counter) + ".png"
            cv2.imwrite(filename, cv2.resize(img, (64, 64)))
            counter += 1
        print(f"Successfully saved {counter - initialCounterValue} images ", end="")

    #============================GET-FUNCTIONS============================
    #Functions that create a new Img attribute with the transformed image
    
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

def toGray(image):
    return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

def showImage(image, pos = 111, title = "", effect = None):
        plot = plt.subplot(pos)
        plot.set_title(title)
        plot.set_yticks([])
        plot.set_xticks([])
        plot.imshow(image, cmap = effect)