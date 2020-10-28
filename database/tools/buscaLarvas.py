import numpy as np
from imgClass import *
from relatorio import *
from funcoesLarva import *
import cv2
from os import path, makedirs, listdir
from time import time    

def buscar():
    #-Croação do caminho path-#
    caminho = path.dirname(path.realpath(__file__)) + "/../results/" + input("Digite o arquivo onde as imagens serão salvas: ")
    if not path.exists(caminho):
        makedirs(caminho)

    caminhoInput = input("Digite o caminho da pasta em que estão as imagens a serem analisadas: ")
    listaImagens = listdir(caminhoInput)
    sufixos = ("jpg", "jpeg", "png")    
    listaImagens = list(
        filter(
            lambda imagem: imagem.endswith(sufixos),
            listaImagens
        )
    )
    
    #-Criação da pasta img-#
    if not path.exists(caminho + "/img"):
        makedirs(caminho + "/img")

    #-Criação da pasta binimg-#
    if not path.exists(caminho + "/binimg"):
        makedirs(caminho + "/binimg")

    #-Criação do HTML-#
    arquivoHTML = open(caminho + "/report.html", 'a+')
    HTML.begin(arquivoHTML)
    
    tempoTotal = time()
    numeroLarvasTotal = 0

    #-Loop principal - Processamento de imagem-#
    for indiceImagem in range(len(listaImagens)):
        #-Image variables declaration-#
        nomeArquivo = caminhoInput + "\\" + listaImagens[indiceImagem]
        imagemAtual = ImagemLarva(nomeArquivo)
        imagemMarcada = ImagemLarva(nomeArquivo)

        #-Processamento de imagem-#
        print(f"Processando {nomeArquivo}...")
        imgBinariaFiltrada = FuncoesLarva.processarLarva(nomeArquivo)
        while(imgBinariaFiltrada.checarObjetosRemoviveis()):
            imgBinariaFiltrada.removerObjetosPorTamanho()        

        #-Contagem de Larvas-#
        contornos, hier = cv2.findContours(imgBinariaFiltrada.imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imagemAtual.numeroLarvas = len(contornos)

        #-Marcação e salvamento das imagens-#
        imgBinariaFiltrada.marcarObjetos(imagemMarcada.imagem, [0, 0, 255])
        cv2.imwrite(f"{caminho}/markedImage{indiceImagem}.jpg", imagemMarcada.imagem)
        
        #-Obtenção de informações das larvas-#
        imagemAtual.larvas, imagemAtual.numeroAdultos, imagemAtual.numeroOvos = FuncoesLarva.extrairVetorLarvas(
            contornos,
            imgBinariaFiltrada.imagem,
            imagemAtual.imagem,
        )

        #-Salvamento das Imagens-#
        for i in range(imagemAtual.numeroLarvas):
            cv2.imwrite(f"{caminho}/img/{numeroLarvasTotal+i}.jpg", imagemAtual.larvas[i].imagem6464)
            cv2.imwrite(f"{caminho}/binimg/{numeroLarvasTotal+i}.jpg", imagemAtual.larvas[i].imagemBinaria)
        
        #-Montagem do HTML-#
        HTML.bigPicture(arquivoHTML, caminhoInput + "\\" + listaImagens[indiceImagem], imagemAtual, indiceImagem + 1)
        HTML.bigPicture(arquivoHTML, f"{caminho}/markedImage{indiceImagem}.jpg", imagemAtual, indiceImagem + 1)
        HTML.lineBreak(arquivoHTML)
        HTML.write(arquivoHTML, "<div>")
        if(imagemAtual.larvas is not None):
            for i in range(imagemAtual.numeroLarvas):
                HTML.bar(
                    arquivoHTML,
                    f"{caminho}/img/{numeroLarvasTotal + i}.jpg",
                    imagemAtual.larvas[i],
                    numeroLarvasTotal + 1 + i
                )
        HTML.write(arquivoHTML, "</div>")
        HTML.lineBreak(arquivoHTML)
        
        numeroLarvasTotal += imagemAtual.numeroLarvas

    HTML.end(arquivoHTML)
    print("Done!")
    print(f"It took {round(time() - tempoTotal, 3)} seconds.")
    return 0