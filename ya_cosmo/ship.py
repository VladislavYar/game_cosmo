import pygame
from pygame.math import Vector2

from methods import scale_images

ANGLE_90 = 90
COEF_DEV = 150
TICK_ENGINES = 100


class ShipCharacter():
    """Класс создающий корабль героя."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.coef_screen = self.settings.coef_screen
        self.radius = 20 // self.coef_screen
        self.fps = ai_game.FPS
        self.tick_engines_check = 0
        self.angle = 1
        self.i = 0

        # cоздание флагов перемещения корабля
        self.up_flag = False
        self.down_flag = False

        # допустипые границы вылета корабля
        permissible_departure = self.screen_rect.height // 300
        self.border_top = 0 - permissible_departure
        self.border_bot = self.screen_rect.height + permissible_departure
        self.border_left = 0 - permissible_departure
        self.border_right = self.screen_rect.width + permissible_departure

        # загрузка изображения корабля главного героя
        self.image = pygame.image.load('images/ships/'
                                       'heros_ship/heros_ship.png')

        # загрузка спрайтов выстрела
        self.engines_1 = [pygame.image.load('images/ships/heros_ship/engine/'
                          f'/speed_1/{i}.png')
                          for i in range(1, 5)]
        self.engines_2 = [pygame.image.load('images/ships/heros_ship/engine/'
                          f'/speed_2/{i}.png')
                          for i in range(1, 5)]
        self.engines_3 = [pygame.image.load('images/ships/heros_ship/engine/'
                          f'/speed_3/{i}.png')
                          for i in range(1, 5)]
        self.engines_4 = [pygame.image.load('images/ships/heros_ship/engine/'
                          f'/speed_4/{i}.png')
                          for i in range(1, 5)]
        self.engines_down = [pygame.image.load('images/ships/heros_ship/'
                             f'engine/speed_down/{i}.png')
                             for i in range(1, 4)]

        # апскейлит изображение под разрешение экрана
        # и назначение атрибута rect
        (self.image, self.engines_1, self.engines_2,
         self.engines_3, self.engines_4,
         self.engines_down) = scale_images(
                                           self.coef_screen, self.image,
                                           self.engines_1, self.engines_2,
                                           self.engines_3, self.engines_4,
                                           self.engines_down
                                           )

        # сохранение исходного изображения
        self.orig_image = self.image
        self.orig_engines_1 = self.engines_1
        self.orig_engines_2 = self.engines_2
        self.orig_engines_3 = self.engines_3
        self.orig_engines_4 = self.engines_4
        self.orig_engines_down = self.engines_down

        # корабль появляется в центре экрана
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect_engines = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        """Отрисовка корабля."""
        self.tick_engines_check += self.fps.get_time()
        if (self.tick_engines_check >= TICK_ENGINES):
            self.tick_engines_check = 0
            if self.i < len(self.engines_rendering):
                self.i += 1
            else:
                self.i = 0
        if self.i >= len(self.engines_rendering):
            self.i = 0

        self.screen.blit(self.engines_rendering[self.i],
                         self.rect_engines)
        self.screen.blit(self.image, self.rect)

    def correct_rect_engines(self):
        """Корректировка положения выхлопа двигателя."""
        center = (pygame.math.Vector2(self.rect.center) +
                  pygame.math.Vector2(0, -self.radius).rotate(self.angle
                                                              - ANGLE_90))
        self.rect_engines = (self.engines_rendering[0].
                             get_rect(center=(round(center.x), round(center.y))
                                      )
                             )

    def check_speed(self, speed):
        """Проверка скорости корабля и назначение соотвествующего выхлопа."""
        if self.up_flag:
            if speed == self.settings.speed_heros_ship_up_object:
                self.engines_rendering = self.engines_4
                self.orig_engines_rendering = self.orig_engines_4
            elif speed >= self.settings.speed_heros_ship_up_object / 1.5:
                self.engines_rendering = self.engines_3
                self.orig_engines_rendering = self.orig_engines_3
            elif speed >= self.settings.speed_heros_ship_up_object / 3:
                self.engines_rendering = self.engines_2
                self.orig_engines_rendering = self.orig_engines_2
            else:
                self.engines_rendering = self.engines_1
                self.orig_engines_rendering = self.orig_engines_1
        elif self.down_flag:
            self.engines_rendering = self.engines_down
            self.orig_engines_rendering = self.orig_engines_down
        else:
            self.engines_rendering = self.engines_1
            self.orig_engines_rendering = self.orig_engines_1

    def moving_active_deactive_ship(self, button, flag):
        """Активация, деактивация, перемещения корабля в пространстве."""
        if button == 'up':
            self.up_flag = flag
        elif button == 'down':
            self.down_flag = flag

    def update(self):
        """Перемещение корабля в пространстве."""
        mouse_pos = pygame.mouse.get_pos()
        fps = int(self.fps.get_fps())
        if fps == 0:
            fps = 1
        distance_x = mouse_pos[0] - self.rect.centerx
        distance_y = mouse_pos[1] - self.rect.centery

        if (abs(distance_x) > 120 / self.coef_screen
           or abs(distance_y) > 120 / self.coef_screen):
            flag_dist = self._dist_miscalculation(mouse_pos)

            if self.up_flag and flag_dist:
                # уможение на дистанцию создаёт
                #  эффект ускорения при отдалении мыши
                move_y = (distance_y * self.settings.speed_heros_ship_up /
                          self.coef_screen / fps // COEF_DEV)
                move_x = (distance_x * self.settings.speed_heros_ship_up /
                          self.coef_screen / fps // COEF_DEV)
                self._move(move_y, move_x)
            elif self.down_flag and flag_dist:
                move_y = -(distance_y * self.settings.speed_heros_ship_down /
                           self.coef_screen / fps //
                           COEF_DEV)
                move_x = -(distance_x * self.settings.speed_heros_ship_down /
                           self.coef_screen / fps //
                           COEF_DEV)
                self._move(move_y, move_x)

            if (self.border_left > self.rect.centerx or
                self.rect.centerx > self.border_right or
                self.border_top > self.rect.centery or
               self.rect.centery > self.border_bot):
                self.rect.centery = self.old_rect_y
                self.rect.centerx = self.old_rect_x
            else:
                self.old_rect_y = self.rect.centery
                self.old_rect_x = self.rect.centerx

    def _move(self, move_y, move_x):
        """Сохранение вычисления в переменных."""
        self.rect.centery = self.rect.centery + move_y
        self.rect.centerx = self.rect.centerx + move_x

    def rotate_heros_ship(self):
        """Поворот относительно мышки."""
        vector_x = self.rect.centerx
        vector_y = self.rect.centery
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = Vector2(mouse_pos[0], mouse_pos[1]) - Vector2(vector_x,
                                                                  vector_y)
        radius, self.angle = mouse_pos.as_polar()
        self.image = pygame.transform.rotate(self.orig_image, -self.angle
                                             - ANGLE_90)

        i = 0
        new_engines = []
        for sprite in self.engines_rendering:
            sprite = pygame.transform.rotate(self.orig_engines_rendering[i],
                                             -self.angle - ANGLE_90)
            new_engines.append(sprite)
            i += 1

        self.engines_rendering = new_engines

        self.rect = self.image.get_rect(center=self.rect.center)

    def _dist_miscalculation(self, mouse_pos):
        "Просчёт расстояния до курсора c помощью векторов."
        vector_mouse = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
        vector_heros = pygame.math.Vector2(self.rect.centerx,
                                           self.rect.centery)
        dist = vector_mouse.distance_to(vector_heros)

        flag = False
        if dist > self.rect.width:
            flag = True

        return flag
