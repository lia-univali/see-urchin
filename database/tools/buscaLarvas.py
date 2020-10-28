import numpy as np
from imgClass import *
from relatorio import *
from funcoesLarva import *
import cv2
from os import path, makedirs, listdir
from time import time    

def buscar():
    #-Croação do caminho path-#
    pathName = path.dirname(path.realpath(__file__)) + "/../results/" + input("Digite o arquivo onde as imagens serão salvas: ")
    if not path.exists(pathName):
        makedirs(pathName)

    inputPath = input("Digite o caminho da pasta em que estão as imagens a serem analisadas: ")
    imageList = listdir(inputPath)
    suffixes = ("jpg", "jpeg", "png")    
    imageList = list(
        filter(
            lambda image: image.endswith(suffixes),
            imageList
        )
    )
    
    #-Criação da pasta img-#
    if not path.exists(pathName + "/img"):
        makedirs(pathName + "/img")

    #-Criação da pasta binimg-#
    if not path.exists(pathName + "/binimg"):
        makedirs(pathName + "/binimg")

    #-Criação do HTML-#
    htmlFile = open(pathName + "/report.html", 'a+')
    HTML.begin(htmlFile)
    
    totalTime = time()
    numberOfLarvaInImage = []
    totalLarvaeCounter = 0

    #-Loop principal - Processamento de imagem-#
    for imageIndex in range(len(imageList)):
        #-Image variables declaration-#
        filename = inputPath + "\\" + imageList[imageIndex]
        currentImage = LarvaImage(filename)
        imageMark = LarvaImage(filename)

        #-Processamento de imagem-#
        print(f"Processando {filename}...")
        binaryFiltered = LarvaeOperation.processLarvae(filename)
        while(binaryFiltered.checkForRemovableObjects()):
            binaryFiltered.removeObjectsBySize()        

        #-Contagem de Larvas-#
        contours, hier = cv2.findContours(binaryFiltered.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        currentImage.numberOfLarvae = len(contours)

        #-Marcação e salvamento das imagens-#
        binaryFiltered.markObjects(imageMark.image, [0, 0, 255])
        cv2.imwrite(f"{pathName}/markedImage{imageIndex}.jpg", imageMark.image)
        
        #-Obtenção de informações das larvas-#
        currentImage.larvaes, currentImage.numberOfAdults, currentImage.numberOfEggs = LarvaeOperation.getLarvaeArray(
            contours,
            binaryFiltered.image,
            currentImage.image,
            imageIndex
        )

        #-Salvamento das Imagens-#
        for i in range(currentImage.numberOfLarvae):
            cv2.imwrite(f"{pathName}/img/{totalLarvaeCounter+i}.jpg", currentImage.larvaes[i].image6464)
            cv2.imwrite(f"{pathName}/binimg/{totalLarvaeCounter+i}.jpg", currentImage.larvaes[i].binaryImage)
        
        #-Montagem do HTML-#
        HTML.bigPicture(htmlFile, inputPath + "\\" + imageList[imageIndex], currentImage, imageIndex + 1)
        HTML.bigPicture(htmlFile, f"{pathName}/markedImage{imageIndex}.jpg", currentImage, imageIndex + 1)
        HTML.lineBreak(htmlFile)
        HTML.write(htmlFile, "<div>")
        if(currentImage.larvaes is not None):
            for i in range(currentImage.numberOfLarvae):
                HTML.bar(htmlFile, f"{pathName}/img/{totalLarvaeCounter + i}.jpg", currentImage.larvaes[i], totalLarvaeCounter + 1 + i)
        HTML.write(htmlFile, "</div>")
        HTML.lineBreak(htmlFile)
        
        totalLarvaeCounter += currentImage.numberOfLarvae

    HTML.end(htmlFile)
    print("Done!")
    print(f"It took {round(time() - totalTime, 3)} seconds.")
    return 0