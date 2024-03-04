import pygame


class Bomb:
    def __init__(self, position):
        self.image = pygame.image.load("images/bomb.png").convert_alpha()
        self.height = self.image.get_height()
        self.position = (position[0], position[1] - self.height)
        self.collisions = self.image.get_rect(topleft=self.position)


