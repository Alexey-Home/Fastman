import pygame


class Player:

    def __init__(self):
        self.x = 200
        self.y = 200
        self.speed = 0
        self.image = pygame.image.load("images/man1.jpg")
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.racing = 0.1
        self.jump_high = 16
        self.jump_count = self.jump_high
        self.max_jump_high = 25
        self.y_begin_jump = self.y
        self.is_jump = False
        self.single_jump = False
        self.step = 1
        self.is_run = True
        self.direction_of_move = None
        self.collision_player = self.image.get_rect(topleft=(self.x, self.y))
        self.is_col = False
        self.side_contact = None
        self.speed_gravity = 5
        self.sliding_time = 50
        self.number_contact_object = None


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
            if keys[pygame.K_RIGHT] and self.x < 1000:
                self.direction_of_move = "right"
                self.speed_increase()
                self.x += self.speed
            elif keys[pygame.K_LEFT] and self.x > 24:
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


    def jump(self, keys):
        """Прыжок игрока"""
        if self.is_jump:
            if keys[pygame.K_SPACE] and self.jump_count <= self.max_jump_high:
                self.jump_count += self.step/2
            if self.side_contact == "left" and not self.is_col:
                self.x -= 3
            elif self.side_contact == "right" and not self.is_col:
                self.x += 3
            if self.jump_count >= 0:
                self.y -= self.jump_count / 2
            else:
                self.is_jump = False
                self.jump_count = self.jump_high + self.step
            self.jump_count -= self.step


    def gravity(self, keys):
        """Притяжение игрока"""
        if self.is_col and (self.side_contact == "left" or self.side_contact == "right"):
            if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and self.sliding_time >= 0:
                self.speed_gravity = 1
                self.sliding_time -= 1
                self.y += self.speed_gravity
                if self.sliding_time <= 0:
                    self.bounce_off_walls(1)
            else:
                self.speed_gravity = 5
                self.is_col = False
                self.bounce_off_walls(0.1)
            print(self.sliding_time)
        else:
            self.speed_gravity = 5
            if not self.is_jump and not self.is_col:
                self.y += self.speed_gravity


    def bounce_off_walls(self, value):
        """Отскок от стены"""
        if self.side_contact == "left":
            self.x -= value
        elif self.side_contact == "right":
            self.x += value


    def check_collision(self, collisions):
        """Проверка коллизии"""
        self.collision_player = self.image.get_rect(topleft=(self.x, self.y))
        col = self.collision_player.collidelistall(collisions)

        if col != self.number_contact_object:
            self.number_contact_object = col
            self.sliding_time = 50
        

        if col:
            self.is_col = True
            self.side_of_contact = self.get_side_of_contact(collisions[col[0]])
            self.contact_side(collisions[col[0]])
        else:
            self.is_col = False
            self.side_of_contact = None


    def get_side_of_contact(self, objects):
        """Определение стороны контакта игрока с объектом"""
        delta = {
            "left": abs(self.collision_player.right - objects.left + self.width),
            "right": abs(self.collision_player.left - objects.right - self.width),
            "top": abs(self.collision_player.bottom - objects.top),
            "bottom": abs(self.collision_player.top - objects.bottom - self.height * 2),
        }
        side = []
        min_num = 9999
        for key, value in delta.items():
            if value < min_num:
                min_num = value
        for key, value in delta.items():
            if value == min_num:
                side.append(key)
        for i in side:
            if self.side_contact == i:
                return
        self.side_contact = side[0]


    def contact_side(self, side):
        """Соприкосновение игрока с объектом"""
        if self.side_contact == "left":
            self.x = side.left - self.width + 0.5
            self.speed_reset()
        elif self.side_contact == "right":
            self.x = side.right - 0.5
            self.speed_reset()
        elif self.side_contact == "top":
            self.y = side.top - self.height + 0.5
        elif self.side_contact == "bottom":
            self.y = side.bottom
            self.is_col = False
            self.is_jump = False
            self.jump_count = self.jump_high + self.step

