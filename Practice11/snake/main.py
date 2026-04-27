import pygame
import random
import sys

pygame.init()

# Настройки экрана
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
WALL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 100, 0)
RED = (220, 30, 30)
YELLOW = (240, 220, 0)
BLUE = (40, 120, 255)
GRAY = (70, 70, 70)

# Шрифты
font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)
big_font = pygame.font.SysFont("Verdana", 45)

# Начальные настройки игры
START_SPEED = 7

# Через сколько очков повышается уровень
POINTS_PER_LEVEL = 5

# Время жизни еды в миллисекундах
FOOD_LIFETIME = 5000

# Разные типы еды
# weight — сколько очков даёт еда
# color — цвет еды
FOOD_TYPES = [
    {"weight": 1, "color": RED},
    {"weight": 2, "color": YELLOW},
    {"weight": 3, "color": BLUE}
]


def generate_food(snake):
    """
    Генерирует еду в случайной позиции.
    Еда не должна появляться на стене или на змейке.
    Также у еды случайно выбирается вес.
    """
    possible_positions = []

    # Перебираем все клетки внутри игрового поля, не включая стены
    for x in range(WALL_SIZE, WIDTH - WALL_SIZE, CELL_SIZE):
        for y in range(WALL_SIZE, HEIGHT - WALL_SIZE, CELL_SIZE):
            if (x, y) not in snake:
                possible_positions.append((x, y))

    # Если свободных клеток нет, возвращаем None
    if not possible_positions:
        return None

    # Выбираем случайную позицию для еды
    position = random.choice(possible_positions)

    # Выбираем случайный тип еды
    food_type = random.choice(FOOD_TYPES)

    # Возвращаем еду как словарь
    return {
        "position": position,
        "weight": food_type["weight"],
        "color": food_type["color"],
        "spawn_time": pygame.time.get_ticks()
    }


def draw_wall():
    """Рисует стены по краям игрового поля."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, WALL_SIZE))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - WALL_SIZE, WIDTH, WALL_SIZE))
    pygame.draw.rect(screen, GRAY, (0, 0, WALL_SIZE, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - WALL_SIZE, 0, WALL_SIZE, HEIGHT))


def check_wall_collision(head):
    """Проверяет, столкнулась ли голова змейки со стеной."""
    x, y = head

    if x < WALL_SIZE or x >= WIDTH - WALL_SIZE:
        return True

    if y < WALL_SIZE or y >= HEIGHT - WALL_SIZE:
        return True

    return False


def show_text(text, font_obj, color, x, y):
    """Выводит текст на экран."""
    message = font_obj.render(text, True, color)
    screen.blit(message, (x, y))


def game_over_screen(score, level):
    """Показывает экран окончания игры."""
    screen.fill(BLACK)

    show_text("Game Over", big_font, RED, 170, 120)
    show_text(f"Score: {score}", font, WHITE, 240, 190)
    show_text(f"Level: {level}", font, WHITE, 245, 225)
    show_text("Press ESC to quit", font, WHITE, 195, 280)

    pygame.display.update()

    # Ожидаем, пока пользователь закроет окно или нажмёт ESC
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    # Начальное положение змейки
    snake = [(300, 200), (280, 200), (260, 200)]

    # Начальное направление движения змейки
    direction = (CELL_SIZE, 0)
    next_direction = direction

    # Начальные значения счёта, уровня и скорости
    score = 0
    level = 1
    speed = START_SPEED

    # Создаём первую еду
    food = generate_food(snake)

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Меняем направление движения
                # Нельзя сразу развернуться в противоположную сторону
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL_SIZE):
                    next_direction = (0, -CELL_SIZE)

                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL_SIZE):
                    next_direction = (0, CELL_SIZE)

                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL_SIZE, 0):
                    next_direction = (-CELL_SIZE, 0)

                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL_SIZE, 0):
                    next_direction = (CELL_SIZE, 0)

        direction = next_direction

        # Проверяем, не истекло ли время жизни еды
        current_time = pygame.time.get_ticks()

        if food is not None:
            food_age = current_time - food["spawn_time"]

            # Если еда слишком долго лежит на поле, она исчезает
            if food_age >= FOOD_LIFETIME:
                food = generate_food(snake)

        # Создаём новую позицию головы змейки
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Проверяем столкновение со стеной
        if check_wall_collision(new_head):
            game_over_screen(score, level)

        # Проверяем столкновение змейки с самой собой
        if new_head in snake:
            game_over_screen(score, level)

        # Добавляем новую голову змейки
        snake.insert(0, new_head)

        # Проверяем, съела ли змейка еду
        if food is not None and new_head == food["position"]:
            # Добавляем очки в зависимости от веса еды
            score += food["weight"]

            # Уровень зависит от количества очков
            level = score // POINTS_PER_LEVEL + 1

            # Чем выше уровень, тем больше скорость
            speed = START_SPEED + (level - 1) * 2

            # Создаём новую еду
            food = generate_food(snake)

            # Если свободного места для еды нет, игра заканчивается
            if food is None:
                game_over_screen(score, level)
        else:
            # Если еда не съедена, убираем хвост
            snake.pop()

        # Очищаем экран
        screen.fill(BLACK)

        # Рисуем стены
        draw_wall()

        # Рисуем еду
        if food is not None:
            food_x, food_y = food["position"]

            pygame.draw.rect(
                screen,
                food["color"],
                (food_x, food_y, CELL_SIZE, CELL_SIZE)
            )

            # Показываем вес еды прямо на клетке
            show_text(str(food["weight"]), small_font, BLACK, food_x + 5, food_y)

            # Показываем оставшееся время еды
            time_left = max(0, (FOOD_LIFETIME - (current_time - food["spawn_time"])) // 1000)
            show_text(f"Food time: {time_left}", small_font, WHITE, 235, 25)

        # Рисуем змейку
        for index, part in enumerate(snake):
            # Голова змейки темнее, чем тело
            color = DARK_GREEN if index == 0 else GREEN
            pygame.draw.rect(screen, color, (part[0], part[1], CELL_SIZE, CELL_SIZE))

        # Выводим счёт и уровень
        show_text(f"Score: {score}", font, WHITE, 30, 25)
        show_text(f"Level: {level}", font, WHITE, 470, 25)

        pygame.display.update()

        # Ограничиваем скорость игры
        clock.tick(speed)


main()