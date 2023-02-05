import pygame
import pygame.font
import string
import json


class Input():
    """Класс создания кнопки ввода."""

    def __init__(self, ai_game, text_input, text_button, width):
        """Инициализирует атрибуты кнопки выдвижного списка."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.click_button = False
        self.active = False
        self.active_button = False
        self.text = ''
        self.font_button = ai_game.button_menu
        self.font_dropdown = ai_game.button_dropdown
        self.old_text_input = text_input
        self.size_text_bottom = int(self.screen_rect.width / 80)
        self.size_text_input = int(self.screen_rect.width / 48)

        # создание списка английских букв
        self.list_letters = list(string.printable)

        # назначение размеров и свойств кнопки ввода
        self.width = int(self.screen_rect.width / 5)
        self.height = int(self.screen_rect.height / 20)
        self.button_color_input = (170, 170, 170)
        self.text_color_click = (100, 150, 100)
        self.text_input_color = (85, 85, 85)

        self.font_input = pygame.font.SysFont('None', self.size_text_input)

        self.rect_input = pygame.Rect(0, 0, self.width, self.height)
        self.rect_input.center = self.screen_rect.center
        self.rect_input.y -= self.screen_rect.width / width

        # кнопки сохранения
        self.button_color = (9, 60, 149)
        self.text_color = (12, 149, 207)
        self.text_color_imput = (200, 200, 200)
        self.text_color_not_active = (70, 70, 70)
        self.text_button = text_button
        self.font_button = pygame.font.Font(self.font_button,
                                            self.size_text_bottom)

        self.rect_button = pygame.Rect(0, 0, self.width, self.height)
        self.rect_button.midtop = self.rect_input.midbottom

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

        self.surf_active = pygame.Surface((self.width, self.height))
        self.surf_active.fill((240, 240, 240))
        self.surf_active.set_alpha(70)

        self._prep_text_input()

        # необходимые преобразования перед входом в метод
        self.msg_image_button = (
            self.font_button.render(self.text_button, True,
                                    self.text_color_not_active))
        self._prep_text_button()

    def _prep_text_input(self):
        # преобразует text в прямоугольник и выравнивает текста по центру
        if self.text and self.click_button is False:
            text = self.text
            text_color = self.text_color_imput
        elif self.click_button:
            text = self.text
            text_color = self.text_color_click
        else:
            text = self.old_text_input
            text_color = self.text_input_color

        self.msg_image_input = self.font_input.render(text, True,
                                                      text_color)
        self.msg_image_rect_input = self.msg_image_input.get_rect()
        self.msg_image_rect_input.center = self.rect_input.center

    def _prep_text_button(self):
        # преобразует text в прямоугольник и выравнивает текста по центру
        self.msg_image_rect_button = self.msg_image_button.get_rect()
        self.msg_image_rect_button.midbottom = self.rect_button.midbottom

    def draw(self):
        # отображение кнопки ввода, сохранения и текста
        # ввод
        if self.active:
            self.screen.blit(self.surf_active, (self.rect_input))
        else:
            self.screen.blit(self.surf_not_active, (self.rect_input))

        pygame.draw.rect(self.screen,
                         self.button_color_input, self.rect_input, 2)
        self.screen.blit(self.msg_image_input, self.msg_image_rect_input)

        # кнопка
        if self.click_button:
            self.screen.blit(self.surf_click, (self.rect_button))
        elif self.active_button:
            self.screen.blit(self.surf, (self.rect_button))
        else:
            self.screen.blit(self.surf_not_active, (self.rect_button))

        pygame.draw.rect(self.screen, self.button_color, self.rect_button, 2)
        self.screen.blit(self.msg_image_button, self.msg_image_rect_button)

    def input_activate_deactivate(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.rect_input.collidepoint(mouse_pos)
           and self.click_button is False):
            self.active = True
            self.button_color_input = (200, 200, 200)
        else:
            self.active = False
            self.button_color_input = (170, 170, 170)

    def text_input(self, event):
        """Обработка ввода текста и активация кнопки сохранения."""
        if self.click_button is False and self.active:
            if event.unicode in self.list_letters:
                self.text += event.unicode
                if len(self.text) == 15:
                    self.text = self.text[:-1]
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
        self._prep_text_input()
        self._active_button_save()

    def hover_display(self):
        """
        Изменение цвета кнопки при наведении курсора
        и при его отводе.
        """
        mouse_pos = pygame.mouse.get_pos()
        if (self.rect_button.collidepoint(mouse_pos) and self.active_button
           and self.click_button is False):
            self.button_color = (0, 150, 150)
            self._prep_text_button()

        elif self.active_button is False:
            self.button_color = (140, 140, 140)
            self.font_button.render(self.text_button, True,
                                    self.text_color_not_active)
            self._prep_text_button()
        else:
            self.button_color = (9, 60, 149)
            self._prep_text_button()

    def _active_button_save(self):
        """Активация/деактивация кнопки сохранения."""
        if self.text and self.click_button is False:
            self.msg_image_button = (
                self.font_button.render(self.text_button, True,
                                        self.text_color))
            self.active_button = True
        elif not self.text:
            self.msg_image_button = (
                self.font_button.render(self.text_button, True,
                                        self.text_color_not_active))
            self.active_button = False
        else:
            self.msg_image_button = (
                self.font_button.render(self.text_button, True,
                                        self.text_color_click))
            self.active_button = False

    def reset_input(self):
        self.text, self.active_button = '', False
        self.click_button, self.active = False, False
        self._prep_text_input()
        self._prep_text_button()
        self._active_button_save()

    def save_name(self, flag=False):
        """Сохранение введённого имени."""
        mouse_pos = pygame.mouse.get_pos()
        if (self.rect_button.collidepoint(mouse_pos) and self.text
           and self.click_button is False or flag):
            # деактивация возможности ввода и отображение сохранения имени
            self.click_button = True
            self.input_activate_deactivate()
            self._active_button_save()
            self._prep_text_input()
            if flag:
                try:
                    with open('data/record_score.json', 'r') as record_score:
                        record_score = json.loads(record_score.read())
                        if record_score:
                            if self.text in record_score:
                                pass
                            else:
                                record_score[self.text] = 0
                        else:
                            record_score = {self.text: 0, }
                        record_score_dump = record_score

                    with open('data/record_score.json', 'w') as record_score:
                        json.dump(record_score_dump, record_score)

                except FileNotFoundError:
                    # создаётся файл в необходимом формате при его отсутствие
                    with open('data/record_score.json', 'w') as record_score:
                        record_score_dump = {}
                        json.dump(record_score_dump, record_score)

                    with open('data/record_score.json', 'r') as record_score:
                        record_score = json.loads(record_score.read())
                        record_score = {self.text: 0, }
                        record_score_dump = record_score

                    with open('data/record_score.json', 'w') as record_score:
                        json.dump(record_score_dump, record_score)
