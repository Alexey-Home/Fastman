import pygame
from enemies import Bomb


class Level:

    def __init__(self, level):
        self.rectangle = []
        self.collisions_rectangle = []
        self.bombs = []
        self.collisions_bomb = []
        self.position_exit = level["door"]
        self.position_button = level["button"]
        self.start_player = level["start_player"]
        self.show_menu = True

        if level["objects_rect"]:
            for key, value in level["objects_rect"].items():
                self.rectangle.append((pygame.Surface((value["width"], value["height"])), value["position"]))
                self.rectangle[-1][0].fill(value["color"])
                self.collisions_rectangle.append(self.rectangle[-1][0].get_rect(topleft=(value["position"])))

        if level["bombs"]:
            for bomb_pos in level["bombs"]:
                self.bombs.append(Bomb(bomb_pos))
                self.collisions_bomb.append(self.bombs[-1].collisions)

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

    def check_alive(self, player):
        """Проверяет жив ли игрок"""
        if not player.alive:
            self.show_menu = True

class Menu:
    def __init__(self):
        self.label = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 30)
        self.new_game_label = self.label.render("Новая игра", False, (193, 196, 199))
        self.new_game_label_rect = self.new_game_label.get_rect(topleft=(700, 50))
        self.play_again_label = self.label.render("Играть заново(R)", False, (193, 196, 199))
        self.play_again_label_rect = self.play_again_label.get_rect(topleft=(700, 50))
        self.first_time = True
        self.press_r = False


    def show_menu(self, screen):
        """Показывает меню"""
        if self.first_time == True:
            screen.blit(self.new_game_label, self.new_game_label_rect)
        else:
            screen.blit(self.play_again_label, self.play_again_label_rect)

    def control_menu(self):
        """Контролирует нажатие на параметры из меню"""
        mouse = pygame.mouse.get_pos()
        if self.new_game_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            return True
        elif (self.play_again_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]) or self.press_r:
            self.press_r = False
            return True







