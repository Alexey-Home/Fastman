import pygame


class Player:

    def __init__(self):
        self.x = 50
        self.y = 400
        self.speed = 0
        self.image = pygame.image.load("images/man1.jpg")
        self.jump_count = 15
        self.racing = 0.1
        self.jump_high = self.jump_count
        self.y_begin_jump = self.y
        self.is_jump = False
        self.single_jump = False
        self.is_run = True
        self.direction_of_move = None
        self.collision = self.image.get_rect(topleft=(self.x, self.y))
        self.is_col = False

    def speed_increase(self):
        """Увелечение скорости игрока"""
        self.speed += self.racing

    def speed_reset(self):
        """Сброс скорости игрока"""
        self.speed = 0
        self.racing = 0.1

    def speed_reduction(self):
        """Уменьшение скорости игрока"""
        self.racing += 0.01
        self.speed -= self.racing

    def run(self, keys):
        """Бег игрока влево и вправо"""
        if self.is_run:
            if keys[pygame.K_RIGHT] and self.x < 1000 and self.is_col:
                self.direction_of_move = "right"
                self.speed_increase()
                self.x += self.speed
            elif keys[pygame.K_LEFT] and self.x > 24 and self.is_col:
                self.direction_of_move = "left"
                self.speed_increase()
                self.x -= self.speed
            else:
                self.speed_reset()
        else:
            if self.direction_of_move == "right" and self.speed > 0 and self.x < 1000:
                self.speed_reduction()
                self.x += self.speed
            elif self.direction_of_move == "left" and self.speed > 0 and self.x > 24:
                self.speed_reduction()
                self.x -= self.speed
            else:
                self.speed_reset()


    def jump(self):
        """Прыжок игрока"""
        if self.is_jump and self.is_col:
            if self.jump_count >= 0:
                self.y -= (self.jump_count ** 2) / 10
            else:
                self.is_jump = False
                self.jump_count = self.jump_high
            self.jump_count -= 1


    def physics(self, collisions):
        """Притяжение игрока"""
        self.collision = self.image.get_rect(topleft=(self.x, self.y))
        for num, col in enumerate(collisions):
            if self.collision.colliderect(col):
                self.is_col = True
                break
            else:
                continue
        else:
            if not self.is_jump:
                self.y += 5
                self.is_col = False


