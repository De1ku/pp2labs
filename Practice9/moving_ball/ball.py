import pygame

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Ball:
    def __init__(self):
        self.radius = 25
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.color = RED

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x - self.radius >= 0 and new_x + self.radius <= WIDTH:
            self.x = new_x

        if new_y - self.radius >= 0 and new_y + self.radius <= HEIGHT:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)