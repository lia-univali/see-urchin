import numpy as np
from imgClass import *
from report import *
from larvaeFunc import *
import cv2
from os import path, makedirs

'''
def processLarvae(filename):
    return Img(cv2.bitwise_and(processLarvaeHard(filename), processLarvaeSoft(filename)))
'''

if __name__ == "__main__":
    filename = ["../../img/LARVAS_1.jpg", 
                "../../img/LARVAS_2.jpg",
                "../../img/LARVAS_3.jpg"]

    #-Getting an array of images to be processed and an array of images to be marked-#
    imageArray = getImagesFromArray(filename)
    markedImagesArray = getImagesFromArray(filename)

    #-Creating a folder, in which everything will be saved, one folder above the script-#
    pathName = path.dirname(path.realpath(__file__)) + "/../" + input("Type the folder in which the images will be saved: ")
    if not path.exists(pathName):
        makedirs(pathName)

    #-Declaring the csv file and creating the HTML report-#
    csv = None
    htmlFile = open(pathName + "/report.html", 'a+')

    #-Asking for user's choice on the saving method-#
    choice = ""
    while(choice.upper() != "A" and choice.upper() != "M"):
        choice = input("Choose between (A)utomatic and (M)anual mode: ")
    if(choice.upper() == "M"):
        print("Press \"D\" to save as Larvae;\nPress\"S\" to save as Egg;\nPress any other key to not save.")
    
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

        #-Creating the marked image-#
        result.markObjects(markedImagesArray[i].image, [0, 0, 255])
        cv2.imwrite(f"{pathName}/markedImage{i}.png", markedImagesArray[i].image)

    #---Creating img folder---#
    if not path.exists(pathName + "/img"):
        makedirs(pathName + "/img")

    for i in range(len(larvaeArray)):
        #-Getting each larvaes' length-#
        binaryImageFiltered = removeObjectsSmallerThan(larvaeArray[i].binaryImage, (int(larvaeArray[i].binaryImage.shape[1]) // 3, int(larvaeArray[i].binaryImage.shape[0]) // 3))
        point1, point2, larvaeArray[i].length = findFarthestPixels(binaryImageFiltered)

    #---Saving the images in the way the user wants---#
    if(choice.upper() == "A"):
        counter = 0
        print("Saving Images...")
        for i in range(len(larvaeArray)):
            cv2.imwrite(f"{pathName}/img/{i}.png", larvaeArray[i].image6464)
            currentImage = Img(cv2.imread(f"{pathName}/img/{i}.png", 0))
            circleArray = cv2.HoughCircles(currentImage.image, cv2.HOUGH_GRADIENT, 1, 64, param1=80, param2=20, minRadius=10, maxRadius=42)
            currentImage.window()
            currentImage.binary(currentImage.getRelativeThreshold())
            currentImage.invert()
            '''
            #-Checking roundness and size to indentify the evolutionary stage-#
            if(not(circleArray is None) and (22 < circleArray[0, 0, 0] < 44) and (22 < circleArray[0, 0, 1] < 44) and cv2.countNonZero(currentImage.image) < 1100):
                counter += 1
                larvaeArray[i].evolStage = "Egg"
                imageArray[larvaeArray[i].srcImgIndex].numberOfEggs += 1
            else: 
                larvaeArray[i].evolStage = "Larvae"
                imageArray[larvaeArray[i].srcImgIndex].numberOfAdults += 1
            if circleArray is not None:
                print(f"#{i+1}: {larvaeArray[i].evolStage} - {circleArray[0, 0, 0]}x{circleArray[0, 0, 1]} - {circleArray[0, 0, 2]};")
            ''' 
        print(f"Identified {counter} eggs and {len(larvaeArray) - counter} adults;")
    else:
        print("Saving Images...")
        csv = CSV(pathName)
        #-Saves images and gathers the evolutionary stage according to the user's input-#
        for i in range(len(larvaeArray)):
            larvaeArray[i].evolStage = saveWithChoice(f"{pathName}/img/{i}.png", larvaeArray[i].image, csv)

    

    #---Creating the HTML file---#
    print("Creating HTML File...")
    HTMLbegin(htmlFile)
    larvaeNameOffset = 0
    for i in range(len(imageArray)):
        #-Inserts the original and marked images in the HTML file-#
        HTMLBigPicture(htmlFile, filename[i], imageArray[i])
        HTMLBigPicture(htmlFile, f"{pathName}/markedImage{i}.png", imageArray[i])
        HTMLlineBreak(htmlFile)
        if(i > 0):
            larvaeNameOffset += imageArray[i-1].numberOfLarvae
        #-Inserts each larvaes' image in the HTML file-#
        for j in range(imageArray[i].numberOfLarvae):
            HTMLBar(htmlFile, f"{pathName}/img/{j + larvaeNameOffset}.png", larvaeArray[j + larvaeNameOffset], j + 1 + larvaeNameOffset)
        HTMLlineBreak(htmlFile)
    HTMLend(htmlFile)

    print("Done!")