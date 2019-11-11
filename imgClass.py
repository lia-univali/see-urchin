import matplotlib.pyplot as plt
import numpy as np
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
        return image

    #---Blur---#
    def blur(self, ksize = (3, 3)):
        self.image = cv2.blur(self.image, ksize)

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
    def floodFill(self, color = 128, dstPixel = (0, 0)):
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
        return image

    #---Insert Border---#
    def insertBorder(self, top, bottom, left, right, borderType):
        self.image = cv2.copyMakeBorder(self.image, top, bottom, left, right, borderType)
        self.borders = [top, bottom, left, right]

    #---Invert---#
    def invert(self):
        self.image = cv2.bitwise_not(self.image)

    #---Mark Objects---#
    def markObjects(self, dst):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(dst, (x, y), (x+w, y+h), 128, 5)

    #---Open---#
    def open(self, ksize = (20, 20), ktype = cv2.MORPH_ELLIPSE):
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)))

    #---Power---#
    def power(self, factor):
        powerImage = np.zeros(self.image.shape)
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                powerImage[y,x] = (255/255**factor) * (self.image[y,x] ** factor)
        self.image = powerImage.astype('uint8')

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
    def removeObjectsBySize(self, sizeMin, sizeMax):
        contours, hier = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if(sizeMin <= cv2.contourArea(cnt) <= sizeMax or (w > 500 or h > 500)):
                self.image[y:y+h, x:x+w] = 0

    #============================TOOLS============================
    #Functions that do not alter the image
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

    #============================GET-FUNCTIONS============================
    #Functions that create a new Img attribute with the transformed image
    #---Get Inverted---#
    def getInverted(self):
        inverted = cv2.bitwise_not(self.image)
        self.inverted = Img(inverted)
        return inverted

    #---Get Blurred---#
    def getBlurred(self, ksize = (3, 3)):
        blurred = cv2.blur(self.image, ksize)
        self.blurred = Img(blurred)
        return blurred

    #---get Channels---#
    def getChannels(self):
        self.channelB = Img(self.image[:, :, 0])
        self.channelG = Img(self.image[:, :, 1])
        self.channelR = Img(self.image[:, :, 2])

    #---Get Gaussian Blurred---#
    def getGuaussianBlurred(self, ksize = (5, 5), sigma = 3):
        gaussBlurred = cv2.GaussianBlur(self.image, ksize, sigma)
        self.gaussBlurred = Img(gaussBlurred)
        return gaussBlurred

    #---Get Laplacian---#
    def getLaplacian(self):
        laplacian = cv2.Laplacian(self.image, -1)
        self.laplacian = Img(laplacian)
        return laplacian

    #---Get Sepia---#
    def getSepia(self):
        sepia = np.zeros(self.image.shape)
        img = self.image
        sepia[:, :, 2] = img[:, :, 0] * 0.272 + img[:, :, 1] * 0.534 + img[:, :, 2] * 0.131
        sepia[:, :, 1] = img[:, :, 0] * 0.349 + img[:, :, 1] * 0.686 + img[:, :, 2] * 0.168
        sepia[:, :, 0] = img[:, :, 0] * 0.393 + img[:, :, 1] * 0.769 + img[:, :, 2] * 0.189
        sepia[sepia > 255] = 255
        self.sepia = Img(sepia.astype('uint8'))
        return sepia.astype('uint8')

    #---Get Sobel---#
    def getSobel(self):
        sobel = cv2.add(cv2.Sobel(self.image, -1, 0, 1), cv2.Sobel(self.image, -1, 1, 0))
        self.sobel = Img(sobel)
        return sobel

    #---Get Canny---#
    def getCanny(self, min, max):
        canny = cv2.Canny(self.image, min, max)
        self.canny = Img(canny)
        return canny

    #---Get Binary---#
    def getBinary(self, limit = 1):
        binary = self.image
        binary[binary >= limit] = 255
        binary[binary < limit] = 0
        self.binary = Img(binary)
        return binary

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

    #---Get Windowed---#
    def getWindowed(self):
        minThreshold, maxThreshold = 255, 0
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                maxThreshold = max(maxThreshold, self.image[y, x])
                minThreshold = min(minThreshold, self.image[y, x])

        result = np.zeros(self.image.shape)
        result = (self.image - minThreshold) * (255/(maxThreshold - minThreshold))
        result[result > 255] = 255
        self.windowed = Img(result.astype('uint8'))
        return result.astype('uint8')


class Image:
    def __init__(self, filename):
        self.original = Img(cv2.cvtColor(cv2.imread(filename), cv2.COLOR_RGB2BGR))
        self.gray = Img(cv2.cvtColor(self.original.image, cv2.COLOR_BGR2GRAY))

def toBGR(image):
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def toGray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)