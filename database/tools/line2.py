import numpy as np
from imgClass import *
from report import *
from larvaeFunc import *
import cv2
from os import path, makedirs
import matplotlib.pyplot as plt

def processLarvae(filename):
    return Img(cv2.bitwise_and(processLarvaeHard(filename), processLarvaeSoft(filename)))
    
if __name__ == "__main__":
    filename = ["../../img/LARVAS_1.jpg", 
                "../../img/LARVAS_2.jpg",
                "../../img/LARVAS_3.jpg"]

    #-Getting an array of images to be processed and an array of images to be marked-#
    imageArray = getImagesFromArray(filename)

    #-Initializes the array in which the larvaes' informations will be stored-#
    larvaeArray = []

    #---Image processing---#
    for i in range(len(imageArray)):
        print(f"Processing {filename[i]}...")
        result = processLarvae(filename[i])
        while(result.checkForRemovableObjects()):
            result.removeObjectsBySize(0, 25)

        #-Getting the number of larvaes in each image-#
        imageArray[i].numberOfLarvae -= len(larvaeArray)
        #-Getting the larvaes' positions and sizes-#
        larvaeArray += getLarvaeInfo(result.image, imageArray[i].image, i)
        imageArray[i].numberOfLarvae += len(larvaeArray)

    for i in range(46):
        binaryImageFiltered = removeObjectsSmallerThan(larvaeArray[i].binaryImage, (int(larvaeArray[i].binaryImage.shape[1]) // 3, int(larvaeArray[i].binaryImage.shape[0]) // 3))

        showImage(cv2.cvtColor(larvaeArray[i].binaryImage, cv2.COLOR_GRAY2BGR), 221)
        showImage(cv2.cvtColor(binaryImageFiltered, cv2.COLOR_GRAY2BGR), 222)
        showImage(cv2.Laplacian(cv2.cvtColor(binaryImageFiltered, cv2.COLOR_GRAY2BGR), -1), 223)
        point1, point2, maxLength = findFarthestPixels(binaryImageFiltered)
        larvaeArray[i].length = maxLength
        print(f"Larvae #{i+1}: {maxLength}px;")
        showImage(cv2.line(cv2.cvtColor(larvaeArray[i].image,cv2.COLOR_BGR2RGB), point1, point2, [255, 0, 0], 5), 224)

        plt.show()