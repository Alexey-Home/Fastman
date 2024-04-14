import random
import pygame
from enemies import Bullet

count = 0


class All:
    def __init__(self, path_image, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(path_image).convert_alpha()
        self.collision = self.image.get_rect(topleft=(self.x, self.y))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.side_contact_left_right = None
        self.side_contact_up_down = None
        self.coordinate_left_right = None
        self.coordinate_up_down = None
        self.contact = None
        self.speed_gravity = 5
        self.is_col = False

    def get_side_of_contact(self, level, num_collisions):
        """Определение стороны контакта с объектом"""
        sides = []

        for col in num_collisions:

            tmp = {
                "left": abs(self.collision.right - level.collisions_rectangle[col].left + self.width),
                "right": abs(self.collision.left - level.collisions_rectangle[col].right - self.width),
                "top": abs(self.collision.bottom - level.collisions_rectangle[col].top),
                "bottom": abs(self.collision.top - level.collisions_rectangle[col].bottom),
            }

            side = sorted(tmp.items(), key=lambda item: item[1])
            side = side[0][0]

            sides.append(side)

            if side == "top":
                self.side_contact_up_down = side
                self.coordinate_up_down = level.collisions_rectangle[col].top
            elif side == "bottom":
                self.side_contact_up_down = side
                self.coordinate_up_down = level.collisions_rectangle[col].bottom
            elif side == "left":
                self.side_contact_left_right = side
                self.coordinate_left_right = level.collisions_rectangle[col].left
            elif side == "right":
                self.side_contact_left_right = side
                self.coordinate_left_right = level.collisions_rectangle[col].right

        if "left" not in sides and "right" not in sides:
            self.side_contact_left_right = None
            self.coordinate_left_right = None
        if "top" not in sides and "bottom" not in sides:
            self.side_contact_up_down = None
            self.coordinate_up_down = None


class Player(All):
    def __init__(self, path_image, x, y, gameplay):
        super().__init__(path_image, x, y)
        self.max_speed = 5
        self.speed = 0
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
        self.is_col = False
        self.number_contact_object = None
        self.alive = True
        self.death_from = None
        self.body = []
        self.keys = None
        self.gameplay = gameplay
        self.level_done = False
        self.is_skid = False

    def speed_increase(self):
        """Увелечение скорости игрока"""
        if self.speed <= self.max_speed:
            self.speed += self.racing

    def speed_reset(self):
        """Сброс скорости игрока"""
        self.speed = 0
        self.racing = 0.1

    def speed_reduction(self):
        """Уменьшение скорости игрока"""
        self.racing += 0.01
        self.speed -= self.racing

    def run(self):
        """Бег игрока влево и вправо"""
        if self.is_skid:
            self.skid()
            return
        if self.is_run:
            if self.keys[pygame.K_RIGHT] and self.keys[pygame.K_LEFT]:
                self.is_skid = True
            elif self.keys[pygame.K_RIGHT] and self.x < 1000:
                self.direction_of_move = "right"
                self.speed_increase()
                self.x += self.speed
            elif self.keys[pygame.K_LEFT] and self.x > 24:
                self.direction_of_move = "left"
                self.speed_increase()
                self.x -= self.speed
        else:
            self.is_skid = False
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_LEFT]:
            self.is_run = True

    def skid(self):
        """Занос после бега"""
        if self.speed <= 0:
            self.is_skid = False
            self.speed_reset()
        if self.direction_of_move == "right" and self.speed > 0 and self.x < 1000:
            self.speed_reduction()
            self.x += self.speed
        elif self.direction_of_move == "left" and self.speed > 0 and self.x > 24:
            self.speed_reduction()
            self.x -= self.speed

    def jump(self):
        """Прыжок игрока"""
        if self.is_jump:
            if self.keys[pygame.K_SPACE] and self.jump_count <= self.max_jump_high:
                self.jump_count += self.step / 2
            self.jumping_off_wall()
            if self.jump_count >= 0:
                self.y -= self.jump_count / 2
            else:
                self.is_jump = False
                self.jump_count = self.jump_high + self.step
            self.jump_count -= self.step

    def jumping_off_wall(self):
        """Отпрыгивание стены"""
        if self.side_contact_left_right == "left" and not self.is_col:
            self.x -= 2
        elif self.side_contact_left_right == "right" and not self.is_col:
            self.x += 2

    def gravity(self):
        """Притяжение игрока"""
        if self.is_col and \
                (self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT]) \
                and self.side_contact_left_right is not None and self.side_contact_up_down is None:
            self.speed_gravity = 1
        else:
            self.speed_gravity = 5
        if not self.is_jump:
            self.y += self.speed_gravity

    def bounce_off_walls(self, value):
        """Отскок от стены"""
        if self.side_contact_left_right == "left":
            self.x -= value
        elif self.side_contact_left_right == "right":
            self.x += value

    def contact_side(self):
        """Соприкосновение игрока с объектом"""
        if self.side_contact_left_right == "left":
            self.x = self.coordinate_left_right - self.width + 0.5
            self.speed_reset()
        elif self.side_contact_left_right == "right":
            self.x = self.coordinate_left_right - 0.5
            self.speed_reset()
        if self.side_contact_up_down == "top":
            self.y = self.coordinate_up_down - self.height + 0.5
        elif self.side_contact_up_down == "bottom":
            self.y = self.coordinate_up_down
            self.is_col = False
            self.is_jump = False
            self.jump_count = self.jump_high + self.step

    def check_collision_rect(self, level):
        """Проверка коллизии"""
        col = self.collision.collidelistall(level.collisions_rectangle)
        if col != self.number_contact_object:
            self.number_contact_object = col
        if col:
            self.is_col = True
            self.get_side_of_contact(level, col)
            self.contact_side()
        else:
            self.is_col = False

    def check_collision_button(self, button, exit_door):
        """Проверка коллизии кнопки открытия двери"""
        if button.collision and self.collision.colliderect(button.collision):
            button.image = pygame.image.load("images/button_green.png").convert_alpha()
            exit_door.open = True
            exit_door.image = pygame.image.load("images/opened_door.png").convert_alpha()

    def check_collision_exit(self, exit_door):
        """Проверка коллизии выхода"""
        if exit_door.collision and exit_door.open and self.collision.colliderect(exit_door.collision):
            self.level_done = True

    def check_collision_bombs(self, level):
        """Проверка коллизии бомб"""
        col = self.collision.collidelistall(level.collisions_bomb)
        if col:
            level.bombs[col[0]].image = pygame.image.load("images/explosion.png").convert_alpha()
            self.death_from = "explosion"
            self.alive = False

    def check_collision_hedgehod(self, collision_hedgehod):
        """Проверка коллизий игрока и ежа-убийцы."""
        col = self.collision.colliderect(collision_hedgehod)
        if col:
            self.death_from = "hedgehod"
            self.alive = False

    def check_collision_add_sec(self, level):
        col = self.collision.collidelistall(level.collisions_add_sec)
        if col:
            return col

    def bomb_explosion(self, screen, level):
        """Подрыв на бомбе"""
        for part in self.body:
            screen.blit(part.image, (part.x, part.y))
            part.collision = part.image.get_rect(topleft=(part.x, part.y))
            col = part.collision.collidelistall(level.collisions_rectangle)
            if not col:
                part.x += part.speed_x
            else:
                part.get_side_of_contact(level, col)
                part.contact_side(level.collisions_rectangle[col[0]])
            if part.flight_altitude >= 0:
                part.y -= part.flight_altitude / 1.8
            else:
                part.y += self.speed_gravity
            part.flight_altitude -= 1

    def create_body(self):
        """Создает части тела"""
        self.body = [
            PartBody("images/partbody.png", self.x, self.y),
            PartBody("images/partbody.png", self.x, self.y, ),
            PartBody("images/partbody.png", self.x, self.y, ),
            PartBody("images/partbody.png", self.x, self.y, ),
        ]

    def gameplay_player(self, menu, screen, level, timer, button=None, exit_door=None):
        """Основные функции игрока: проверка нажатие клавиш, проверка коллизий с объектами."""
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameplay = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.is_col:
                self.is_jump = True
                self.is_col = False
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                self.is_run = True
            elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                self.is_run = False
                self.is_skid = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                menu.press_r = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                menu.press_p = True

        if self.alive:
            screen.blit(self.image, (self.x, self.y))
            self.run()
            self.jump()
        else:
            if self.death_from == "explosion":
                if self.body:
                    self.bomb_explosion(screen, level)
                    self.alive = False
                else:
                    self.create_body()
        self.update_the_collision_player()
        self.gravity()
        self.check_collision_rect(level)
        if button and exit_door:
            self.check_collision_button(button, exit_door)
            self.check_collision_exit(exit_door)
        self.check_collision_bombs(level)
        self.detection_player(level)
        col = self.check_collision_add_sec(level)
        if col:
            level.add_sec.pop(col[0])
            level.collisions_add_sec.pop(col[0])
            timer.start_time += 3
        if self.alive:
            self.detection_gun(level)

    def detection_gun(self, level):
        """Обнаружение цели пушкой"""
        for i in range(len(level.guns)):
            if level.guns[i].top_gun <= self.y <= level.guns[i].bottom_gun:
                bullet = Bullet((level.guns[i].position[0], level.guns[i].position[1] + 1))
                try:
                    if abs(level.guns[i].bullets[-1].position[0] - bullet.position[0]) > 100:
                        bullet.dimension = 3 if bullet.position[0] < self.x else - 3
                        level.guns[i].bullets.append(bullet)
                except IndexError:
                    bullet.dimension = 3 if bullet.position[0] < self.x else - 3
                    level.guns[i].bullets.append(bullet)

    def detection_player(self, level):
        """Определние находится ли игрок на поверхности вместе с ежом-убийцей"""
        if self.alive:
            for i in level.hedgehods:
                if i.number_collision_rect in self.number_contact_object:
                    i.attack(self.x)
                    self.check_collision_hedgehod(i.collision)
                else:
                    i.speed = 0

    def update_the_collision_player(self):
        """Обновляет место положение колизии игрока"""
        self.collision = self.image.get_rect(topleft=(self.x, self.y))

    def check_death(self, screen):
        """Проверяет умер ли игрок"""
        if self.alive and self.y > screen.get_height():
            self.gameplay = False
            self.alive = False
        elif not self.alive:
            self.gameplay = False

    def check_level_done(self):
        """Проверяет ли прошел ли уровень игрок"""
        if self.level_done:
            self.gameplay = False
            self.alive = False

    def check_timeover(self, tracking):
        """Проверка окончания время """
        if tracking <= 0:
            self.gameplay = False
            self.alive = False


class PartBody(All):
    def __init__(self, path_image, x, y):
        super().__init__(path_image, x, y)
        self.speed_x = random.randint(-5, 5)
        self.flight_altitude = random.randint(10, 20)

    def contact_side(self, collision_rect):
        """Определение контакта частей тела с обьектом"""
        if self.side_contact_left_right == "left" or self.side_contact_left_right == "right":
            self.speed_x = self.speed_x / 2 * -1
            self.x += self.speed_x
        if self.side_contact_up_down == "top":
            self.flight_altitude = 0
            self.y = collision_rect.top - self.height + 0.5
        elif self.side_contact_up_down == "bottom":
            self.flight_altitude = 0
            self.y = collision_rect.bottom + 0.5
