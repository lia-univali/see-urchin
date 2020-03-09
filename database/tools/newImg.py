import numpy as np
from imgClass import *
from report import *
from larvaeFunc import *
import cv2
from os import path, makedirs
import matplotlib.pyplot as pl

if __name__ == "__main__":
    filename = []
    for i in range(500):
        print(i)
        filename.append(f"../../img/LARVAS/0 ({i+1}).jpg")

    #-Getting an array of images to be processed and an array of images to be marked-#
    imageArray = getImagesFromArray(filename)
    markedImagesArray = getImagesFromArray(filename)

    #-Initializes the array in which the larvaes' informations will be stored-#
    larvaeArray = []

    #---Image processing---#
    for i in range(len(imageArray)):
        print(f"Processing {filename[i]}...")
        result = processLarvae(filename[i])
        result.show(222)
        while(result.checkForRemovableObjects()):
            result.removeObjectsBySize(0, 25)

        #-Getting the number of larvaes in each image-#
        imageArray[i].numberOfLarvae -= len(larvaeArray)
        #-Getting the larvaes' positions and sizes-#
        larvaeArray += getLarvaeInfo(result.image, imageArray[i].image, i)
        imageArray[i].numberOfLarvae += len(larvaeArray)
        
        #-Marking Image-#
        result.markObjects(markedImagesArray[i].image, [0, 0, 255])

    for i in range(500):
        binaryImageFiltered = removeObjectsSmallerThan(larvaeArray[i].binaryImage, (int(larvaeArray[i].binaryImage.shape[1]) // 3, int(larvaeArray[i].binaryImage.shape[0]) // 3))
        result.show(223)
        showImage(cv2.cvtColor(imageArray[i].image, cv2.COLOR_RGB2BGR), 221)
        showImage(cv2.cvtColor(markedImagesArray[i].image, cv2.COLOR_RGB2BGR), 224)
        cv2.imwrite(f"saved/{i+1}.png", larvaeArray[i].image6464)
        plt.show()