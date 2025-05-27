import keras
from keras.src import Sequential 
from keras.src.layers import Dense,Dropout,Flatten
from keras.src.optimizers import Adam
import pandas
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical # type: ignore

MAX_JOBS = 40
JOB_ATTRIBUTES = 3
MAX_RS = 4

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

modl = _build_model()
modl.summary()

modl.load_weights('DL_MODULE_RM.weights.h5')

# result = modl.predict( np.array( [[4,5,4,2,2,4,4,3,4,2,2,5,2,5,5,5,5,3,2,2,3,2,4,5,5,4,5,2,4,5,2,4,5,5,5,5,4,4,4,5,2,5,5,2,2,2,2,2,2,2,2,2,2,2,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
# 4, 0, 4, 4, 0, 5, 4, 0, 4, 4, 0, 2, 4, 0, 2, 4, 0, 4, 4, 0, 4, 4, 0, 3, 4, 0, 4, 4, 0, 2, 4, 0, 2, 4, 0, 5, 4, 0, 2, 4, 0, 5, 4, 0, 5, 4, 0, 5, 4, 0, 5, 4, 0, 3, 4, 0, 2, 4, 0, 2, 4, 0, 3, 4, 0, 2, 4, 0, 4, 4, 0, 5, 4, 0, 5, 4, 0, 4, 4, 0, 5, 4, 0, 2, 6, 10, 4, 6, 10, 5, 8, 14, 2, 7, 12, 4, 9, 15, 5, 6, 10, 5, 7, 12, 5, 6, 10, 5, 9, 15, 4, 8, 14, 4, 9, 15, 4, 8, 14, 5, 9, 15, 2, 6, 10, 5, 8, 14, 5, 9, 15, 2, 9, 15, 2, 6, 10, 2, 7, 12, 2, 9, 15, 2, 6, 10, 2, 8, 14, 2, 7, 12, 2, 7, 12, 2, 6, 10, 2, 7, 12, 2, 9, 15, 5, 6, 10, 2, 8, 14],
# [4,5,4,2,2,4,4,3,4,2,2,5,2,5,5,5,5,3,2,2,3,2,4,5,5,4,5,2,4,3,4,4,2,5,5,2,2,4,5,2,3,5,4,5,2,4,5,2,5,5,5,3,4,4,2,2,3,4,4,3,2,2,2,2,5,3,5,2,2,2,5,2,2,4,4,2,5,2,2,4,4,5,2,2,0,
# 4, 0, 4, 4, 0, 3, 4, 0, 4, 4, 0, 4, 4, 0, 2, 4, 0, 5, 4, 0, 5, 4, 0, 2, 4, 0, 2, 4, 0, 4, 4, 0, 5, 4, 0, 2, 4, 0, 3, 4, 0, 5, 4, 0, 4, 4, 0, 5, 4, 0, 2, 4, 0, 4, 4, 0, 5, 4, 0, 2, 4, 0, 5, 4, 0, 5, 4, 0, 5, 4, 0, 3, 4, 0, 4, 4, 0, 4, 4, 0, 2, 4, 0, 2, 6, 10, 3, 6, 10, 4, 8, 14, 4, 7, 12, 3, 9, 15, 2, 6, 10, 2, 7, 12, 2, 6, 10, 2, 9, 15, 5, 8, 14, 3, 9, 15, 5, 8, 14, 2, 9, 15, 2, 6, 10, 2, 8, 14, 5, 9, 15, 2, 9, 15, 2, 6, 10, 4, 7, 12, 4, 9, 15, 2, 6, 10, 5, 8, 14, 2, 7, 12, 2, 7, 12, 4, 6, 10, 4, 7, 12, 5, 9, 15, 2, 6, 10, 2, 8, 14]
# ] ))

for j in range(MAX_JOBS):
    pp = np.argmax(result[j][0])
    print(pp)
