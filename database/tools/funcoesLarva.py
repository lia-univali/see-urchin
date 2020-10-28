from imgClass import *
import cv2

class Larva:
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

class LarvaImage:
    def __init__(self, filename):
        self.image = cv2.imread(filename)
        self.numberOfLarvae = 0
        self.numberOfEggs = 0
        self.numberOfAdults = 0
        self.larvaes = []

class LarvaeOperation:
    @staticmethod
    def processLarvae(filename):
        img = Image(filename)
        nW = img.gray.image.shape[0] // 50
        nH = img.gray.image.shape[1] // 50
        img.gray.image = np.array(img.gray.image[nH:img.gray.image.shape[0] - nH, nW:img.gray.image.shape[1] - nW])
        img.gray.image = np.array(255*(img.gray.image/255)**2, dtype='uint8')
        img.gray.binary(25)
        img.gray.dilate((3, 3))
        img.gray.invert()
        img.gray.image = cv2.copyMakeBorder(img.gray.image, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=0)
        return Img(img.gray.image)

    @staticmethod
    def __getLarvaeLength(binaryImage):
        contours, hier = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if(contours):
            (x,y), radius = cv2.minEnclosingCircle(
                contours[ImageFunction.getLargestContour(contours)]
            )
            return int(2*radius)
        else:
            return 0

    @staticmethod
    def __getLarvaeInfoFromContour(contour, binaryImage, srcImage, srcImageFilenameIndex):
        (x, y, w, h) = cv2.boundingRect(contour)

        #Tamanho da imagem/bordas nas imagens de proporção 1:1
        imgSize = max(w, h)
        border = imgSize//2

        #Aplicação das bordas na imagem original
        img = cv2.copyMakeBorder(
            srcImage,
            border,
            border,
            border,
            border,
            cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )

        #Aplicação das bordas na imagem binária
        binImg = cv2.copyMakeBorder(
            binaryImage,
            border,
            border,
            border,
            border,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )

        result = Larva(x, y, w, h)
        result.image = np.array(img[y:y+h*2, x:x+w*2])
        #result.binaryImage = np.array(binImg[y:y+h*2, x:x+w*2])

        #watershed
        binaryImageFiltered = ImageFunction.watershed(result.image)
        contours, hier = cv2.findContours(binaryImageFiltered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        (x, y, w, h) = cv2.boundingRect(contours[0])
        newImgSize = max(w, h)

        #Centralização da larva/Transormação em 1:1
        cutTop = max(y - (newImgSize - h), 0)
        cutBottom = cutTop + newImgSize
        cutLeft = max(x - (newImgSize - w), 0)
        cutRight = cutLeft + newImgSize

        result.image6464 = result.image[cutTop : cutBottom, cutLeft : cutRight]
        result.image6464 = np.array(cv2.resize(result.image6464, (64, 64)))

        result.binaryImage = binaryImageFiltered[cutTop : cutBottom, cutLeft : cutRight]
        result.binaryImage = np.array(cv2.resize(result.binaryImage, (64, 64)))

        result.length = LarvaeOperation.__getLarvaeLength(binaryImageFiltered)
        result.evolStage = LarvaeOperation.__classifyLarvae(result)
        return result

    @staticmethod
    def getLarvaeArray(contours, binaryImage, srcImage, imageArrayIndex):
        larvaeArray = []
        for cnt in contours:
            larvaeArray += [LarvaeOperation.__getLarvaeInfoFromContour(cnt, binaryImage, srcImage, imageArrayIndex)]
        larvaeCounter = 0
        eggCounter = 0
        for i in range(len(larvaeArray)):
            if(larvaeArray[i].evolStage == "Egg"):
                eggCounter += 1
            elif(larvaeArray[i].evolStage == "Larvae"):
                larvaeCounter += 1
        return larvaeArray, larvaeCounter, eggCounter

    @staticmethod
    def __classifyLarvae(larvae):
        if(abs(larvae.w - larvae.h) <= 20 and larvae.length <= 180): #larvae.length in pixels (180px is about 200µm)
            return "Egg"
        else:
            return "Larvae"
        if circleArray is None:
            return "Unknown"