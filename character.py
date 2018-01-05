from enum import Enum
import math
import os.path
import json
import random

import pygame

from constants import *
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

    def __init__(self, filename, width, height, move_speed, animation_speed=0, frames=4):
        pygame.sprite.Sprite.__init__(self)
        self._speed = move_speed
        self._direction = direction.DOWN

        if animation_speed < 1:
            animation_speed = (HERO_MOVE_SPEED / move_speed) * HERO_ANIMATION_SPEED

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
        self.interaction_rect = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update_interaction_rect(self):
        self.interaction_rect.topleft = self._position[:]
        self.interaction_rect.size = (self.rect.width, self.rect.height)
        if self._direction == direction.UP:
            self.interaction_rect.height *= 0.5
            self.interaction_rect.y -= self.interaction_rect.height
        elif self._direction == direction.DOWN:
            self.interaction_rect.height *= 0.5
            self.interaction_rect.y += self.interaction_rect.height
        elif self._direction == direction.LEFT:
            self.interaction_rect.width *= 0.5
            self.interaction_rect.x -= self.interaction_rect.width
        elif self._direction == direction.RIGHT:
            self.interaction_rect.width *= 0.5
            self.interaction_rect.x += self.interaction_rect.width

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        self.update_interaction_rect()

    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        self.update_interaction_rect()

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

    def __init__(self, filename, path):
        with open(os.path.join(RESOURCES_DIR, 'c_' + filename + '.json'), 'r') as f:
            sprite_info = json.load(f)
        self._filename = filename
        animation_speed = sprite_info['animation_speed'] if 'animation_speed' in sprite_info else 0
        frames = sprite_info['frames_per_row'] if 'frames_per_row' in sprite_info else None
        super().__init__(sprite_info['spritesheet'], sprite_info['sprite_width'],
            sprite_info['sprite_height'], sprite_info['move_speed'], animation_speed, frames)

        self._path = path
        # Path with more than one node means the character is moving
        self._moving = len(self._path) > 1
        self._path_index = 0
        self._origin = self._path[self._path_index]
        if self._moving:
            self._goal = self._path[-1]
            self._path_incrementer = 1
            self._current_goal_index = self._path_index + self._path_incrementer
        else:
            self._current_goal_index = 0
        self._threshold = 2
        self.position = self._origin[0], self._origin[1]

        self._name = sprite_info['name'] if 'name' in sprite_info else '?????'
        self._dialogue = sprite_info['dialogue'] if 'dialogue' in sprite_info else []

    @property
    def dialogue(self):
        if self._dialogue:
            return random.choice(self._dialogue)
        else:
            return '...'

    @property
    def name(self):
        return self._name

    def move_toward(self, goal):
        if self._moving:
            if math.fabs(goal[0] - self.position[0]) > self._threshold:
                self.stop_moving_vertical()
                if goal[0] > self.position[0]:
                    self.move_right()
                else:
                    self.move_left()
            elif math.fabs(goal[1] - self.position[1]) > self._threshold:
                self.stop_moving_horizontal()
                if goal[1] > self.position[1]:
                    self.move_down()
                else:
                    self.move_up()

    def update(self, dt):
        self.move_toward(self._path[self._current_goal_index])
        super().update(dt)

        if self._moving:
            delta_x = self.position[0] - self._old_position[0]
            delta_y = self.position[1] - self._old_position[1]
            goal_x_hit = False
            goal_y_hit = False
            current_goal = self._path[self._current_goal_index]
            if math.fabs(self.position[0] - current_goal[0]) < self._threshold:
                self.position[0] = current_goal[0]
                goal_x_hit = True
            if math.fabs(self.position[1] - current_goal[1]) < self._threshold:
                self.position[1] = current_goal[1]
                goal_y_hit = True

            if goal_x_hit and goal_y_hit:
                self._path_index = self._current_goal_index
                next_goal_index = self._path_index + self._path_incrementer
                if not 0 <= next_goal_index < len(self._path):
                    self._path_incrementer *= -1
                    next_goal_index = self._path_index + self._path_incrementer
                self._current_goal_index = next_goal_index
