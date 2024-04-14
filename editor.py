import datetime
import pygame

from enemies import Bomb, Hedgehod, Gun
import databasefunction as dbf


class Level:
    def __init__(self, level):
        self.rectangle = []
        self.collisions_rectangle = []
        self.bombs = []
        self.hedgehods = []
        self.collisions_hedgehods = []
        self.collisions_bomb = []
        self.position_exit = self.check_exist_object(level["door"])
        self.position_button = self.check_exist_object(level["button"])
        self.start_player = self.check_exist_object(level["start_player"])
        self.title = level["title"]
        self.show_menu = True
        self.guns = []
        self.bullets = []
        self.collisions_bullets = []
        self.add_sec = []
        self.collisions_add_sec = []
        self.start_time = None

        if level["objects_rect"]:
            for key, value in level["objects_rect"].items():
                self.rectangle.append((pygame.Surface((value["width"], value["height"])), value["position"]))
                self.rectangle[-1][0].fill(value["color"])
                self.collisions_rectangle.append(self.rectangle[-1][0].get_rect(topleft=(value["position"])))

        if level["bombs"]:
            for bomb_pos in level["bombs"]:
                self.bombs.append(Bomb(bomb_pos))
                self.collisions_bomb.append(self.bombs[-1].collisions)

        if level["hedgehods"]:
            for hed_pos in level["hedgehods"]:
                self.hedgehods.append(Hedgehod(hed_pos, self.collisions_rectangle))
                self.collisions_hedgehods.append(self.hedgehods[-1].collision)

        if level["gun"]:
            for gun_pos in level["gun"]:
                self.guns.append(Gun(gun_pos))

        if level["add_sec"]:
            for pos_el in level["add_sec"]:
                self.add_sec.append(AddSec(pos_el))
                self.collisions_add_sec.append(self.add_sec[-1].collision)

        if level["time"]:
            self.start_time = int(level["time"][0][0])

    @staticmethod
    def check_exist_object(obj):
        return obj[0] if obj else []

    def show_add_sec(self, screen):
        """Показывает элементы добавления секунды"""
        if self.add_sec:
            for sec in self.add_sec:
                screen.blit(sec.image, sec.position)

    def show_rect(self, screen):
        """Показывает обьекты интерьра уровня"""
        if self.rectangle:
            for rect in self.rectangle:
                screen.blit(rect[0], (rect[1][0], rect[1][1]))

    def show_bombs(self, screen):
        """Показывает бомбы"""
        if self.bombs:
            for bomb in self.bombs:
                screen.blit(bomb.image, bomb.position)

    def show_gun(self, screen):
        """Показывают пушки"""
        if self.guns:
            for gun in self.guns:
                screen.blit(gun.image, gun.position)

    def show_bullets(self, screen):
        """Показывает пули"""
        for gun in self.guns:
            if gun.bullets:
                for bullet in gun.bullets:
                    screen.blit(bullet.image, bullet.position)
                    new_position = bullet.position[0] + bullet.dimension
                    bullet.position = (new_position, bullet.position[1])

    def show_hedgehods(self, screen):
        """Показывает ежа-убийцу"""
        if self.hedgehods:
            for hedgehod in self.hedgehods:
                screen.blit(hedgehod.image, hedgehod.position)

    def check_alive(self, player):
        """Проверяет жив ли игрок"""
        if not player.alive:
            self.show_menu = True

    def detection_collision(self, player):
        """Обнаружение сталкновение с пулей"""
        for gun in self.guns:
            for i in range(len(gun.bullets)):
                gun.bullets[i].collision = gun.bullets[i].image.get_rect(topleft=gun.bullets[i].position)
                if gun.bullets[i].collision.colliderect(player.collision):
                    player.alive = False
                    break
                elif gun.bullets[i].collision.collidelistall(self.collisions_rectangle):
                    gun.bullets.pop(i)
                    break


class AddSec:
    def __init__(self, position):
        self.image = pygame.image.load("images/add_sec.png").convert_alpha()
        self.height = self.image.get_height()
        self.position = (position[0], position[1] - self.height)
        self.collision = self.image.get_rect(topleft=self.position)


class Menu:
    def __init__(self):
        self.label = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 30)
        self.new_game_label = self.label.render("Новая игра", False, "black")
        self.new_game_label_rect = self.new_game_label.get_rect(topleft=(700, 50))
        self.play_again_label = self.label.render("Играть заново(R)", False, "black")
        self.play_again_label_rect = self.play_again_label.get_rect(topleft=(700, 50))
        self.game_continue_label = self.label.render("Продолжить", False, "black")
        self.game_continue_label_rect = self.game_continue_label.get_rect(topleft=(700, 100))
        self.help = {"Влево": "Стрелка влево", "Вправо": "Стрелка вправо", "Прыжок": "Space"}
        self.image_button = pygame.image.load("images/button_red.png").convert_alpha()
        self.image_door = pygame.image.load("images/closed_door.png").convert_alpha()
        self.first_time = True
        self.press_r = False
        self.press_p = False

    def show_menu(self, screen):
        """Показывает меню"""
        if self.first_time:
            screen.blit(self.new_game_label, self.new_game_label_rect)
            pos_x = 100
            pos_y = 50
            for key, event in self.help.items():
                h = self.label.render(f"{key} - {event}", False, "grey")
                h_rect = h.get_rect(topleft=(pos_x, pos_y))
                screen.blit(h, h_rect)
                pos_y += 50
            screen.blit(self.image_button, (pos_x, 214))
            b = self.label.render("- кнопка открытия двери", False, "grey")
            b_rect = b.get_rect(topleft=(125, 200))
            screen.blit(b, b_rect)

            screen.blit(self.image_door, (pos_x, 260))
            d = self.label.render("- выход из локации", False, "grey")
            d_rect = d.get_rect(topleft=(125, 250))
            screen.blit(d, d_rect)

        else:
            screen.blit(self.play_again_label, self.play_again_label_rect)
        screen.blit(self.game_continue_label, self.game_continue_label_rect)

    def control_menu(self, level, flag):
        """Контролирует нажатие на параметры из меню"""
        mouse = pygame.mouse.get_pos()

        if self.new_game_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            dbf.new_game()
            return True
        elif (self.play_again_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]) or self.press_r:
            dbf.repeat_game(level)
            self.press_r = False
            return True
        elif (self.game_continue_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]) or self.press_p:
            self.press_p = False
            if flag:
                dbf.set_status_done(level)
            return True


class ClockOver:
    def __init__(self):
        self.time_over = None
        self.time_end = None
        self.res_sec = None
        self.second_begin = None
        self.minute_begin = None
        self.minute = None
        self.second = None
        self.start_time = None
        self.time_end = self.start_time
        self.tracking = 99999
        self.time = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 25)
        self.begin_level = False

    def subtraction_time(self):
        """Отсчет времени"""
        if not self.begin_level:
            self.second_begin = datetime.datetime.now().second
            self.begin_level = True
        seconds = datetime.datetime.now().second
        if self.second_begin <= seconds:
            self.second = self.res_sec + seconds - self.second_begin
            self.time_over = self.second
        else:
            self.res_sec = self.second + seconds
            self.time_over = self.res_sec

    def reset_time(self, t):
        """Сбросить время"""
        self.second_begin = 0
        self.time_over = 0
        self.time_end = 0
        self.res_sec = 0
        self.second_begin = 0
        self.minute_begin = 0
        self.minute = 0
        self.second = 0
        self.start_time = t
        self.time_end = self.start_time
        self.tracking = 99999
        self.begin_level = False

    def show_time(self, screen, player):
        """Показывает время"""
        if player.alive and self.tracking > 0:
            self.subtraction_time()
        self.tracking = self.start_time - self.time_over
        surface_tracking = self.time.render(str(self.tracking), False, (255, 0, 0))
        screen.blit(surface_tracking, (970, 3))
