import pygame
import random

from player import *
from enemy import Enemy

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

        # Create a custom event for adding a new enemy
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        # Instantiate player. Right now, this is just a rectangle.
        self.player = Player()

        # Create groups to hold enemy sprites and all sprites
        # - enemies is used for collision detection and position updates
        # - all_sprites is used for rendering
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

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

                # Add a new enemy?
                elif event.type == self.ADDENEMY:
                    # Create the new enemy and add it to sprite groups
                    new_enemy = Enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)

            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

            # Update enemy position
            self.enemies.update()

            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Draw all sprites
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                # If so, then remove the player and stop the loop
                self.player.kill()
                self.running = False

            # Update the display
            pygame.display.flip()

            # Ensure program maintains a rate of 30 frames per second
            self.clock.tick(30)