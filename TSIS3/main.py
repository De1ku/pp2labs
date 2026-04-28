import sys

import pygame

from persistence import add_score, load_leaderboard, load_settings, save_settings
from racer import Game, HEIGHT, WIDTH
from ui import (
    BLACK,
    BLUE,
    ChoiceButton,
    DARK,
    GREEN,
    RED,
    WHITE,
    Button,
    TextInput,
    draw_center_text,
    draw_panel,
)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TSIS 3 - Racer Game')
clock = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont('Verdana', 28, bold=True)
SUBTITLE_FONT = pygame.font.SysFont('Verdana', 18, bold=True)
FONT = pygame.font.SysFont('Verdana', 20)
SMALL_FONT = pygame.font.SysFont('Verdana', 16)


def draw_background():
    screen.fill(DARK)
    pygame.draw.rect(screen, (24, 24, 40), (18, 18, WIDTH - 36, HEIGHT - 36), border_radius=18)
    pygame.draw.rect(screen, WHITE, (18, 18, WIDTH - 36, HEIGHT - 36), 2, border_radius=18)



def menu_screen():
    play_btn = Button((100, 180, 200, 50), 'Play', FONT)
    lead_btn = Button((100, 250, 200, 50), 'Leaderboard', FONT)
    settings_btn = Button((100, 320, 200, 50), 'Settings', FONT)
    quit_btn = Button((100, 390, 200, 50), 'Quit', FONT, bg=RED)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if play_btn.is_clicked(event):
                return 'play'
            if lead_btn.is_clicked(event):
                return 'leaderboard'
            if settings_btn.is_clicked(event):
                return 'settings'
            if quit_btn.is_clicked(event):
                return 'quit'

        draw_background()
        draw_center_text(screen, 'TSIS 3: Racer Game', TITLE_FONT, WHITE, (WIDTH // 2, 80))
        draw_center_text(screen, 'Advanced driving, leaderboard & power-ups', SMALL_FONT, WHITE, (WIDTH // 2, 112))
        hint = SMALL_FONT.render('Use LEFT/RIGHT arrows during the race', True, WHITE)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 145)))

        for btn in (play_btn, lead_btn, settings_btn, quit_btn):
            btn.draw(screen)
        pygame.display.flip()



def username_screen():
    input_box = TextInput((65, 240, 270, 50), FONT, placeholder='Enter player name')
    input_box.text = 'Player'
    start_btn = Button((65, 330, 125, 48), 'Start', FONT, bg=GREEN)
    back_btn = Button((210, 330, 125, 48), 'Back', FONT, bg=RED)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            input_box.handle_event(event)
            if start_btn.is_clicked(event):
                name = input_box.text.strip() or 'Player'
                return name[:16]
            if back_btn.is_clicked(event):
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                name = input_box.text.strip() or 'Player'
                return name[:16]

        draw_background()
        draw_center_text(screen, 'Enter Username', TITLE_FONT, WHITE, (WIDTH // 2, 110))
        draw_center_text(screen, 'This name will be saved in the leaderboard', SMALL_FONT, WHITE, (WIDTH // 2, 150))
        input_box.draw(screen)
        start_btn.draw(screen)
        back_btn.draw(screen)
        pygame.display.flip()



def settings_screen(settings):
    sound_on = ChoiceButton((60, 170, 120, 42), 'Sound: ON', SMALL_FONT)
    sound_off = ChoiceButton((220, 170, 120, 42), 'Sound: OFF', SMALL_FONT)

    color_buttons = {
        'blue': ChoiceButton((35, 270, 75, 42), 'Blue', SMALL_FONT),
        'red': ChoiceButton((125, 270, 75, 42), 'Red', SMALL_FONT),
        'green': ChoiceButton((215, 270, 75, 42), 'Green', SMALL_FONT),
        'yellow': ChoiceButton((305, 270, 75, 42), 'Yellow', SMALL_FONT),
    }

    diff_buttons = {
        'easy': ChoiceButton((50, 380, 90, 42), 'Easy', SMALL_FONT),
        'normal': ChoiceButton((155, 380, 90, 42), 'Normal', SMALL_FONT),
        'hard': ChoiceButton((260, 380, 90, 42), 'Hard', SMALL_FONT),
    }

    save_btn = Button((65, 500, 125, 48), 'Save', FONT, bg=GREEN)
    back_btn = Button((210, 500, 125, 48), 'Back', FONT, bg=RED)

    local = settings.copy()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return settings
            if sound_on.is_clicked(event):
                local['sound'] = True
            if sound_off.is_clicked(event):
                local['sound'] = False
            for color, btn in color_buttons.items():
                if btn.is_clicked(event):
                    local['car_color'] = color
            for diff, btn in diff_buttons.items():
                if btn.is_clicked(event):
                    local['difficulty'] = diff
            if save_btn.is_clicked(event):
                save_settings(local)
                return local
            if back_btn.is_clicked(event):
                return settings

        sound_on.selected = bool(local.get('sound', True))
        sound_off.selected = not bool(local.get('sound', True))
        for color, btn in color_buttons.items():
            btn.selected = local.get('car_color') == color
        for diff, btn in diff_buttons.items():
            btn.selected = local.get('difficulty') == diff

        draw_background()
        draw_center_text(screen, 'Settings', TITLE_FONT, WHITE, (WIDTH // 2, 80))

        draw_center_text(screen, 'Sound', SUBTITLE_FONT, WHITE, (WIDTH // 2, 145))
        sound_on.draw(screen)
        sound_off.draw(screen)

        draw_center_text(screen, 'Car Color', SUBTITLE_FONT, WHITE, (WIDTH // 2, 240))
        for btn in color_buttons.values():
            btn.draw(screen)

        draw_center_text(screen, 'Difficulty', SUBTITLE_FONT, WHITE, (WIDTH // 2, 350))
        for btn in diff_buttons.values():
            btn.draw(screen)

        note = SMALL_FONT.render('Preferences are saved to settings.json', True, WHITE)
        screen.blit(note, note.get_rect(center=(WIDTH // 2, 460)))

        save_btn.draw(screen)
        back_btn.draw(screen)
        pygame.display.flip()



def leaderboard_screen():
    back_btn = Button((135, 535, 130, 42), 'Back', FONT, bg=RED)
    while True:
        clock.tick(60)
        entries = load_leaderboard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if back_btn.is_clicked(event):
                return

        draw_background()
        draw_center_text(screen, 'Top 10 Leaderboard', TITLE_FONT, WHITE, (WIDTH // 2, 70))
        draw_panel(screen, pygame.Rect(30, 110, 340, 400))

        headers = ['#', 'Name', 'Score', 'Dist']
        x_positions = [45, 82, 210, 305]
        for header, x in zip(headers, x_positions):
            screen.blit(SMALL_FONT.render(header, True, WHITE), (x, 128))

        if not entries:
            draw_center_text(screen, 'No scores yet', FONT, WHITE, (WIDTH // 2, 300))
        else:
            for i, item in enumerate(entries[:10], start=1):
                y = 155 + (i - 1) * 31
                line = [
                    str(i),
                    str(item.get('name', 'Player'))[:10],
                    str(item.get('score', 0)),
                    str(item.get('distance', 0)),
                ]
                for text, x in zip(line, x_positions):
                    screen.blit(SMALL_FONT.render(text, True, WHITE), (x, y))

        back_btn.draw(screen)
        pygame.display.flip()



def game_over_screen(result):
    retry_btn = Button((55, 500, 125, 48), 'Retry', FONT, bg=GREEN)
    menu_btn = Button((220, 500, 125, 48), 'Main Menu', FONT, bg=BLUE)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if retry_btn.is_clicked(event):
                return 'retry'
            if menu_btn.is_clicked(event):
                return 'menu'

        draw_background()
        title = 'You Finished!' if result.get('won') else 'Game Over'
        color = GREEN if result.get('won') else RED
        draw_center_text(screen, title, TITLE_FONT, color, (WIDTH // 2, 90))
        draw_panel(screen, pygame.Rect(48, 150, 304, 270))

        lines = [
            f"Player: {result.get('name', 'Player')}",
            f"Score: {result.get('score', 0)}",
            f"Distance: {result.get('distance', 0)}",
            f"Coins: {result.get('coins', 0)}",
            f"Result: {'Finished track' if result.get('won') else 'Crashed'}",
        ]
        for i, line in enumerate(lines):
            text = FONT.render(line, True, WHITE)
            screen.blit(text, (72, 185 + i * 42))

        tip = SMALL_FONT.render('Score is saved to leaderboard.json', True, WHITE)
        screen.blit(tip, tip.get_rect(center=(WIDTH // 2, 445)))

        retry_btn.draw(screen)
        menu_btn.draw(screen)
        pygame.display.flip()



def main():
    settings = load_settings()

    while True:
        action = menu_screen()
        if action == 'quit':
            break

        if action == 'settings':
            settings = settings_screen(settings)
            continue

        if action == 'leaderboard':
            leaderboard_screen()
            continue

        if action == 'play':
            username = username_screen()
            if not username:
                continue

            while True:
                game = Game(screen, settings, username)
                result = game.run()
                add_score({
                    'name': result['name'],
                    'score': result['score'],
                    'distance': result['distance'],
                    'coins': result['coins'],
                })
                next_action = game_over_screen(result)
                if next_action == 'retry':
                    continue
                if next_action == 'quit':
                    pygame.quit()
                    sys.exit()
                break

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
