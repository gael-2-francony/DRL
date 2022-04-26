import os
import pygame

from player import *
from enemy import Enemy
from RL import RL_Agent
from DQN import DQN

class ClassicScene():
    def __init__(self, use_AIPlayer=False):

        self.add_enemy_time = 5
        self.add_enemy_tick = 0

        self.agent = None
        if (use_AIPlayer):
            self.agent = DQN()
            if os.path.exists("dqn.h5"):
                self.agent.model.load_weights("dqn.h5")
        self.player = Player(self.agent)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemy_speed = (1, 3)
        self.enemies = pygame.sprite.Group()

    def reset(self):
        self.player = Player(self.agent)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()

    def update(self, frame):
        alive = True
        if not self.player.update(frame):
            self.player.has_died(frame)
            alive = False
        else:
            self.add_enemy_tick += 1
            if self.add_enemy_tick >= self.add_enemy_time:
                self.add_enemy_tick = 0
                new_enemy = Enemy(self.enemy_speed)
                self.enemies.add(new_enemy)
                self.all_sprites.add(new_enemy)

            self.enemies.update()

            # Check collisions
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                self.player.has_died(frame)
                alive = False
        return alive

    def end(self):
        if self.agent:
            self.agent.save()

class FastScene(ClassicScene):
    def __init__(self, use_AIPlayer=False):
        super(FastScene, self).__init__(use_AIPlayer)
        pygame.time.set_timer(self.ADDENEMY, 100)
        self.enemy_speed = (20, 30)
