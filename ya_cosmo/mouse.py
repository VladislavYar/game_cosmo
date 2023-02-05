import pygame
import math
from pygame.sprite import Sprite


ANGLE_90 = 90
ANGLE_180 = 180
TICK_SPEED = 50
TICK_STOP = 25
DEV_RADIUS = 30


class Mouse(Sprite):
    """Класс создающий курсор как объект."""

    def __init__(self, ai_game):
        """Инициализирует курсор и задает его начальную позицию."""
        Sprite.__init__(self)
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.coef_screen = self.settings.coef_screen
        self.fps = ai_game.FPS
        self.check_time = 0
        self.coef_rad = 0.3
        self.arc = pygame.Surface((2560, 1440), pygame.SRCALPHA)
        self.color_arc = (237, 118, 14, 100)
        self.color_circle_1 = (250, 0, 100, 20)
        self.color_circle_2 = (250, 0, 100, 100)

        self.rect = pygame.Rect(0, 0, 60 / self.coef_screen,
                                60 / self.coef_screen)
        self.old_pos_mouse = (0, 0)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos

    def draw(self, flag, heros, dir_move):
        """Отрисовка мышки."""
        mouse_pos = pygame.mouse.get_pos()
        self._get_angle(heros, mouse_pos)
        if flag:
            self._angle_miscalculation()
            pygame.mouse.set_pos(self.rect.center)
        else:
            self.old_rect = self.rect

        if heros.up_flag and dir_move != -1:
            self.color_arc = (250, 0, 100, 100)
            self.check_time += self.fps.get_time()
            if self.check_time >= TICK_SPEED and self.coef_rad <= 1.3:
                self.coef_rad += 0.1
                self.check_time = 0
        elif self.coef_rad > 0.3:
            self.color_arc = (237, 118, 14, 80)
            self.check_time += self.fps.get_time()
            if self.check_time >= TICK_STOP:
                self.coef_rad -= 0.1
                self.check_time = 0

        radius = self.angle % 360
        radius = radius / 58

        # очищение экрана
        self.arc.fill((0, 0, 0, 0))

        pygame.draw.circle(self.arc, (self.color_circle_1),
                           self.rect.center, int(self.dist / self.coef_screen
                                                 / DEV_RADIUS))
        pygame.draw.arc(self.arc, self.color_arc,
                        self.rect,
                        -radius - self.coef_rad, -radius + self.coef_rad, 2)
        pygame.draw.circle(self.arc, (self.color_circle_2),
                           self.rect.center, int(self.dist / self.coef_screen
                                                 / DEV_RADIUS),
                           1)
        pygame.draw.circle(self.arc, (self.color_circle_2),
                           self.rect.center, int(3 / self.coef_screen))

        self.screen.blit(self.arc, self.screen_rect.topleft)

    def _angle_miscalculation(self):
        """Просчёт угла и отодвигание курсора с мышкой."""
        if -ANGLE_90 <= self.angle <= 0:
            if self.angle == 0:
                self.rect.centerx = abs(self.old_rect.centerx
                                        + self.coef_shift)
            elif self.angle == -ANGLE_90:
                self.rect.centery = abs(self.old_rect.centery
                                        - self.coef_shift)
            else:
                self.rect.centerx = abs(self.old_rect.centerx
                                        + self.coef_shift)
                self.rect.centery = abs(self.old_rect.centery
                                        - self.coef_shift)
        elif -ANGLE_180 < self.angle < -ANGLE_90:
            self.rect.centerx = abs(self.old_rect.centerx - self.coef_shift)
            self.rect.centery = abs(self.old_rect.centery - self.coef_shift)
        elif 0 < self.angle < ANGLE_90:
            self.rect.centerx = self.old_rect.centerx + self.coef_shift
            self.rect.centery = abs(self.old_rect.centery + self.coef_shift)
        elif ANGLE_90 <= self.angle <= ANGLE_180:
            if self.angle == ANGLE_90:
                self.rect.centery = abs(self.old_rect.centery
                                        + self.coef_shift)
            elif self.angle == ANGLE_180:
                self.rect.centerx = abs(self.old_rect.centerx
                                        - self.coef_shift)
            else:
                self.rect.centerx = abs(self.old_rect.centerx
                                        - self.coef_shift)
                self.rect.centery = abs(self.old_rect.centery
                                        + self.coef_shift)

    def _get_angle(self, heros, mouse_pos):
        """Просчёт угла и расстояния."""
        x = mouse_pos[0] - heros.rect.centerx
        y = mouse_pos[1] - heros.rect.centery

        self.radians = math.atan2(y, x)
        self.angle = math.degrees(self.radians)
        self.dist = math.hypot(x, y)

        self.coef_shift = 200 // self.dist
