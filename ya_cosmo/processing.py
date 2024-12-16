from random import randint

from dropdown import Button, Slider
from space_menu import Star
from shot import ShotHeros


def dropdown_slider_method(ai_game, method, name_drop,
                           name=None, width=None, texts=None):
    """Обработка методов класса Slider и создание объектов."""
    if method == 'new_dropdown_slider':
        i = 1
        number_buttons = len(texts)
        for text, volume in texts.items():
            new_dropdown_slider = Slider(ai_game, text, name, i, width,
                                         volume, number_buttons)
            name_drop.append(new_dropdown_slider)
            i += 1

    elif method == 'draw':
        name_drop[0].draw_name()
        for dropdown_slider in name_drop:
            dropdown_slider.draw()

    elif method == 'open_close_dropdown':
        for dropdown_slider in name_drop:
            open_stats_slider = dropdown_slider.open_close_dropdown()
        return open_stats_slider

    elif method == 'hover_display_name':
        name_drop[0].hover_display_name()

    elif method == 'slider_control':
        for dropdown_slider in name_drop:
            dropdown_slider.slider_control()

    elif method == 'surf_slider_control':
        for dropdown_slider in name_drop:
            dropdown_slider.surf_slider_control()

    elif method == 'slider_control_active':
        for dropdown_slider in name_drop:
            dropdown_slider.slider_control_active()

    elif method == 'slider_control_deactive':
        for dropdown_slider in name_drop:
            dropdown_slider.slider_control_deactive()

    elif method == 'slider_reset_position':
        volumes = [ai_game.settings.volume_music,
                   ai_game.settings.volume_effects,
                   ai_game.settings.volume_voice]
        for dropdown_slider in name_drop:
            ai_game._volume_reset()
            dropdown_slider.slider_reset_position(volumes[name_drop.
                                                  index(dropdown_slider)])
    elif method == 'save_settings_volume':
        """Сохраняет настройки звука."""
        ai_game.settings.volume_music = ai_game.dropdown_sliders[0].volume
        ai_game.settings.volume_effects = ai_game.dropdown_sliders[1].volume
        ai_game.settings.volume_voice = ai_game.dropdown_sliders[2].volume


def dropdown_button_method(ai_game, method, name_drop, width=None, name=None,
                           texts=None, flag=None):
    """Обработка методов класса Button и создание объектов."""
    if method == 'draw':
        for ai_game.dropdown_button in name_drop:
            ai_game.dropdown_button.draw()
        name_drop[0].draw_name()

    elif method == 'open_close_dropdown':
        for dropdown_button in name_drop:
            open_stats_dropdown_buttons = dropdown_button.open_close_dropdown()
        return open_stats_dropdown_buttons

    elif method == 'collidepoint_mouse_pos':
        for dropdown_button in name_drop:
            response_pressed_button = dropdown_button.collidepoint_mouse_pos()
            if response_pressed_button:
                # очистка неактивных кнопок
                dropdown_button_method(ai_game, method='color_reset',
                                       name_drop=(name_drop),
                                       flag=response_pressed_button
                                       [1])

    elif method == 'new_dropdown_button':
        i = 1
        for text in texts:
            new_dropdown_button = Button(ai_game, text, name, i, width)
            name_drop.append(new_dropdown_button)
            i += 1

    elif method == 'color_reset':
        for dropdown_button in name_drop:
            dropdown_button.color_reset(flag)

    elif method == 'hover_display_name':
        name_drop[0].hover_display_name()

    elif method == 'hover_display_button':
        ai_game.check_intersection = []
        for dropdown_button in name_drop:
            result = dropdown_button.hover_display_button()
            # создания списка для проверки коллизии мышки
            # с кнопками
            ai_game.check_intersection.append(result)

    elif method == 'validation_validity':
        for dropdown_button in name_drop:
            dropdown_button.validation_validity()


def space_menu_method(ai_game, method, name_list, count_star=300):
    """Обратока методов класса Star."""
    if method == 'new_space_menu':
        for _ in range(count_star):
            new_space = Star(ai_game)
            name_list.append(new_space)
    elif method == 'shift_starts':
        for star in name_list:
            star.shift_start_behind_screen(ai_game)
    elif method == 'draw':
        for star in name_list:
            star.draw()
    elif method == '_random_flag_star':
        for star in name_list:
            star.flag = randint(0, 2)


def shot_method(ai_game, method, name_class, name_drop):
    """Обработка методов класса Shot"""
    if method == 'new_shot':
        if name_class == 'ShotHeros':
            new_shot = ShotHeros(ai_game)
            name_drop.append(new_shot)

    if method == 'draw':
        if name_class == 'ShotHeros' and len(name_drop):
            for shot in name_drop:
                shot.draw()

    if method == 'check_bank_shor':
        for shot in name_drop:
            if shot.time_rocket_bang == -1:
                name_drop.remove(shot)
