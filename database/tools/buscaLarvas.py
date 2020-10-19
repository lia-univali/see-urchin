import numpy as np
from database.tools.imgClass import *
from database.tools.relatorio import *
from database.tools.funcoesLarva import *
import cv2
from os import path, makedirs
from time import time    

def buscar(startImage=0, endImage=1):
    #-Croação do caminho path-#
    pathName = path.dirname(path.realpath(__file__)) + "/../results/" + input("Digite o arquivo onde as imagens serão salvas: ")
    if not path.exists(pathName):
        makedirs(pathName)

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
    for imageIndex in range(startImage, endImage):
        #-Image variables declaration-#
        filename = f"../input/0 ({imageIndex+1}).jpg"
        currentImage = LarvaeImage(filename)
        imageMark = LarvaeImage(filename)

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
        HTML.bigPicture(htmlFile, f"../{filename}", currentImage, imageIndex + 1 - startImage)
        HTML.bigPicture(htmlFile, f"{pathName}/markedImage{imageIndex}.jpg", currentImage, imageIndex + 1 - startImage)
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