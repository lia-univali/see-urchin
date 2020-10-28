from collections import Counter

import cv2
import numpy as np


class Img:
    # ======================================INIT=======================================
    def __init__(self, img: np.ndarray):
        self.imagem = img

    # ============================IMAGE-REPLACING-FUNCTIONS============================
    # Functions that replaces the target image by the transformed one

    # ---Binary---#
    def binario(self, limit=127):
        binario = self.imagem
        binario[binario >= limit] = 255
        binario[binario < limit] = 0
        self.imagem = binario

    # ---Dilate---#
    def dilatar(self, ksize=(3, 3)):
        kernel = np.ones((ksize))
        self.imagem = cv2.dilate(self.imagem, kernel)

    # ---Flood Fill---#
    def floodFill(self, dstPixel=(0, 0)):
        cv2.floodFill(
            self.imagem,
            np.zeros((self.imagem.shape[0] + 2, self.imagem.shape[1] + 2), dtype='uint8'),
            (0, 0),
            128
        )
        self.imagem[self.imagem < 1] = 255
        self.imagem[self.imagem <= 128] = 0

    #---Invert---#
    def inverter(self):
        self.imagem = cv2.bitwise_not(self.imagem)

    # ---Mark Objects---#
    def marcarObjetos(self, dst: np.ndarray, color: list):
        contours, hier = cv2.findContours(self.imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            size = max(w, h)
            borderSize = size // 2
            corteCima = y - (borderSize * 3 - h)
            corteBaixo = corteCima + size * 2
            corteEsquerda = x - (borderSize * 3 - w)
            corteDireita = corteEsquerda + size * 2
            cv2.rectangle(dst, (corteEsquerda, corteCima), (corteDireita, corteBaixo), color, 5)

    # ---Remove Objects by Size---#
    def removerObjetosPorTamanho(self, minPercentOfNonWhite=20):
        imgArea = self.imagem.shape[0] * self.imagem.shape[1]
        contours, hier = cv2.findContours(self.imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if ((cv2.countNonZero(self.imagem[y:y + h, x:x + w]) < h * w * minPercentOfNonWhite / 100) or \
                    h > w * 4 or \
                    w > h * 4 or \
                    h < self.imagem.shape[0] * 0.035 or \
                    w < self.imagem.shape[1] * 0.035):
                self.imagem[y:y + h, x:x + w] = 0
            elif (w > self.imagem.shape[1] / 4 or h > self.imagem.shape[0] / 4):
                cv2.floodFill(self.imagem, np.zeros((self.imagem.shape[0] + 2, self.imagem.shape[1] + 2), dtype='uint8'),
                              (cnt[0][0][0], cnt[0][0][1]), 0)

    # ============================TOOLS============================
    # ------------Functions that do not alter the image------------

    # ---Check for Removable Objects---#
    def checarObjetosRemoviveis(self):
        contours, hier = cv2.findContours(self.imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgArea = self.imagem.shape[0] * self.imagem.shape[1]
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if (w > self.imagem.shape[1] / 4 or h > self.imagem.shape[0] / 4 or \
                    (cv2.countNonZero(self.imagem[y:y + h, x:x + w]) < h * w * 20 / 100) or \
                    h > w * 4 or \
                    w > h * 4 or \
                    h < self.imagem.shape[0] * 0.035 or \
                    w < self.imagem.shape[1] * 0.035):
                return True
        return False
            
class Image:
    def __init__(self, filename):
        try:
            self.original = Img(cv2.cvtColor(cv2.imread(filename), cv2.COLOR_RGB2BGR))
            self.escalaCinza = Img(cv2.cvtColor(self.original.imagem, cv2.COLOR_BGR2GRAY))
        except:
            print("\nUm erro ocorreu ao carregar a imagem.")
            quit()


class FuncoesImagem:
    @staticmethod
    def pegarContornoMaior(contornos: np.ndarray):
        maiorContorno = 0
        for i in range(len(contornos)):
            if (len(contornos[i]) > len(contornos[maiorContorno])):
                maiorContorno = i
        return maiorContorno

    @staticmethod
    def watershed(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.CALIB_CB_ADAPTIVE_THRESH, kernel, iterations=1)

        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1
        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0

        markers = cv2.watershed(image, markers)

        markers2 = np.array(markers)
        markers2 = markers2.flatten()
        counter = Counter(markers2)

        # buscando segundo valor
        comum = counter.most_common()
        valor = comum[0][0]
        try:
            if comum[0][0] == 1 or comum[0][0] == -1:
                valor = comum[1][0]
                if comum[1][0] == 1 or comum[1][0] == -1:
                    valor = comum[2][0]
        except Exception:
            print("erro")

        dilated = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        dilated[markers == valor] = 255
        dilated[markers != valor] = 0

        dilated = cv2.dilate(dilated, np.ones((3, 3)))
        return dilated
