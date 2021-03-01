import pygame
import random

from config import SCREEN_HEIGHT_g, SCREEN_WIDTH_g

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_range=(5, 20)):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((5, 2))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH_g + 20, SCREEN_WIDTH_g + 100),
                random.randint(0, SCREEN_HEIGHT_g),
            )
        )
        self.speed = random.randint(*speed_range)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() # removed from sprite groups