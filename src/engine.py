import matplotlib.pyplot as plt
import pygame
import random
import numpy as np

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from scene import ClassicScene
from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g

class Engine():
    def __init__(self, use_AIPlayer=True, render=False):
        # Initialize pygame
        self.render = render
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH_g, SCREEN_HEIGHT_g))

        self.scene = ClassicScene(use_AIPlayer)

        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.score = 0
        self.scores = []
        self.episode = 0

        self.prev_frame = None

    def reset(self):
        self.prev_frame = None
        print(f"Game Over, Episode {self.episode}: score {self.score}")
        self.scores.append(self.score)
        self.score = 0
        self.episode += 1
        self.scene.reset()

    def draw(self):
        # Draw all sprites
        self.screen.fill((0, 0, 0))
        for entity in self.scene.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        if self.render:
            pygame.display.flip()

    def compute_decision_frame(self):
        frame = pygame.surfarray.array2d(self.screen)
        if self.prev_frame is not None:
            diff = frame - self.prev_frame
        else:
            diff = frame
        self.prev_frame = frame
        return diff

    def update(self):
        state = self.compute_decision_frame()
        self.running = self.scene.update(state)

    def end(self):
        pass

    def run_loop(self):
        while self.running:
            self.score += 1
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == QUIT:
                    self.running = False

            self.update()

            self.draw()

            self.clock.tick(self.fps)

        self.end()

class TrainingEngine(Engine):
    def __init__(self, file_name=None, render=True):
        super(TrainingEngine, self).__init__(True, render)
        self.out_file_name = file_name
        self.fps = 360

    def update(self):
        state = self.compute_decision_frame()[:, :, 0]
        alive = self.scene.update(state)
        self.scene.player.agent.memorize(self.scene.player.agent.last_state,
                                         self.scene.player.agent.last_action, 1 if alive else -1, state, True if not alive else False)
        if self.scene.player.agent.can_replay():
            self.scene.player.agent.replay()
        if not alive:
            self.reset()

    def end(self):
        fig, ax = plt.subplots(figsize=(15, 9))
        ax.set_title("Score of agent through time")
        ax.set_xlabel("Number of training episodes")
        ax.set_ylabel("Frames survived")
        ax.plot(np.arange(len(self.scores) / 2), self.scores[::2])
        plt.show()
        self.scene.player.agent.save()
        self.scene.end()
