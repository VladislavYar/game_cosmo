import pygame
from pygame.sprite import Sprite
from random import randint
import math

from methods import scale_images
from ship import COEF_DEV


TICK_ANIM = 150
TICK_BANG = 100
ANGLE_90 = 90
ANGLE_180 = 180


class ShotHeros(Sprite):
    """Класс создающий выстрел героя."""

    def __init__(self, ai_game):
        """Инициализирует выстрел и задает его начальную позицию."""
        Sprite.__init__(self)
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.coef_screen = self.settings.coef_screen
        self.min_dist = 30 * self.coef_screen
        self.rand = round(1 / self.coef_screen)
        self.speed_shot = ai_game.settings.speed_shot_heros
        self.heros = ai_game.heros_ship
        self.flag_move_forward = ai_game.heros_ship.up_flag
        self.flag_move_back = ai_game.heros_ship.down_flag
        self.speed = ai_game.camera.speed
        self.fps = ai_game.FPS
        self.calculation_logic_flag = True
        self.time_one_sprite = 0
        self.time_rocket_bang = 0
        self.i = 0

        self.braking_speed = (self.settings.speed_heros_ship_up_object
                              - ai_game.camera.div_up)

        self.mouse_pos = pygame.mouse.get_pos()

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.rect.center = self.heros.rect.center

        self.images = [pygame.image.load('images/shots/'
                                         f'shot_heros/fire/{i}.png')
                       for i in range(1, 12)]

        self.images = scale_images(self.coef_screen, self.images)

        self.orig_images = self.images

        self._calculation_rand_displacement()

        self._rotate_shot()

        self._overall_speed()

        self._calculating_dist_ship_to_mouse()

    def draw(self):
        """Отрисовка выстрела."""
        self._move_shot()

        self._calculating_sprite_output()

        self.screen.blit(self.images[self.i],
                         self.rect)

    def _overall_speed(self):
        """Метод просчёта скрости выстрела."""
        pass

    def _rotate_shot(self):
        """Просчёт угла выстрела относительно мышки."""
        self._calculating_distance_X_Y_to_mouse()

        self.initial_radians = math.atan2(self.y, self.x)
        self.angle = math.degrees(self.initial_radians)

        i = 0
        new_images = []
        for sprite in self.images:
            sprite = pygame.transform.rotate(self.orig_images[i], -self.angle
                                             - ANGLE_90)
            new_images.append(sprite)
            i += 1

        self.images = new_images

        self._correct_rect()

    def _move_shot(self):
        """Просчёт движения выстрела."""
        self._speed_miscalculation()

        self._calculating_distance_X_Y_to_mouse()

        radians = math.atan2(self.y, self.x)
        dist = math.hypot(self.y, self.x)

        if dist > self.min_dist and self.calculation_logic_flag:
            self.rect.centerx += (self.speed * math.cos(radians))
            self.rect.centery += (self.speed * math.sin(radians))
        else:
            self.calculation_logic_flag = False
            self.rect.centerx += (self.speed * math.cos(self.initial_radians))
            self.rect.centery += (self.speed * math.sin(self.initial_radians))

    def _calculation_rand_displacement(self):
        """Создание рандомного коэффициента угла."""
        if self.flag_move_forward:
            self.rand_x = randint(0 - self.rand * 5, 0 + self.rand * 5)
            self.rand_y = randint(0 - self.rand * 5, 0 + self.rand * 5)
        else:
            self.rand_x = randint(0 - self.rand * 2, 0 + self.rand * 2)
            self.rand_y = randint(0 - self.rand * 2, 0 + self.rand * 2)

    def _correct_rect(self):
        """Корректировка выстрела в зависимости от угла."""
        coefs = {1440: 5, 1080: 6, 900: 7, 768: 8, 720: 9}
        coef = coefs[self.settings.screen_height]

        correct_x = 0
        correct_y = 0
        if ANGLE_90 < self.angle < ANGLE_180:
            correct_x = (abs(self.angle - ANGLE_90) /
                         self.coef_screen / coef)
        elif -ANGLE_90 < self.angle < 0:
            correct_y = (abs(self.angle) /
                         self.coef_screen / coef)

        self.rect.centerx -= correct_x
        self.rect.centery -= correct_y

    def _speed_miscalculation(self):
        """Просчёт скорости и уменьшение при взрыве."""
        fps = self.fps.get_fps()

        if self.time_rocket_bang >= TICK_BANG and self.i > 3:
            self.speed_shot = self.speed_shot / 1.05

        if self.flag_move_forward:
            self.speed = (
                          self.dist_ship_to_mouse *
                          self.settings.speed_heros_ship_up /
                          fps / self.coef_screen /
                          self.coef_screen // COEF_DEV +
                          self.speed_shot /
                          fps // self.coef_screen +
                          self.settings.speed_heros_ship_up_object * 1.3
            )
        elif self.flag_move_back:
            self.speed = (
                          - self.dist_ship_to_mouse *
                          self.settings.speed_heros_ship_down /
                          fps / self.coef_screen /
                          self.coef_screen // COEF_DEV +
                          self.speed_shot /
                          fps // self.coef_screen -
                          self.settings.speed_heros_ship_down_object * 1.3
            )
        else:
            self.speed = (
                        self.speed_shot
                        / fps // self.coef_screen + self.braking_speed
            )

    def _calculating_distance_X_Y_to_mouse(self):
        """Расстояние до курсора мышки по координатам X Y."""
        self.x = self.mouse_pos[0] - self.rect.centerx + self.rand_x
        self.y = self.mouse_pos[1] - self.rect.centery + self.rand_y

    def _calculating_sprite_output(self):
        """Просчёт спрайта для вывода."""
        self.time_one_sprite += self.fps.get_time()

        if self.time_rocket_bang >= TICK_BANG:
            if self.time_one_sprite >= TICK_ANIM:
                self.i += 1
                self.time_one_sprite = 0
            if self.i == len(self.images) - 1:
                self.time_rocket_bang = -1

        elif self.time_one_sprite >= TICK_ANIM:
            self.i += 1
            if self.i == 4:
                self.i = 0
            self.time_rocket_bang += self.time_one_sprite
            self.time_one_sprite = 0

    def _calculating_dist_ship_to_mouse(self):
        """Расстояние от корабля до мышки."""
        self._calculating_distance_X_Y_to_mouse()
        self.dist_ship_to_mouse = math.hypot(self.y, self.x)
        if self.dist_ship_to_mouse < 155:
            self.dist_ship_to_mouse = 1
