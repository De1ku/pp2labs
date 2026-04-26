import pygame
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 680
CENTER = (400, 400)
FPS = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()


def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def draw_rotated(surface, image, angle, center):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=center)
    surface.blit(rotated, rect)


clock_img = load_image("images/mainclock.png", (600, 600))
minute_hand = load_image("images/right_hand1.png", (800, 700))
second_hand = load_image("images/left_hand1.png", (40, 500))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.now()
    minute = now.minute
    second = now.second

    minute_angle = -minute * 7 - 11
    second_angle = -second * 6 - 5

    screen.fill((255, 255, 255))

    screen.blit(clock_img, (100, 100))
    draw_rotated(screen, second_hand, second_angle, CENTER)
    draw_rotated(screen, minute_hand, minute_angle, CENTER)

    pygame.draw.circle(screen, (0, 0, 0), CENTER, 22)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()