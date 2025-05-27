from operator import gt, le
import random
import gym 
import keras
import numpy as np
import tensorflow as tf
from collections import deque
from keras.src import Sequential 
from keras.src.layers import Dense
from keras.src.optimizers import Adam
from devices import STATE

#A deep Q-learning agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=1000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = self._build_model()

    def load_mdl(self):
        self.model.load_weights('weights_1500.weights.h5')
        self.epsilon = 0.009920974201040588

    def _build_model(self):
        model = Sequential() 
        model.add(Dense(32, activation="relu",
                        input_dim=self.state_size))
        model.add(Dense(32, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse",
                     optimizer=Adam(learning_rate=self.learning_rate))
        return model
 
        #receive feedback to agent
    def remember(self, state, action, reward, next_state): 
        self.memory.append((state, action,
                            reward, next_state))

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:
            target = reward     
            target_f = self.model.predict(state,verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1,verbose=0) 
        
        if gt (self.epsilon , self.epsilon_min):
                self.epsilon *= self.epsilon_decay

    def act(self, state):
        if le(np.random.rand() , self.epsilon):
            return random.randrange(self.action_size) 
        act_values = self.model.predict(state,verbose=0)
        return np.argmax(act_values[0])
    
    def save(self, name): 
        self.model.save_weights(name)
        name = name + 'new.txt'
        strval = "self.epsilon:"+ str(self.epsilon)
        with open(name, 'a') as f:
            f.write(strval)
            f.close()
