import pygame
import random

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from scene import ClassicScene

class Engine():
    def __init__(self):
        # Define constants for the screen width and height
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # Initialize pygame
        pygame.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.scene = ClassicScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Variable to keep the main loop running
        self.running = True

        # Setup the clock for a decent framerate
        self.clock = pygame.time.Clock()
    
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

            self.running = self.scene.update()

            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Draw all sprites
            for entity in self.scene.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            # Update the display
            pygame.display.flip()

            # Ensure program maintains a rate of 30 frames per second
            self.clock.tick(30)