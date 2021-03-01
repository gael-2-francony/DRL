import pygame

from player import *
from enemy import Enemy
from RL import RL_Agent

class ClassicScene():
    def __init__(self, use_AIPlayer=False):

        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.agent = None
        if (use_AIPlayer):
            self.agent = RL_Agent()
        self.player = Player(self.agent)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemy_speed = (5, 20)
        self.enemies = pygame.sprite.Group()

    def reset(self):
        self.player = Player(self.agent)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()

    
    def update_event(self, event):
        if event.type == self.ADDENEMY:
            new_enemy = Enemy(self.enemy_speed)
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)

    def update(self, frame):
        self.player.update(frame)

        self.enemies.update()

        # Check collisions
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.has_died(frame)
            return False
        return True
    
    def end(self):
        if self.agent:
            self.agent.save()

class FastScene(ClassicScene):
    def __init__(self, use_AIPlayer=False):
        super(FastScene, self).__init__(use_AIPlayer)
        pygame.time.set_timer(self.ADDENEMY, 100)
        self.enemy_speed = (20, 30)
