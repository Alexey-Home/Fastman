import pygame
from player import Player

def main():

    pygame.init()

    screen = pygame.display.set_mode((1024, 768))
    color_bkg = (230, 234, 240)
    player = Player()

    pygame.display.flip()
    running = True

    while running:
        screen.fill(color_bkg)
        screen.blit(player.image, (player.x, player.y))

        keys = pygame.key.get_pressed()

        player.run(keys)
        player.jump(keys)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        pygame.display.update()



if __name__ == "__main__":
    main()