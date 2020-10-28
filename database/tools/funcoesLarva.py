from imgClass import *
import numpy as np
import cv2

class Larva:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.comprimento = 0
        self.estagioEvolutivo = "Desconhecido"
        self.imagem = []
        self.imagem6464 = []
        self.imagemBinaria = []

class ImagemLarva:
    def __init__(self, nomeArquivo: str):
        self.imagem = cv2.imread(nomeArquivo)
        self.numeroLarvas = 0
        self.numeroOvos = 0
        self.numeroAdultos = 0
        self.larvas = []

class FuncoesLarva:
    @staticmethod
    def processarLarva(nomeArquivo: str):
        img = Image(nomeArquivo)
        nW = img.escalaCinza.imagem.shape[0] // 50
        nH = img.escalaCinza.imagem.shape[1] // 50
        img.escalaCinza.imagem = np.array(
            img.escalaCinza.imagem[
                nH:img.escalaCinza.imagem.shape[0] - nH,
                nW:img.escalaCinza.imagem.shape[1] - nW
            ]
        )
        img.escalaCinza.imagem = np.array(255*(img.escalaCinza.imagem/255)**2, dtype='uint8')
        img.escalaCinza.binario(25)
        img.escalaCinza.dilatar((3, 3))
        img.escalaCinza.inverter()
        img.escalaCinza.imagem = cv2.copyMakeBorder(img.escalaCinza.imagem, nH, nH, nW, nW, cv2.BORDER_CONSTANT, value=0)
        return Img(img.escalaCinza.imagem)

    @staticmethod
    def __extrairComprimentoLarva(imagemBinaria: np.ndarray):
        contorno, hier = cv2.findContours(imagemBinaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if(contorno):
            (x,y), raio = cv2.minEnclosingCircle(
                contorno[FuncoesImagem.pegarContornoMaior(contorno)]
            )
            return int(2*raio)
        else:
            return 0

    @staticmethod
    def __extrairInformacoesDoContorno(contorno: np.ndarray, imagemBinaria: np.ndarray, imagemOriginal: np.ndarray):
        (x, y, w, h) = cv2.boundingRect(contorno)

        #Tamanho da imagem/bordas nas imagens de proporção 1:1
        tamanhoImagem = max(w, h)
        borda = tamanhoImagem//2

        #Aplicação das bordas na imagem original
        img = cv2.copyMakeBorder(
            imagemOriginal,
            borda,
            borda,
            borda,
            borda,
            cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )

        #Aplicação das bordas na imagem binária
        binImg = cv2.copyMakeBorder(
            imagemBinaria,
            borda,
            borda,
            borda,
            borda,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )

        resultado = Larva(x, y, w, h)
        resultado.imagem = np.array(img[y:y+h*2, x:x+w*2])

        #watershed
        imagemBinariaFiltrada = FuncoesImagem.watershed(resultado.imagem)
        contorno, hier = cv2.findContours(imagemBinariaFiltrada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        (x, y, w, h) = cv2.boundingRect(contorno[0])
        novoTamanhoImagem = max(w, h)

        #Centralização da larva/Transormação em 1:1
        corteCima = max(y - (novoTamanhoImagem - h), 0)
        corteBaixo = corteCima + novoTamanhoImagem
        corteEsquerda = max(x - (novoTamanhoImagem - w), 0)
        corteDireita = corteEsquerda + novoTamanhoImagem

        resultado.imagem6464 = resultado.imagem[corteCima : corteBaixo, corteEsquerda : corteDireita]
        resultado.imagem6464 = np.array(cv2.resize(resultado.imagem6464, (64, 64)))

        resultado.imagemBinaria = imagemBinariaFiltrada[corteCima : corteBaixo, corteEsquerda : corteDireita]
        resultado.imagemBinaria = np.array(cv2.resize(resultado.imagemBinaria, (64, 64)))

        resultado.comprimento = FuncoesLarva.__extrairComprimentoLarva(imagemBinariaFiltrada)
        resultado.estagioEvolutivo = FuncoesLarva.__classificarLarva(resultado)
        return resultado

    @staticmethod
    def extrairVetorLarvas(contorno: np.ndarray, imagemBinaria: np.ndarray, imagemOriginal: np.ndarray):
        vetorLarva = []
        for cnt in contorno:
            vetorLarva += [FuncoesLarva.__extrairInformacoesDoContorno(cnt, imagemBinaria, imagemOriginal)]
        contadorLarva = 0
        contadorOvo = 0
        for i in range(len(vetorLarva)):
            if(vetorLarva[i].estagioEvolutivo == "Egg"):
                contadorOvo += 1
            elif(vetorLarva[i].estagioEvolutivo == "Larvae"):
                contadorLarva += 1
        return vetorLarva, contadorLarva, contadorOvo

    @staticmethod
    def __classificarLarva(larva: Larva):
        if(abs(larva.w - larva.h) <= 20 and larva.comprimento <= 180): #larva.comprimento em pixels (180px ~= 200µm)
            return "Egg"
        else:
            return "Larvae"
        if circleArray is None:
            return "Unknown"