import pygame
import random
import numpy as np

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from scene import ClassicScene
from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g

class Engine():
    def __init__(self, use_AIPlayer=True):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH_g, SCREEN_HEIGHT_g))

        self.scene = ClassicScene(use_AIPlayer)

        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.prev_frame = None 
    
    def reset(self):
        self.prev_frame = None
        self.scene.reset()
        pass
    
    def draw(self):
        # Draw all sprites
        self.screen.fill((0, 0, 0))
        for entity in self.scene.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        pygame.display.flip()

    def compute_decision_frame(self):
        frame = self.screen.get_buffer()
        frame_buffer = np.fromstring(frame.raw, dtype='b').reshape(SCREEN_HEIGHT_g, SCREEN_WIDTH_g, 4)
        if self.prev_frame is not None:
            diff = frame_buffer - self.prev_frame
        else:
            diff = frame_buffer
        self.prev_frame = frame_buffer
        del frame
        return diff

    def update(self):
        self.running = self.scene.update(self.compute_decision_frame()[:,:,0])
    
    def end(self):
        pass

    def run_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == QUIT:
                    self.running = False

                self.scene.update_event(event)

            self.update()

            self.draw()

            self.clock.tick(self.fps)

        self.end()

class TrainingEngine(Engine):
    def __init__(self, file_name=None):
        super(TrainingEngine, self).__init__(True)
        self.out_file_name = file_name
        self.fps = 360
    
    def update(self):
        if not self.scene.update(self.compute_decision_frame()[:,:,0]):
            self.reset()
    
    def end(self):
        self.scene.end()