import json
import numpy as np
from src.fcgr import FCGR
from src.model_loader import ModelLoader
from src.preprocessing import Pipeline
from src.utils import clean_seq
fcgr = FCGR(k=6)
loader = ModelLoader()
order_output = ['S','L','G','V','GR','GH','GV','GK','GRY','O','GRA']
model = loader("resnet50_6mers", 11, "trained-models/model-34-0.954.hdf5")
with open("trained-models/preprocessing.json") as fp:
    pipe = json.load(fp)
    preprocessing = Pipeline(pipe)


def predict_seq(seq):
    array = fcgr(clean_seq(seq))
    array = preprocessing(array)
    pred = model.predict(np.expand_dims(np.expand_dims(array,axis=0),axis=-1))[0]
    argmax = pred.argmax()
    confidence = pred[argmax]    
    return order_output[argmax], confidence