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
        self.nb_episodes = 0

    def update(self, frame, is_dead):
        frame = preprocessing(frame)
        act_h, y_pred = self.model.forward_keep_activations(frame)
        self.activations.append((act_h, y_pred))
        return np.argmax(y_pred)

        self.iter += 1
        if is_dead or self.iter == self.episode_size:
            for activation in self.activations:
                if is_dead: # Agent is dead
                    y_true = wrong_move(one_hot(activation[1]))
                    grads = self.model.gradients(frame, activation[0], activation[1], y_true)
                    self.model.backward(grads)
                else:
                    y_true = one_hot(activation[1])
                    grads = self.model.gradients(frame, activation[0], activation[1], y_true)
                    self.model.backward(grads)

            self.reset()
            self.nb_episodes += 1
            print(f"Episode #{self.nb_episodes} : {'LOSE' if is_dead else 'WIN'}")
        return np.argmax(y_pred)

    def reset(self):
        self.activations = []
        self.iter = 0



