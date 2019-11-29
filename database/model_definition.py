from ludwig.api import LudwigModel
import pandas as pd

cvsFile = pd.read_csv('grayscaleTrain.csv')
print(cvsFile)
cvsFilePredict = pd.read_csv('grayscaleTest.csv')

model_definition = {
    'input_features':[
        {'name':'image_path', 'type':'image', 'encoder':'stacked_cnn'}
    ],
    'output_features': [
        {'name': 'class', 'type': 'binary'}
    ]
}

model = LudwigModel(model_definition)
trainData = model.train(data_df=cvsFile)
predictionData1 = model.predict(data_df=cvsFilePredict)

print("=========================PREDICTION 1=========================")
print(predictionData1.to_string())


model.close()