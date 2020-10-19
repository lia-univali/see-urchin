import cv2 as cv
import numpy as np
from collections import Counter
import os


def watershed(end, nome_arquivo, wait):
    print("end = " + end)
    img = cv.imread(end)
    img_copia = cv.imread(end)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 0, 255, cv.CALIB_CB_ADAPTIVE_THRESH + cv.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.CALIB_CB_ADAPTIVE_THRESH, kernel, iterations=1)

    # sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=3)

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)

    # print(sure_bg)

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

    markers = cv.watershed(img, markers)

    submarkers = markers[16:48, 16:48]
    markers2 = np.array(submarkers)
    markers2 = markers2.flatten()
    counter = Counter(markers2)

    # buscando segundo valor
    comum = counter.most_common()
    print(comum)
    valor = comum[0][0]
    try:
        if comum[0][0] == 1 or comum[0][0] == -1:
            valor = comum[1][0]
            if comum[1][0] == 1 or comum[1][0] == -1:
                valor = comum[2][0]
    except Exception:
        print("erro")

    dilated = np.array(img_copia)
    dilated[markers == valor] = [255, 255, 255]
    dilated[markers != valor] = [0, 0, 0]

    dilated = cv.dilate(dilated, np.ones((3, 3)))
    dilated = cv.cvtColor(dilated, cv.COLOR_BGR2GRAY)
    img_copia[dilated == 0] = [255, 255, 255]

    cv.imwrite("C:/Users/hidan/git/see-urchin/database/results/b/watershed/"+nome_arquivo + ".jpg", img_copia)
    cv.imshow("image", img_copia)
    cv.resizeWindow('image', 200, 200)
    if wait:
        cv.waitKey(0)


# for arquivo in os.listdir("/see-urchin/database/results/b/img"):
#     watershed("/see-urchin/database/results/b/img/"+arquivo, arquivo, False)