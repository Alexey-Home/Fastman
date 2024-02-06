import pygame


def main():

    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    color_bkg = (230, 234, 240)
    player = pygame.image.load("images/man1.jpg")
    player_x = 30
    player_y = 700
    player_speed = 1
    is_jump = False
    jump_count = 7
    pygame.display.flip()
    running = True

    while running:
        screen.fill(color_bkg)
        screen.blit(player, (player_x, player_y))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and player_x < 1000:
            player_x += player_speed
        elif keys[pygame.K_LEFT] and player_x > 24:
            player_x -= player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -7:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 7
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        pygame.display.update()

if __name__ == "__main__":
    main()