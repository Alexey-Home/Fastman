import pygame


class Bomb:
    def __init__(self, position):
        self.image = pygame.image.load("images/bomb.png").convert_alpha()
        self.height = self.image.get_height()
        self.position = (position[0], position[1] - self.height)
        self.collisions = self.image.get_rect(topleft=self.position)


class Hedgehod:
    def __init__(self, position, collisions_rect):
        self.image = pygame.image.load("images/hedgehod.png").convert_alpha()
        self.height = self.image.get_height()
        self.position = (position[0], position[1] - self.height)
        self.collision = self.image.get_rect(topleft=self.position)
        tmp = self.collision.collidelistall(collisions_rect)
        if tmp:
            self.number_collision_rect = tmp[0]
        else:
            self.number_collision_rect = None
        self.attack_on = False
        self.speed = 0

    def attack(self, player_x):
        """Атака ежа-убийцы"""
        if self.speed < 6:
            self.speed += 0.3
        if self.position[0] < player_x:
            self.position = (self.position[0] + self.speed, self.position[1])
        elif self.position[0] > player_x:
            self.position = (self.position[0] - self.speed, self.position[1])
        self.collision = self.image.get_rect(topleft=self.position)


class Bullet:
    def __init__(self, position):
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.position = (position[0] + 3, position[1] + 3)
        self.collision = self.image.get_rect(topleft=self.position)
        self.dimension = 0


class Gun:
    def __init__(self, position):
        self.image = pygame.image.load("images/gun.png").convert_alpha()
        self.height = self.image.get_height()
        self.top_gun = position[1] - self.height
        self.bottom_gun = position[1]
        self.position = (position[0], position[1] - self.height)
        self.bullets = []
