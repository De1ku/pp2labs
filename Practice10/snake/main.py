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
RED = (220, 30, 30)
GRAY = (70, 70, 70)
DARK_GREEN = (0, 100, 0)

# Шрифты
font = pygame.font.SysFont("Verdana", 22)
big_font = pygame.font.SysFont("Verdana", 45)

# Начальные настройки игры
START_SPEED = 7
FOODS_PER_LEVEL = 3


def generate_food(snake):
    """
    Генерирует еду в случайной позиции.
    Еда не должна появляться на стене или на змейке.
    """
    possible_positions = []

    # Перебираем только клетки внутри игрового поля, не включая стены
    for x in range(WALL_SIZE, WIDTH - WALL_SIZE, CELL_SIZE):
        for y in range(WALL_SIZE, HEIGHT - WALL_SIZE, CELL_SIZE):
            if (x, y) not in snake:
                possible_positions.append((x, y))

    if possible_positions:
        return random.choice(possible_positions)

    return None


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

    waiting = True
    while waiting:
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

    # Начальное направление движения
    direction = (CELL_SIZE, 0)
    next_direction = direction

    # Начальные значения счёта, уровня и скорости
    score = 0
    level = 1
    speed = START_SPEED

    # Создаём первую еду
    food = generate_food(snake)

    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Меняем направление движения
                # Запрещаем змейке разворачиваться сразу назад
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL_SIZE):
                    next_direction = (0, -CELL_SIZE)

                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL_SIZE):
                    next_direction = (0, CELL_SIZE)

                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL_SIZE, 0):
                    next_direction = (-CELL_SIZE, 0)

                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL_SIZE, 0):
                    next_direction = (CELL_SIZE, 0)

        direction = next_direction

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
        if new_head == food:
            score += 1

            # Каждые 3 еды уровень увеличивается
            level = score // FOODS_PER_LEVEL + 1

            # С каждым новым уровнем скорость становится выше
            speed = START_SPEED + (level - 1) * 2

            # Создаём новую еду
            food = generate_food(snake)

            # Если места для еды больше нет, игра заканчивается
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
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Рисуем змейку
        for index, part in enumerate(snake):
            color = DARK_GREEN if index == 0 else GREEN
            pygame.draw.rect(screen, color, (part[0], part[1], CELL_SIZE, CELL_SIZE))

        # Выводим счёт и уровень
        show_text(f"Score: {score}", font, WHITE, 30, 25)
        show_text(f"Level: {level}", font, WHITE, 470, 25)

        pygame.display.update()

        # Ограничиваем скорость игры
        clock.tick(speed)


main()