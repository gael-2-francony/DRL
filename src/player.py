import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, agent=None):
        super(Player, self).__init__()
        self.agent = agent
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, screen_width, screen_height, frame=None):
        if self.agent is not None:
            self.update_agent(frame, screen_width, screen_height)
        else:
            self.update_player(screen_width, screen_height)
    
    # Move the sprite based on user keypresses
    def update_player(self, screen_width, screen_height):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
    
    def has_died(self, frame):
        self.kill()
        if self.agent:
            self.agent.update(frame, True)
    
    def update_agent(self, frame, screen_width, screen_height):
        move = self.agent.update(frame, False)
        if move == 1: #UP
            self.rect.move_ip( 0, -5)
        if move == 2: # DOWN
            self.rect.move_ip( 0,  5)
        if move == 3: # LEFT
            self.rect.move_ip(-5,  0)
        if move == 4: # RIGHT
            self.rect.move_ip( 5,  0)
        if move == 5: # UP/Left
            self.rect.move_ip(-5, -5)
        if move == 6: # UP/RIGHT
            self.rect.move_ip( 5, -5)
        if move == 7: # DOWN/LEFT
            self.rect.move_ip(-5,  5)
        if move == 8: # DOWN/RIGHT
            self.rect.move_ip( 5,  5)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height