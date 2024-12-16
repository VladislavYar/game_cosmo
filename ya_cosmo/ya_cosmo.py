import sys
from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from score import Score
from scroll_page import Scroll
from planet import Planet
from input import Input
from audio import Audio
from ship import ShipCharacter
from camera import Camera
from mouse import Mouse
from space_menu import Logo, Comet
from processing import (dropdown_slider_method, dropdown_button_method,
                        space_menu_method, shot_method)


class YaCosmo():
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height),
                                              pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("YaCosmo")
        self.FPS = pygame.time.Clock()

        # создание ссылок на шрифты
        self.button_menu = 'fonts/button_menu.ttf'
        self.button_dropdown = 'fonts/button_dropdown.ttf'

        # инициализация данных игры
        self.stats = GameStats(self)
        self.score = Score(self)
        self.audio = Audio(self)

        # создание динамических объектов
        self.heros_ship = ShipCharacter(self)
        self.mouse = Mouse(self)

        # создание камеры
        self.camera = Camera(self)

        # создание кнопок главного меню
        self.play_button = Button(self, text='Новая игра')
        self.score_button = Button(self, text='Рекорды')
        self.settings_button = Button(self, text='Настройки')
        self.exit_button = Button(self, text='Выход')
        self.back_button = Button(self, text='Назад')
        self.pause_button = Button(self, text='Пауза')
        self.reset_button = Button(self, text='Сбросить')
        self.save_button = Button(self, text='Сохранить')
        self.start_button = Button(self, text='Запуск')

        # создание кнопок меню во время игры
        self.resum_button = Button(self, text='Продолжить')
        self.exit_main_menu = Button(self, text='В меню')
        self.exit_desktop = Button(self, text='На рабочий стол')

        # создание кнопки ввода имени
        self.input_name = Input(self, text_input='Введите имя...',
                                text_button='Подтвердить', width=15)

        # создание списков кнопок меню
        self.dropdown_buttons = []
        dropdown_button_method(
                               self, method='new_dropdown_button',
                               name_drop=self.dropdown_buttons,
                               name='Разрешение экрана',
                               width=15,
                               texts=[
                                      '2560:1440', '1920:1080', '1600:900',
                                      '1366:768', '1280:720'
                                     ]
                                )

        self.dropdown_difficulty_buttons = []
        dropdown_button_method(
                               self, method='new_dropdown_button',
                               name_drop=self.dropdown_difficulty_buttons,
                               name='Сложность игры',
                               width=95,
                               texts=['Легко', 'Нормально', 'Сложно', ]
                               )

        # создание списков ползунов меню
        self.dropdown_sliders = []
        volume_music = self.settings.volume_music
        volume_effects = self.settings.volume_effects
        volume_voice = self.settings.volume_voice
        dropdown_slider_method(
                               self, method='new_dropdown_slider',
                               name_drop=self.dropdown_sliders,
                               name='Звук',
                               width=30,
                               texts={'Музыка': volume_music,
                                      'Эффекты': volume_effects,
                                      'Речь': volume_voice}
                                )

        # создание прокручивающихся страниц
        fields_names = ['Имя', 'Очки']
        fields_arg = self.stats.read_record()
        self.scroll_page_score = Scroll(self, width=29,
                                        text='Таблица рекордов',
                                        fields_names=fields_names,
                                        fields_arg=fields_arg)

        # создание звёздного пространства в меню
        self.space_menu = []
        space_menu_method(self, method='new_space_menu',
                          name_list=self.space_menu,
                          )
        self.comet = Comet(self)

        # создание логотипа
        self.logo = Logo(self)
        self.planet_menu = Planet(self, 'planet_menu', 5)

        self._rect_menu_transformation()

        # создание флагов
        self.active_lowering = False
        self.play_button_active = True
        self.score_button_active = True
        self.settings_button_active = True
        self.pause_game = False
        self.open_stats_dropdown_buttons = False
        self.open_dropdown_difficulty_buttons = False
        self.open_stats_slider = False

        # предварительная работа с данными
        self.save_button.activate_deactevate_button(False)
        self.reset_button.activate_deactevate_button(False)
        self.start_button.activate_deactevate_button(False)
        self.check_intersection = []
        self.shot_heros = []
        self.player = ''

    def _rect_menu_transformation(self):
        """Расчёт положения элементов меню."""
        self.logo.rect.midbottom = self.play_button.rect.midtop
        self.logo.rect.y -= self.play_button.height

        self.planet_menu.rect.topleft = self.logo.rect.midleft
        self.planet_menu.rect.x += self.planet_menu.rect.height / 4
        self.planet_menu.rect.y += self.planet_menu.rect.height / 6

    def run_game(self):
        """Запуск основного цикла игры."""
        self.audio.load_music_menu()
        self.audio.start_music()
        while True:
            self.FPS.tick(self.settings.setting_fps)
            self.heros_ship.check_speed(self.camera.speed)
            self._check_mouse_pos()
            self._check_events()
            if self.stats.game_active and not self.pause_game:
                self.heros_ship.update()
                self.mouse.update()
                shot_method(self, 'check_bank_shor', 'ShotHeros',
                            self.shot_heros)
                self.col_flag = pygame.sprite.collide_circle(self.heros_ship,
                                                             self.mouse)
            self._update_screen()

    def _check_events(self):
        """Отслеживает события клавиатуры и мыши."""
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.stats.save_record(self.player)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_mouse = pygame.mouse.get_pressed()
                if pressed_mouse[0]:
                    self._left_mouse_check(pressed_mouse[0])
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed_mouse = pygame.mouse.get_pressed()
                if not pressed_mouse[0]:
                    self._left_mouse_check(pressed_mouse[0])

    def _left_mouse_check(self, flag):
        if flag:
            mouse_pos = pygame.mouse.get_pos()
            if self.stats.game_active and not self.pause_game:
                shot_method(self, 'new_shot', 'ShotHeros', self.shot_heros)
            elif (self.play_button_active and self.score_button_active and
                  self.settings_button_active):
                self._check_play_button(mouse_pos)
                self._check_score_button(mouse_pos)
                self._check_settings_button(mouse_pos)
                self._check_exit_button(mouse_pos)

            elif not self.play_button_active:
                self._check_complexity_button(mouse_pos)

            elif not self.score_button_active:
                self._check_record_score_button(mouse_pos)

            elif not self.settings_button_active:
                self._check_display_button(mouse_pos)
                if self.open_stats_slider:
                    dropdown_slider_method(self, method=(
                                           'slider_control_active'),
                                           name_drop=(self.
                                                      dropdown_sliders))
        else:
            if not self.settings_button_active:
                if self.open_stats_slider:
                    dropdown_slider_method(self, method=(
                                           'slider_control_deactive'),
                                           name_drop=(
                                               self.dropdown_sliders))
            elif not self.score_button_active:
                (self.scroll_page_score.
                 slider_deactivate())

    def _check_mouse_pos(self):
        """
        Отслеживание позиции мышки и просчёт коллизии.
        """
        if self.stats.game_active:
            self.heros_ship.rotate_heros_ship()
            self.heros_ship.correct_rect_engines()
        elif (self.play_button_active and self.score_button_active
              and self.settings_button_active):
            self.play_button.hover_display()
            self.score_button.hover_display()
            self.settings_button.hover_display()
            self.exit_button.hover_display()

        elif not self.play_button_active:
            self.back_button.hover_display()
            self.start_button.hover_display()
            self.reset_button.hover_display()
            self.input_name.hover_display()
            dropdown_button_method(self, method='hover_display_name',
                                   name_drop=self.dropdown_difficulty_buttons)
            if self.open_dropdown_difficulty_buttons:
                dropdown_button_method(self, method='hover_display_button',
                                       name_drop=(
                                        self.dropdown_difficulty_buttons))

        elif not self.score_button_active:
            self.back_button.hover_display()
            self.scroll_page_score.slider_control()

        elif not self.settings_button_active:
            self.back_button.hover_display()
            self.save_button.hover_display()
            self.reset_button.hover_display()
            dropdown_button_method(self, method='hover_display_name',
                                   name_drop=self.dropdown_buttons)
            dropdown_slider_method(self, method='hover_display_name',
                                   name_drop=self.dropdown_sliders)
            if self.open_stats_dropdown_buttons:
                dropdown_button_method(self, method='hover_display_button',
                                       name_drop=self.dropdown_buttons)
            elif self.open_stats_slider:
                dropdown_slider_method(self, method=('slider_control'),
                                       name_drop=(self.dropdown_sliders))
                self._volume_settings()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if self.input_name.active:
            self.input_name.text_input(event)
        elif event.key == pygame.K_p and self.stats.game_active:
            self._pause_game()
        elif event.key == pygame.K_RIGHT and not self.pause_game:
            pass
        elif event.key == pygame.K_LEFT and not self.pause_game:
            pass
        elif event.key == pygame.K_w and not self.pause_game:
            self.heros_ship.moving_active_deactive_ship('up', True)
        elif event.key == pygame.K_s and not self.pause_game:
            self.heros_ship.moving_active_deactive_ship('down', True)
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_record(self.player)
            sys.exit()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            pass
        elif event.key == pygame.K_LEFT:
            pass
        elif event.key == pygame.K_w:
            self.heros_ship.moving_active_deactive_ship('up', False)
        elif event.key == pygame.K_s:
            self.heros_ship.moving_active_deactive_ship('down', False)

    def _check_play_button(self, mouse_pos):
        """
        Переходит к вкладке настроек сложности
        и введения имени при нажатии мышки.
        """
        if (self.play_button.rect.collidepoint(mouse_pos)
           and self.stats.game_active is False):
            self.play_button_active = False

    def _check_complexity_button(self, mouse_pos):
        """
        Сохраняет настройки сложности и имя игрока запускает
        игру при нажатии кнопок мышки.
        """
        # подтверждение выбранного имени
        self.input_name.save_name()
        # вход/выход из поля ввода
        self.input_name.input_activate_deactivate()

        if (self.dropdown_difficulty_buttons[0].
           rect_name.collidepoint(mouse_pos)):
            # открытие/закрытие списка сложности игры
            self.open_dropdown_difficulty_buttons = (
                                            dropdown_button_method
                                            (self, 'open_close_dropdown',
                                             name_drop=(
                                              self.
                                              dropdown_difficulty_buttons)))

        elif (self.open_dropdown_difficulty_buttons and
              any(self.check_intersection)):
            # проверка на нажатие сложности
            dropdown_button_method(self, 'collidepoint_mouse_pos',
                                   name_drop=(
                                            self.dropdown_difficulty_buttons))

        if self.input_name.click_button or any(self.check_intersection):
            self.reset_button.activate_deactevate_button(True)

            if self.input_name.click_button and any(self.check_intersection):
                self._actvate_deactvate_button(True)

        if (self.start_button.rect.collidepoint(mouse_pos) and
           self.start_button.active):
            # проверка нажатия кнопки сохранения
            # сохранение имени в файл и запуск игры
            self.input_name.save_name(True)
            self.player = self.input_name.text
            self._start_game()
            self.settings.difficulty_game(self.check_intersection.index(True)
                                          + 1)

        # проверка нажатия кнопки сброса или назад
        self._back_or_reset_play(mouse_pos)

    def _back_or_reset_play(self, mouse_pos):
        """Очистка активности и возвращение назад в меню(при условии)."""
        if (self.back_button.rect.collidepoint(mouse_pos) or
            (self.reset_button.rect.collidepoint(mouse_pos) and
           self.reset_button.active)):
            dropdown_button_method(self, method='color_reset',
                                   name_drop=(
                                    self.dropdown_difficulty_buttons))

            # удаление и обнуление не нужных значений
            self._del_reset_attribute()

            # возвращение к исходному виду поля ввода
            self.input_name.reset_input()

            if self.back_button.rect.collidepoint(mouse_pos):
                self.play_button_active = True

    def _check_score_button(self, mouse_pos):
        """Переходит к вкладке рекордов при нажатии мышки."""
        if (self.score_button.rect.collidepoint(mouse_pos) and
           self.stats.game_active is False):
            self.score_button_active = False

    def _check_record_score_button(self, mouse_pos):
        self.scroll_page_score.slider_activate()
        self._back_score(mouse_pos)

    def _back_score(self, mouse_pos):
        """Возвращается обратно в главное меню
        при нажатии кнопки назад."""
        if self.back_button.rect.collidepoint(mouse_pos):
            self.scroll_page_score.j = 0
            self.score_button_active = True

    def _check_settings_button(self, mouse_pos):
        """
        Переходит к вкладке настроек игры
        при нажатии мышки.
        """
        if (self.settings_button.rect.collidepoint(mouse_pos) and
           self.stats.game_active is False):
            self.settings_button_active = False

    def _check_display_button(self, mouse_pos):
        """
        Сохраняет настройки и перезапускает дисплей
        по необходимости.
        """
        # деактивация недопустимых значений
        dropdown_button_method(self, 'validation_validity',
                               name_drop=self.dropdown_buttons)

        # открывает/закрывает список кнопок по нажатию мыши
        if self.dropdown_buttons[0].rect_name.collidepoint(mouse_pos):
            self.open_stats_dropdown_buttons = (
                                                dropdown_button_method
                                               (self, 'open_close_dropdown',
                                                name_drop=self.
                                                dropdown_buttons))

        elif self.open_stats_dropdown_buttons and any(self.check_intersection):
            # внешняя активация кнопки сохранения
            dropdown_button_method(self, 'collidepoint_mouse_pos',
                                   name_drop=self.dropdown_buttons)

            self._actvate_deactvate_button(True)

        if (self.dropdown_sliders[0].rect_name.collidepoint(mouse_pos) and
           self.open_stats_dropdown_buttons is False):
            # открывает/закрывает список ползунков по нажатию мыши
            self.open_stats_slider = (
                                      dropdown_slider_method
                                     (self, 'open_close_dropdown',
                                      name_drop=self.dropdown_sliders)
                                      )

        elif (self.save_button.rect.collidepoint(mouse_pos) and
              self.save_button.active):
            # проверка нажатия кнопки сохранения
            self._actvate_deactvate_button(False)
            if (self.dropdown_sliders[0].volume !=
                self.settings.volume_music or
                self.dropdown_sliders[1].volume !=
                self.settings.volume_effects or
               self.dropdown_sliders[2].volume != self.settings.volume_voice):
                # сохранение настроек звука
                dropdown_slider_method(self, 'save_settings_volume',
                                       name_drop=self.dropdown_sliders)

            if True in self.check_intersection:
                selected_resolution = (
                    self.dropdown_buttons
                    [self.check_intersection.index(True)].text.split(':'))
                self.settings.screen_width = int(
                                                selected_resolution[0])
                self.settings.screen_height = int(
                                                selected_resolution[1])
                self.settings.save_settings_menu()
                self._restart_game(self.settings.screen_width,
                                   self.settings.screen_height)
            else:
                self.settings.save_settings_menu()

        # проверка нажатия кнопки сброса или назад
        self._back_or_reset_settings(mouse_pos)

    def _back_or_reset_settings(self, mouse_pos):
        """Очистка активности и возвращение назад в меню(при условии)."""
        if (self.back_button.rect.collidepoint(mouse_pos) or
           (self.reset_button.rect.collidepoint(mouse_pos)
           and self.reset_button.active)):
            # сброс настроек звука
            dropdown_slider_method(self, 'slider_reset_position',
                                   name_drop=self.dropdown_sliders)

            dropdown_slider_method(self, method='surf_slider_control',
                                   name_drop=self.dropdown_sliders)

            dropdown_button_method(self, method='color_reset',
                                   name_drop=self.dropdown_buttons)

            # удаление и обнуление не нужных значений
            self._del_reset_attribute()

        if self.back_button.rect.collidepoint(mouse_pos):
            self.settings_button_active = True

    def _volume_settings(self):
        """Проверка изменения громкости."""
        volume = self.dropdown_sliders[0].volume
        old_volume = self.dropdown_sliders[0].old_volume
        flag = self.dropdown_sliders[0].flag
        if volume != old_volume and flag:
            self._actvate_deactvate_button(True)
            self.audio.volume_music(volume)

        volume = self.dropdown_sliders[1].volume
        old_volume = self.dropdown_sliders[1].old_volume
        flag = self.dropdown_sliders[1].flag
        if volume != old_volume and flag:
            self._actvate_deactvate_button(True)
            try:
                self.audio.volume_effects(volume, self.effect)
                if self.channel_effect.get_busy() is False:
                    self.channel_effect.play(self.effect)
            except AttributeError:
                self.channel_effect = self.audio.load_channel(1)
                self.effect = (self.audio.
                               load_effects('sounds/settings_effect.ogg'))
                self.audio.volume_effects(volume, self.effect)
                self.channel_effect.play(self.effect)

        volume = self.dropdown_sliders[2].volume
        old_volume = self.dropdown_sliders[2].old_volume
        flag = self.dropdown_sliders[2].flag
        if volume != old_volume and flag:
            self._actvate_deactvate_button(True)
            try:
                self.audio.volume_voice(volume, self.voice)
                if self.channel_voice.get_busy() is False:
                    self.channel_voice.play(self.voice)
            except AttributeError:
                self.channel_voice = self.audio.load_channel(2)
                self.voice = (self.audio.
                              load_voice('sounds/settings_voice.ogg'))
                self.audio.volume_voice(volume, self.voice)
                self.channel_voice.play(self.voice)

    def _volume_reset(self):
        """Сбрасывает настройки звука."""
        if self.settings.volume_music != self.dropdown_sliders[0].volume:
            self.audio.volume_music(self.settings.volume_music)
        if self.settings.volume_effects != self.dropdown_sliders[1].volume:
            self.audio.volume_effects(self.settings.volume_effects,
                                      self.effect)
        if self.settings.volume_voice != self.dropdown_sliders[2].volume:
            self.audio.volume_voice(self.settings.volume_voice, self.voice)

    def _check_exit_button(self, mouse_pos):
        """Выходит из игры при нажатии кнопки мыши."""
        if (self.exit_button.rect.collidepoint(mouse_pos) and not
           self.stats.game_active):
            self.stats.save_record(self.player)
            sys.exit()

    def _actvate_deactvate_button(self, flag):
        """Активация/деактивация кнопок сброса и сохранения."""
        self.save_button.activate_deactevate_button(flag)
        self.reset_button.activate_deactevate_button(flag)
        self.start_button.activate_deactevate_button(flag)

    def _del_reset_attribute(self):
        """Удаление не нужных аттрибутов и обнуление необходимых."""
        self.check_intersection = []
        self._actvate_deactvate_button(False)
        if self.open_stats_dropdown_buttons:
            self.open_stats_dropdown_buttons = (dropdown_button_method
                                                (self, 'open_close_dropdown',
                                                 name_drop=(self.
                                                            dropdown_buttons)))
        if self.open_stats_slider:
            self.open_stats_slider = (dropdown_slider_method
                                      (self, 'open_close_dropdown',
                                       name_drop=self.dropdown_sliders))
        if self.open_dropdown_difficulty_buttons:
            self.open_dropdown_difficulty_buttons = (
                                            dropdown_button_method
                                            (self, 'open_close_dropdown',
                                             name_drop=(
                                                self.
                                                dropdown_difficulty_buttons)))

    def _start_game(self):
        pygame.mouse.set_visible(False)
        self.stats.game_active = True

    def _pause_game(self):
        self.pause_game = not self.pause_game

    def _reinitialization_table_score(self):
        """Переинициализация таблицы рекордов."""
        fields_names = ['Имя', 'Очки']
        fields_arg = self.stats.read_record()
        self.scroll_page_score = Scroll(self, width=29,
                                        text='Таблица рекордов',
                                        fields_names=fields_names,
                                        fields_arg=fields_arg)

    def _random_fly_comets_and_star(self):
        """Рандомный вылет комет и смена мигания звёзд их отрисовка."""
        random_time_comet = randint(1, 1000)
        random_time_star = randint(1, 1500)

        time_tick = pygame.time.get_ticks()
        if not (time_tick % random_time_comet):
            self._creating_comet()

        if not (time_tick % random_time_star):
            space_menu_method(self, method='_random_flag_star',
                              name_list=self.space_menu)

        self.comet.draw()

    def _creating_comet(self):
        if self.comet.flag_fly is False:
            self.comet = Comet(self)
            self.comet.flag_fly = True

    def _menu_button(self):
        """Отрисовка кнопок меню."""
        # отрисовка задника меню
        space_menu_method(self, method='draw',
                          name_list=self.space_menu)
        self._random_fly_comets_and_star()

        self.logo.draw()
        self.planet_menu.draw()

        if (self.play_button_active and self.score_button_active and
           self.settings_button_active):
            self.play_button.draw()
            self.score_button.draw()
            self.settings_button.draw()
            self.exit_button.draw()

        elif not self.play_button_active:
            self.start_button.draw()
            self.back_button.draw()
            self.reset_button.draw()
            self.input_name.draw()
            dropdown_button_method(self, 'draw',
                                   name_drop=(
                                        self.dropdown_difficulty_buttons))

        elif not self.score_button_active:
            self.scroll_page_score.draw()
            self.scroll_page_score.draw_name()
            self.back_button.draw()

        elif not self.settings_button_active:
            self.save_button.draw()
            self.back_button.draw()
            self.reset_button.draw()

            dropdown_button_method(self, 'draw',
                                   name_drop=self.dropdown_buttons)
            if not self.open_stats_dropdown_buttons:
                dropdown_slider_method(self, 'draw',
                                       name_drop=self.dropdown_sliders)

    def _rendering_game(self):
        """Отрисовка игрового процесса."""
        for space in self.space_menu:
            space.flag_rect = True
            self.camera.update(space, self.heros_ship)

        for sprite in self.shot_heros:
            self.camera.update(sprite, self.heros_ship)

        self.camera.update(self.logo, self.heros_ship)
        space_menu_method(self, method='shift_starts',
                          name_list=self.space_menu)
        space_menu_method(self, method='draw',
                          name_list=self.space_menu)

        shot_method(self, 'draw',  'ShotHeros', self.shot_heros)
        self.heros_ship.draw()
        self.mouse.draw(self.col_flag, self.heros_ship,
                        self.camera.dir_move)

        if self.pause_game:
            self.pause_button.draw_text()

    def _game_text(self):
        """Отрисовка текста в игре."""
        pass

    def _update_screen(self):
        # при каждом проходе цикла перерисовывется экран
        self.screen.fill(self.settings.bg_color)
        if self.stats.game_active:
            self._rendering_game()

        # отображение кнопок, если игра не активна
        if not self.stats.game_active:
            self._menu_button()

        # отображение последнего прорисованного экрана
        pygame.display.flip()

    def _restart_game(self, screen_width, screen_height):
        "Рестарт дисплея под новое разрешение."
        pygame.display.quit()
        pygame.display.init()

        self.settings = Settings()
        self.settings.screen_width = screen_width
        self.settings.screen_height = screen_height

        self.screen = pygame.display.set_mode((screen_width, screen_height),
                                              pygame.FULLSCREEN)
        pygame.display.set_caption("YaCosmo")

        # создание ссылок на шрифты
        self.button_menu = 'fonts/button_menu.ttf'
        self.button_dropdown = 'fonts/button_dropdown.ttf'

        # создание динамических объектов
        self.heros_ship = ShipCharacter(self)
        self.mouse = Mouse(self)

        # создание камеры
        self.camera = Camera(self)

        # создание кнопок меню
        self.play_button = Button(self, text='Новая игра')
        self.score_button = Button(self, text='Рекорды')
        self.settings_button = Button(self, text='Настройки')
        self.exit_button = Button(self, text='Выход')
        self.back_button = Button(self, text='Назад')
        self.pause_button = Button(self, text='Пауза')
        self.reset_button = Button(self, text='Сбросить')
        self.save_button = Button(self, text='Сохранить')
        self.start_button = Button(self, text='Запуск')

        # создание кнопки ввода имени
        self.input_name = Input(self, text_input='Введите имя...',
                                text_button='Подтвердить', width=15)

        # создание списков кнопок меню
        self.dropdown_buttons = []
        dropdown_button_method(
                               self, method='new_dropdown_button',
                               name_drop=self.dropdown_buttons,
                               name='Разрешение экрана',
                               width=15,
                               texts=[
                                      '2560:1440', '1920:1080', '1600:900',
                                      '1366:768', '1280:720'
                                     ]
                                )

        self.dropdown_difficulty_buttons = []
        dropdown_button_method(
                               self, method='new_dropdown_button',
                               name_drop=self.dropdown_difficulty_buttons,
                               name='Сложность игры',
                               width=95,
                               texts=['Легко', 'Нормально', 'Сложно', ]
                               )

        # создание списков ползунов меню
        self.dropdown_sliders = []
        volume_music = self.settings.volume_music
        volume_effects = self.settings.volume_effects
        volume_voice = self.settings.volume_voice
        dropdown_slider_method(
                               self, method='new_dropdown_slider',
                               name_drop=self.dropdown_sliders,
                               name='Звук',
                               width=30,
                               texts={'Музыка': volume_music,
                                      'Эффекты': volume_effects,
                                      'Речь': volume_voice}
                                )

        # создание прокручивающихся страниц
        fields_names = ['Имя', 'Очки']
        fields_arg = self.stats.read_record()
        self.scroll_page_score = Scroll(self, width=29,
                                        text='Таблица рекордов',
                                        fields_names=fields_names,
                                        fields_arg=fields_arg)

        # создание звёздного пространства в меню
        self.space_menu = []
        space_menu_method(self, method='new_space_menu',
                          name_list=self.space_menu,
                          )
        self.comet = Comet(self)

        # создание логотипа
        self.logo = Logo(self)
        self.planet_menu = Planet(self, 'planet_menu', 5)

        self._rect_menu_transformation()

        # создание флагов
        self.active_lowering = False
        self.play_button_active = True
        self.score_button_active = True
        self.settings_button_active = False
        self.pause_game = False
        self.open_stats_dropdown_buttons = False
        self.open_dropdown_difficulty_buttons = False
        self.open_stats_slider = False

        # предварительная работа с данными
        self.save_button.activate_deactevate_button(False)
        self.reset_button.activate_deactevate_button(False)
        self.start_button.activate_deactevate_button(False)
        self.check_intersection = []
        self.player = ''


if __name__ == '__main__':
    # создание экземпляра и запуск игры
    ai = YaCosmo()
    ai.run_game()
