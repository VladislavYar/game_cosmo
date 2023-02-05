import pygame


ANGLE_90 = 90
ANGLE_180 = 180
TICK_SPEED = 5000
TICK_STOP = 2500


class Camera():
    """Класс, создания камеры."""

    def __init__(self, ai_game):
        self.heros_speed_up = ai_game.settings.speed_heros_ship_up_object
        self.heros_speed_down = ai_game.settings.speed_heros_ship_down_object
        self.fps = ai_game.FPS
        self.dir_move = 0
        self.check_time = 0
        self.div_up = self.heros_speed_up
        self.div_down = self.heros_speed_down
        self.steep_up = self.heros_speed_up / 48
        self.steep_down = self.heros_speed_down / 48
        self.speed = self.heros_speed_up

    def update(self, object, heros):
        """Перемещает объекты относительно движения главного героя."""

        fps = int(self.fps.get_fps())
        mouse_pos = pygame.mouse.get_pos()

        vector_mouse = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
        vector_heros = pygame.math.Vector2(heros.rect.centerx,
                                           heros.rect.centery)

        angle = pygame.math.Vector2()

        angle = angle.angle_to(vector_mouse-vector_heros)

        if heros.up_flag and self.dir_move != -1:
            self.dir_move = 1
            if self.speed != self.heros_speed_up:
                self.check_time += self.fps.get_time()

            if self.check_time >= TICK_SPEED:
                self.check_time = 0
                self.div_up -= self.steep_up
            self.speed = self.heros_speed_up - self.div_up
            self._move(angle, fps, object, self.speed, 1)

        elif heros.down_flag and self.dir_move != 1:
            self.dir_move = -1
            if self.speed != self.heros_speed_down:
                self.check_time += self.fps.get_time()

            if self.check_time >= TICK_STOP:
                self.check_time = 0
                self.div_down -= self.steep_down
            self.speed = self.heros_speed_down - self.div_down
            self._move(angle, fps, object, self.speed, -1)
        else:
            if self.dir_move == 1:
                self.check_time += self.fps.get_time()
                if (self.check_time >= TICK_SPEED and
                   self.div_up < self.heros_speed_up):
                    self.check_time = 0
                    self.div_up += self.steep_up
                self.speed = self.heros_speed_up - self.div_up
                if self.speed == 0:
                    self.dir_move = 0
                self._move(angle, fps, object, self.speed, 1)
            elif self.dir_move == -1:
                self.check_time += self.fps.get_time()
                if (self.check_time >= TICK_SPEED and
                   self.div_down < self.heros_speed_down):
                    self.check_time = 0
                    self.div_down += self.steep_down
                self.speed = self.heros_speed_down - self.div_down
                if self.speed == 0:
                    self.dir_move = 0
                self._move(angle, fps, object, self.speed, -1)

    def _move(self, angle, fps, object, speed, sign):
        """Перемещение вперёд/назад."""
        if -ANGLE_90 <= angle <= ANGLE_90:
            if angle == 0:
                object.rect.centerx -= (speed *
                                        ANGLE_90) // fps * sign
            elif angle != -ANGLE_90 and angle != ANGLE_90:
                object.rect.centerx -= (speed *
                                        (ANGLE_90 -
                                         abs(angle))) // fps * sign

        elif (-ANGLE_180 < angle < -ANGLE_90 or
              ANGLE_90 < angle <= ANGLE_180):
            if angle == ANGLE_180:
                object.rect.centerx += (speed *
                                        ANGLE_90) // fps * sign
            else:
                object.rect.centerx += (speed *
                                        (abs(angle)
                                         - ANGLE_90)) // fps * sign

        if -ANGLE_180 < angle < 0:
            if angle == -ANGLE_90:
                object.rect.centery += (speed *
                                        (ANGLE_90)) // fps * sign
            elif -ANGLE_90 < angle < 0:
                object.rect.centery += (speed *
                                        abs(angle)) // fps * sign
            elif -ANGLE_180 < angle < -ANGLE_90:
                object.rect.centery += (speed *
                                        (2 * ANGLE_90 -
                                         abs(angle))) // fps * sign
        elif 0 < angle < ANGLE_180:
            if angle == ANGLE_90:
                object.rect.centery -= (speed *
                                        (ANGLE_90)) // fps * sign
            elif 0 < angle < ANGLE_90:
                object.rect.centery -= (speed *
                                        angle) // fps * sign

            elif ANGLE_90 < angle < ANGLE_180:
                object.rect.centery -= (speed *
                                        (2 * ANGLE_90 -
                                         angle)) // fps * sign
