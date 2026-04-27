# Импортируем нужные библиотеки
import pygame, sys
from pygame.locals import *
import random, time

# Инициализация pygame
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Настройки экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Основные переменные игры
SPEED = 5
SCORE = 0
COINS = 0

# После каждых N монет скорость врага будет увеличиваться
COINS_FOR_SPEED_UP = 10
SPEED_BOOST = 1
speed_level = 0

# Настройка шрифтов
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фона
background = pygame.image.load("AnimatedStreet.png")

# Создание игрового окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Загружаем изображение врага
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()

        # Враг появляется в случайном месте сверху
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # Враг двигается вниз
        self.rect.move_ip(0, SPEED)

        # Если враг ушёл за нижнюю границу экрана,
        # он снова появляется сверху
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Загружаем изображение игрока
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()

        # Начальная позиция игрока
        self.rect.center = (160, 520)

    def move(self):
        # Получаем список нажатых клавиш
        pressed_keys = pygame.key.get_pressed()

        # Движение влево
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        # Движение вправо
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Загружаем изображение монеты
        self.base_image = pygame.image.load("Coin.png")

        # Создаём случайную монету
        self.create_random_coin()

    def create_random_coin(self):
        # Типы монет:
        # первое число — ценность монеты
        # второе число — размер монеты
        coin_types = [
            (1, 30),
            (2, 38),
            (5, 45)
        ]

        # Случайно выбираем тип монеты
        # Монета ценностью 1 появляется чаще,
        # а монета ценностью 5 появляется реже
        self.value, size = random.choices(
            coin_types,
            weights=[70, 25, 5]
        )[0]

        # Изменяем размер монеты в зависимости от её ценности
        self.image = pygame.transform.scale(self.base_image, (size, size))
        self.rect = self.image.get_rect()

        # Размещаем монету в случайном месте выше экрана
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-600, -50)
        )

    def move(self):
        # Монета двигается вниз вместе с дорогой
        self.rect.move_ip(0, SPEED)

        # Если монета ушла за нижнюю границу экрана,
        # создаём новую случайную монету
        if self.rect.top > SCREEN_HEIGHT:
            self.create_random_coin()


# Создаём игрока и врага
P1 = Player()
E1 = Enemy()

# Создаём несколько монет
C1 = Coin()
C2 = Coin()
C3 = Coin()

# Группа врагов
enemies = pygame.sprite.Group()
enemies.add(E1)

# Группа монет
coins = pygame.sprite.Group()
coins.add(C1)
coins.add(C2)
coins.add(C3)

# Группа всех спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)
all_sprites.add(C3)


# Основной игровой цикл
while True:

    # Проверяем события игры
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовываем фон
    DISPLAYSURF.blit(background, (0, 0))

    # Показываем счёт в левом верхнем углу
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Показываем количество собранных монет в правом верхнем углу
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Отрисовываем и двигаем все спрайты
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверяем, собрал ли игрок монеты
    collected_coins = pygame.sprite.spritecollide(P1, coins, False)

    for coin in collected_coins:
        # Добавляем ценность монеты к общему количеству монет
        COINS += coin.value

        # После сбора создаём новую случайную монету
        coin.create_random_coin()

    # Увеличиваем скорость врага после каждых N монет
    new_speed_level = COINS // COINS_FOR_SPEED_UP

    if new_speed_level > speed_level:
        SPEED += SPEED_BOOST
        speed_level = new_speed_level

    # Проверяем столкновение игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(0.5)

        # Показываем экран окончания игры
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        # Удаляем все спрайты
        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Обновляем экран
    pygame.display.update()

    # Ограничиваем FPS
    FramePerSec.tick(FPS)