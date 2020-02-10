import numpy as np
from imgClass import *
from report import *
import cv2
from os import path, makedirs

def removeBinaryRelative(filename):
    img = Image(filename)
    img.gray.window()
    thresh = img.gray.getRelativeThreshold()
    img.gray.binary(thresh * 1.1)
    img.gray.invert()
    img.gray.floodFill()
    if(img.gray.image.shape[0] > 1000 and img.gray.image.shape[1] > 1000):
        img.gray.erode()
    return img.gray.image

def removeBinary(filename):
    img = Image(filename)
    img.gray.window()
    img.gray.binary(10)
    img.gray.invert()
    img.gray.close((10, 10))
    img.gray.dilate((15, 15))
    return img.gray.image

filename = ["../../img/LARVAS_1.jpg", 
            "../../img/LARVAS_2.jpg",
            "../../img/LARVAS_3.jpg"]

pathName = path.dirname(path.realpath(__file__)) + "/../" + input("Type the folder in which the images will be saved: ")

if not path.exists(pathName):
    makedirs(pathName)
counter = 0

csvFileTrain = open(pathName + "/train.csv", 'w+')
csvFileTrain.write("image_path,class\n")

csvFilePredict = open(pathName + "/predict.csv", 'w+')
csvFilePredict.write("image_path,class\n")

htmlFile = open(pathName + "/report.html", 'a+')
beginHTML(htmlFile)

choice = ""
while(choice.upper() != "Q" and choice.upper() != "S"):
    choice = input("Choose between (Q)uick and (S)low mode: ")

markedImagesCounter = 0

for name in filename:
    #---Begginning the HTML File---#
    makeHTMLBigPicture(htmlFile, name)

    #---Declaring the Image Variables---#
    grayImage = cv2.cvtColor(cv2.cvtColor(cv2.imread(name), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    picToBeMarked = cv2.imread(name)

    #---Image Processing Sequence---#
    result = Img(cv2.bitwise_and(removeBinary(name), removeBinaryRelative(name)))
    while(result.checkForRemovableObjects()):
        result.removeObjectsBySize(0, 25)
    larvaeArray = result.getObjectInfo()
    
    #---Marking the Image and Inserting it in the HTML File---#
    result.markObjects(picToBeMarked, [0, 0, 255])
    cv2.imwrite(f"{pathName}/markedImage{markedImagesCounter}.png", picToBeMarked)
    makeHTMLBigPicture(htmlFile, f"{pathName}/markedImage{markedImagesCounter}.png")
    markedImagesCounter += 1
    htmlFile.write("<br>")

    #---Inserting the Larvae in the HTML File---#
    for i in range(len(larvaeArray)):
        makeHTMLBar(htmlFile, f"img/{counter+i}.png", larvaeArray[i], i + counter)
    htmlFile.write("<br>")

    #---Saving the Laevae Images---#
    if(choice.upper() == "Q"):
        counter = result.writeObjects(cv2.cvtColor(grayImage, cv2.COLOR_BGR2GRAY), csvFileTrain, csvFilePredict, pathName, counter)
    else:  
        counter = result.writeEachObject(cv2.cvtColor(grayImage, cv2.COLOR_BGR2GRAY), csvFileTrain, csvFilePredict, pathName, counter)

    cv2.destroyAllWindows()

endHTML(htmlFile)
print("Done!")