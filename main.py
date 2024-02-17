import pygame
from player import Player


def main():

    width = 1024
    height = 768

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    color_bkg = (230, 234, 240)
    player = Player()

    pygame.display.flip()
    gameplay = True

    rect1 = pygame.Surface((200, 30))
    rect1.fill("Grey")
    rect1_col = rect1.get_rect(topleft=(0, 720))

    rect2 = pygame.Surface((200, 30))
    rect2.fill("Grey")
    rect2_col = rect2.get_rect(topleft=(250, 720))

    rect3 = pygame.Surface((200, 100))
    rect3.fill("Grey")
    rect3_col = rect3.get_rect(topleft=(250, 550))


    object_collisions = [rect1_col, rect2_col, rect3_col]


    while gameplay:
        screen.fill(color_bkg)
        screen.blit(rect1, (0, 720))
        screen.blit(rect2, (250, 720))
        screen.blit(rect3, (250, 550))
        screen.blit(player.image, (player.x, player.y))

        keys = pygame.key.get_pressed()
        #player_col = player.image.get_rect(topleft=(player.x, player.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameplay = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.is_col:
                player.is_jump = True
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                player.is_run = True
            elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                player.is_run = False

        player.physics(object_collisions)
        player.run(keys)
        player.jump()

        if player.y > height:
            gameplay = False

        pygame.display.update()
        clock.tick(60)




if __name__ == "__main__":
    main()