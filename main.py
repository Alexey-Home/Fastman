import pygame


def main():

    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    color_bkg = (230, 234, 240)
    screen.fill(color_bkg)
    pygame.display.flip()
    running = True

    while running:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


if __name__ == "__main__":
    main()