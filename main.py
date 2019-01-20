import pygame
from map import Map

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Life")


def main():
    game_over = False
    size = 10

    screen.fill((255, 255, 255))

    # input textbox
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(300, 100, 140, 32)
    color = pygame.Color('darkgreen')
    text = ''
    active = False
    ready = False
    clock = pygame.time.Clock()
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ready = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    size = text
                    ready = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill((255, 255, 255))
        txt_surface2 = font.render("Enter map size (max 23):", True, color)
        screen.blit(txt_surface2, (35, 105))
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(60)

    # validity check
    print("Enter map size")
    try:
        size = int(size)
    except ValueError:
        print('Enter integer')
        return -1
    if not (23 >= size >= 1):
        print('Enter 23 >= size >= 1')
        return -1

    my_map = Map(size)
    my_map.generate()

    # main cycle
    while not game_over:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()

        game_over = my_map.draw()

        # pygame draw
        screen.fill((255, 255, 255))
        my_map.draw_pics(screen)
        pygame.display.flip()
        my_map.turn()

        pygame.time.wait(1000)  # pause between steps

    pygame.time.wait(1000)  # endgame pause


if __name__ == '__main__':
    main()
