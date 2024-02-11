import pygame


class Player:

    def __init__(self):
        self.x = 30
        self.y = 700
        self.speed = 0.001
        self.image = pygame.image.load("images/man1.jpg")
        self.jump_count = 7
        self.jump_high = 7
        self.y_begin_jump = self.y
        self.is_jump = True

    def speed_increase(self):
        self.speed += 0.001

    def speed_reset(self):
        self.speed = 0.001



