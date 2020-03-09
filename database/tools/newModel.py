import numpy as np
from imgClass import *
from report import *
from larvaeFunc import *
import cv2
from os import path, makedirs
import matplotlib.pyplot as pl
from time import time

def printTime(title, basedOnTime, logFile):
    logFile.write(f"{title}: {round(time() - basedOnTime, 3)};\n")
    print(f"{title}: {round(time() - basedOnTime, 3)};")

if __name__ == "__main__":
    #-Creating path-#
    pathName = path.dirname(path.realpath(__file__)) + "/../" + input("Type the folder in which the images will be saved: ")
    totalTime = time()
    if not path.exists(pathName):
        makedirs(pathName)

    #---Creating img folder---#
    if not path.exists(pathName + "/img"):
        makedirs(pathName + "/img")

    #-Creating HTML-#
    htmlFile = open(pathName + "/report.html", 'a+')
    timeLogFile = open(pathName + "/time.log", 'a+')
    HTMLbegin(htmlFile)

    numberOfLarvaInImage = []
    totalLarvaeCounter = 0

    '''''''''printTime("Made HTML and declared variables", totalTime, timeLogFile)'''
    numberOfImages = 150
    for imageIndex in range(50, numberOfImages):
        imageTime = time()
        localTime = time()
        print(f"------------------IMAGE {imageIndex + 1}------------------")
        timeLogFile.write(f"------------------IMAGE {imageIndex + 1}------------------\n")
        #-Image variables declaration-#
        filename = f"../../img/LARVAS/0 ({imageIndex+1}).jpg"
        currentImage = LarvaeImage(filename)
        imageMark = LarvaeImage(filename)

        '''''''''printTime("|   Declared image", localTime, timeLogFile); localTime = time()'''
        
        #-Image processing-#
        #print(f"Processing {filename}...")
        binaryFiltered = processLarvae(filename)
        while(binaryFiltered.checkForRemovableObjects()):
            binaryFiltered.removeObjectsBySize(0, 25)
        
        binaryFiltered.show(133)

        plt.show()
                
        '''''''''printTime("|   Processed image", localTime, timeLogFile); localTime = time()'''

        #-Larvae counting-#
        contours, hier = cv2.findContours(binaryFiltered.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        currentImage.numberOfLarvae = len(contours)

        #-Marking and saving marked image-#
        binaryFiltered.markObjects(imageMark.image, [0, 0, 255])
        cv2.imwrite(f"{pathName}/markedImage{imageIndex}.jpg", imageMark.image)
        '''''''''printTime("|   Saved marked image", localTime, timeLogFile); localTime = time()'''

        #-Getting larvae's info-#
        currentImage.larvaes, currentImage.numberOfAdults, currentImage.numberOfEggs = getObjectInfo(contours, binaryFiltered.image, currentImage.image, imageIndex)

        '''''''''printTime("|   Got larvae info", localTime, timeLogFile); localTime = time()'''

        #-Saving Images-#
        for i in range(currentImage.numberOfLarvae):
            cv2.imwrite(f"{pathName}/img/{totalLarvaeCounter+i}.jpg", currentImage.larvaes[i].image6464)

        #-HTML building-#
        HTMLBigPicture(htmlFile, filename, currentImage, imageIndex + 1)
        HTMLBigPicture(htmlFile, f"{pathName}/markedImage{imageIndex}.jpg", currentImage, imageIndex + 1)
        HTMLlineBreak(htmlFile)
        HTMLwrite(htmlFile, "<div>")
        if(currentImage.larvaes is not None):
            for i in range(currentImage.numberOfLarvae):
                HTMLBar(htmlFile, f"{pathName}/img/{totalLarvaeCounter + i}.jpg", currentImage.larvaes[i], totalLarvaeCounter + 1 + i)
        HTMLwrite(htmlFile, "</div>")
        HTMLlineBreak(htmlFile)

        '''''''''printTime("Image took", imageTime, timeLogFile)'''
        #print("---------------------------------------------------------------------------------------")
        totalLarvaeCounter += currentImage.numberOfLarvae
HTMLend(htmlFile)
print("Done!")
print(f"It took {round(time() - totalTime, 3)} seconds.")
timeLogFile.write(f"{numberOfImages} images took {round(time() - totalTime, 3)} seconds.")
