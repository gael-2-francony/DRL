import pygame

from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g

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
        self.surf = pygame.Surface((20, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.move_ip( SCREEN_WIDTH_g // 4, SCREEN_HEIGHT_g // 2)
        self.speed = 1

    def update(self, frame=None):
        if self.agent is not None:
            return self.update_agent(frame)
        else:
            self.update_player()
        return True

    # Move the sprite based on user keypresses
    def update_player(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH_g:
            self.rect.right = SCREEN_WIDTH_g
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT_g:
            self.rect.bottom = SCREEN_HEIGHT_g

    def has_died(self, frame):
        self.kill()
        if self.agent:
            self.agent.replay()

    def update_agent(self, frame):
        move = self.agent.act(frame)
        if move == 1: #UP
            self.rect.move_ip( 0, -self.speed)
        if move == 2: # DOWN
            self.rect.move_ip( 0,  self.speed)
        if move == 3: # LEFT
            self.rect.move_ip(-self.speed,  0)
        if move == 4: # RIGHT
            self.rect.move_ip( self.speed,  0)
        if move == 5: # UP/Left
            self.rect.move_ip(-self.speed, -self.speed)
        if move == 6: # UP/RIGHT
            self.rect.move_ip( self.speed, -self.speed)
        if move == 7: # DOWN/LEFT
            self.rect.move_ip(-self.speed,  self.speed)
        if move == 8: # DOWN/RIGHT
            self.rect.move_ip( self.speed,  self.speed)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
            return False
        if self.rect.right > SCREEN_WIDTH_g:
            self.rect.right = SCREEN_WIDTH_g
            return False
        if self.rect.top <= 0:
            self.rect.top = 0
            return False
        if self.rect.bottom >= SCREEN_HEIGHT_g:
            self.rect.bottom = SCREEN_HEIGHT_g
            return False
        return True