import numpy as np
import cv2

from database.tools import main


# Retorna True se for larva / False se não for
def classificar(end):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = main.model
    print(end)
    img = cv2.imread(end)
    img = np.reshape(img, [1, 64, 64, 3])

    classes = model.predict_classes(img)
    print(classes[0])

    return classes[0] == 0