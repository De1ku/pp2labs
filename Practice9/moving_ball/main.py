import pygame
from ball import Ball, WIDTH, HEIGHT, WHITE

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

clock = pygame.time.Clock()
running = True

ball = Ball()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -20)
            elif event.key == pygame.K_DOWN:
                ball.move(0, 20)
            elif event.key == pygame.K_LEFT:
                ball.move(-20, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(20, 0)

    screen.fill(WHITE)
    ball.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()