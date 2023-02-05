import pygame
import pygame.font


class Button():
    """Класс создания выжвижного списка кнопок."""

    def __init__(self, ai_game, text, name, i, width):
        """Инициализирует атрибуты кнопки выдвижного списка."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.font_button = ai_game.button_menu
        self.font_dropdown = ai_game.button_dropdown
        self.click_button = False
        self.open_dropdown = False
        self.active = True
        self.name = name
        self.text = text
        self.number = i

        # назначение размеров и свойств кнопок
        self.width = int(self.screen_rect.width / 5)
        self.height = int(self.screen_rect.height / 20)
        self.button_color = (0, 150, 150)
        self.button_color_click = (0, 150, 150)
        self.text_color = (12, 149, 207)
        self.text_color_not_active = (85, 85, 85)
        self.text_color_not_col = (85, 130, 130)
        self.text_color_dropdown = (0, 200, 200)
        self.text_color_dropdown_col = ((0, 150, 150))

        self.size_text = int(self.screen_rect.width / 80)
        self.font_dropdown = pygame.font.Font(self.font_dropdown,
                                              self.size_text)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y -= self.screen_rect.width / width

        # преобразует text в прямоугольник и выравнивает текста по центру
        self.msg_image = self.font_dropdown.render(text, True,
                                                   self.text_color_not_col)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

        # создание слоев наложения
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((9, 60, 149))
        self.surf.set_alpha(50)

        self.surf_not_active = pygame.Surface((self.width, self.height))
        self.surf_not_active.fill((200, 200, 200))
        self.surf_not_active.set_alpha(50)

        self.surf_click = pygame.Surface((self.width, self.height))
        self.surf_click.fill((0, 150, 150))
        self.surf_click.set_alpha(50)

        # создание заготовки для заголовка списка
        if self.number == 1:
            self.button_color_name = (9, 60, 149)
            self.font_name = pygame.font.Font(self.font_button, self.size_text)
            self.rect_name = pygame.Rect(0, 0, self.width, self.height)
            self.rect_name.center = self.screen_rect.center
            self.rect_name.y -= self.screen_rect.width / width
            self.msg_image_name = (
                self.font_name.render(self.name, True,
                                      self.text_color))
            self.msg_image_name_rect = self.msg_image_name.get_rect()
            self.msg_image_name_rect.midbottom = self.rect_name.midbottom

    def open_close_dropdown(self):
        """ Открывает список кнопок и возвращает состояние."""
        self.rect.y = self.rect.y + self.number * self.height
        self.msg_image_rect.center = self.rect.center
        if self.number > 0:
            self.number = self.number * (-1)
            self.open_dropdown = True
            return self.open_dropdown
        self.number = self.number * (-1)
        self.open_dropdown = False
        return self.open_dropdown

    def draw(self):
        # отображение кнопки и вывод сообщения
        if self.open_dropdown:
            pygame.draw.rect(self.screen, self.button_color, self.rect, 1)

            self.screen.blit(self.surf_click,
                             (self.rect.topleft))

            if not self.active:
                self.screen.blit(self.surf_not_active,
                                 (self.rect.topleft))
            elif self.click_button:
                self.screen.blit(self.surf_click,
                                 (self.rect.topleft))

            self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_name(self):
        # отображение названия списка
        pygame.draw.rect(self.screen, self.button_color_name, self.rect_name,
                         2)
        self.screen.blit(self.surf, (self.rect_name.topleft))
        self.screen.blit(self.msg_image_name, self.msg_image_name_rect)

    def collidepoint_mouse_pos(self):
        # проверка нажатия на кнопку
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.active:
            self.button_color = self.button_color_click
            self.click_button = True
            return [self.text, self.number, self.click_button]

    def color_reset(self, flag=(-1)):
        # возврат к базовому цвету кнопок и сброс флага
        if flag != self.number and self.active:
            self.click_button = False

    def hover_display_name(self):
        """
        Изменение цвета заголовка при наведении курсора
        и при его отводе.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_name.collidepoint(mouse_pos):
            self.button_color_name = (0, 150, 150)
        else:
            self.button_color_name = (9, 60, 149)

    def hover_display_button(self):
        """
        Изменение цвета кнопки списка при наведении курсора
        и при его отводе.
        """
        mouse_pos = pygame.mouse.get_pos()
        if (self.rect.collidepoint(mouse_pos) and self.click_button is False
           and self.active):
            self.surf_click.fill((0, 150, 150))
            self.msg_image = (
                self.font_dropdown.render(self.text, True,
                                          self.text_color_dropdown_col))
            return True
        elif self.click_button:
            # изменение цвета текста при нажатии на кнопку
            self.msg_image = (
                        self.font_dropdown.render(self.text, True,
                                                  self.text_color_dropdown))
            return True
        elif self.active is False:
            # не изменяет цвет, если соответствует
            # сохранённому значению
            return
        else:
            self.msg_image = (
                self.font_dropdown.render(self.text, True,
                                          self.text_color_not_col))
            self.surf_click.fill((0, 0, 0))
            return False

    def validation_validity(self):
        """Проверка совпадения."""
        settings = self.ai_game.settings
        data_verification = (f'{settings.screen_width}:'
                             f'{settings.screen_height}')
        if data_verification == self.text:
            self.active = False
            self._inactive_button(self.active)

    def _inactive_button(self, active):
        """Активация, деактивация кнопки."""
        if active:
            self.button_color = (0, 150, 150)
            self.msg_image = (
                        self.font_dropdown.render(self.text, True,
                                                  self.text_color_not_col))
        else:
            self.button_color = (140, 140, 140)
            self.msg_image = (
                self.font_dropdown.render(self.text, True,
                                          self.text_color_not_active))


class Slider():
    """Класс создания выжвижного списка ползунов."""

    def __init__(self, ai_game, text, name, i, width, volume, number_buttons):
        """Инициализирует атрибуты кнопки."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.mouse_slider_control = False
        self.font_button = ai_game.button_menu
        self.font_dropdown = ai_game.button_dropdown
        self.old_mouse_pos = [0, 0]
        self.volume = volume
        self.old_volume = self.volume
        self.name = name
        self.text = text
        self.number = i
        self.flag = False
        self.open_slider = False

        # назначение размеров и свойств кнопок
        self.width_button = int(self.screen_rect.width / 5)
        self.height_button = int(self.screen_rect.height / 20)
        self.button_color = (100, 150, 150)
        self.rect_button = pygame.Rect(0, 0, self.width_button,
                                       self.height_button)
        self.rect_button.center = self.screen_rect.center
        self.rect_button.y -= self.screen_rect.width / width

        self.width_footing = int(self.screen_rect.width / 5.5)
        self.height_footing = int(self.screen_rect.height / 33)
        self.footing_color = (0, 150, 150)
        self.rect_footing = pygame.Rect(0, 0, self.width_footing,
                                        self.height_footing)
        self.rect_footing.center = self.rect_button.center
        self.percentages_footing = self.width_footing / 100

        self.width_slider = int(self.screen_rect.width / 100)
        self.height_slider = int(self.screen_rect.height / 33)
        self.slider_color = (0, 0, 150)
        self.rect_slider = pygame.Rect(0, 0, self.width_slider,
                                       self.height_slider)
        self.rect_slider.center = self.rect_footing.center
        self._slider_position()

        # создание текста
        self.text_color = (85, 85, 85)
        self.size_text = int(self.screen_rect.width / 80)
        self.font_dropdown = pygame.font.Font(self.font_dropdown,
                                              self.size_text)
        self.msg_image = self.font_dropdown.render(self.text, True,
                                                   self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect_button.center

        # создание заготовки для заголовка списка и цветную границу выбора
        if self.number == 1:
            self.text_color_name = (12, 149, 207)
            self.button_color_name = (9, 60, 149)
            self.font_name = pygame.font.Font(self.font_button,
                                              self.size_text)
            self.rect_name = pygame.Rect(0, 0, self.width_button,
                                         self.height_button)
            self.rect_name.center = self.screen_rect.center
            self.rect_name.y -= self.screen_rect.width / width
            self.msg_image_name = self.font_name.render(self.name, True,
                                                        self.text_color_name)
            self.msg_image_name_rect = self.msg_image_name.get_rect()
            self.msg_image_name_rect.midbottom = self.rect_name.midbottom

            self.button_color_border = (0, 150, 150)
            self.rect_border = pygame.Rect(0, 0, self.width_button,
                                           (self.height_button
                                            * number_buttons))

        # создание слоя наложения
        self.surf = pygame.Surface((self.width_button, self.height_button))
        self.surf.fill((9, 60, 149))
        self.surf.set_alpha(50)

        width_volume = (self.rect_slider.left - self.rect_footing.left) + 1
        size_surf_volume = (width_volume, self.height_footing)
        self.surf_volume = pygame.Surface(size_surf_volume)
        self.surf_volume.fill((100, 150, 150))
        self.surf_volume.set_alpha(50)

    def draw(self):
        if self.open_slider:
            pygame.draw.rect(self.screen, self.footing_color,
                             self.rect_footing, 1)
            self.screen.blit(self.msg_image, self.msg_image_rect)
            self.screen.blit(self.surf_volume, (self.rect_footing.topleft))
            pygame.draw.rect(self.screen, self.slider_color, self.rect_slider,
                             1)
            if self.number == -1:
                self.rect_border.topleft = self.rect_button.topleft
                pygame.draw.rect(self.screen, self.button_color_border,
                                 self.rect_border, 1)

    def draw_name(self):

        pygame.draw.rect(self.screen, self.button_color_name, self.rect_name,
                         2)
        self.screen.blit(self.surf, (self.rect_name.topleft))
        self.screen.blit(self.msg_image_name, self.msg_image_name_rect)

    def open_close_dropdown(self):
        """ Открывает список кнопок и возвращает состояние."""
        self.rect_button.y = (self.rect_button.y + self.number
                              * self.height_button)
        self.rect_footing.y = (self.rect_footing.y + self.number
                               * self.height_button)
        self.rect_slider.y = (self.rect_slider.y + self.number
                              * self.height_button)
        self.msg_image_rect.y = (self.msg_image_rect.y + self.number
                                 * self.height_button)
        if self.number > 0:
            self.number = self.number * (-1)
            self.open_slider = True
            return self.open_slider
        else:
            self.number = self.number * (-1)
            self.open_slider = False
            return self.open_slider

    def hover_display_name(self):
        """
        Изменение цвета заголовка при наведении курсора
        и при его отводе.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_name.collidepoint(mouse_pos):
            self.button_color_name = (0, 150, 150)
            self.msg_image_name = self.font_name.render(self.name, True,
                                                        self.text_color_name)
        else:
            self.button_color_name = (9, 60, 149)
            self.msg_image_name = self.font_name.render(self.name, True,
                                                        self.text_color_name)

    def slider_control(self):
        """Логика управления ползуном."""
        if self.flag:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] > self.old_mouse_pos[0] and
               self.rect_slider.right <= self.rect_footing.right):
                self.rect_slider.centerx = (self.rect_slider.centerx
                                            + mouse_pos[0]
                                            - self.old_mouse_pos[0])

            elif (mouse_pos[0] < self.old_mouse_pos[0] and
                  self.rect_slider.left >= self.rect_footing.left):
                self.rect_slider.centerx = (self.rect_slider.centerx
                                            + mouse_pos[0]
                                            - self.old_mouse_pos[0])

            if self.rect_slider.left < self.rect_footing.left:
                self.rect_slider.left = self.rect_footing.left

            elif self.rect_slider.right > self.rect_footing.right:
                self.rect_slider.right = self.rect_footing.right
            self.old_mouse_pos = mouse_pos

            self.surf_slider_control()

            # просчёт значения громкости
            self.old_volume = self.volume
            self.volume = ((self.rect_slider.left -
                            self.rect_footing.left) /
                           self.percentages_footing / 100)

    def surf_slider_control(self):
        """Обновление слоя наложения для закрашивания уровня громкости."""
        width_volume = (self.rect_slider.left - self.rect_footing.left) + 1
        size_surf_volume = (width_volume, self.height_footing)
        self.surf_volume = pygame.transform.scale(self.surf_volume,
                                                  size_surf_volume)

    def slider_control_active(self):
        """Активация перемещения."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_footing.collidepoint(mouse_pos):
            self.old_mouse_pos = mouse_pos
            self.flag = True

    def slider_control_deactive(self):
        """Деактивация перемещения."""
        mouse_pos = pygame.mouse.get_pos()
        self.old_mouse_pos = mouse_pos
        self.flag = False

    def _slider_position(self):
        """Просчёт положения ползунка."""
        self.rect_slider.left = (self.volume *
                                 self.width_footing +
                                 self.rect_footing.left)

    def slider_reset_position(self, setting_volume):
        """Сброс положения ползунка до начального."""
        self.rect_slider.left = (setting_volume *
                                 self.width_footing +
                                 self.rect_footing.left)
        self.volume = setting_volume
        self.old_volume = self.volume
