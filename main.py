import pygame
from player import Player

def main():

    pygame.init()

    screen = pygame.display.set_mode((1024, 768))
    color_bkg = (230, 234, 240)
    # player = pygame.image.load("images/man1.jpg")
    player = Player()

    pygame.display.flip()
    running = True

    while running:
        screen.fill(color_bkg)
        screen.blit(player.image, (player.x, player.y))
        print(player.x)

        keys = pygame.key.get_pressed()


        if keys[pygame.K_RIGHT] and player.x < 1000:
            player.speed_increase()
            player.x += player.speed
        elif keys[pygame.K_LEFT] and player.x > 24:
            player.speed_increase()
            player.x -= player.speed
        else:
            player.speed_reset()

        if not player.is_jump:
            if keys[pygame.K_SPACE]:
                player.is_jump = True
        else:
            if player.jump_count >= -player.jump_high:
                if player.jump_count > 0:
                    player.y -= (player.jump_count ** 2) / 2
                else:
                    player.y += (player.jump_count ** 2) / 2
                player.jump_count -= 1
            else:
                player.is_jump = False
                player.jump_count = player.jump_high
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        pygame.display.update()



if __name__ == "__main__":
    main()