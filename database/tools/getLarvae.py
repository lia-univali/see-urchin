import numpy as np
from imgClass import *
from report import *
from larvaeFunc import *
import cv2
from os import path, makedirs
import matplotlib.pyplot as pl
from time import time    

def getLarvae(startImage=0, endImage=1):
    #-Creating path-#
    pathName = path.dirname(path.realpath(__file__)) + "/../results/" + input("Type the folder in which the images will be saved: ")
    if not path.exists(pathName):
        makedirs(pathName)

    #---Creating img folder---#
    if not path.exists(pathName + "/img"):
        makedirs(pathName + "/img")

    #-Creating HTML-#
    htmlFile = open(pathName + "/report.html", 'a+')
    HTMLbegin(htmlFile)
    
    totalTime = time()
    numberOfLarvaInImage = []
    totalLarvaeCounter = 0

    #-Main loop - Image processing-#
    for imageIndex in range(startImage, endImage):
        #-Image variables declaration-#
        filename = f"../input_images/0 ({imageIndex+1}).jpg"
        currentImage = LarvaeImage(filename)
        imageMark = LarvaeImage(filename)

        #-Image processing-#
        print(f"Processing {filename}...")
        binaryFiltered = processLarvae(filename)
        while(binaryFiltered.checkForRemovableObjects()):
            binaryFiltered.removeObjectsBySize()        

        #-Larvae counting-#
        contours, hier = cv2.findContours(binaryFiltered.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        currentImage.numberOfLarvae = len(contours)

        #-Marking and saving marked image-#
        binaryFiltered.markObjects(imageMark.image, [0, 0, 255])
        cv2.imwrite(f"{pathName}/markedImage{imageIndex}.jpg", imageMark.image)
        
        #-Getting larvae's info-#
        currentImage.larvaes, currentImage.numberOfAdults, currentImage.numberOfEggs = getObjectInfo(contours, binaryFiltered.image, currentImage.image, imageIndex)

        #-Saving Images-#
        for i in range(currentImage.numberOfLarvae):
            cv2.imwrite(f"{pathName}/img/{totalLarvaeCounter+i}.jpg", currentImage.larvaes[i].image6464)
        
        #-Building HTML-#
        HTMLBigPicture(htmlFile, f"../{filename}", currentImage, imageIndex + 1 - startImage)
        HTMLBigPicture(htmlFile, f"{pathName}/markedImage{imageIndex}.jpg", currentImage, imageIndex + 1 - startImage)
        HTMLlineBreak(htmlFile)
        HTMLwrite(htmlFile, "<div>")
        if(currentImage.larvaes is not None):
            for i in range(currentImage.numberOfLarvae):
                HTMLBar(htmlFile, f"{pathName}/img/{totalLarvaeCounter + i}.jpg", currentImage.larvaes[i], totalLarvaeCounter + 1 + i)
        HTMLwrite(htmlFile, "</div>")
        HTMLlineBreak(htmlFile)
        
        totalLarvaeCounter += currentImage.numberOfLarvae

    HTMLend(htmlFile)
    print("Done!")
    print(f"It took {round(time() - totalTime, 3)} seconds.")
    return 0