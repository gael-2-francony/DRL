from collections import deque
import random

import numpy as np

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Input, MaxPooling2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam

from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g
REPLAY_SIZE = 100
BATCH_SIZE = 30

class DQN():
    def __init__(self, input_shape=(SCREEN_HEIGHT_g, SCREEN_WIDTH_g, 1)):
        self.input_shape = input_shape
        self.model = self.get_model()
        self.replay_memory = deque(maxlen=REPLAY_SIZE)

        self.discount_factor = 0.95

        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.9995

        self.prev_state = None
        self.prev_action = None

    def get_model(self):
       state = Input(shape=self.input_shape)
       x = Conv2D(16, 3, activation="relu")(state)
       x = MaxPooling2D(2)(x)
       x = Conv2D(32, 3, activation="relu")(x)
       x = Flatten()(x)
       x = Dense(32, activation="relu")(x)
       action = Dense(9, activation="linear")(x)
       model = Model(inputs=state, outputs=action)
       model.compile(optimizer=Adam(lr=0.001), loss="mse")
       return model

    def act(self, state):
        if np.random.random_sample() < self.epsilon:
            action = np.random.randint(9)
        else:
            action = self.model.predict(np.array([state]))
            action = np.argmax(action[0])
        self.last_action = action
        self.last_state = state
        return action

    def memorize(self, state, action, reward, new_state, terminal_state):
        try:
            if state.all() != None and action != None:
                self.replay_memory.append((state, action, reward, new_state, terminal_state))
        except:
            pass

    def replay(self):
        batch = random.sample(self.replay_memory, BATCH_SIZE)
        for state, action, reward, new_state, terminal_state in batch:
            if terminal_state:
                target = reward
            else:
                target = reward + self.discount_factor * \
                    np.amax(self.model.predict(np.array([new_state]))[0])
            updated_action_reward = self.model.predict(np.array([state]))
            # Change value of action, we now have better target
            updated_action_reward[0][action] = target
            self.model.fit(np.array([state]), updated_action_reward, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def can_replay(self):
        return len(self.replay_memory) > BATCH_SIZE

    def save(self, name="dqn"):
        self.model.save_weights(f"{name}.h5")
