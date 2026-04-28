import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (18, 18, 28)
PANEL = (35, 35, 55)
BLUE = (70, 120, 220)
BLUE_HOVER = (100, 145, 235)
GREEN = (80, 180, 120)
RED = (210, 80, 80)
YELLOW = (240, 210, 90)
GRAY = (150, 150, 160)
LIGHT_GRAY = (210, 210, 220)


class Button:
    def __init__(self, rect, text, font, bg=BLUE, hover=BLUE_HOVER, fg=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg
        self.hover = hover
        self.fg = fg

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mouse_pos) else self.bg
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        text_surf = self.font.render(self.text, True, self.fg)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class ChoiceButton(Button):
    def __init__(self, rect, text, font):
        super().__init__(rect, text, font, bg=PANEL, hover=BLUE)
        self.selected = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.selected:
            color = GREEN
        else:
            color = self.hover if self.rect.collidepoint(mouse_pos) else self.bg
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class TextInput:
    def __init__(self, rect, font, placeholder='Enter name'):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.placeholder = placeholder
        self.text = ''
        self.active = True
        self.max_len = 16

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_SPACE:
                if self.text and len(self.text) < self.max_len:
                    self.text += ' '
            elif event.unicode.isprintable() and len(self.text) < self.max_len:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLUE if self.active else GRAY, self.rect, 3, border_radius=10)
        value = self.text if self.text else self.placeholder
        color = BLACK if self.text else GRAY
        surface = self.font.render(value, True, color)
        screen.blit(surface, (self.rect.x + 12, self.rect.y + 12))



def draw_center_text(screen, text, font, color, center):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)



def draw_panel(screen, rect, color=PANEL):
    pygame.draw.rect(screen, color, rect, border_radius=16)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=16)
