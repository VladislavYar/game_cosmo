import pygame
import pygame.font


DEL_COEF_SHIFT = 15


class Button():
    """Класс создания кнопок."""

    def __init__(self, ai_game, text):
        """Инициализирует атрибуты кнопки."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.text = text
        self.active = True
        font = ai_game.button_menu
        # назначение размеров и свойств кнопок
        self.width = int(self.screen_rect.width / 5)
        self.height = int(self.screen_rect.height / 20)
        self.button_color = (9, 60, 149)
        self.text_color = (12, 149, 207)
        self.text_color_not_active = (85, 85, 85)
        self.text_color_run_game = (255, 255, 255)
        self.size_text = int(self.screen_rect.width / 80)
        self.font = pygame.font.Font(font, self.size_text)

        # создание слоя наложения
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((9, 60, 149))
        self.surf.set_alpha(50)

        # сообщение кнопки создается только один раз
        if text == 'Новая игра':
            self._prep_midtop(self.text)
        elif text == 'Рекорды':
            self._prep_top(self.text)
        elif text == 'Настройки':
            self._prep_middle(self.text)
        elif text == 'Выход':
            self._prep_bottom(self.text),
        elif text == 'Легко':
            self._prep_midtop(self.text)
        elif text == 'Нормально':
            self._prep_middle(self.text)
        elif text == 'Тяжело':
            self._prep_bottom(self.text)
        elif text == 'Назад':
            self._prep_lower_right_corner(self.text)
        elif text == 'Сохранить' or text == 'Запуск':
            self._prep_save_sattings(self.text)
        elif text == 'Сбросить':
            self._prep_lower_left_corner(self.text)
        elif text == 'Пауза':
            self._prep_pause(self.text)

    def _prep_midtop(self, text):
        """Создание текста и прямоугольника с выравниванием по центру."""
        # построение объекта rect кнопки и выравнивание по центру экрана
        # выше кнопки _prep_middle
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y -= self.screen_rect.width / DEL_COEF_SHIFT

        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_top(self, text):
        """Создание текста и прямоугольника с выравниванием по центру."""
        # построение объекта rect кнопки и выравнивание по центру экрана
        # ниже кнопки _prep_midtop
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y -= self.screen_rect.width / 30

        # преобразует text в прямоугольник и выравнивает текста по центру
        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_middle(self, text):
        """Создание текста и прямоугольника с выравниванием по центру."""
        # построение объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # преобразует text в прямоугольник и выравнивает текста по центру
        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_bottom(self, text):
        """Создание текста и прямоугольника с выравниванием по центру."""
        # построение объекта rect кнопки и выравнивание по центру экрана
        # ниже кнопки _prep_middle
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += self.screen_rect.width / DEL_COEF_SHIFT

        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_lower_right_corner(self, text):
        """
        Создание текста и прямоугольника с
        выравниванием по правому нижему углу.
        """
        # построение объекта rect кнопки и выравнивание по правому углу
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomright = self.screen_rect.bottomright
        self.rect.y -= self.screen_rect.width / DEL_COEF_SHIFT
        self.rect.x -= self.screen_rect.width / DEL_COEF_SHIFT

        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_lower_left_corner(self, text):
        """
        Создание текста и прямоугольника с
        выравниванием по левому нижему углу.
        """
        # построение объекта rect кнопки и выравнивание по левому углу
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.rect.y -= self.screen_rect.width / DEL_COEF_SHIFT
        self.rect.x += self.screen_rect.width / DEL_COEF_SHIFT

        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_save_sattings(self, text):
        """Создание текста и прямоугольника с выравниванием по центру."""
        # построение объекта rect кнопки и выравнивание по центру экрана
        # ниже кнопки сложности настроек
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y -= (self.screen_rect.width /
                        DEL_COEF_SHIFT - 6 * self.height)

        self.msg_image = self.font.render(text, True,
                                          self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def _prep_pause(self, text):
        """Создание текста и прямоугольника с выравниванием по центру."""
        # построение объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.msg_image = self.font.render(text, True,
                                          self.text_color_run_game)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def hover_display(self):
        """
        Изменение цвета кнопки при наведении курсора
        и при его отводе.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.active:
            self.button_color = (0, 150, 150)
            self.msg_image = self.font.render(self.text, True,
                                              self.text_color)
        elif self.active is False:
            self.msg_image = self.font.render(self.text, True,
                                              self.text_color_not_active)
        else:
            self.button_color = (9, 60, 149)
            self.msg_image = self.font.render(self.text, True,
                                              self.text_color)

    def activate_deactevate_button(self, active):
        """Активация, деактивация кнопки."""
        self.active = active
        if self.active:
            self.button_color = (9, 60, 149)
            self.msg_image = self.font.render(self.text, True,
                                              self.text_color)
        else:
            self.button_color = (140, 140, 140)
            self.msg_image = self.font.render(self.text, True,
                                              self.text_color)

    def draw(self):
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(self.surf, (self.rect.topleft))
        pygame.draw.rect(self.screen, self.button_color, self.rect, 2)

    def draw_text(self):
        # отображение текста
        self.screen.blit(self.msg_image, self.msg_image_rect)
