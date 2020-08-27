import numpy as np
from imgClass import *
from report import *
from larvaeFunc import *
import cv2
from os import path, makedirs
import matplotlib.pyplot as pl
from time import time

def viewLarvaePixelRatio(laevaes):
    for i in range(len(larvaes)):
        imgArea = larvaes[i].image.shape[0] * larvaes[i].image.shape[1]
        #imgArea = larvaes[i].w * larvaes[i].h
        cv2.imshow("a", larvaes[i].binaryImage)
        cv2.waitKey()
        cv2.destroyAllWindows()
        whitePix = cv2.countNonZero(cv2.cvtColor(larvaes[i].image, cv2.COLOR_BGR2GRAY))
        print(f"#{imageIndex+1}: White pixels: {whitePix} / {imgArea} ({(whitePix/imgArea)*100}%)")
    

def printTime(title, basedOnTime, logFile):
    logFile.write(f"{title}: {round(time() - basedOnTime, 3)};\n")
    print(f"{title}: {round(time() - basedOnTime, 3)};")
    return time()


def getLarvae(timeLogging=False,
              viewBinary=False,
              listLarvaePixelRatio=False,
              startImage=0,
              endImage=1):

    #-Creating path-#
    pathName = path.dirname(path.realpath(__file__)) + "/../images/" + input("Type the folder in which the images will be saved: ")
    totalTime = time()
    if not path.exists(pathName):
        makedirs(pathName)

    #---Creating img folder---#
    if not path.exists(pathName + "/img"):
        makedirs(pathName + "/img")

    #-Creating HTML-#
    htmlFile = open(pathName + "/report.html", 'a+')
    if timeLogging: timeLogFile = open(pathName + "/time.log", 'a+')

    HTMLbegin(htmlFile)
    numberOfLarvaInImage = []
    totalLarvaeCounter = 0
    if timeLogging: printTime("Made HTML and declared variables", totalTime, timeLogFile)

    for imageIndex in range(startImage, endImage):
        if timeLogging: imageTime, localTime = time(), time(); print(f"------------------IMAGE {imageIndex + 1}------------------"); timeLogFile.write(f"------------------IMAGE {imageIndex + 1}------------------\n")

        #-Image variables declaration-#
        filename = f"../../img/LARVAS/0 ({imageIndex+1}).jpg"
        currentImage = LarvaeImage(filename)
        imageMark = LarvaeImage(filename)
        
        if timeLogging: localTime = printTime("|   Declared image", localTime, timeLogFile)

        #-Image processing-#
        if not timeLogging: print(f"Processing {filename}...")
        binaryFiltered = processLarvae(filename)
        if viewBinary: cv2.namedWindow(f"Image {imageIndex + 1}", cv2.WINDOW_NORMAL); cv2.resizeWindow(f"Image {imageIndex + 1}", 512, 512); cv2.imshow(f"Image {imageIndex + 1}", binaryFiltered.image); cv2.waitKey(); cv2.destroyAllWindows()
        while(binaryFiltered.checkForRemovableObjects(20)):
            binaryFiltered.removeObjectsBySize(20)
        
        #binaryFiltered.show(133)
        #plt.show()
        
        if timeLogging: localTime = printTime("|   Processed image", localTime, timeLogFile)

        #-Larvae counting-#
        contours, hier = cv2.findContours(binaryFiltered.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        currentImage.numberOfLarvae = len(contours)

        #-Marking and saving marked image-#
        binaryFiltered.markObjects(imageMark.image, [0, 0, 255])
        cv2.imwrite(f"{pathName}/markedImage{imageIndex}.jpg", imageMark.image)
        
        if timeLogging: localTime = printTime("|   Saved marked image", localTime, timeLogFile)

        #-Getting larvae's info-#
        currentImage.larvaes, currentImage.numberOfAdults, currentImage.numberOfEggs = getObjectInfo(contours, binaryFiltered.image, currentImage.image, imageIndex)
        if listLarvaePixelRatio: viewLarvaePixelRatio(currentImage.larvaes)

        if timeLogging: localTime = printTime("|   Got larvae info", localTime, timeLogFile)

        #-Saving Images-#
        for i in range(currentImage.numberOfLarvae):
            cv2.imwrite(f"{pathName}/img/{totalLarvaeCounter+i}.jpg", currentImage.larvaes[i].image6464)
        #-HTML building-#
        HTMLBigPicture(htmlFile, f"../{filename}", currentImage, imageIndex + 1 - startImage)
        HTMLBigPicture(htmlFile, f"{pathName}/markedImage{imageIndex}.jpg", currentImage, imageIndex + 1 - startImage)
        HTMLlineBreak(htmlFile)
        HTMLwrite(htmlFile, "<div>")
        if(currentImage.larvaes is not None):
            for i in range(currentImage.numberOfLarvae):
                HTMLBar(htmlFile, f"{pathName}/img/{totalLarvaeCounter + i}.jpg", currentImage.larvaes[i], totalLarvaeCounter + 1 + i)
        HTMLwrite(htmlFile, "</div>")
        HTMLlineBreak(htmlFile)
        
        if timeLogging: printTime("Image took", imageTime, timeLogFile); print("---------------------------------------------------------------------------------------")

        totalLarvaeCounter += currentImage.numberOfLarvae

    HTMLend(htmlFile)
    print("Done!")
    print(f"It took {round(time() - totalTime, 3)} seconds.")
    if timeLogging: timeLogFile.write(f"{endImage - startImage} images took {round(time() - totalTime, 3)} seconds.")
    return 0