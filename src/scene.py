import pygame

from player import *
from enemy import Enemy

class ClassicScene():
    def __init__(self, screen_width, screen_height):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
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
    
    def update_event(self, event):
        # Add a new enemy?
        if event.type == self.ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)

    def update(self):
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Update enemy position
        self.enemies.update()

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            # If so, then remove the player and stop the loop
            self.player.kill()
            return False
        return True