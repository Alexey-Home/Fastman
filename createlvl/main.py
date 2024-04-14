import pygame

from inputBox import InputBox


def main():
    pygame.init()
    color_bkg = (230, 234, 240)
    screen = pygame.display.set_mode((1324, 768))
    gameplay = True
    label = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 16)
    parameter = {
        "active": "reset"
    }
    platforms = []
    bombs = []
    guns = []

    colors = {
        "color_platform": "black",
        "color_bomb": "black",
        "color_gun": "black",
        }

    rect1 = pygame.Surface((45, 768))
    rect1.fill("grey")
    rect2 = pygame.Surface((45, 768))
    rect2.fill("grey")
    rect3 = pygame.Surface((1024, 40))
    rect3.fill("grey")
    click = False
    input_box_rect_x = InputBox(1150, 15, 100, 30, label)
    input_box_rect_y = InputBox(1210, 15, 100, 30, label)
    input_boxes = [input_box_rect_x, input_box_rect_y]

    while gameplay:
        platform_label = label.render("Платформа", False, colors["color_platform"])
        platform_label_rect = platform_label.get_rect(topleft=(1050, 20))

        bomb_label = label.render("Бомба", False, colors["color_bomb"])
        bomb_label_rect = bomb_label.get_rect(topleft=(1050, 60))

        gun_label = label.render("Пушка", False, colors["color_gun"])
        gun_label_rect = gun_label.get_rect(topleft=(1050, 100))

        reset_label = label.render("Отменить выбор", False, "black")
        reset_label_rect = reset_label.get_rect(topleft=(1050, 700))

        menu = [(platform_label, platform_label_rect),
                (reset_label, reset_label_rect),
                (bomb_label, bomb_label_rect),
                (gun_label, gun_label_rect)]

        screen.fill(color_bkg)
        screen.blit(rect1, (0, 0))
        screen.blit(rect2, (1000, 0))
        screen.blit(rect3, (0, 0))

        mouse = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if platform_label_rect.collidepoint(mouse):
                parameter["active"] = "platforms"
                colors = reset_color(colors)
                colors["color_platform"] = "green"
            elif bomb_label_rect.collidepoint(mouse):
                parameter["active"] = "bomb"
                colors = reset_color(colors)
                colors["color_bomb"] = "green"
            elif gun_label_rect.collidepoint(mouse):
                parameter["active"] = "gun"
                colors = reset_color(colors)
                colors["color_gun"] = "green"
            elif reset_label_rect.collidepoint(mouse):
                colors = reset_color(colors)
                parameter["active"] = "reset"
            elif 40 <= mouse[0] <= 1005 and 35 <= mouse[1] <= 750 and click:
                if parameter["active"] in ["gun", "bomb"]:
                    for i in range(len(platforms)):
                        if platforms[i][1].collidepoint(mouse):
                            mouse = (mouse[0], platforms[i][1].top)
                            break

                if parameter["active"] == "platforms":
                    platforms = create_platform(platforms, mouse, input_boxes)
                elif parameter["active"] == "bomb":
                    bombs = create_object(bombs, mouse, "C:/python3.7/pythonProject/GameDev/fastman/images/bomb.png")
                elif parameter["active"] == "gun":
                    guns = create_object(guns, mouse, "C:/python3.7/pythonProject/GameDev/fastman/images/gun.png")
                click = False

        for m in menu:
            screen.blit(m[0], m[1])

        all_obj = [
            platforms, bombs, guns
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameplay = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_DELETE:
                for obj in all_obj:
                    for i in range(len(obj)):
                        if obj[i][1].collidepoint(mouse):
                            obj.pop(i)
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                click = True

            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)

        for plat in platforms:
            screen.blit(plat[0], plat[1])

        for bomb in bombs:
            screen.blit(bomb[0], bomb[1])

        for gun in guns:
            screen.blit(gun[0], gun[1])

        pygame.display.update()



def reset_color(colors):
    temp = {}
    for obj, color in colors.items():
        temp[obj] = "black"
    return temp



def create_object(obj, mouse, path):
    tmp = pygame.image.load(path).convert_alpha()
    mouse = (mouse[0], mouse[1] - tmp.get_height())
    tmp_rect = tmp.get_rect(topleft=mouse)
    obj.append((tmp, tmp_rect, mouse))
    return obj


def create_platform(platform, mouse, input_boxes):
    size = get_size(input_boxes)

    tmp = pygame.Surface(size)
    tmp.fill("grey")
    tmp_rect = tmp.get_rect(topleft=mouse)
    platform.append((tmp, tmp_rect, mouse))
    return platform


def get_size(input_boxes):
    width = input_boxes[0].text
    height = input_boxes[1].text

    try:
        width = float(width)
    except ValueError:
        width = 30

    if width < 30:
        width = 30

    try:
        height = float(height)
    except ValueError:
        height = 30

    if height < 30:
        height = 30

    return width, height




if __name__ == "__main__":
    main()