import pygame
from pygame.sprite import Sprite
from random import randint


class Alien(Sprite):
    """Класс создающий пришельца."""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задает его начальную позицию."""
        Sprite.__init__(self)
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # загрузка изображения пришельца
        aliens = ['images/alien_1.png', 'images/alien_2.png']

        self.image = pygame.image.load(aliens[randint(0, 1)])
        # апскейлит изображение под разрешение экрана
        # и назначение отрибута rect
        self._scale_images()

        # каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # сохранение горизонтальной позиции пришельца в вещественном виде
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def _scale_images(self):
        """Апскейл изображение под разрешение экрана."""
        if self.settings.screen_width == 2560:
            scale = 1
        if self.settings.screen_width == 1920:
            scale = 1.33
        elif self.settings.screen_width == 1366:
            scale = 1.874
        elif self.settings.screen_width == 1600:
            scale = 1.6
        elif self.settings.screen_width == 1280:
            scale = 2
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width / scale
        self.rect.height = self.rect.height / scale
        self.image = pygame.transform.scale(self.image,
                                            (self.rect.width,
                                             self.rect.height))
