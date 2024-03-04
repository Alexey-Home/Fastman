import pygame


class Exit:
    def __init__(self, pos_exit):
        self.image = pygame.image.load("images/closed_door.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if pos_exit:
            self.position = (pos_exit[0] - self.width, pos_exit[1] - self.height)
            self.collision = self.image.get_rect(topleft=(self.position[0] + self.width/2, self.position[1]),
                                                 size=(self.width/4, self.height))
        else:
            self.position = ()
            self.collision = None
        self.open = False


class Button:
    def __init__(self, pos_button):
        self.image = pygame.image.load("images/button_red.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if pos_button:
            self.position = (pos_button[0] - self.width, pos_button[1] - self.height - self.height/2)
            self.collision = self.image.get_rect(topleft=self.position)
        else:
            self.position = ()
            self.collision = None
