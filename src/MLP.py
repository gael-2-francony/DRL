import numpy as np
from RL import preprocessing

def softmax_ind(X, ind):
    return np.exp(X[ind]) / np.sum(np.exp(X), axis=-1)

def softmax(X):
    return np.array([softmax_ind(X, i) for i,_ in enumerate(X)])

def deriv_softmax_ind(X, ind):
    return np.exp(X[ind]) * np.sum(np.exp([x for i,x in enumerate(X) if i!=ind] ), axis=-1) / np.square(np.sum(np.exp(X), axis=-1))

def deriv_softmax(X):
    return np.array([deriv_softmax_ind(X, i) for i,_ in enumerate(X)])

def sigmoid(X):
    return 1 / (1 + np.exp(-X))

def deriv_sigmoid(X):
    return sigmoid(X) * (1 - sigmoid(X))

class MLP():
    """
    A Multi-Layer Perceptron, also called Fully Connected Neural Network to decide the policy
    for the RL framework.

    Should be fed with a frame from the game and outputs a number between 0 and 7 corresponding
    to the direction the player should move in.
    """
    def __init__(self, input_shape, hidden_shape, output_shape=9, learning_rate=0.0001):
        self.Wh = np.random.uniform(low=-0.05, high=0.05, size=(np.prod(input_shape), hidden_shape))
        self.Bh = np.zeros(hidden_shape)
        self.Wo = np.random.uniform(low=-0.05, high=0.05, size=(hidden_shape, output_shape))
        self.Bo = np.zeros(output_shape)
        self.learning_rate = learning_rate
        return

    def forward(self, X):
        _,_,probas = self.forward_keep_activations(X)
        return probas


    def forward_keep_activations(self, X):
        zh = np.dot(X, self.Wh) + self.Bh
        activation_h = sigmoid(zh)
        zo = np.dot(zh, self.Wo) + self.Bo
        activation_o = sigmoid(zo)
        probas = softmax(activation_o)
        return activation_h, activation_o, probas

    #Implement Negative Log Likehood (also called cross-entropy)
    def loss(self, y_pred, y_true):
        return -np.mean(np.sum(y_true * np.log(y_pred), axis=-1))

    def gradients(self, FIXME): #TODO
        pass #Compute gradients for weights and biases using Chain rule

    def backward(self, y_pred): #TODO
        pass #Update weights and biases using gradients

    def train(self, X): #TODO
        pass #Iterate cross-entropy over batch of data and backpropagate accordingly

    def predict(self, X): #TODO
        # Use final weights and biases to compute prediction for given input
        X = preprocessing(X)
        return np.argmax(self.forward(X))