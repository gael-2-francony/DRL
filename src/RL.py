from MLP import MLP, one_hot, preprocessing
from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g
import numpy as np

def wrong_move(y_true):
    y_true[y_true == 0] = 1 / (y_true.shape[0] - 1)
    y_true[y_true == 1] = 0
    return y_true

class RL_Agent():
    def __init__(self, episode_size=150):
        self.model = MLP((SCREEN_HEIGHT_g, SCREEN_WIDTH_g), 16)
        self.activations = []
        self.episode_size = episode_size
        self.iter = 0

    def update(self, frame, is_dead):
        frame = preprocessing(frame)
        act_h, y_pred = self.model.forward_keep_activations(frame)
        self.activations.append((act_h, y_pred))
        return np.argmax(y_pred)

        y_true_cur = one_hot(y_pred)
        grads = self.model.gradients(frame, act_h, y_pred, y_true_cur)
        self.model.backward(grads)

        self.iter += 1
        if is_dead or self.iter == self.episode_size:
            for activation in self.activations:
                if is_dead: # Agent is dead
                    y_true = wrong_move(one_hot(activation[1]))
                    grads = self.model.gradients(frame, activation[0], activation[1], y_true)
                    self.model.backward(grads)
            self.reset()
            print("Episode done.")
        return np.argmax(y_pred)

    def reset(self):
        self.activations = []
        self.iter = 0



