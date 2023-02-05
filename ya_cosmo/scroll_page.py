import pygame
import pygame.font


class Scroll():
    """Класс, создающий прокручивающию страницу."""

    def __init__(self, ai_game, width, text, fields_names, fields_arg=None):
        """Инициализация атрибутов страницы."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = width
        self.fields_names = fields_names
        self.font_button = ai_game.button_menu
        self.font_dropdown = ai_game.button_dropdown

        if fields_arg[0]:
            self.fields_arg = fields_arg
        else:
            self.fields_arg = []
            for i in fields_names:
                self.fields_arg.append(['Пока тут пусто'])

        self.j = 0

        self.size_text = int(self.screen_rect.width / 80)
        self.text_color_number = (12, 149, 207)
        self.text_color = (12, 149, 207)
        self.old_mouse_pos = [0, 0]
        self.slider_active = False

        # назначение размеров и свойств полей
        self.width_name = int(self.screen_rect.width / 6)
        self.height_name = int(self.screen_rect.height / 20)
        self.font_name = pygame.font.Font(self.font_dropdown, self.size_text)
        self.acceptable_size = self.screen_rect[0]

        # назначение размеров и свойств страницы
        self.width_page = int(self.width_name * len(fields_names))
        self.height_page = int(self.screen_rect.height / 2)
        self.page_color = (9, 60, 149)
        self.rect_page = pygame.Rect(0, 0, self.width_page,
                                     self.height_page)
        self.font_page = pygame.font.Font(self.font_button, self.size_text)
        self.rect_page.center = self.screen_rect.center

        # преобразует text в прямоугольник и выравнивает текста
        self.msg_image_page = self.font_page.render(text, True,
                                                    self.text_color)
        self.msg_image_page_rect = self.msg_image_page.get_rect()
        self.msg_image_page_rect.midtop = self.rect_page.midtop
        self.msg_image_page_rect.y += self.size_text / 4

        # !!!создание нижней заглушки для скрытия отрисовки!!!
        self.width_plug = self.width_page
        self.height_plug = self.height_name
        self.rect_plug = pygame.Rect(0, 0, self.width_plug,
                                     self.height_plug)
        self.rect_plug.midtop = self.rect_page.midbottom

        # назначение размеров и свойств значения полей
        self.width_arg = int(self.screen_rect.width / 6)
        self.height_arg = int(self.screen_rect.height / 20)
        self.arg_color = (0, 150, 150)
        self.font_arg = pygame.font.SysFont(None, self.size_text)

        # назначение размеров и свойств ползуна
        self.width_footing = int(self.screen_rect.width / 120)
        self.height_footing = int(self.height_page - self.size_text
                                  - self.size_text / 2 -
                                  self.height_name)
        self.footing_color = (0, 150, 150)
        self.rect_footing = pygame.Rect(0, 0, self.width_footing,
                                        self.height_footing)
        self.rect_footing.topright = self.rect_page.topright
        self.rect_footing.y += (self.size_text + self.size_text / 2 +
                                self.height_name)

        self.width_slider = int(self.screen_rect.width / 120)
        if ((len(self.fields_arg[0]) / 8) == 1 or
           (len(self.fields_arg[0]) / 8) < 1):
            self.height_slider = self.rect_footing.height
        else:
            self.height_slider = int(self.rect_footing.height /
                                     (len(self.fields_arg[0]) / 8))

        self.rect_slider = pygame.Rect(0, 0, self.width_slider,
                                       self.height_slider)
        self.rect_slider.topright = self.rect_footing.topright

        # создание слоя наложения
        height_page_surf = self.height_page + self.height_plug

        self.surf = pygame.Surface((self.width_page, height_page_surf))
        self.surf.fill((9, 60, 149))
        self.surf.set_alpha(100)

        self.surf_down = pygame.Surface((self.width_page, self.height_plug))
        self.surf_down.set_alpha(240)

        self.surf_arg = pygame.Surface((self.width_arg, self.height_arg))
        self.surf_arg.fill((0, 150, 150))
        self.surf_arg.set_alpha(30)

        self.surf_name = pygame.Surface((self.width_name, self.height_name))
        self.surf_name.set_alpha(240)

        self.surf_table_name = pygame.Surface((self.width_page,
                                               self.height_name))
        self.surf_table_name.set_alpha(200)

        # множитель перемещения ползуна
        self.speed_dividers = 8 / (self.height_slider)

        self.width_arg_end = self.width_arg - self.width_footing

    def slider_control(self):
        # логика управления ползуном
        mouse_pos = pygame.mouse.get_pos()
        if self.slider_active:
            if (mouse_pos[1] > self.old_mouse_pos[1] and
               self.rect_slider.bottom <= self.rect_slider.bottom):
                self.rect_slider.centery = (self.rect_slider.centery
                                            + mouse_pos[1]
                                            - self.old_mouse_pos[1])
                self.old_mouse_pos = mouse_pos

            elif (mouse_pos[1] < self.old_mouse_pos[1] and
                  self.rect_slider.top >= self.rect_footing.top):
                self.rect_slider.centery = (self.rect_slider.centery
                                            + mouse_pos[1]
                                            - self.old_mouse_pos[1])
                self.old_mouse_pos = mouse_pos

            if self.rect_slider.top < self.rect_footing.top:
                self.rect_slider.top = self.rect_footing.top

            elif self.rect_slider.bottom > self.rect_footing.bottom:
                self.rect_slider.bottom = self.rect_footing.bottom

            # просчёт сдвига значений полей
            self.j = ((self.rect_footing.y - self.rect_slider.y)
                      * self.speed_dividers)

    def slider_activate(self):
        # активация ползуна
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_slider.collidepoint(mouse_pos):
            self.old_mouse_pos = mouse_pos
            self.slider_active = True

    def slider_deactivate(self):
        # деактивация ползуна
        mouse_pos = pygame.mouse.get_pos()
        self.old_mouse_pos = mouse_pos
        self.slider_active = False

    def draw(self):
        # отображение страницы
        self.screen.blit(self.surf_table_name, self.rect_page.topleft)
        pygame.draw.rect(self.screen, self.page_color, self.rect_page, 2)
        self.screen.blit(self.msg_image_page, self.msg_image_page_rect)

        # отображение ползуна
        pygame.draw.rect(self.screen, self.page_color, self.rect_footing, 1)

        pygame.draw.rect(self.screen, self.page_color, self.rect_slider)

    def draw_name(self):
        """Создание имёт полей."""
        i = 1
        for arg in self.fields_names:
            self.rect_name = pygame.Rect(0, 0, self.width_name,
                                         self.height_name)
            self.rect_name.topleft = self.rect_page.topleft
            self.rect_name.y += self.size_text + self.size_text / 2
            if i % 2 == 0 and i <= len(self.fields_names):
                if i % 4 == 0:
                    self.rect_name.x += (self.acceptable_size / 2 +
                                         self.width_name * (i - 1))
                else:
                    self.rect_name.x += (self.acceptable_size / 2 +
                                         self.width_name)
            elif i % 2 != 0 and i <= len(self.fields_names):
                if i == 1:
                    self.rect_name.x += self.acceptable_size / 2
                else:
                    self.rect_name.x += (self.acceptable_size / 2 +
                                         self.width_name * (i - 1))

            self._draw_arg(i)

            if i <= len(self.fields_names):
                i += 1

            # преобразует text в прямоугольник и выравнивает текста
            msg_image_name = self.font_name.render(arg, True,
                                                   self.text_color)
            msg_image_name_rect = msg_image_name.get_rect()
            msg_image_name_rect.center = self.rect_name.center

            # отображение имен полей, нижней и верхней заглушки
            self.screen.blit(self.surf_down, (self.rect_plug.topleft))
            self.screen.blit(self.surf_name, self.rect_name.topleft)

            pygame.draw.rect(self.screen, self.page_color, self.rect_name, 2)
            self.screen.blit(msg_image_name, msg_image_name_rect)

            if i == len(self.fields_names) + 1:
                self.screen.blit(self.surf, (self.rect_page.topleft))

            pygame.draw.rect(self.screen, self.page_color, self.rect_plug, 2)

    def _draw_arg(self, i):
        """Создание значений полей."""
        j = self.j
        k = 1
        for arg in self.fields_arg[i-1]:
            if i == len(self.fields_names):
                self.rect_arg = pygame.Rect(0, 0,  self.width_arg_end,
                                            self.height_arg)
            else:
                self.rect_arg = pygame.Rect(0, 0, self.width_arg,
                                            self.height_arg)

            # назначение размеров и свойств значения полей
            arg = str(arg)
            self.rect_arg.topleft = self.rect_name.bottomleft
            self.rect_arg.y += self.height_arg * j
            j += 1

            if i == 1:
                # инициализация места
                font = pygame.font.SysFont(None, self.size_text)
                self.msg_image_namber = font.render(f'{k}.', True,
                                                    self.text_color_number)
                self.msg_image_namber_rect = (self.msg_image_namber.get_rect())
                self.msg_image_namber_rect.midleft = self.rect_arg.midleft
                self.msg_image_namber_rect.x += self.size_text / 2
                k += 1

            if (self.rect_arg.top >= self.rect_name.top and
               self.rect_arg.top <= self.rect_page.bottom):
                # преобразует text в прямоугольник и выравнивает текста
                msg_image_arg = (self.font_arg.render(arg, True,
                                 self.text_color))
                msg_image_arg_rect = (msg_image_arg.get_rect())
                msg_image_arg_rect.center = self.rect_arg.center
                pygame.draw.rect(self.screen, self.arg_color, self.rect_arg, 1)
                self.screen.blit(self.surf_arg, (self.rect_arg.topleft))
                self.screen.blit(msg_image_arg, msg_image_arg_rect)

                if self.msg_image_namber_rect.top <= self.rect_page.bottom:
                    self.screen.blit(self.msg_image_namber,
                                     self.msg_image_namber_rect)
