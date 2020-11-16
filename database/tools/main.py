from database.tools.buscaLarvas import buscar
import tensorflow

model = tensorflow.keras.models.load_model('model_saved.h5')

if __name__ == "__main__":
    buscar()