import pygame
import math


# размеры окна
WIDTH = 640
HEIGHT = 480
TOOLBAR_HEIGHT = 70

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (90, 90, 90)

COLORS = [
    ("black", (0, 0, 0)),
    ("red", (255, 0, 0)),
    ("green", (0, 180, 0)),
    ("blue", (0, 0, 255)),
    ("yellow", (255, 220, 0)),
    ("purple", (160, 0, 200))
]


def draw_line(surface, start, end, color, radius):
    """Рисует плавную линию между двумя точками"""
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(steps + 1):
        t = i / steps
        x = int(start[0] * (1 - t) + end[0] * t)
        y = int(start[1] * (1 - t) + end[1] * t)
        pygame.draw.circle(surface, color, (x, y), radius)


def make_rect(start, end):
    """Создает прямоугольник по двум точкам"""
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)

    return pygame.Rect(left, top, width, height)


def draw_toolbar(screen, font, current_tool, current_color, radius):
    """Панель инструментов сверху"""
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    text = font.render(
        f"Tool: {current_tool} | Size: {radius} | Keys: P-brush, R-rect, C-circle, E-eraser",
        True,
        BLACK
    )
    screen.blit(text, (10, 8))

    # кнопки цветов
    x = 10
    y = 35

    for name, color in COLORS:
        rect = pygame.Rect(x, y, 30, 25)
        pygame.draw.rect(screen, color, rect)

        if color == current_color:
            pygame.draw.rect(screen, BLACK, rect, 3)
        else:
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

        x += 40

    hint = font.render("+ / - or mouse wheel = change size", True, BLACK)
    screen.blit(hint, (270, 38))


def get_color_from_toolbar(pos):
    """Проверяет, выбрал ли пользователь цвет на панели"""
    x, y = pos

    color_x = 10
    color_y = 35

    for name, color in COLORS:
        rect = pygame.Rect(color_x, color_y, 30, 25)

        if rect.collidepoint(x, y):
            return color

        color_x += 40

    return None


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    # отдельная поверхность для рисования
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    radius = 8
    current_color = (0, 0, 255)
    current_tool = "brush"

    drawing = False
    start_pos = None
    last_pos = None

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if event.key == pygame.K_w and ctrl_held:
                    pygame.quit()
                    return

                if event.key == pygame.K_F4 and alt_held:
                    pygame.quit()
                    return

                # выбор инструмента
                if event.key == pygame.K_p:
                    current_tool = "brush"

                elif event.key == pygame.K_r:
                    current_tool = "rectangle"

                elif event.key == pygame.K_c:
                    current_tool = "circle"

                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                # выбор цвета через клавиши
                elif event.key == pygame.K_1:
                    current_color = COLORS[0][1]
                elif event.key == pygame.K_2:
                    current_color = COLORS[1][1]
                elif event.key == pygame.K_3:
                    current_color = COLORS[2][1]
                elif event.key == pygame.K_4:
                    current_color = COLORS[3][1]
                elif event.key == pygame.K_5:
                    current_color = COLORS[4][1]
                elif event.key == pygame.K_6:
                    current_color = COLORS[5][1]

                # изменение размера кисти
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    radius = min(50, radius + 1)

                elif event.key == pygame.K_MINUS:
                    radius = max(1, radius - 1)

                # очистка экрана
                elif event.key == pygame.K_BACKSPACE:
                    canvas.fill(WHITE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # колесико мыши меняет размер
                if event.button == 4:
                    radius = min(50, radius + 1)

                elif event.button == 5:
                    radius = max(1, radius - 1)

                # левая кнопка мыши
                elif event.button == 1:

                    # если нажали на панель инструментов
                    if mouse_pos[1] < TOOLBAR_HEIGHT:
                        selected_color = get_color_from_toolbar(mouse_pos)

                        if selected_color is not None:
                            current_color = selected_color

                    # если нажали на область рисования
                    else:
                        drawing = True

                        # переводим координаты мыши в координаты canvas
                        start_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)
                        last_pos = start_pos

                        if current_tool == "brush":
                            pygame.draw.circle(canvas, current_color, start_pos, radius)

                        elif current_tool == "eraser":
                            pygame.draw.circle(canvas, WHITE, start_pos, radius)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_pos = event.pos

                    if mouse_pos[1] >= TOOLBAR_HEIGHT:
                        current_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                        if current_tool == "brush":
                            draw_line(canvas, last_pos, current_pos, current_color, radius)
                            last_pos = current_pos

                        elif current_tool == "eraser":
                            draw_line(canvas, last_pos, current_pos, WHITE, radius)
                            last_pos = current_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    mouse_pos = event.pos
                    end_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                    # рисование прямоугольника
                    if current_tool == "rectangle":
                        rect = make_rect(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, radius)

                    # рисование круга
                    elif current_tool == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        circle_radius = int(math.sqrt(dx ** 2 + dy ** 2))
                        pygame.draw.circle(canvas, current_color, start_pos, circle_radius, radius)

                    drawing = False
                    start_pos = None
                    last_pos = None

        # отрисовка всего окна
        screen.fill(WHITE)

        draw_toolbar(screen, font, current_tool, current_color, radius)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # предпросмотр прямоугольника и круга во время зажатия мыши
        if drawing and current_tool in ["rectangle", "circle"]:
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] >= TOOLBAR_HEIGHT:
                preview_end = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                if current_tool == "rectangle":
                    rect = make_rect(start_pos, preview_end)
                    rect.y += TOOLBAR_HEIGHT
                    pygame.draw.rect(screen, current_color, rect, radius)

                elif current_tool == "circle":
                    dx = preview_end[0] - start_pos[0]
                    dy = preview_end[1] - start_pos[1]
                    circle_radius = int(math.sqrt(dx ** 2 + dy ** 2))

                    center = (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT)
                    pygame.draw.circle(screen, current_color, center, circle_radius, radius)

        pygame.display.flip()
        clock.tick(60)


main()