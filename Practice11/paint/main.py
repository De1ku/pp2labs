import pygame
import math


# -------------------- НАСТРОЙКИ ОКНА --------------------

WIDTH = 640
HEIGHT = 480
TOOLBAR_HEIGHT = 90

# -------------------- ЦВЕТА --------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)

# Список доступных цветов
COLORS = [
    ("black", (0, 0, 0)),
    ("red", (255, 0, 0)),
    ("green", (0, 180, 0)),
    ("blue", (0, 0, 255)),
    ("yellow", (255, 220, 0)),
    ("purple", (160, 0, 200))
]


# -------------------- ФУНКЦИИ ДЛЯ РИСОВАНИЯ --------------------

def draw_line(surface, start, end, color, radius):
    """Рисует плавную линию между двумя точками"""

    dx = start[0] - end[0]
    dy = start[1] - end[1]

    steps = max(abs(dx), abs(dy))

    # Если мышь почти не двигалась, рисуем просто точку
    if steps == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    # Рисуем много маленьких кругов между двумя точками
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


def make_square(start, end):
    """Создает квадрат по начальной и конечной точке"""

    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    # Сторона квадрата равна большей стороне движения мыши
    side = max(abs(dx), abs(dy))

    # Определяем направление рисования
    if dx < 0:
        side_x = -side
    else:
        side_x = side

    if dy < 0:
        side_y = -side
    else:
        side_y = side

    return pygame.Rect(x1, y1, side_x, side_y)


def make_right_triangle(start, end):
    """Создает точки для прямоугольного треугольника"""

    x1, y1 = start
    x2, y2 = end

    # Один угол треугольника будет прямым
    return [
        (x1, y1),
        (x2, y1),
        (x1, y2)
    ]


def make_equilateral_triangle(start, end):
    """Создает точки для равностороннего треугольника"""

    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    # Длина стороны зависит от движения мыши
    side = max(abs(dx), abs(dy))

    # Высота равностороннего треугольника
    height = int(side * math.sqrt(3) / 2)

    # Если мышь идет вверх, треугольник рисуется вверх
    if dy < 0:
        direction = -1
    else:
        direction = 1

    top = (x1, y1)
    left = (x1 - side // 2, y1 + direction * height)
    right = (x1 + side // 2, y1 + direction * height)

    return [top, left, right]


def make_rhombus(start, end):
    """Создает точки для ромба"""

    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    return [
        (center_x, top),
        (right, center_y),
        (center_x, bottom),
        (left, center_y)
    ]


# -------------------- ПАНЕЛЬ ИНСТРУМЕНТОВ --------------------

def draw_toolbar(screen, font, current_tool, current_color, radius):
    """Рисует верхнюю панель инструментов"""

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    text1 = font.render(
        f"Tool: {current_tool} | Size: {radius}",
        True,
        BLACK
    )

    text2 = font.render(
        "P brush | R rect | C circle | E eraser | S square | T right triangle | Q equilateral | H rhombus",
        True,
        BLACK
    )

    text3 = font.render(
        "1-6 colors | Mouse wheel or +/- size | Backspace clear | Esc exit",
        True,
        BLACK
    )

    screen.blit(text1, (10, 5))
    screen.blit(text2, (10, 27))
    screen.blit(text3, (10, 49))

    # Рисуем кнопки цветов
    x = 10
    y = 68

    for name, color in COLORS:
        rect = pygame.Rect(x, y, 28, 18)
        pygame.draw.rect(screen, color, rect)

        # Выбранный цвет выделяется толстой рамкой
        if color == current_color:
            pygame.draw.rect(screen, BLACK, rect, 3)
        else:
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

        x += 38


def get_color_from_toolbar(pos):
    """Проверяет, нажал ли пользователь на цвет в панели"""

    x, y = pos

    color_x = 10
    color_y = 68

    for name, color in COLORS:
        rect = pygame.Rect(color_x, color_y, 28, 18)

        if rect.collidepoint(x, y):
            return color

        color_x += 38

    return None


# -------------------- ОСНОВНАЯ ПРОГРАММА --------------------

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    # Canvas — это отдельная поверхность, на которой остается рисунок
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    radius = 6
    current_color = (0, 0, 255)
    current_tool = "brush"

    drawing = False
    start_pos = None
    last_pos = None

    while True:

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        # -------------------- ОБРАБОТКА СОБЫТИЙ --------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # -------------------- КЛАВИАТУРА --------------------

            if event.type == pygame.KEYDOWN:

                # Выход из программы
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if event.key == pygame.K_w and ctrl_held:
                    pygame.quit()
                    return

                if event.key == pygame.K_F4 and alt_held:
                    pygame.quit()
                    return

                # Выбор инструмента
                if event.key == pygame.K_p:
                    current_tool = "brush"

                elif event.key == pygame.K_r:
                    current_tool = "rectangle"

                elif event.key == pygame.K_c:
                    current_tool = "circle"

                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                elif event.key == pygame.K_s:
                    current_tool = "square"

                elif event.key == pygame.K_t:
                    current_tool = "right triangle"

                elif event.key == pygame.K_q:
                    current_tool = "equilateral triangle"

                elif event.key == pygame.K_h:
                    current_tool = "rhombus"

                # Выбор цвета цифрами
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

                # Увеличение размера кисти
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    radius = min(50, radius + 1)

                # Уменьшение размера кисти
                elif event.key == pygame.K_MINUS:
                    radius = max(1, radius - 1)

                # Очистка экрана
                elif event.key == pygame.K_BACKSPACE:
                    canvas.fill(WHITE)

            # -------------------- НАЖАТИЕ МЫШИ --------------------

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Колесико вверх — увеличить размер
                if event.button == 4:
                    radius = min(50, radius + 1)

                # Колесико вниз — уменьшить размер
                elif event.button == 5:
                    radius = max(1, radius - 1)

                # Левая кнопка мыши
                elif event.button == 1:

                    # Если нажали на верхнюю панель
                    if mouse_pos[1] < TOOLBAR_HEIGHT:
                        selected_color = get_color_from_toolbar(mouse_pos)

                        if selected_color is not None:
                            current_color = selected_color

                    # Если нажали на область рисования
                    else:
                        drawing = True

                        # Переводим координаты мыши в координаты canvas
                        start_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)
                        last_pos = start_pos

                        # Чтобы кисть и ластик сразу оставляли след
                        if current_tool == "brush":
                            pygame.draw.circle(canvas, current_color, start_pos, radius)

                        elif current_tool == "eraser":
                            pygame.draw.circle(canvas, WHITE, start_pos, radius)

            # -------------------- ДВИЖЕНИЕ МЫШИ --------------------

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_pos = event.pos

                    # Рисуем только внутри canvas
                    if mouse_pos[1] >= TOOLBAR_HEIGHT:
                        current_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                        if current_tool == "brush":
                            draw_line(canvas, last_pos, current_pos, current_color, radius)
                            last_pos = current_pos

                        elif current_tool == "eraser":
                            draw_line(canvas, last_pos, current_pos, WHITE, radius)
                            last_pos = current_pos

            # -------------------- ОТПУСКАНИЕ МЫШИ --------------------

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    mouse_pos = event.pos

                    # Ограничиваем точку, чтобы она не уходила в панель
                    if mouse_pos[1] < TOOLBAR_HEIGHT:
                        mouse_pos = (mouse_pos[0], TOOLBAR_HEIGHT)

                    end_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

                    # Рисуем прямоугольник
                    if current_tool == "rectangle":
                        rect = make_rect(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, radius)

                    # Рисуем круг
                    elif current_tool == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        circle_radius = int(math.sqrt(dx ** 2 + dy ** 2))
                        pygame.draw.circle(canvas, current_color, start_pos, circle_radius, radius)

                    # Рисуем квадрат
                    elif current_tool == "square":
                        square = make_square(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, square, radius)

                    # Рисуем прямоугольный треугольник
                    elif current_tool == "right triangle":
                        points = make_right_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, radius)

                    # Рисуем равносторонний треугольник
                    elif current_tool == "equilateral triangle":
                        points = make_equilateral_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, radius)

                    # Рисуем ромб
                    elif current_tool == "rhombus":
                        points = make_rhombus(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, radius)

                    drawing = False
                    start_pos = None
                    last_pos = None

        # -------------------- ОТРИСОВКА ЭКРАНА --------------------

        screen.fill(WHITE)

        # Рисуем панель и canvas
        draw_toolbar(screen, font, current_tool, current_color, radius)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # -------------------- ПРЕДПРОСМОТР ФИГУР --------------------
        # Фигура показывается во время зажатия мыши,
        # но сохраняется на canvas только после отпускания кнопки

        shape_tools = [
            "rectangle",
            "circle",
            "square",
            "right triangle",
            "equilateral triangle",
            "rhombus"
        ]

        if drawing and current_tool in shape_tools:
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

                elif current_tool == "square":
                    square = make_square(start_pos, preview_end)
                    square.y += TOOLBAR_HEIGHT
                    pygame.draw.rect(screen, current_color, square, radius)

                elif current_tool == "right triangle":
                    points = make_right_triangle(start_pos, preview_end)
                    points = [(x, y + TOOLBAR_HEIGHT) for x, y in points]
                    pygame.draw.polygon(screen, current_color, points, radius)

                elif current_tool == "equilateral triangle":
                    points = make_equilateral_triangle(start_pos, preview_end)
                    points = [(x, y + TOOLBAR_HEIGHT) for x, y in points]
                    pygame.draw.polygon(screen, current_color, points, radius)

                elif current_tool == "rhombus":
                    points = make_rhombus(start_pos, preview_end)
                    points = [(x, y + TOOLBAR_HEIGHT) for x, y in points]
                    pygame.draw.polygon(screen, current_color, points, radius)

        pygame.display.flip()
        clock.tick(60)


main()