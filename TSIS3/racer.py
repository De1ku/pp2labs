import random
import sys
from pathlib import Path

import pygame

WIDTH = 400
HEIGHT = 600
LANES_X = [70, 155, 245, 330]
ROAD_LEFT = 25
ROAD_RIGHT = 375
ASSETS_DIR = Path(__file__).resolve().parent / 'assets'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 70, 70)
GREEN = (60, 180, 110)
BLUE = (70, 120, 220)
YELLOW = (240, 205, 75)
ORANGE = (255, 160, 60)
PURPLE = (155, 90, 220)
GRAY = (130, 130, 140)
DARK = (18, 18, 28)

CAR_TINTS = {
    'blue': (70, 130, 255),
    'red': (235, 85, 85),
    'green': (80, 210, 120),
    'yellow': (255, 215, 60),
}

DIFFICULTY = {
    'easy': {'speed': 5.5, 'finish': 1800, 'traffic_ms': 1600, 'hazard_ms': 1800},
    'normal': {'speed': 6.5, 'finish': 2400, 'traffic_ms': 1250, 'hazard_ms': 1500},
    'hard': {'speed': 7.5, 'finish': 3000, 'traffic_ms': 1000, 'hazard_ms': 1250},
}


def load_image(name, size=None):
    image = pygame.image.load(str(ASSETS_DIR / name)).convert_alpha()
    if size:
        image = pygame.transform.smoothscale(image, size)
    return image



def tint_image(image, color):
    tinted = image.copy()
    overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
    overlay.fill((*color, 90))
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name='blue'):
        super().__init__()
        base = load_image('Player.png', (44, 96))
        self.image = tint_image(base, CAR_TINTS.get(color_name, CAR_TINTS['blue']))
        self.rect = self.image.get_rect(center=(LANES_X[1], 520))
        self.lane = 1
        self.target_x = LANES_X[self.lane]

    def change_lane(self, direction):
        self.lane = max(0, min(len(LANES_X) - 1, self.lane + direction))
        self.target_x = LANES_X[self.lane]

    def update(self, dt, game):
        dx = self.target_x - self.rect.centerx
        if abs(dx) > 1:
            step = 500 * dt
            if abs(dx) <= step:
                self.rect.centerx = self.target_x
            else:
                self.rect.centerx += step if dx > 0 else -step


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, lane, speed_factor=1.0):
        super().__init__()
        self.image = load_image('Enemy.png', (44, 92))
        self.rect = self.image.get_rect(center=(LANES_X[lane], -70))
        self.lane = lane
        self.speed_factor = speed_factor

    def update(self, dt, game):
        self.rect.y += int(game.scroll_pixels_per_second * self.speed_factor * dt)
        if self.rect.top > HEIGHT + 30:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.base = load_image('Coin.png')
        self.lane = lane
        self.reset_random(-random.randint(60, 300))

    def reset_random(self, y):
        coin_types = [(1, 28), (2, 35), (5, 42)]
        self.value, size = random.choices(coin_types, weights=[70, 22, 8])[0]
        self.image = pygame.transform.smoothscale(self.base, (size, size))
        self.rect = self.image.get_rect(center=(LANES_X[self.lane], y))

    def update(self, dt, game):
        self.rect.y += int(game.scroll_pixels_per_second * dt)
        if self.rect.top > HEIGHT + 25:
            self.kill()


class Hazard(pygame.sprite.Sprite):
    def __init__(self, lane, kind, y=-80, direction=1):
        super().__init__()
        self.lane = lane
        self.kind = kind
        self.direction = direction
        self.move_timer = 0
        self.image = self.make_image(kind)
        self.rect = self.image.get_rect(center=(LANES_X[lane], y))
        self.deadly = kind in {'barrier', 'pothole', 'moving_barrier'}
        self.slow = kind in {'oil', 'speed_bump'}
        self.boost = kind == 'nitro_strip'

    def make_image(self, kind):
        if kind == 'barrier':
            surf = pygame.Surface((64, 26), pygame.SRCALPHA)
            pygame.draw.rect(surf, RED, (0, 0, 64, 26), border_radius=6)
            pygame.draw.rect(surf, WHITE, (0, 0, 64, 26), 2, border_radius=6)
        elif kind == 'moving_barrier':
            surf = pygame.Surface((74, 22), pygame.SRCALPHA)
            pygame.draw.rect(surf, ORANGE, (0, 0, 74, 22), border_radius=6)
            pygame.draw.rect(surf, BLACK, (0, 0, 74, 22), 2, border_radius=6)
        elif kind == 'pothole':
            surf = pygame.Surface((52, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, DARK, (0, 0, 52, 24))
            pygame.draw.ellipse(surf, GRAY, (3, 4, 46, 16), 2)
        elif kind == 'oil':
            surf = pygame.Surface((58, 28), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, BLACK, (0, 2, 58, 24))
            pygame.draw.ellipse(surf, (40, 40, 55), (5, 8, 40, 12))
        elif kind == 'speed_bump':
            surf = pygame.Surface((68, 18), pygame.SRCALPHA)
            pygame.draw.rect(surf, YELLOW, (0, 0, 68, 18), border_radius=8)
            for x in range(4, 68, 12):
                pygame.draw.line(surf, BLACK, (x, 3), (x, 15), 2)
        else:  # nitro_strip
            surf = pygame.Surface((56, 60), pygame.SRCALPHA)
            pygame.draw.rect(surf, BLUE, (10, 0, 36, 60), border_radius=8)
            for y in range(6, 55, 12):
                pygame.draw.rect(surf, WHITE, (18, y, 20, 6), border_radius=4)
        return surf

    def update(self, dt, game):
        self.rect.y += int(game.scroll_pixels_per_second * dt)
        if self.kind == 'moving_barrier':
            self.move_timer += dt
            if self.move_timer >= 0.35:
                self.move_timer = 0
                new_lane = self.lane + self.direction
                if new_lane < 0 or new_lane >= len(LANES_X):
                    self.direction *= -1
                    new_lane = self.lane + self.direction
                self.lane = new_lane
                self.rect.centerx = LANES_X[self.lane]
        if self.rect.top > HEIGHT + 40:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    COLORS = {'nitro': BLUE, 'shield': GREEN, 'repair': PURPLE}
    LABELS = {'nitro': 'N', 'shield': 'S', 'repair': 'R'}

    def __init__(self, lane, kind):
        super().__init__()
        self.kind = kind
        self.lane = lane
        self.image = self.make_image(kind)
        self.rect = self.image.get_rect(center=(LANES_X[lane], -70))
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5500

    def make_image(self, kind):
        surf = pygame.Surface((42, 42), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.COLORS[kind], (21, 21), 20)
        pygame.draw.circle(surf, WHITE, (21, 21), 20, 2)
        font = pygame.font.SysFont('Verdana', 24, bold=True)
        text = font.render(self.LABELS[kind], True, WHITE)
        surf.blit(text, text.get_rect(center=(21, 21)))
        return surf

    def update(self, dt, game):
        self.rect.y += int(game.scroll_pixels_per_second * dt)
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime or self.rect.top > HEIGHT + 25:
            self.kill()


class Game:
    def __init__(self, screen, settings, username):
        self.screen = screen
        self.settings = settings
        self.username = username or 'Player'
        self.clock = pygame.time.Clock()
        self.bg = load_image('AnimatedStreet.png', (WIDTH, HEIGHT))
        self.bg_y1 = 0
        self.bg_y2 = -HEIGHT
        self.player = Player(settings.get('car_color', 'blue'))

        self.all_sprites = pygame.sprite.Group(self.player)
        self.traffic = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.big_font = pygame.font.SysFont('Verdana', 28, bold=True)
        self.font = pygame.font.SysFont('Verdana', 20)
        self.small_font = pygame.font.SysFont('Verdana', 16)

        diff = DIFFICULTY.get(settings.get('difficulty', 'normal'), DIFFICULTY['normal'])
        self.base_speed = diff['speed']
        self.finish_distance = diff['finish']
        self.traffic_interval = diff['traffic_ms']
        self.hazard_interval = diff['hazard_ms']

        self.distance = 0.0
        self.coins_collected = 0
        self.power_bonus = 0
        self.running = True
        self.won = False
        self.reason = 'crash'

        self.active_power = None
        self.active_until = 0
        self.shield_ready = False
        self.slow_until = 0
        self.track_boost_until = 0

        self.scroll_pixels_per_second = 250
        self.last_traffic = 0
        self.last_hazard = 0
        self.last_powerup = 0
        self.last_coin = 0
        self.last_event = 0

        self.sound_enabled = bool(settings.get('sound', True))
        self.crash_sound = None
        self.music_loaded = False
        self._setup_audio()

    @property
    def score(self):
        return int(self.coins_collected * 10 + self.distance + self.power_bonus)

    @property
    def progress_level(self):
        return int(self.distance // 500)

    def _setup_audio(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.crash_sound = pygame.mixer.Sound(str(ASSETS_DIR / 'crash.wav'))
            pygame.mixer.music.load(str(ASSETS_DIR / 'background.wav'))
            self.music_loaded = True
            if self.sound_enabled:
                pygame.mixer.music.play(-1)
        except pygame.error:
            self.crash_sound = None
            self.music_loaded = False

    def stop_audio(self):
        if self.music_loaded:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass

    def current_speed(self):
        speed = self.base_speed + self.progress_level * 0.35
        now = pygame.time.get_ticks()
        if now < self.track_boost_until:
            speed += 2.0
        if self.active_power == 'nitro' and now < self.active_until:
            speed += 3.5
        if now < self.slow_until:
            speed = max(3.5, speed - 3)
        return speed

    def lane_free(self, lane, y, margin=120):
        for group in (self.traffic, self.coins, self.hazards, self.powerups):
            for sprite in group:
                sprite_lane = getattr(sprite, 'lane', None)
                if sprite_lane == lane and abs(sprite.rect.centery - y) < margin:
                    return False
        return True

    def spawn_coin(self):
        lane_choices = [lane for lane in range(4) if self.lane_free(lane, -80, 100)]
        if not lane_choices:
            return
        lane = random.choice(lane_choices)
        coin = Coin(lane)
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def spawn_traffic_car(self):
        lane_choices = [lane for lane in range(4) if self.lane_free(lane, -70, 130)]
        if not lane_choices:
            return
        # Понижаем шанс появления машины прямо в текущей полосе игрока,
        # чтобы избегать нечестных спавнов.
        if self.player.lane in lane_choices and len(lane_choices) > 1 and random.random() < 0.7:
            lane_choices.remove(self.player.lane)
        lane = random.choice(lane_choices)
        car = TrafficCar(lane, speed_factor=random.uniform(0.9, 1.15 + self.progress_level * 0.05))
        self.traffic.add(car)
        self.all_sprites.add(car)

    def spawn_hazard_row(self):
        safe_count = random.choice([1, 2])
        safe_lanes = set(random.sample(range(4), safe_count))

        # Если текущая полоса игрока не безопасна и безопасные полосы далеко,
        # добавляем рядом безопасный путь.
        if self.player.lane not in safe_lanes:
            nearest = min(safe_lanes, key=lambda lane: abs(lane - self.player.lane))
            if abs(nearest - self.player.lane) > 1:
                safe_lanes.add(max(0, min(3, self.player.lane + random.choice([-1, 1]))))

        kinds = ['barrier', 'pothole', 'oil']
        for lane in range(4):
            if lane in safe_lanes:
                continue
            kind = random.choices(kinds, weights=[40, 25, 35])[0]
            if self.lane_free(lane, -80, 100):
                hazard = Hazard(lane, kind)
                self.hazards.add(hazard)
                self.all_sprites.add(hazard)

    def spawn_road_event(self):
        event_kind = random.choice(['moving_barrier', 'speed_bump', 'nitro_strip'])
        lane_choices = [lane for lane in range(4) if self.lane_free(lane, -85, 130)]
        if not lane_choices:
            return
        lane = random.choice(lane_choices)
        hazard = Hazard(lane, event_kind, y=-90, direction=random.choice([-1, 1]))
        self.hazards.add(hazard)
        self.all_sprites.add(hazard)

    def spawn_powerup(self):
        # Держим на экране не более одного активного предмета одновременно.
        if len(self.powerups) > 0:
            return
        lane_choices = [lane for lane in range(4) if self.lane_free(lane, -90, 140)]
        if not lane_choices:
            return
        lane = random.choice(lane_choices)
        kind = random.choice(['nitro', 'shield', 'repair'])
        powerup = PowerUp(lane, kind)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def clear_nearest_obstacle(self):
        candidates = []
        for sprite in list(self.traffic) + list(self.hazards):
            if sprite.rect.centery < self.player.rect.centery + 80:
                candidates.append(sprite)
        if not candidates:
            return False
        nearest = min(candidates, key=lambda s: abs(s.rect.centery - self.player.rect.centery) + abs(s.rect.centerx - self.player.rect.centerx))
        nearest.kill()
        return True

    def handle_collisions(self):
        # Монеты
        for coin in pygame.sprite.spritecollide(self.player, self.coins, dokill=True):
            self.coins_collected += coin.value

        # Power-ups
        for powerup in pygame.sprite.spritecollide(self.player, self.powerups, dokill=True):
            if powerup.kind == 'repair':
                cleared = self.clear_nearest_obstacle()
                self.power_bonus += 40 if cleared else 20
            elif powerup.kind == 'nitro':
                self.active_power = 'nitro'
                self.active_until = pygame.time.get_ticks() + 4000
                self.shield_ready = False
                self.power_bonus += 25
            elif powerup.kind == 'shield':
                self.active_power = 'shield'
                self.active_until = 0
                self.shield_ready = True
                self.power_bonus += 25

        # Опасные препятствия и трафик
        deadly_hits = pygame.sprite.spritecollide(self.player, self.traffic, dokill=False)
        deadly_hits += [h for h in pygame.sprite.spritecollide(self.player, self.hazards, dokill=False) if h.deadly]
        if deadly_hits:
            if self.shield_ready:
                self.shield_ready = False
                self.active_power = None
                deadly_hits[0].kill()
                self.power_bonus += 10
            else:
                self.reason = 'crash'
                self.running = False
                if self.crash_sound and self.sound_enabled:
                    try:
                        self.crash_sound.play()
                    except pygame.error:
                        pass
                return

        # Замедляющие зоны
        for hazard in pygame.sprite.spritecollide(self.player, self.hazards, dokill=False):
            if hazard.slow:
                self.slow_until = pygame.time.get_ticks() + 1600
                hazard.kill()
            elif hazard.boost:
                self.track_boost_until = pygame.time.get_ticks() + 2200
                self.power_bonus += 10
                hazard.kill()

    def update_spawn_timers(self, now):
        traffic_interval = max(450, self.traffic_interval - self.progress_level * 70)
        hazard_interval = max(700, self.hazard_interval - self.progress_level * 60)
        powerup_interval = max(5000, 7000 - self.progress_level * 250)
        coin_interval = 900
        event_interval = max(1800, 3200 - self.progress_level * 100)

        if now - self.last_coin >= coin_interval:
            self.spawn_coin()
            self.last_coin = now
        if now - self.last_traffic >= traffic_interval:
            self.spawn_traffic_car()
            self.last_traffic = now
        if now - self.last_hazard >= hazard_interval:
            self.spawn_hazard_row()
            self.last_hazard = now
        if now - self.last_event >= event_interval:
            self.spawn_road_event()
            self.last_event = now
        if now - self.last_powerup >= powerup_interval:
            self.spawn_powerup()
            self.last_powerup = now

    def update(self, dt):
        now = pygame.time.get_ticks()
        if self.active_power == 'nitro' and now >= self.active_until:
            self.active_power = None
        self.scroll_pixels_per_second = 185 + self.current_speed() * 18

        self.bg_y1 += self.scroll_pixels_per_second * dt
        self.bg_y2 += self.scroll_pixels_per_second * dt
        if self.bg_y1 >= HEIGHT:
            self.bg_y1 = self.bg_y2 - HEIGHT
        if self.bg_y2 >= HEIGHT:
            self.bg_y2 = self.bg_y1 - HEIGHT

        self.distance += self.current_speed() * 8.5 * dt
        self.update_spawn_timers(now)
        self.all_sprites.update(dt, self)
        self.handle_collisions()

        if self.distance >= self.finish_distance:
            self.won = True
            self.reason = 'finish'
            self.power_bonus += 50
            self.running = False

    def draw_lane_guides(self):
        # Простая визуализация полос дороги.
        for x in [112, 200, 288]:
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT), 3)
        pygame.draw.rect(self.screen, WHITE, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT), 4)

    def draw_hud(self):
        panel = pygame.Rect(8, 8, WIDTH - 16, 92)
        pygame.draw.rect(self.screen, (0, 0, 0, 140), panel, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, panel, 2, border_radius=12)

        lines = [
            f'Score: {self.score}',
            f'Coins: {self.coins_collected}',
            f'Distance: {int(self.distance)} / {self.finish_distance}',
            f'Remaining: {max(0, int(self.finish_distance - self.distance))}',
        ]
        for i, line in enumerate(lines):
            surf = self.small_font.render(line, True, WHITE)
            self.screen.blit(surf, (18, 15 + i * 18))

        now = pygame.time.get_ticks()
        if self.active_power == 'nitro':
            remaining = max(0, (self.active_until - now) / 1000)
            status = f'Active power: Nitro ({remaining:.1f}s)'
        elif self.active_power == 'shield' and self.shield_ready:
            status = 'Active power: Shield (until hit)'
        else:
            status = 'Active power: None'
        status_surf = self.small_font.render(status, True, YELLOW)
        self.screen.blit(status_surf, (185, 15))

        diff_surf = self.small_font.render(
            f'Difficulty: {self.settings.get("difficulty", "normal").title()} | Level: {self.progress_level + 1}',
            True,
            WHITE,
        )
        self.screen.blit(diff_surf, (185, 35))

        hint = self.small_font.render('Power-ups: N=nitro, S=shield, R=repair', True, WHITE)
        self.screen.blit(hint, (185, 55))

    def draw(self):
        self.screen.blit(self.bg, (0, self.bg_y1))
        self.screen.blit(self.bg, (0, self.bg_y2))
        self.draw_lane_guides()
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_audio()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.change_lane(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.player.change_lane(1)

            self.update(dt)
            self.draw()

        self.stop_audio()
        return {
            'name': self.username,
            'score': self.score,
            'distance': int(self.distance),
            'coins': self.coins_collected,
            'won': self.won,
            'reason': self.reason,
        }
