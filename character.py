from constants import *
from enum import Enum
import math
import pygame
import spritesheet


class direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 4
    LEFT = 8


class character(pygame.sprite.Sprite):
    """ Character

    Characters have three collision rects, one for the whole sprite "rect" and
    "old_rect", and another to check collisions with walls, called "feet".

    The position list is used because pygame rects are inaccurate for
    positioning sprites; because the values they get are 'rounded down'
    as integers, the sprite would move faster moving left or up.

    Feet is 1/2 as wide as the normal rect, and 1/4 as tall.  This size size
    allows the top of the sprite to overlap walls.  The feet rect is used for
    collisions, while the 'rect' rect is used for drawing.

    There is also an old_rect that is used to reposition the sprite if it
    collides with level walls.
    """

    def __init__(self, filename, width, height, speed, frames = 4):
        pygame.sprite.Sprite.__init__(self)
        self._speed = speed
        self._direction = direction.DOWN

        animation_speed = (HERO_MOVE_SPEED / speed) * HERO_ANIMATION_SPEED
        self._spritesdown = spritesheet.spritestripanim(
            filename, (0, 0, width, height),
            frames, ALPHA_COLOUR, True, animation_speed
        )
        self._spritesleft = spritesheet.spritestripanim(
            filename, (0, height, width, height),
            frames, ALPHA_COLOUR, True, animation_speed
        )
        self._spritesright = spritesheet.spritestripanim(
            filename, (0, 2 * height, width, height),
            frames, ALPHA_COLOUR, True, animation_speed
        )
        self._spritesup = spritesheet.spritestripanim(
            filename, (0, 3 * height, width, height),
            frames, ALPHA_COLOUR, True, animation_speed
        )
        self.image = self._spritesdown.next()
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, self.rect.height / 4)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def stop_moving_vertical(self):
        self.velocity[1] = 0

    def move_up(self):
        self.velocity[1] = -self._speed
        self.image = self._spritesup.next()
        self._direction = direction.UP

    def move_down(self):
        self.velocity[1] = self._speed
        self.image = self._spritesdown.next()
        self._direction = direction.DOWN

    def stop_moving_horizontal(self):
        self.velocity[0] = 0

    def move_left(self):
        self.velocity[0] = -self._speed
        self.image = self._spritesleft.next()
        self._direction = direction.LEFT
    
    def move_right(self):
        self.velocity[0] = self._speed
        self.image = self._spritesright.next()
        self._direction = direction.RIGHT


class npc(character):
    """NPC (Non-Player Character)
    """

    def __init__(self, filename, width, height, speed, frames = 4):
        super().__init__(filename, width, height, speed, frames)
        self._origin = [26 * 32, 35 * 32]
        self._target = [30 * 32, 36 * 32]
        self._returning = False
        self._currentTarget = self._target
        self._threshold = 2
        self.position = self._origin[0], self._origin[1]

    def move_toward(self, targetPosition):
        if math.fabs(targetPosition[0] - self.position[0]) > self._threshold:
            self.stop_moving_vertical()
            if targetPosition[0] > self.position[0]:
                self.move_right()
            else:
                self.move_left()
        elif math.fabs(targetPosition[1] - self.position[1]) > self._threshold:
            self.stop_moving_horizontal()
            if targetPosition[1] > self.position[1]:
                self.move_down()
            else:
                self.move_up()

    def update(self, dt):
        self.move_toward(self._currentTarget)
        super().update(dt)
        deltaX = self.position[0] - self._old_position[0]
        deltaY = self.position[1] - self._old_position[1]
        targetXHit = False
        targetYHit = False
        if math.fabs(self.position[0] - self._currentTarget[0]) < self._threshold:
            self.position[0] = self._currentTarget[0]
            targetXHit = True
        if math.fabs(self.position[1] - self._currentTarget[1]) < self._threshold:
            self.position[1] = self._currentTarget[1]
            targetYHit = True
        if targetXHit and targetYHit:
            self._returning = not self._returning
            if self._returning:
                self._currentTarget = self._origin
            else:
                self._currentTarget = self._target
