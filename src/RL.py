from MLP import MLP, one_hot, preprocessing
from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g
import numpy as np

def wrong_move(y_true):
    y_true[y_true == 0] = 1 / (y_true.shape[0] - 1)
    y_true[y_true == 1] = 0
    return y_true

class RL_Agent():
    def __init__(self, episode_size=150):
        self.model = MLP((SCREEN_HEIGHT_g, SCREEN_WIDTH_g), 300)
        #self.load("models/model_1185.npz")
        self.activations = []
        self.frames = []
        self.states_alive = []

        self.episode_size = episode_size
        self.episode_decisions = np.zeros((8))

        self.episodes_wins = 0
        self.episodes_nb = 0
        self.iter = 0

    def explore_exploit(self, prediction):
        choice = np.random.rand()
        if choice <= .8:
            return prediction
        return one_hot(round(np.random.rand() * 7))

    def update(self, frame, is_dead):
        frame = preprocessing(frame)
        act_h, y_pred = self.model.forward_keep_activations(frame)
        y_pred = self.explore_exploit(y_pred)
        self.activations.append((act_h, y_pred))
        self.frames.append(frame)

        #print(y_pred)

        self.episode_decisions += one_hot(y_pred)

        self.iter += 1
        if is_dead or self.iter == self.episode_size:
            for activation, frame in zip(self.activations, self.frames):
                if is_dead: # Agent is dead
                    #y_true = np.array([0, 0, 0, 0.5, 0.5, 0, 0, 0])
                    y_true = wrong_move(one_hot(activation[1]))
                    #print("\n", activation[1],'\n', y_true, '\n\n')
                    grads = self.model.gradients(frame, activation[0], activation[1], y_true)
                    self.model.backward(grads)
                else:
                    y_true = one_hot(activation[1])
                    grads = self.model.gradients(frame, activation[0], activation[1], y_true)
                    self.model.backward(grads)

            print(f"Episode #{self.episodes_nb} : {'LOSE' if is_dead else 'WIN'}   Decisions : {self.episode_decisions}")

            self.reset()
            self.episodes_nb += 1
            self.episode_decisions.fill(0)

            if not is_dead:
                self.episodes_wins += 1

            if self.episodes_nb % 100 == 0:
                print(f"Last 100 episodes : {self.episodes_wins}%")
                self.episodes_wins = 0


        return np.argmax(y_pred)

    def reset(self):
        self.activations = []
        self.iter = 0
    
    def load(self, path):
        loaded = np.load(path)
        self.model.Wh = loaded['Wh']
        self.model.Bh = loaded['Bh']
        self.model.Wo = loaded['Wo']
        self.model.Bo = loaded['Bo']
    
    def save(self):
        np.savez_compressed("models/model_" + str(self.episodes_nb),
            Wh=self.model.Wh,
            Bh=self.model.Bh,
            Wo=self.model.Wo,
            Bo=self.model.Bo)



