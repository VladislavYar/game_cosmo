import json


class Settings():
    """Класс для хранения всех настроек игры YaCosmo."""

    def __init__(self):
        """Инициализация настройки игры."""
        # загрузка файла с  найстройками
        with open('data/settings.json', 'r') as settings:
            settings = json.load(settings)

            # параметры экрана
            self.screen_width = settings['screen_width']
            self.screen_height = settings['screen_height']
            self.bg_color = (0, 0, 0)
            # настройка громкости
            self.volume_music = settings['volume_music']
            self.volume_effects = settings['volume_effects']
            self.volume_voice = settings['volume_voice']

        # настройка ФПС
        self.setting_fps = 60
        # инициализация динамических настроек
        self._coef_screen()
        self._dynamic_settings()

    def _dynamic_settings(self):
        """Инициализация динамических настроек игры."""
        self.speed_heros_ship_up = int(self.screen_height) / 15
        self.speed_heros_ship_down = int(self.screen_height) / 60

        self.speed_heros_ship_up_object = int(self.screen_height) / 60
        self.speed_heros_ship_down_object = int(self.screen_height) / 120

        self.speed_shot_heros = self.coef_screen * 800

    def difficulty_game(self, deifficulty=0):
        """Сохранение настроек сложности."""
        pass

    def _coef_screen(self):
        coefs = {2560: 1, 1920: 1.33,
                 1600: 1.6, 1366: 1.874, 1280: 2}

        self.coef_screen = coefs[self.screen_width]

    def save_settings_menu(self):
        """Сохранение настроек меню."""
        with open('data/settings.json', 'r') as settings:
            settings = json.load(settings)

            settings['screen_width'] = self.screen_width
            settings['screen_height'] = self.screen_height

            # настройка громкости
            settings['volume_music'] = self.volume_music
            settings['volume_effects'] = self.volume_effects
            settings['volume_voice'] = self.volume_voice
            self.settings_dump = settings

        with open('data/settings.json', 'w') as settings:

            json.dump(self.settings_dump, settings)
