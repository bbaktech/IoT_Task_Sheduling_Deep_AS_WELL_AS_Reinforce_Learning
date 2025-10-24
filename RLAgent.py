from operator import gt, le
import random
import keras
from keras.src import Sequential 
from keras.src.layers import Dense,Dropout,Flatten
from keras.src.optimizers import Adam
import numpy as np
import tensorflow as tf
from collections import deque
from keras.utils import to_categorical # type: ignore
from config import MAX_JOBS
batch_size = 32

#A deep Q-learning agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=200)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = self._build_model()
#        self.load_mdl()

    def _build_model(self):
        # Define model architecture
        inputs = keras.Input(shape=(self.state_size,))
        x = Dense(128, activation="relu")(inputs)
        oo = []
        names= []
        for job in range(MAX_JOBS):
            x0 = Dense(64, activation="relu")(x)
            name = 'outputs'+str(job)
            names.append(name)
            oo.append(Dense(self.action_size, activation="linear",name = name)(x0) )

        model = keras.Model(inputs = inputs, outputs = oo)
        #loss is the distnary you need to implement
        loss = {}
        for job in range(MAX_JOBS):
            loss.update({ names[job]: 'mse'})

        model.compile(optimizer= Adam(learning_rate=self.learning_rate),
                    loss=loss )
        return model

    def load_mdl(self):
        self.model.load_weights('weights_0500.weights.h5')
        self.epsilon = 0.05

    def act(self, state, sim_time, sl_no):
        if le(np.random.rand() , self.epsilon):
            #genarate MAX_JOBS random values
            result1 =[]
            for j in range(MAX_JOBS):
                idx = random.randrange(self.action_size)
                ary_val = []
                for i in range(self.action_size):
                    ary_val.append(0)
                ary_val[idx] = 1
                result1.append([ary_val])
            return result1
        result = self.model.predict(state,verbose = 0 )
        self.writeresults(result,sl_no)
        return result
    
    def writeresults(self,result,sl):
        name = 'predict_new.txt'
        f = open(name, 'a') 
        f.write(str(sl))
        for j in range(MAX_JOBS):
            for vl in range(self.action_size):
                f.write(' '+str(result[j][0][vl]))
        f.write('\n ')
        f.close()

    #receive feedback to agent
    def remember(self, state, action, rewards):
        self.memory.append((state, action,rewards))
 
    def train(self):
        if len(self.memory) > batch_size:
            minibatch = random.sample(self.memory, batch_size)
            for state, action, rewards in minibatch:
                n_action = self.model.predict(state,verbose = 0 )

                for jb in range(MAX_JOBS):
                    pp = np.argmax(action[jb][0])
                    for vl in range(self.action_size):
                        if n_action[jb][0][vl] > rewards[jb]:
                            n_action[jb][0][vl] = rewards[jb]
                    n_action[jb][0][pp] = rewards[jb]

                self.model.fit(state, n_action, epochs=1,verbose=0)
            #epson if should be at minbatch for level
            if gt (self.epsilon , self.epsilon_min):
                self.epsilon *= self.epsilon_decay
    
    def save(self, name): 
        self.model.save_weights(name)
        name = name + 'new.txt'
        strval = " self.epsilon:"+ str(self.epsilon)
        with open(name, 'a') as f:
#            f.write(strval)
            for state, action, rewards in self.memory:
                for jb in range(MAX_JOBS):
                    strval = ''
                    for vl in range(self.action_size):
                        strval = strval+ str(action[jb][0][vl]) + ', '+ str(rewards[jb]) +', '
                    f.write(str(jb)+' ' +strval+'\n')
        f.close()
