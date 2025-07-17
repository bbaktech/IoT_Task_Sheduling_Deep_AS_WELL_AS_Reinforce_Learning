import keras
from keras.src import Sequential 
from keras.src.layers import Dense,Dropout,Flatten
from keras.src.optimizers import Adam
import pandas
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical # type: ignore

MAX_JOBS = 85
JOB_ATTRIBUTES = 3
MAX_RS = 6

df1 = pandas.read_csv('DataSet3.csv')
X = df1.iloc[:, :MAX_JOBS*3]
x = np.array(X).astype(np.int32)

Y = []
for y in range(MAX_JOBS):
    res = df1.iloc[:, MAX_JOBS*JOB_ATTRIBUTES + y:MAX_JOBS *JOB_ATTRIBUTES +1+y]
    res = np.array(res).astype(np.int32)
    Y.append(res)

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

# # # Train the model
callbacks = [keras.callbacks.ModelCheckpoint("DENS_ASSIN.keras",save_best_only=True)]
Z = []
for ind in range(MAX_JOBS):
    Z.append (to_categorical(Y[ind], num_classes = MAX_RS))

history = modl.fit(x, Z,epochs=1000,callbacks=callbacks)
modl.save_weights('DL_MODULE_4RMV1.weights.h5')

modl.load_weights('DL_MODULE_4RMV1.weights.h5')
print (modl.evaluate(x, Z))

jobs = modl.predict(x[0:5] )
print (len(jobs))

for i in range (5):
    print ('sample' + str(i))
    for jb in range(MAX_JOBS):
        pp = np.argmax(jobs[jb][i])
        print(str(pp)+":"+ str(Y[jb][i]) + ':'+ str(Z[jb][i]) )
