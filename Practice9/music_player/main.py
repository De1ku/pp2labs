import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font_big = pygame.font.SysFont("arial", 36, bold=True)
font = pygame.font.SysFont("arial", 26)
small_font = pygame.font.SysFont("arial", 22)

clock = pygame.time.Clock()
running = True

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

player = MusicPlayer("music")


def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == SONG_END:
            if not player.manual_stop:
                player.next_track()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()

    screen.fill((235, 235, 245))

    draw_text("Music Player", font_big, (20, 20, 20), 30, 20)

    draw_text("Controls:", font, (30, 30, 30), 30, 90)
    draw_text("P - Play", small_font, (50, 50, 50), 50, 130)
    draw_text("S - Stop", small_font, (50, 50, 50), 50, 165)
    draw_text("N - Next", small_font, (50, 50, 50), 50, 200)
    draw_text("B - Previous", small_font, (50, 50, 50), 50, 235)
    draw_text("Q - Quit", small_font, (50, 50, 50), 50, 270)

    draw_text("Current track:", font, (30, 30, 30), 30, 340)
    draw_text(player.get_current_name(), font, (0, 70, 160), 30, 380)

    status_text = "Status: Playing" if player.is_playing else "Status: Stopped"
    draw_text(status_text, font, (30, 30, 30), 30, 430)

    current_time, total_time, progress = player.get_progress()

    pygame.draw.rect(screen, (180, 180, 180), (30, 480, 500, 25))
    pygame.draw.rect(screen, (70, 130, 220), (30, 480, int(500 * progress), 25))
    pygame.draw.rect(screen, (40, 40, 40), (30, 480, 500, 25), 2)

    draw_text(f"{current_time} / {total_time}", small_font, (30, 30, 30), 550, 478)

    draw_text("Playlist:", font, (30, 30, 30), 650, 90)

    y = 130
    for i, track in enumerate(player.playlist):
        color = (200, 50, 50) if i == player.current_index else (50, 50, 50)
        draw_text(f"{i + 1}. {track}", small_font, color, 650, y)
        y += 35

    if len(player.playlist) == 0:
        draw_text("No music files found in /music", small_font, (180, 0, 0), 30, 540)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()