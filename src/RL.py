from MLP import MLP, one_hot, preprocessing
from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g
import numpy as np

def preprocessing(X):
    X = X.flatten()
    return X

def one_hot(move):
    return np.eye(move.shape[0])[np.argmax(move)]

def wrong_move(y_true):
    y_true[y_true == 0] = 1 / (y_true.shape[0] - 1)
    y_true[y_true == 1] = 0
    return y_true
class RL_Agent():
    def __init__(self, episode_size=50):
        self.model = MLP((SCREEN_HEIGHT_g, SCREEN_WIDTH_g), 16)
        self.moves = []
        self.episode_size = episode_size
        self.iter = 0

    def update(self, frame, is_dead):
        y_pred = self.model.forward(frame)
        self.moves.append(y_pred)

        y_true_cur = one_hot(y_pred)
        self.model.backward(y_pred, y_true_cur)

        self.iter += 1
        if is_dead or self.iter == self.episode_size:
            for move in self.moves:
                if is_dead: # Agent is dead
                    y_true = wrong_move(one_hot(move))
                    self.model.backward(move, y_true)
            self.reset()
        return move

    def reset(self):
        self.moves = []
        self.iter = 0



