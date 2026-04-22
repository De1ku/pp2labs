import os
import pygame


class MusicPlayer:
    def __init__(self, folder):
        self.folder = folder
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.track_length = 0
        self.manual_stop = False

        self.load_playlist()

    def load_playlist(self):
        if not os.path.exists(self.folder):
            return

        for file_name in os.listdir(self.folder):
            if file_name.endswith(".mp3") or file_name.endswith(".wav") or file_name.endswith(".ogg"):
                self.playlist.append(file_name)

        self.playlist.sort()

    def play(self):
        if len(self.playlist) == 0:
            return

        path = os.path.join(self.folder, self.playlist[self.current_index])
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        self.is_playing = True
        self.manual_stop = False

        sound = pygame.mixer.Sound(path)
        self.track_length = sound.get_length()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.manual_stop = True
        self.track_length = 0

    def next_track(self):
        if len(self.playlist) == 0:
            return

        self.current_index += 1
        if self.current_index >= len(self.playlist):
            self.current_index = 0

        self.play()

    def previous_track(self):
        if len(self.playlist) == 0:
            return

        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1

        self.play()

    def get_current_name(self):
        if len(self.playlist) == 0:
            return "No track"
        return self.playlist[self.current_index]

    def get_progress(self):
        if not self.is_playing or self.track_length == 0:
            return "00:00", self.format_time(self.track_length), 0

        current_seconds = pygame.mixer.music.get_pos() / 1000

        if current_seconds < 0:
            current_seconds = 0

        progress = current_seconds / self.track_length
        if progress > 1:
            progress = 1

        return self.format_time(current_seconds), self.format_time(self.track_length), progress

    def format_time(self, seconds):
        total_seconds = int(seconds)
        minutes = total_seconds // 60
        sec = total_seconds % 60
        return f"{minutes:02}:{sec:02}"