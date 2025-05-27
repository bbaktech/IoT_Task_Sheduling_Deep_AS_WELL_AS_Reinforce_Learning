import keras
from keras.src import Sequential 
from keras.src.layers import Dense,Dropout,Flatten
from keras.src.optimizers import Adam
import pandas
import numpy as np
from sklearn.model_selection import train_test_split

from config import JOB_ATTRIBUTES, MAX_JOBS, MAX_RS

def _build_model():
    # Define model architecture
    inputs = keras.Input(shape=(MAX_JOBS*JOB_ATTRIBUTES,))
    x = Dense(128, activation="relu")(inputs)
    oo = []
    names= []
    for job in range(MAX_JOBS):
        x0 = Dense(64, activation="relu")(x)
        name = 'outputs'+str(job)
        names.append(name)
        oo.append(Dense(MAX_RS, activation="softmax",name = name)(x0) )

    model = keras.Model(inputs = inputs, outputs = oo)
    #loss is the distnary you need to implement
    loss = {}
    for job in range(MAX_JOBS):
        loss.update({ names[job]: 'categorical_crossentropy'})

    #model.compile(optimizer="rmsprop",loss="categorical_crossentropy",metrics=["accuracy"])
    model.compile(optimizer='rmsprop',
                loss=loss )
    return model

