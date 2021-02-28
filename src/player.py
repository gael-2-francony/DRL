import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
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
    
    # Move the sprite based on user keypresses
    def update_player(self, pressed_keys, screen_width, screen_height):
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
    
    def update_agent(self, frame, screen_width, screen_height):
        move = self.agent.predict(frame)
        print(f"Move : {move}")
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