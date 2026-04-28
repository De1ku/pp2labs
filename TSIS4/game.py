import json
import os
import random
import sys

import pygame

from db import Database


# -------------------- ОСНОВНЫЕ НАСТРОЙКИ --------------------

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
WALL_SIZE = 20
FPS = 60

START_SPEED = 7
POINTS_PER_LEVEL = 5
FOOD_LIFETIME = 5000
POISON_LIFETIME = 8000
POWERUP_LIFETIME = 8000
POWERUP_DURATION = 5000

SETTINGS_FILE = "settings.json"


# -------------------- ЦВЕТА --------------------

BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
GRAY = (70, 70, 70)
DARK_GRAY = (35, 35, 35)
LIGHT_GRAY = (120, 120, 120)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 100, 0)
RED = (220, 30, 30)
DARK_RED = (120, 0, 0)
YELLOW = (240, 220, 0)
BLUE = (40, 120, 255)
PURPLE = (160, 70, 220)
ORANGE = (255, 150, 40)
CYAN = (40, 220, 220)

FOOD_TYPES = [
    {"weight": 1, "color": RED},
    {"weight": 2, "color": YELLOW},
    {"weight": 3, "color": BLUE}
]

POWERUP_TYPES = [
    {"type": "speed", "name": "Speed boost", "color": ORANGE},
    {"type": "slow", "name": "Slow motion", "color": CYAN},
    {"type": "shield", "name": "Shield", "color": PURPLE}
]

COLOR_OPTIONS = [
    (0, 180, 0),
    (40, 120, 255),
    (240, 220, 0),
    (160, 70, 220),
    (255, 150, 40)
]


class SnakeGame:
    """Основной класс игры Snake с БД, экранами, настройками и бонусами."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Verdana", 22)
        self.small_font = pygame.font.SysFont("Verdana", 15)
        self.big_font = pygame.font.SysFont("Verdana", 42)
        self.title_font = pygame.font.SysFont("Verdana", 32)

        self.db = Database()
        self.settings = self.load_settings()
        self.username = "Player"

    # -------------------- ОБЩИЕ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ --------------------

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def load_settings(self):
        """Загружает настройки из settings.json. Если файла нет, создаёт стандартные настройки."""
        default_settings = {
            "snake_color": [0, 180, 0],
            "grid": True,
            "sound": False
        }

        if not os.path.exists(SETTINGS_FILE):
            self.save_settings(default_settings)
            return default_settings

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                loaded = json.load(file)

            for key, value in default_settings.items():
                if key not in loaded:
                    loaded[key] = value

            return loaded
        except Exception:
            self.save_settings(default_settings)
            return default_settings

    def save_settings(self, settings=None):
        """Сохраняет настройки в settings.json."""
        if settings is None:
            settings = self.settings

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)

    def draw_text(self, text, font, color, x, y, center=False):
        """Выводит текст на экран."""
        surface = font.render(str(text), True, color)
        rect = surface.get_rect()

        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(surface, rect)
        return rect

    def draw_button(self, text, rect, mouse_pos):
        """Рисует кнопку и возвращает её прямоугольник."""
        color = LIGHT_GRAY if rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=8)
        self.draw_text(text, self.font, WHITE, rect.centerx, rect.centery - 1, center=True)
        return rect

    def draw_wall(self):
        """Рисует рамку игрового поля."""
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, WALL_SIZE))
        pygame.draw.rect(self.screen, GRAY, (0, HEIGHT - WALL_SIZE, WIDTH, WALL_SIZE))
        pygame.draw.rect(self.screen, GRAY, (0, 0, WALL_SIZE, HEIGHT))
        pygame.draw.rect(self.screen, GRAY, (WIDTH - WALL_SIZE, 0, WALL_SIZE, HEIGHT))

    def draw_grid(self):
        """Рисует сетку, если она включена в настройках."""
        if not self.settings.get("grid", True):
            return

        for x in range(WALL_SIZE, WIDTH - WALL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, WALL_SIZE), (x, HEIGHT - WALL_SIZE))

        for y in range(WALL_SIZE, HEIGHT - WALL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (WALL_SIZE, y), (WIDTH - WALL_SIZE, y))

    def get_all_cells(self):
        """Возвращает все клетки внутри стен."""
        cells = []
        for x in range(WALL_SIZE, WIDTH - WALL_SIZE, CELL_SIZE):
            for y in range(WALL_SIZE, HEIGHT - WALL_SIZE, CELL_SIZE):
                cells.append((x, y))
        return cells

    def is_inside_arena(self, position):
        """Проверяет, находится ли клетка внутри игрового поля."""
        x, y = position
        return WALL_SIZE <= x < WIDTH - WALL_SIZE and WALL_SIZE <= y < HEIGHT - WALL_SIZE

    def is_collision(self, position, snake, obstacles):
        """Проверяет столкновение со стеной, телом змейки или препятствием."""
        return (
            not self.is_inside_arena(position)
            or position in snake
            or position in obstacles
        )

    def generate_item_position(self, snake, obstacles, extra_blocked=None):
        """Генерирует свободную клетку для еды, яда или power-up."""
        if extra_blocked is None:
            extra_blocked = []

        blocked = set(snake) | set(obstacles) | set(extra_blocked)
        possible_positions = [cell for cell in self.get_all_cells() if cell not in blocked]

        if not possible_positions:
            return None

        return random.choice(possible_positions)

    # -------------------- ГЕНЕРАЦИЯ ОБЪЕКТОВ НА ПОЛЕ --------------------

    def generate_food(self, snake, obstacles, extra_blocked=None):
        """Создаёт обычную еду со случайным весом."""
        position = self.generate_item_position(snake, obstacles, extra_blocked)

        if position is None:
            return None

        food_type = random.choice(FOOD_TYPES)
        return {
            "position": position,
            "weight": food_type["weight"],
            "color": food_type["color"],
            "spawn_time": pygame.time.get_ticks()
        }

    def generate_poison(self, snake, obstacles, extra_blocked=None):
        """Создаёт ядовитую еду, которая укорачивает змейку."""
        position = self.generate_item_position(snake, obstacles, extra_blocked)

        if position is None:
            return None

        return {
            "position": position,
            "spawn_time": pygame.time.get_ticks()
        }

    def generate_powerup(self, snake, obstacles, extra_blocked=None):
        """Создаёт временный power-up. На поле одновременно может быть только один power-up."""
        position = self.generate_item_position(snake, obstacles, extra_blocked)

        if position is None:
            return None

        powerup_type = random.choice(POWERUP_TYPES)
        return {
            "position": position,
            "type": powerup_type["type"],
            "name": powerup_type["name"],
            "color": powerup_type["color"],
            "spawn_time": pygame.time.get_ticks()
        }

    def has_escape_cell(self, head, snake, obstacles):
        """Проверяет, есть ли у головы змейки хотя бы один свободный соседний ход."""
        moves = [(CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)]

        for dx, dy in moves:
            next_cell = (head[0] + dx, head[1] + dy)
            if self.is_inside_arena(next_cell) and next_cell not in snake and next_cell not in obstacles:
                return True

        return False

    def generate_obstacles(self, level, snake):
        """Генерирует препятствия с 3 уровня и не блокирует голову змейки со всех сторон."""
        if level < 3:
            return []

        head = snake[0]
        safe_zone = {head}
        for dx, dy in [(CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)]:
            safe_zone.add((head[0] + dx, head[1] + dy))

        candidates = [
            cell for cell in self.get_all_cells()
            if cell not in snake and cell not in safe_zone
        ]

        obstacle_count = min(6 + (level - 3) * 2, 25, len(candidates))

        for _ in range(100):
            obstacles = random.sample(candidates, obstacle_count)
            if self.has_escape_cell(head, snake, obstacles):
                return obstacles

        return []

    def get_item_position(self, item):
        if item is None:
            return None
        return item["position"]

    # -------------------- ЭКРАНЫ --------------------

    def main_menu(self):
        """Главное меню: ввод username и кнопки Play, Leaderboard, Settings, Quit."""
        input_rect = pygame.Rect(170, 115, 260, 38)
        play_rect = pygame.Rect(210, 175, 180, 42)
        leaderboard_rect = pygame.Rect(185, 230, 230, 42)
        settings_rect = pygame.Rect(210, 285, 180, 42)
        quit_rect = pygame.Rect(210, 340, 180, 42)

        input_active = True

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    input_active = input_rect.collidepoint(event.pos)

                    if play_rect.collidepoint(event.pos):
                        self.username = self.username.strip() or "Player"
                        return "play"

                    if leaderboard_rect.collidepoint(event.pos):
                        return "leaderboard"

                    if settings_rect.collidepoint(event.pos):
                        return "settings"

                    if quit_rect.collidepoint(event.pos):
                        self.quit_game()

                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_RETURN:
                        self.username = self.username.strip() or "Player"
                        return "play"

                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        if len(self.username) < 16 and event.unicode.isprintable():
                            self.username += event.unicode

            self.screen.fill(BLACK)
            self.draw_text("Snake Game", self.big_font, WHITE, WIDTH // 2, 45, center=True)
            self.draw_text("Username:", self.font, WHITE, WIDTH // 2, 95, center=True)

            pygame.draw.rect(self.screen, DARK_GRAY, input_rect, border_radius=6)
            pygame.draw.rect(self.screen, WHITE if input_active else LIGHT_GRAY, input_rect, 2, border_radius=6)
            self.draw_text(self.username, self.font, WHITE, input_rect.x + 10, input_rect.y + 5)

            self.draw_button("Play", play_rect, mouse_pos)
            self.draw_button("Leaderboard", leaderboard_rect, mouse_pos)
            self.draw_button("Settings", settings_rect, mouse_pos)
            self.draw_button("Quit", quit_rect, mouse_pos)

            if self.db.connection is None:
                self.draw_text("DB offline: check config.py", self.small_font, RED, WIDTH // 2, 385, center=True)

            pygame.display.update()
            self.clock.tick(FPS)

    def leaderboard_screen(self):
        """Экран таблицы лидеров: Top-10 из PostgreSQL."""
        back_rect = pygame.Rect(220, 340, 160, 40)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_rect.collidepoint(event.pos):
                        return

            rows = self.db.get_leaderboard(10)

            self.screen.fill(BLACK)
            self.draw_text("Leaderboard", self.title_font, WHITE, WIDTH // 2, 35, center=True)

            if self.db.connection is None:
                self.draw_text("Database is not connected", self.font, RED, WIDTH // 2, 120, center=True)
                self.draw_text("Edit config.py and create PostgreSQL database", self.small_font, WHITE, WIDTH // 2, 155, center=True)
            else:
                headers = ["#", "Username", "Score", "Level", "Date"]
                x_positions = [35, 85, 260, 350, 430]
                y = 80

                for i, header in enumerate(headers):
                    self.draw_text(header, self.small_font, YELLOW, x_positions[i], y)

                y += 28
                for index, row in enumerate(rows, start=1):
                    username, score, level, played_at = row
                    values = [index, username[:12], score, level, played_at]

                    for i, value in enumerate(values):
                        self.draw_text(value, self.small_font, WHITE, x_positions[i], y)

                    y += 24

                if not rows:
                    self.draw_text("No saved games yet", self.font, WHITE, WIDTH // 2, 190, center=True)

            self.draw_button("Back", back_rect, mouse_pos)
            pygame.display.update()
            self.clock.tick(FPS)

    def settings_screen(self):
        """Экран настроек: сетка, звук, цвет змейки."""
        color_rect = pygame.Rect(210, 115, 180, 42)
        grid_rect = pygame.Rect(210, 175, 180, 42)
        sound_rect = pygame.Rect(210, 235, 180, 42)
        save_rect = pygame.Rect(190, 315, 220, 42)

        current_color = tuple(self.settings.get("snake_color", [0, 180, 0]))
        if current_color not in COLOR_OPTIONS:
            current_color = COLOR_OPTIONS[0]

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if color_rect.collidepoint(event.pos):
                        index = COLOR_OPTIONS.index(current_color)
                        current_color = COLOR_OPTIONS[(index + 1) % len(COLOR_OPTIONS)]
                        self.settings["snake_color"] = list(current_color)

                    if grid_rect.collidepoint(event.pos):
                        self.settings["grid"] = not self.settings.get("grid", True)

                    if sound_rect.collidepoint(event.pos):
                        self.settings["sound"] = not self.settings.get("sound", False)

                    if save_rect.collidepoint(event.pos):
                        self.save_settings()
                        return

            self.screen.fill(BLACK)
            self.draw_text("Settings", self.title_font, WHITE, WIDTH // 2, 45, center=True)

            self.draw_button("Snake color", color_rect, mouse_pos)
            pygame.draw.rect(self.screen, current_color, (410, 120, 32, 32), border_radius=5)
            pygame.draw.rect(self.screen, WHITE, (410, 120, 32, 32), 2, border_radius=5)

            grid_text = "Grid: ON" if self.settings.get("grid", True) else "Grid: OFF"
            sound_text = "Sound: ON" if self.settings.get("sound", False) else "Sound: OFF"
            self.draw_button(grid_text, grid_rect, mouse_pos)
            self.draw_button(sound_text, sound_rect, mouse_pos)
            self.draw_button("Save & Back", save_rect, mouse_pos)

            self.draw_text("Settings are saved to settings.json", self.small_font, WHITE, WIDTH // 2, 285, center=True)

            pygame.display.update()
            self.clock.tick(FPS)

    def game_over_screen(self, score, level, personal_best):
        """Экран Game Over с кнопками Retry и Main Menu."""
        retry_rect = pygame.Rect(125, 295, 150, 45)
        menu_rect = pygame.Rect(325, 295, 150, 45)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "retry"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_rect.collidepoint(event.pos):
                        return "retry"
                    if menu_rect.collidepoint(event.pos):
                        return "menu"

            self.screen.fill(BLACK)
            self.draw_text("Game Over", self.big_font, RED, WIDTH // 2, 85, center=True)
            self.draw_text(f"Final score: {score}", self.font, WHITE, WIDTH // 2, 155, center=True)
            self.draw_text(f"Level reached: {level}", self.font, WHITE, WIDTH // 2, 190, center=True)
            self.draw_text(f"Personal best: {personal_best}", self.font, YELLOW, WIDTH // 2, 225, center=True)
            self.draw_text("R - retry, ESC - main menu", self.small_font, LIGHT_GRAY, WIDTH // 2, 260, center=True)

            self.draw_button("Retry", retry_rect, mouse_pos)
            self.draw_button("Main Menu", menu_rect, mouse_pos)

            pygame.display.update()
            self.clock.tick(FPS)

    # -------------------- ИГРОВОЙ ПРОЦЕСС --------------------

    def get_effective_speed(self, base_speed, active_powerup):
        """Возвращает текущую скорость с учётом power-up эффекта."""
        if active_powerup == "speed":
            return base_speed + 5

        if active_powerup == "slow":
            return max(4, base_speed - 3)

        return base_speed

    def activate_powerup(self, powerup, current_time):
        """Активирует собранный power-up."""
        if powerup["type"] == "shield":
            return "shield", 0

        return powerup["type"], current_time + POWERUP_DURATION

    def update_powerup_timer(self, active_powerup, powerup_end_time, current_time):
        """Отключает временный эффект speed/slow после 5 секунд."""
        if active_powerup in ("speed", "slow") and current_time >= powerup_end_time:
            return None, 0

        return active_powerup, powerup_end_time

    def find_safe_direction(self, snake, obstacles):
        """Ищет безопасное направление после срабатывания щита."""
        head = snake[0]
        moves = [(CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)]

        for dx, dy in moves:
            next_cell = (head[0] + dx, head[1] + dy)
            if not self.is_collision(next_cell, snake, obstacles):
                return dx, dy

        return 0, 0

    def finish_game(self, score, level):
        """Сохраняет игру в БД и открывает Game Over screen."""
        self.db.save_game_session(self.username, score, level)
        personal_best = max(score, self.db.get_personal_best(self.username))
        return self.game_over_screen(score, level, personal_best)

    def draw_game(self, snake, food, poison, powerup, obstacles, score, level, personal_best,
                  active_powerup, powerup_end_time, current_time, message=""):
        """Рисует все элементы игрового поля."""
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_wall()

        # Препятствия появляются с 3 уровня.
        for obstacle in obstacles:
            pygame.draw.rect(self.screen, LIGHT_GRAY, (obstacle[0], obstacle[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, GRAY, (obstacle[0], obstacle[1], CELL_SIZE, CELL_SIZE), 2)

        # Обычная еда с весом.
        if food is not None:
            food_x, food_y = food["position"]
            pygame.draw.rect(self.screen, food["color"], (food_x, food_y, CELL_SIZE, CELL_SIZE))
            self.draw_text(food["weight"], self.small_font, BLACK, food_x + 5, food_y + 1)
            time_left = max(0, (FOOD_LIFETIME - (current_time - food["spawn_time"])) // 1000)
            self.draw_text(f"Food: {time_left}s", self.small_font, WHITE, 235, 23)

        # Ядовитая еда.
        if poison is not None:
            poison_x, poison_y = poison["position"]
            pygame.draw.rect(self.screen, DARK_RED, (poison_x, poison_y, CELL_SIZE, CELL_SIZE))
            self.draw_text("P", self.small_font, WHITE, poison_x + 4, poison_y + 1)

        # Power-up.
        if powerup is not None:
            power_x, power_y = powerup["position"]
            pygame.draw.rect(self.screen, powerup["color"], (power_x, power_y, CELL_SIZE, CELL_SIZE), border_radius=4)
            self.draw_text("*", self.font, BLACK, power_x + 4, power_y - 4)

        # Змейка.
        snake_color = tuple(self.settings.get("snake_color", [0, 180, 0]))
        for index, part in enumerate(snake):
            color = DARK_GREEN if index == 0 else snake_color
            pygame.draw.rect(self.screen, color, (part[0], part[1], CELL_SIZE, CELL_SIZE))

        # Информация на экране.
        self.draw_text(f"Score: {score}", self.small_font, WHITE, 28, 23)
        self.draw_text(f"Level: {level}", self.small_font, WHITE, 500, 23)
        self.draw_text(f"Best: {personal_best}", self.small_font, YELLOW, 28, HEIGHT - 38)

        if active_powerup is not None:
            if active_powerup == "shield":
                power_text = "Power: Shield"
            else:
                seconds = max(0, (powerup_end_time - current_time) // 1000)
                power_text = f"Power: {active_powerup} {seconds}s"
            self.draw_text(power_text, self.small_font, CYAN, 390, HEIGHT - 38)

        if message:
            self.draw_text(message, self.small_font, YELLOW, WIDTH // 2, HEIGHT - 38, center=True)

        pygame.display.update()

    def play_game(self):
        """Главный игровой цикл."""
        snake = [(300, 200), (280, 200), (260, 200)]
        direction = (CELL_SIZE, 0)
        next_direction = direction

        score = 0
        level = 1
        base_speed = START_SPEED
        obstacles = []

        food = self.generate_food(snake, obstacles)
        poison = None
        powerup = None

        active_powerup = None
        powerup_end_time = 0
        shield_message_until = 0

        current_time = pygame.time.get_ticks()
        next_poison_time = current_time + random.randint(5000, 9000)
        next_powerup_time = current_time + random.randint(7000, 12000)

        personal_best = self.db.get_personal_best(self.username)

        while True:
            current_time = pygame.time.get_ticks()
            active_powerup, powerup_end_time = self.update_powerup_timer(
                active_powerup,
                powerup_end_time,
                current_time
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                    # Нельзя разворачиваться сразу в противоположную сторону.
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL_SIZE):
                        next_direction = (0, -CELL_SIZE)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL_SIZE):
                        next_direction = (0, CELL_SIZE)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL_SIZE, 0):
                        next_direction = (-CELL_SIZE, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL_SIZE, 0):
                        next_direction = (CELL_SIZE, 0)

            direction = next_direction

            # Обычная еда исчезает после таймера.
            if food is not None and current_time - food["spawn_time"] >= FOOD_LIFETIME:
                blocked = [self.get_item_position(poison), self.get_item_position(powerup)]
                food = self.generate_food(snake, obstacles, blocked)

            # Яд появляется случайно рядом с обычной едой.
            if poison is None and current_time >= next_poison_time:
                blocked = [self.get_item_position(food), self.get_item_position(powerup)]
                poison = self.generate_poison(snake, obstacles, blocked)

            if poison is not None and current_time - poison["spawn_time"] >= POISON_LIFETIME:
                poison = None
                next_poison_time = current_time + random.randint(6000, 11000)

            # На поле одновременно может быть только один power-up.
            if powerup is None and current_time >= next_powerup_time:
                blocked = [self.get_item_position(food), self.get_item_position(poison)]
                powerup = self.generate_powerup(snake, obstacles, blocked)

            if powerup is not None and current_time - powerup["spawn_time"] >= POWERUP_LIFETIME:
                powerup = None
                next_powerup_time = current_time + random.randint(8000, 14000)

            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Столкновение со стеной, собой или препятствием.
            if self.is_collision(new_head, snake, obstacles):
                if active_powerup == "shield":
                    active_powerup = None
                    shield_message_until = current_time + 1200
                    safe_direction = self.find_safe_direction(snake, obstacles)
                    if safe_direction != (0, 0):
                        direction = safe_direction
                        next_direction = safe_direction

                    self.draw_game(
                        snake, food, poison, powerup, obstacles, score, level,
                        max(personal_best, score), active_powerup, powerup_end_time,
                        current_time, "Shield saved you!"
                    )
                    self.clock.tick(self.get_effective_speed(base_speed, active_powerup))
                    continue

                return self.finish_game(score, level)

            # Добавляем новую голову.
            snake.insert(0, new_head)

            ate_food = food is not None and new_head == food["position"]
            ate_poison = poison is not None and new_head == poison["position"]
            ate_powerup = powerup is not None and new_head == powerup["position"]

            if ate_food:
                score += food["weight"]
                personal_best = max(personal_best, score)

                new_level = score // POINTS_PER_LEVEL + 1
                if new_level != level:
                    level = new_level
                    base_speed = START_SPEED + (level - 1) * 2
                    obstacles = self.generate_obstacles(level, snake)

                blocked = [self.get_item_position(poison), self.get_item_position(powerup)]
                food = self.generate_food(snake, obstacles, blocked)

                if food is None:
                    return self.finish_game(score, level)

                # Если после нового уровня объект оказался на препятствии, пересоздаём его.
                if poison is not None and poison["position"] in obstacles:
                    poison = None
                    next_poison_time = current_time + random.randint(3000, 7000)
                if powerup is not None and powerup["position"] in obstacles:
                    powerup = None
                    next_powerup_time = current_time + random.randint(5000, 9000)

            elif ate_poison:
                poison = None
                next_poison_time = current_time + random.randint(6000, 11000)

                # После вставки новой головы длина стала L + 1.
                # Чтобы итоговая длина была на 2 меньше старой, убираем 3 сегмента хвоста.
                target_length = len(snake) - 3
                if target_length <= 1:
                    return self.finish_game(score, level)

                while len(snake) > target_length:
                    snake.pop()

            else:
                # Если обычная еда не съедена, хвост убирается как при обычном движении.
                snake.pop()

            if ate_powerup:
                active_powerup, powerup_end_time = self.activate_powerup(powerup, current_time)
                powerup = None
                next_powerup_time = current_time + random.randint(8000, 14000)

            message = ""
            if current_time < shield_message_until:
                message = "Shield saved you!"

            self.draw_game(
                snake, food, poison, powerup, obstacles, score, level,
                max(personal_best, score), active_powerup, powerup_end_time,
                current_time, message
            )

            self.clock.tick(self.get_effective_speed(base_speed, active_powerup))

    def run(self):
        """Запускает приложение и переключает экраны."""
        while True:
            action = self.main_menu()

            if action == "leaderboard":
                self.leaderboard_screen()

            elif action == "settings":
                self.settings_screen()

            elif action == "play":
                while True:
                    result = self.play_game()
                    if result == "retry":
                        continue
                    break
