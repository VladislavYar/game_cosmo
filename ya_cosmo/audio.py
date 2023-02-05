import pygame.mixer


class Audio():
    """Класс управления звуками и музыкой"""

    def __init__(self, ai_game):
        """Инициализирует настройки."""
        self.music_volume = ai_game.settings.volume_music
        self.effects_volume = ai_game.settings.volume_effects
        self.voice_volume = ai_game.settings.volume_voice
        pygame.mixer.music.set_volume(self.music_volume)

    def load_music_menu(self):
        # загрузка музыки меню
        pygame.mixer.music.load('sounds/menu.mp3')

    def start_music(self):
        pygame.mixer.music.play(-1)

    def volume_music(self, vol):
        pygame.mixer.music.set_volume(vol)

    def load_effects(self, filename):
        # загрузка эффектов
        effect = pygame.mixer.Sound(filename)
        effect.set_volume(self.effects_volume)
        return effect

    def load_voice(self, filename):
        # загрузка речи
        voice = pygame.mixer.Sound(filename)
        voice.set_volume(self.voice_volume)
        return voice

    def volume_effects(self, vol, effect):
        effect.set_volume(vol)

    def volume_voice(self, vol, voice):
        voice.set_volume(vol)

    def load_channel(self, id):
        return pygame.mixer.Channel(id)
