import pygame
from player import Player, PartBody
from exit import Exit, Button
from editor import Level, Menu
from data.levels import level_1, menu


def main():

    width = 1024
    height = 768
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    color_bkg = (230, 234, 240)
    level, l_menu, player = create_menu()


    while True:
        screen.fill(color_bkg)
        if not player.gameplay:
            if level.show_menu:
                l_menu.show_menu(screen)
                player.gameplay = l_menu.control_menu()
            screen.blit(player.image, (player.x, player.y))
            level.show_rect(screen)
            player.gameplay_player(l_menu, screen, level)
            pygame.display.flip()
        else:
            l_menu.first_time = False
            level = Level(level_1)
            level.show_menu = False
            exit_door = Exit(level.position_exit)
            button = Button(level.position_button)
            player = Player("images/man1.jpg", level.start_player[0], level.start_player[1], True)
            while True:
                screen.fill(color_bkg)
                if level.show_menu:
                    l_menu.show_menu(screen)
                    player.gameplay = l_menu.control_menu()
                    if player.gameplay:
                        break
                level.show_rect(screen)
                level.show_bombs(screen)
                screen.blit(exit_door.image, exit_door.position)
                screen.blit(button.image, button.position)
                player.gameplay_player(l_menu, screen, level, button,  exit_door)
                player.check_death(screen)
                level.check_alive(player)
                player.check_level_done()
                pygame.display.flip()
                pygame.display.update()
                clock.tick(60)

        pygame.display.update()
        clock.tick(60)



def create_menu():
    level = Level(menu)
    l_menu = Menu()
    player = Player("images/man1.jpg", level.start_player[0], level.start_player[1], False)
    return level, l_menu, player


if __name__ == "__main__":
    main()
