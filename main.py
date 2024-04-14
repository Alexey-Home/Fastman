import pygame
from player import Player
from exit import Exit, Button
from editor import Level, Menu, ClockOver
from databasefunction import get_level_from_db


def main():
    pygame.init()
    width = 1024
    height = 768
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    color_bkg = (230, 234, 240)
    level, l_menu, player = create_menu()
    timer = ClockOver()

    while True:
        screen.fill(color_bkg)
        if not player.gameplay:
            if level.show_menu:
                l_menu.show_menu(screen)
                player.gameplay = l_menu.control_menu(level, player.level_done)
            screen.blit(player.image, (player.x, player.y))
            level.show_rect(screen)
            player.gameplay_player(l_menu, screen, level, timer)
            pygame.display.flip()
        else:
            l_menu.first_time = False
            lvl = get_level_from_db()
            level = Level(lvl)
            level.show_menu = False
            exit_door = Exit(level.position_exit)
            button = Button(level.position_button)
            player = Player("images/man1.jpg", level.start_player[0], level.start_player[1], True)
            timer.reset_time(level.start_time)
            while True:
                if screen.get_width() != width:
                    screen = pygame.display.set_mode((width, height))
                screen.fill(color_bkg)
                level.show_rect(screen)
                timer.show_time(screen, player)
                level.show_bombs(screen)
                level.show_add_sec(screen)
                level.show_hedgehods(screen)
                level.show_gun(screen)
                level.show_bullets(screen)
                if level.show_menu:
                    l_menu.show_menu(screen)
                    player.gameplay = l_menu.control_menu(level, player.level_done)
                    if player.gameplay:
                        break
                if exit_door.image and exit_door.position:
                    screen.blit(exit_door.image, exit_door.position)
                if button.image and button.position:
                    screen.blit(button.image, button.position)
                player.gameplay_player(l_menu, screen, level, timer, button,  exit_door)
                level.detection_collision(player)
                player.check_death(screen)
                player.check_timeover(timer.tracking)
                level.check_alive(player)
                player.check_level_done()
                pygame.display.flip()
                pygame.display.update()
                clock.tick(60)

        pygame.display.update()
        clock.tick(60)


def create_menu():
    lvl = get_level_from_db(1)
    level = Level(lvl)
    l_menu = Menu()
    player = Player("images/man1.jpg", level.start_player[0], level.start_player[1], False)
    return level, l_menu, player


if __name__ == "__main__":
    main()
