import pygame


class Player:

    def __init__(self):
        self.x = 30
        self.y = 700
        self.speed = 0.001
        self.image = pygame.image.load("images/man1.jpg")
        self.jump_count = 100
        self.jump_high = 100
        self.y_begin_jump = self.y
        self.is_jump = False
        self.single_jump = True

    def speed_increase(self):
        self.speed += 0.001

    def speed_reset(self):
        self.speed = 0.001

    def run(self, keys):
        if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            self.speed_reset()
        elif keys[pygame.K_RIGHT] and self.x < 1000:
            self.speed_increase()
            self.x += self.speed
        elif keys[pygame.K_LEFT] and self.x > 24:
            self.speed_increase()
            self.x -= self.speed
        else:
            self.speed_reset()


    def jump(self, keys):

        if not self.is_jump:
            if keys[pygame.K_SPACE]:
                self.is_jump = True
            else:
                self.single_jump = False
        else:
            if self.jump_count >= -self.jump_high:
                if self.jump_count > 0:
                    self.y -= (self.jump_count ** 2) / 5000
                else:
                    self.y += (self.jump_count ** 2) / 5000
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = self.jump_high



