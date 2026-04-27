import pygame
import math
import os
from datetime import datetime
from collections import deque


# -------------------- НАСТРОЙКИ ОКНА --------------------

WIDTH = 640
HEIGHT = 500
TOOLBAR_HEIGHT = 120
FPS = 60


# -------------------- ЦВЕТА --------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (80, 80, 80)
BLUE_SELECT = (70, 130, 255)

COLORS = [
    ("black", (0, 0, 0)),
    ("red", (255, 0, 0)),
    ("green", (0, 180, 0)),
    ("blue", (0, 0, 255)),
    ("yellow", (255, 220, 0)),
    ("purple", (160, 0, 200))
]

# Три обязательных размера кисти по заданию
BRUSH_SIZES = [
    ("1", "2 px", 2),
    ("2", "5 px", 5),
    ("3", "10 px", 10)
]

TOOLS = [
    ("Pencil", "pencil", pygame.K_p),
    ("Line", "line", pygame.K_l),
    ("Rect", "rectangle", pygame.K_r),
    ("Circle", "circle", pygame.K_c),
    ("Eraser", "eraser", pygame.K_e),
    ("Fill", "fill", pygame.K_f),
    ("Text", "text", pygame.K_t),
    ("Square", "square", pygame.K_s),
    ("R-Tri", "right triangle", pygame.K_g),
    ("Eq-Tri", "equilateral triangle", pygame.K_q),
    ("Rhomb", "rhombus", pygame.K_h)
]


# -------------------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ --------------------

def canvas_pos(mouse_pos):
    """Переводит координаты окна в координаты canvas."""
    return mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT


def inside_canvas(mouse_pos):
    """Проверяет, находится ли курсор в области рисования."""
    return 0 <= mouse_pos[0] < WIDTH and TOOLBAR_HEIGHT <= mouse_pos[1] < HEIGHT


def draw_pencil_line(surface, start, end, color, width):
    """Рисует плавную линию карандаша между двумя соседними позициями мыши."""
    pygame.draw.line(surface, color, start, end, width)

    # Маленькие круги на концах убирают разрывы при толстом размере кисти
    radius = max(1, width // 2)
    pygame.draw.circle(surface, color, start, radius)
    pygame.draw.circle(surface, color, end, radius)


def make_rect(start, end):
    """Создает прямоугольник по двум точкам."""
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)

    return pygame.Rect(left, top, width, height)


def make_square(start, end):
    """Создает квадрат по начальной и конечной точке."""
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    side = max(abs(dx), abs(dy))

    side_x = -side if dx < 0 else side
    side_y = -side if dy < 0 else side

    return pygame.Rect(x1, y1, side_x, side_y)


def make_right_triangle(start, end):
    """Создает точки для прямоугольного треугольника."""
    x1, y1 = start
    x2, y2 = end

    return [
        (x1, y1),
        (x2, y1),
        (x1, y2)
    ]


def make_equilateral_triangle(start, end):
    """Создает точки для равностороннего треугольника."""
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    side = max(abs(dx), abs(dy))
    height = int(side * math.sqrt(3) / 2)
    direction = -1 if dy < 0 else 1

    top = (x1, y1)
    left = (x1 - side // 2, y1 + direction * height)
    right = (x1 + side // 2, y1 + direction * height)

    return [top, left, right]


def make_rhombus(start, end):
    """Создает точки для ромба."""
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


def flood_fill(surface, start_pos, new_color):
    """Заливает область одного цвета выбранным цветом через get_at() и set_at()."""
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(new_color)

    # Если область уже такого цвета, ничего не делаем
    if target_color == fill_color:
        return

    pixels = deque([(x, y)])

    while pixels:
        px, py = pixels.pop()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        pixels.append((px + 1, py))
        pixels.append((px - 1, py))
        pixels.append((px, py + 1))
        pixels.append((px, py - 1))


def save_canvas(canvas):
    """Сохраняет canvas в .png файл с timestamp, чтобы файлы не перезаписывались."""
    os.makedirs("saves", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("saves", f"paint_{timestamp}.png")
    pygame.image.save(canvas, filename)
    return filename


# -------------------- ПАНЕЛЬ ИНСТРУМЕНТОВ --------------------

def get_tool_rects():
    """Возвращает прямоугольники кнопок инструментов."""
    rects = []
    x = 10
    y = 31

    for label, tool, key in TOOLS:
        button_width = max(42, len(label) * 7 + 12)
        rects.append((pygame.Rect(x, y, button_width, 22), label, tool))
        x += button_width + 5

    return rects


def get_color_rects():
    """Возвращает прямоугольники кнопок цветов."""
    rects = []
    x = 10
    y = 66

    for name, color in COLORS:
        rects.append((pygame.Rect(x, y, 28, 20), name, color))
        x += 36

    return rects


def get_size_rects():
    """Возвращает прямоугольники кнопок размеров кисти."""
    rects = []
    x = 250
    y = 66

    for hotkey, label, size in BRUSH_SIZES:
        rects.append((pygame.Rect(x, y, 58, 20), hotkey, label, size))
        x += 66

    return rects


def draw_toolbar(screen, font, small_font, current_tool, current_color, brush_size, status_text):
    """Рисует верхнюю панель инструментов."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_HEIGHT - 1), (WIDTH, TOOLBAR_HEIGHT - 1), 2)

    title = font.render(
        f"Tool: {current_tool} | Brush size: {brush_size}px | Ctrl+S save",
        True,
        BLACK
    )
    screen.blit(title, (10, 7))

    # Кнопки инструментов
    for rect, label, tool in get_tool_rects():
        button_color = WHITE if tool != current_tool else (190, 215, 255)
        border_color = DARK_GRAY if tool != current_tool else BLUE_SELECT

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, border_color, rect, 2)

        text = small_font.render(label, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Кнопки цветов
    for rect, name, color in get_color_rects():
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK if color == current_color else DARK_GRAY, rect, 3 if color == current_color else 1)

    # Кнопки размеров кисти
    size_label = small_font.render("Size:", True, BLACK)
    screen.blit(size_label, (214, 68))

    for rect, hotkey, label, size in get_size_rects():
        button_color = WHITE if size != brush_size else (190, 215, 255)
        border_color = DARK_GRAY if size != brush_size else BLUE_SELECT

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, border_color, rect, 2)

        text = small_font.render(f"{hotkey}: {label}", True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    help_text = small_font.render(
        "Keys: P pencil | L line | R rect | C circle | E eraser | F fill | T text | S square | G right tri | Q eq tri | H rhomb",
        True,
        BLACK
    )
    screen.blit(help_text, (10, 93))

    if status_text:
        status = small_font.render(status_text, True, BLACK)
        screen.blit(status, (440, 68))


def get_tool_from_toolbar(pos):
    """Проверяет, нажал ли пользователь на кнопку инструмента."""
    for rect, label, tool in get_tool_rects():
        if rect.collidepoint(pos):
            return tool
    return None


def get_color_from_toolbar(pos):
    """Проверяет, нажал ли пользователь на цвет."""
    for rect, name, color in get_color_rects():
        if rect.collidepoint(pos):
            return color
    return None


def get_size_from_toolbar(pos):
    """Проверяет, нажал ли пользователь на размер кисти."""
    for rect, hotkey, label, size in get_size_rects():
        if rect.collidepoint(pos):
            return size
    return None


# -------------------- ОСНОВНАЯ ПРОГРАММА --------------------

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Extended")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    small_font = pygame.font.SysFont("Arial", 13)
    text_font = pygame.font.SysFont("Arial", 26)

    # Canvas — отдельная поверхность, на которой остается готовый рисунок
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    brush_size = 5
    current_color = (0, 0, 255)
    current_tool = "pencil"

    drawing = False
    start_pos = None
    last_pos = None

    # Переменные для инструмента Text
    text_active = False
    text_pos = None
    text_buffer = ""

    status_text = ""
    status_until = 0

    running = True
    while running:
        now_ticks = pygame.time.get_ticks()
        if status_text and now_ticks > status_until:
            status_text = ""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # -------------------- КЛАВИАТУРА --------------------

            elif event.type == pygame.KEYDOWN:
                mod = pygame.key.get_mods()
                ctrl_or_cmd = mod & (pygame.KMOD_CTRL | pygame.KMOD_META)
                alt_held = mod & pygame.KMOD_ALT

                # Если сейчас вводится текст, клавиатура должна печатать символы,
                # а не переключать инструменты.
                if text_active:
                    if event.key == pygame.K_RETURN:
                        if text_buffer:
                            text_surface = text_font.render(text_buffer, True, current_color)
                            canvas.blit(text_surface, text_pos)
                        text_active = False
                        text_pos = None
                        text_buffer = ""

                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_pos = None
                        text_buffer = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]

                    elif event.unicode:
                        text_buffer += event.unicode

                    continue

                # Ctrl+S / Cmd+S — сохранить canvas
                if event.key == pygame.K_s and ctrl_or_cmd:
                    filename = save_canvas(canvas)
                    status_text = f"Saved: {filename}"
                    status_until = pygame.time.get_ticks() + 3000
                    continue

                # Выход из программы
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_w and ctrl_or_cmd:
                    running = False

                elif event.key == pygame.K_F4 and alt_held:
                    running = False

                # Выбор размера кисти: 1, 2, 3
                elif event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

                # Очистка canvas
                elif event.key == pygame.K_BACKSPACE:
                    canvas.fill(WHITE)

                # Выбор инструмента горячими клавишами
                else:
                    for label, tool, key in TOOLS:
                        if event.key == key:
                            current_tool = tool
                            break

            # -------------------- НАЖАТИЕ МЫШИ --------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Левая кнопка мыши
                if event.button == 1:

                    # Верхняя панель: кнопки инструментов, цветов и размеров
                    if mouse_pos[1] < TOOLBAR_HEIGHT:
                        selected_tool = get_tool_from_toolbar(mouse_pos)
                        selected_color = get_color_from_toolbar(mouse_pos)
                        selected_size = get_size_from_toolbar(mouse_pos)

                        if selected_tool is not None:
                            current_tool = selected_tool
                            text_active = False
                            text_buffer = ""

                        elif selected_color is not None:
                            current_color = selected_color

                        elif selected_size is not None:
                            brush_size = selected_size

                    # Область рисования
                    elif inside_canvas(mouse_pos):
                        pos = canvas_pos(mouse_pos)

                        if current_tool == "fill":
                            flood_fill(canvas, pos, current_color)

                        elif current_tool == "text":
                            text_active = True
                            text_pos = pos
                            text_buffer = ""

                        else:
                            drawing = True
                            start_pos = pos
                            last_pos = pos

                            # Карандаш и ластик оставляют точку сразу после нажатия
                            if current_tool == "pencil":
                                pygame.draw.circle(canvas, current_color, pos, max(1, brush_size // 2))

                            elif current_tool == "eraser":
                                pygame.draw.circle(canvas, WHITE, pos, max(1, brush_size // 2))

            # -------------------- ДВИЖЕНИЕ МЫШИ --------------------

            elif event.type == pygame.MOUSEMOTION:
                if drawing and inside_canvas(event.pos):
                    current_pos = canvas_pos(event.pos)

                    if current_tool == "pencil":
                        draw_pencil_line(canvas, last_pos, current_pos, current_color, brush_size)
                        last_pos = current_pos

                    elif current_tool == "eraser":
                        draw_pencil_line(canvas, last_pos, current_pos, WHITE, brush_size)
                        last_pos = current_pos

            # -------------------- ОТПУСКАНИЕ МЫШИ --------------------

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and event.button == 1:
                    mouse_pos = event.pos

                    # Если мышь отпустили над панелью, фиксируем точку на верхней границе canvas
                    if mouse_pos[1] < TOOLBAR_HEIGHT:
                        mouse_pos = (mouse_pos[0], TOOLBAR_HEIGHT)

                    # Ограничиваем конечную точку внутри окна
                    x = max(0, min(WIDTH - 1, mouse_pos[0]))
                    y = max(TOOLBAR_HEIGHT, min(HEIGHT - 1, mouse_pos[1]))
                    end_pos = canvas_pos((x, y))

                    if current_tool == "line":
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                    elif current_tool == "rectangle":
                        rect = make_rect(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, brush_size)

                    elif current_tool == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        circle_radius = int(math.sqrt(dx ** 2 + dy ** 2))
                        pygame.draw.circle(canvas, current_color, start_pos, circle_radius, brush_size)

                    elif current_tool == "square":
                        square = make_square(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, square, brush_size)

                    elif current_tool == "right triangle":
                        points = make_right_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, brush_size)

                    elif current_tool == "equilateral triangle":
                        points = make_equilateral_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, brush_size)

                    elif current_tool == "rhombus":
                        points = make_rhombus(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, brush_size)

                    drawing = False
                    start_pos = None
                    last_pos = None

        # -------------------- ОТРИСОВКА ЭКРАНА --------------------

        screen.fill(WHITE)
        draw_toolbar(screen, font, small_font, current_tool, current_color, brush_size, status_text)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # -------------------- ПРЕДПРОСМОТР ФИГУР И ЛИНИИ --------------------
        # Превью показывается во время зажатия мыши, но на canvas сохраняется
        # только после отпускания кнопки мыши.

        preview_tools = [
            "line",
            "rectangle",
            "circle",
            "square",
            "right triangle",
            "equilateral triangle",
            "rhombus"
        ]

        if drawing and current_tool in preview_tools and start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] >= TOOLBAR_HEIGHT:
                preview_end = canvas_pos(mouse_pos)
            else:
                preview_end = (mouse_pos[0], 0)

            if current_tool == "line":
                start_screen = (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT)
                end_screen = (preview_end[0], preview_end[1] + TOOLBAR_HEIGHT)
                pygame.draw.line(screen, current_color, start_screen, end_screen, brush_size)

            elif current_tool == "rectangle":
                rect = make_rect(start_pos, preview_end)
                rect.y += TOOLBAR_HEIGHT
                pygame.draw.rect(screen, current_color, rect, brush_size)

            elif current_tool == "circle":
                dx = preview_end[0] - start_pos[0]
                dy = preview_end[1] - start_pos[1]
                circle_radius = int(math.sqrt(dx ** 2 + dy ** 2))
                center = (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT)
                pygame.draw.circle(screen, current_color, center, circle_radius, brush_size)

            elif current_tool == "square":
                square = make_square(start_pos, preview_end)
                square.y += TOOLBAR_HEIGHT
                pygame.draw.rect(screen, current_color, square, brush_size)

            elif current_tool == "right triangle":
                points = make_right_triangle(start_pos, preview_end)
                points = [(x, y + TOOLBAR_HEIGHT) for x, y in points]
                pygame.draw.polygon(screen, current_color, points, brush_size)

            elif current_tool == "equilateral triangle":
                points = make_equilateral_triangle(start_pos, preview_end)
                points = [(x, y + TOOLBAR_HEIGHT) for x, y in points]
                pygame.draw.polygon(screen, current_color, points, brush_size)

            elif current_tool == "rhombus":
                points = make_rhombus(start_pos, preview_end)
                points = [(x, y + TOOLBAR_HEIGHT) for x, y in points]
                pygame.draw.polygon(screen, current_color, points, brush_size)

        # -------------------- LIVE-ПРЕДПРОСМОТР ТЕКСТА --------------------

        if text_active and text_pos is not None:
            preview_text = text_font.render(text_buffer, True, current_color)
            screen.blit(preview_text, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

            # Мигающий курсор
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                cursor_x = text_pos[0] + preview_text.get_width() + 2
                cursor_y = text_pos[1] + TOOLBAR_HEIGHT
                pygame.draw.line(screen, current_color, (cursor_x, cursor_y), (cursor_x, cursor_y + 28), 2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
