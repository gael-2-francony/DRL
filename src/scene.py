import pygame

from player import *
from enemy import Enemy
from MLP import MLP
from engine import SCREEN_HEIGHT_g, SCREEN_WIDTH_g

class ClassicScene():
    def __init__(self, screen_width, screen_height):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        # Event to spawn enemies
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.agent = MLP((SCREEN_WIDTH_g, SCREEN_HEIGHT_g), 16)
        self.player = Player(self.agent)

        self.enemies = pygame.sprite.Group()
        self.enemy_speed = (5, 20)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
    
    def update_event(self, event):
        # Add a new enemy?
        if event.type == self.ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.enemy_speed)
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)

    def update(self, frame_buffer):
        # Get the set of keys pressed and check for user input
        #pressed_keys = pygame.key.get_pressed()
        self.player.update_agent(frame_buffer, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Update enemy position
        self.enemies.update()

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            # If so, then remove the player and stop the loop
            self.player.kill()
            return False
        return True

class FastScene(ClassicScene):
    def __init__(self, screen_width, screen_height):
        super(FastScene, self).__init__(screen_width, screen_height)
        pygame.time.set_timer(self.ADDENEMY, 100)
        self.enemy_speed = (20, 30)
