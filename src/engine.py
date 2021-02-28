import pygame
import random
import numpy as np

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from scene import ClassicScene
SCREEN_WIDTH_g = 800
SCREEN_HEIGHT_g = 600
class Engine():
    def __init__(self):
        # Define constants for the screen width and height
        self.SCREEN_WIDTH = SCREEN_WIDTH_g
        self.SCREEN_HEIGHT = SCREEN_HEIGHT_g

        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.scene = ClassicScene(self.screen_width, self.screen_height)

        self.running = True
        self.clock = pygame.time.Clock()

        self.prev_frame = None 

    
    def run_loop(self):
        # Main loop
        while self.running:
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:
                    running = False

                self.scene.update_event(event)

            frame = self.screen.get_buffer()
            frame_buffer = np.fromstring(frame.raw, dtype='b').reshape(self.screen_height, self.screen_width, 4)
            if self.prev_frame is not None:
                diff = frame_buffer - self.prev_frame
            else:
                diff = frame_buffer
            self.prev_frame = frame_buffer

            self.running = self.scene.update(diff[:,:,0])
            del frame

            # Draw all sprites
            self.screen.fill((0, 0, 0))
            for entity in self.scene.all_sprites:
                self.screen.blit(entity.surf, entity.rect)
            pygame.display.flip()

            self.clock.tick(30)