import pygame

from methods import scale_images


TICK_ANIM = 230


class Planet():
    """Класс для создания планет."""

    def __init__(self, ai_game, adress_sprite, quantity):
        """Инициализирует планету и задает ей первоначальное положение."""
        self.screen = ai_game.screen
        coef_screen = ai_game.settings.coef_screen
        self.screen_rect = ai_game.screen.get_rect()
        self.flag_sprite_change = 0
        self.fps = ai_game.FPS
        self.i = 0

        # загружает изображение планеты и получает прямоугольник
        self.animation_set = [
            pygame.image.load(f'images/planets/{adress_sprite}/{i+1}.png')
            for i in range(0, quantity)]

        # апскейлит спрайтов под разрешение экрана
        self.animation_set = scale_images(coef_screen, self.animation_set)

        self.rect = self.animation_set[0].get_rect()

    def draw(self):
        """Отрисовка анимации планеты."""
        self.flag_sprite_change += self.fps.get_time()

        self.screen.blit(self.animation_set[self.i],
                         self.rect)

        if self.flag_sprite_change >= TICK_ANIM:
            self.i += 1
            if self.i == len(self.animation_set) - 1:
                self.i = 0
            self.flag_sprite_change = 0
