import pygame
from random import randint

from methods import scale_images


STAR_COLOR = [(250, 250, 250), (50, 0, 0), (0, 50, 0),
              (200, 200, 200), (0, 100, 150), (100, 100, 100)]


class Star():
    """Класс создающий звезду."""

    def __init__(self, ai_game):
        """Инициализирует зведу и задает его начальную позицию."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.fps = ai_game.FPS
        self.flag = randint(0, 2)
        self.reverse = False
        self.i = 0

        self.color = STAR_COLOR[randint(0, 5)]

        self.size_star = int(self.screen_rect.width // randint(900, 1000))

        self.rect = pygame.Rect(0, 0, self.size_star,
                                self.size_star)

        self.rect.x = randint(1, self.screen_rect.width)
        self.rect.y = randint(1, self.screen_rect.height)

        self.animation_set_star = [(pygame.Rect(0, 0, (self.size_star
                                    + (i // 6)),
                                    (self.size_star + (i // 6))))
                                   for i in range(0, 61)]

        self.flag_rect = False

        self._correct_animation_rect()

    def draw(self):
        # пересчёт положения анимаций звезды при изменении rect
        if self.flag_rect:
            self.flag_rect = False
            self._correct_animation_rect()

        # вывод звезды в меню и её анимация
        if self.flag == 0:
            self.end_animation = 0
        else:
            self.end_animation = -1

        if self.i != self.end_animation:
            if self.i <= 60 and not self.reverse:
                self.screen.fill(self.color,
                                 self.animation_set_star[int(self.i / 2)])
                flag_sprite_change = self.fps.get_time() / 20
                self.i += flag_sprite_change
            else:
                self.reverse = True
                self.screen.fill(self.color,
                                 self.animation_set_star[int(self.i / 2)])

        if self.i >= 1 and self.reverse:
            self.screen.fill(self.color,
                             self.animation_set_star[int(self.i / 2)])
            flag_sprite_change = self.fps.get_time() / 20
            self.i -= flag_sprite_change
        else:
            self.reverse = False
            self.screen.fill(self.color, self.rect)

    def _correct_animation_rect(self):
        """Передвижение всех спрайтов из анимаций звезды."""
        for star_animation_rect in self.animation_set_star:
            star_animation_rect.center = self.rect.center

    def shift_start_behind_screen(self, ai_game) -> None:
        """Сдвиг звезды за экраном."""
        screen_rect = ai_game.screen.get_rect()
        width = screen_rect.width
        height = screen_rect.height
        x = self.rect.x
        y = self.rect.y
        rand_shift = int(width // randint(900, 1000))
        if x < 0:
            self.color = STAR_COLOR[randint(0, 5)]
            self.rect.x = width + x - rand_shift
        if y < 0:
            self.color = STAR_COLOR[randint(0, 5)]
            self.rect.y = height + y - rand_shift
        if x > width:
            self.color = STAR_COLOR[randint(0, 5)]
            self.rect.x = width - x + rand_shift
        if y > height:
            self.color = STAR_COLOR[randint(0, 5)]
            self.rect.y = height - y + rand_shift


class Logo():
    """Класс для создания логотипа."""

    def __init__(self, ai_game):
        """Инициализирует логотип и задает ему первоначальное положение."""
        self.screen = ai_game.screen
        coef_screen = ai_game.settings.coef_screen
        self.screen_rect = ai_game.screen.get_rect()

        # загружает изображение логотип и получает прямоугольник
        self.image = pygame.image.load('images/logo.png')

        # апскейлит изображение под разрешение экрана
        # и назначение отрибута rect
        self.image = scale_images(coef_screen, self.image)

        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def draw(self):
        """Рисует логотип в текущей позиции."""
        self.screen.blit(self.image, self.rect)


class Comet():
    """Класс создающий комету."""

    def __init__(self, ai_game):
        """Инициализирует комету."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.settings_fps = self.settings.setting_fps
        self.fps = ai_game.FPS
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        self.flag = randint(0, 7)
        self.flag_fly = False
        self.comet_color = (200, 200, 200)
        size = randint(20, 100)
        self.i = 0
        self.j = 0

        # просчёт скорости с зависимостью от FPS
        if int(self.fps.get_fps()):
            self.speed = randint(2000, 2500) / int(self.fps.get_fps())
        else:
            self.speed = randint(2000, 2500) / self.settings_fps

        # максимальное количество FPS на полёт кометы
        self.fps_max_fly = screen_width * 2 / self.speed

        if self.flag == 0:
            self.beginning_1 = randint(screen_width * (-1) // 3, 0)
            self.beginning_2 = randint(screen_height * (-1) // 2, 0)

            self.end_1 = self.beginning_1 - size
            self.end_2 = self.beginning_2 - size

        if self.flag == 1:
            self.beginning_1 = randint(screen_width, screen_width
                                       + screen_width // 3)
            self.beginning_2 = randint(screen_height, screen_height
                                       + screen_height // 3)

            self.end_1 = self.beginning_1 + size
            self.end_2 = self.beginning_2 + size

        if self.flag == 2:
            self.beginning_1 = randint(0, screen_width)
            self.beginning_2 = randint(screen_height,
                                       screen_height + screen_height // 3)

            self.end_1 = self.beginning_1
            self.end_2 = self.beginning_2 + size

        if self.flag == 3:
            self.beginning_1 = randint(0, screen_width)
            self.beginning_2 = randint(screen_height * (-1), 0)

            self.end_1 = self.beginning_1
            self.end_2 = self.beginning_2 - size

        if self.flag == 4:
            self.beginning_1 = randint(screen_width // 4,
                                       screen_width - screen_width // 3)
            self.beginning_2 = randint(screen_height * (-1) // 2, 0)

            self.end_1 = self.beginning_1 + size
            self.end_2 = self.beginning_2 - size

        if self.flag == 5:
            self.beginning_1 = randint(screen_width * (-1) // 2,
                                       screen_width * (-1) // 3)
            self.beginning_2 = randint(30, screen_height - 50)

            self.end_1 = self.beginning_1 - size
            self.end_2 = self.beginning_2

        if self.flag == 6:
            self.beginning_1 = randint(screen_width + (screen_width // 3),
                                       screen_width + (screen_width // 2))
            self.beginning_2 = randint(30, screen_height - 50)

            self.end_1 = self.beginning_1 + size
            self.end_2 = self.beginning_2

        if self.flag == 7:
            self.beginning_1 = randint(screen_width + (screen_width // 3),
                                       screen_width + (screen_width // 2))
            self.beginning_2 = randint(screen_height * (-1) // 2,
                                       screen_height * (-1) // 3)

            self.end_1 = self.beginning_1 + size
            self.end_2 = self.beginning_2 - size

    def draw(self):
        # вывод кометы и её анимация
        if self.j < self.fps_max_fly and self.flag_fly:
            self.j += 1

            if self.flag == 0:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1 + self.i,
                                  self.beginning_2 + self.i),
                                 (self.end_1 + self.i,
                                  self.end_2 + self.i))

            if self.flag == 1:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1 - self.i,
                                  self.beginning_2 - self.i),
                                 (self.end_1 - self.i,
                                  self.end_2 - self.i))

            if self.flag == 2:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1,
                                  self.beginning_2 - self.i),
                                 (self.end_1,
                                  self.end_2 - self.i))

            if self.flag == 3:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1,
                                  self.beginning_2 + self.i),
                                 (self.end_1,
                                  self.end_2 + self.i))

            if self.flag == 4:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1 - self.i,
                                  self.beginning_2 + self.i),
                                 (self.end_1 - self.i,
                                  self.end_2 + self.i))

            if self.flag == 5:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1 + self.i,
                                  self.beginning_2),
                                 (self.end_1 + self.i,
                                  self.end_2))

            if self.flag == 6:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1 - self.i,
                                  self.beginning_2),
                                 (self.end_1 - self.i,
                                  self.end_2))
            if self.flag == 7:
                pygame.draw.line(self.screen, self.comet_color,
                                 (self.beginning_1 - self.i,
                                  self.beginning_2 + self.i),
                                 (self.end_1 - self.i,
                                  self.end_2 + self.i))

            self.i += self.speed
        else:
            self.flag_fly = False
