from enum import Enum
import copy
import json
import math
import os.path
import random

import pygame

from constants import *
import spritesheet


class direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 4
    LEFT = 8


class base_sprite(pygame.sprite.Sprite):
    def __init__(self, prefix, filename):
        pygame.sprite.Sprite.__init__(self)

        with open(os.path.join(RESOURCES_DIR, prefix + '_' + filename + '.json'), 'r') as f:
            sprite_info = json.load(f)
        self._prefix = prefix
        self._filename = filename

        self._name = sprite_info['name'] \
            if 'name' in sprite_info else '?????'
        self._spritesheet_filename = sprite_info['spritesheet'] \
            if 'spritesheet' in sprite_info else None
        self._spritesheet = spritesheet.spritesheet(
            self._spritesheet_filename
        )
        self._sprite_width = sprite_info['sprite_width'] \
            if 'sprite_width' in sprite_info else DEFAULT_SPRITE_WIDTH
        self._sprite_height = sprite_info['sprite_height'] \
            if 'sprite_height' in sprite_info else DEFAULT_SPRITE_HEIGHT
        self._animation_speed = sprite_info['animation_speed'] \
            if 'animation_speed' in sprite_info else 0
        self._frames = sprite_info['frames_per_row'] \
            if 'frames_per_row' in sprite_info else None
        self._properties = sprite_info

    @property
    def image(self):
        return self._image

    @property
    def animation_frames(self):
        return self._animation_speed * TARGET_FPS


class character(base_sprite):
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

    def __init__(self, filename):
        super().__init__('c', filename)

        move_speed = self._properties['move_speed'] \
            if 'move_speed' in self._properties else 1.0

        self._speed = move_speed * BASE_MOVE_SPEED
        self._direction = direction.DOWN

        if self._animation_speed <= 0:
            self._animation_speed = (1.0 / move_speed) * BASE_ANIMATION_SPEED

        self._spritesdown = spritesheet.spritestripanim(
            self._spritesheet_filename,
            (0, 0, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR, True, self.animation_frames
        )
        self._spritesleft = spritesheet.spritestripanim(
            self._spritesheet_filename,
            (0, self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR, True, self.animation_frames
        )
        self._spritesright = spritesheet.spritestripanim(
            self._spritesheet_filename,
            (0, 2 * self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR, True, self.animation_frames
        )
        self._spritesup = spritesheet.spritestripanim(
            self._spritesheet_filename,
            (0, 3 * self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR, True, self.animation_frames
        )
        self._image = self._spritesdown.next()
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, self.rect.height / 4)
        self._movement_blocked_timer = 0.0

        self.max_health = self._properties['health'] \
            if 'health' in self._properties else 1
        self._current_health = self.max_health


    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    @property
    def movement_blocked(self):
        return self._movement_blocked_timer > 0

    @property
    def health(self):
        return self._current_health

    @health.setter
    def health(self, value):
        self._current_health = max(value, 0)
        self._current_health = min(self._current_health, self.max_health)

    def update_movement_blocked(self, dt):
        self._movement_blocked_timer -= dt
        if self._movement_blocked_timer < 0:
            self._movement_blocked_timer = 0.0

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        self.update_movement_blocked(dt)

    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def stop_moving_vertical(self):
        if not self.movement_blocked:
            self.velocity[1] = 0

    def move_up(self):
        if not self.movement_blocked:
            self.velocity[1] = -self._speed
            self._image = self._spritesup.next()
            self._direction = direction.UP

    def move_down(self):
        if not self.movement_blocked:
            self.velocity[1] = self._speed
            self._image = self._spritesdown.next()
            self._direction = direction.DOWN

    def stop_moving_horizontal(self):
        if not self.movement_blocked:
            self.velocity[0] = 0

    def move_left(self):
        if not self.movement_blocked:
            self.velocity[0] = -self._speed
            self._image = self._spritesleft.next()
            self._direction = direction.LEFT

    def move_right(self):
        if not self.movement_blocked:
            self.velocity[0] = self._speed
            self._image = self._spritesright.next()
            self._direction = direction.RIGHT

    def stop_moving(self):
        self.stop_moving_horizontal()
        self.stop_moving_vertical()

    def block_movement(self, duration):
        self._movement_blocked_timer = duration


class weapon(base_sprite):
    def __init__(self, filename):
        super().__init__('w', filename)

        self._direction = direction.DOWN

        self.speed = self._properties['speed'] \
            if 'speed' in self._properties else WEAPON_SPEED_MIN
        self.knockback = self._properties['knockback'] \
            if 'knockback' in self._properties else 0
        self._min_damage = self._properties['min_damage'] \
            if 'min_damage' in self._properties else 1
        self._max_damage = self._properties['max_damage'] \
            if 'max_damage' in self._properties else 1

        self._hitboxes = {}
        if 'hitbox' in self._properties:
            x = self._properties['hitbox']['x']
            y = self._properties['hitbox']['y']
            w = self._properties['hitbox']['width']
            h = self._properties['hitbox']['height']
            self._hitboxes[direction.DOWN] = pygame.Rect(
                (-x - w), (-y + h), w, h
            )
            self._hitboxes[direction.LEFT] = pygame.Rect(
                -y, (-x - w), h, w
            )
            self._hitboxes[direction.RIGHT] = pygame.Rect(
                (-y + h), x, h, w
            )
            self._hitboxes[direction.UP] = pygame.Rect(
                x, -y, w, h
            )
        else:
            raise KeyError("Weapon missing hitbox")

        self.sprites = {}
        self.sprites[direction.DOWN] = self._spritesheet.load_strip(
            (0, self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR
        )
        self.sprites[direction.LEFT] = self._spritesheet.load_strip(
            (0, 2 * self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR
        )
        self.sprites[direction.RIGHT] = self._spritesheet.load_strip(
            (0, 3 * self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR
        )
        self.sprites[direction.UP] = self._spritesheet.load_strip(
            (0, 4 * self._sprite_height, self._sprite_width, self._sprite_height),
            self._frames, ALPHA_COLOUR
        )

        self._timer = 0.0
        self._current_image_index = 0
        self._image = self.sprites[self._direction][self._current_image_index]

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = max(value, WEAPON_SPEED_MIN)
        self._speed = min(self._speed, WEAPON_SPEED_MAX)

        speed_increment = (WEAPON_SPEED_SLOWEST - WEAPON_SPEED_FASTEST) \
            / (WEAPON_SPEED_MAX - WEAPON_SPEED_MIN)
        self._animation_speed = WEAPON_SPEED_SLOWEST \
            - ((self._speed - 1) * speed_increment)

    @property
    def damage(self):
        return random.randint(self._min_damage, self._max_damage)

    @property
    def attacking(self):
        return self._timer > 0

    @property
    def current_image_index(self):
        return self._current_image_index

    @current_image_index.setter
    def current_image_index(self, value):
        self._current_image_index = max(value, 0)
        self._current_image_index = min(
            self._current_image_index, self._frames - 1
        )

    @property
    def hitbox(self):
        return self._hitboxes[self._direction]

    def attack(self, direction):
        self._direction = direction
        self._timer = self._animation_speed

    def update(self, dt):
        if self.attacking:
            self._timer -= dt
            if self._timer < 0:
                self._timer = 0
            time_passed = self._animation_speed - self._timer
            self.current_image_index = math.floor(
                time_passed / (self._animation_speed / self._frames)
            )
            self._image = self.sprites[self._direction][self.current_image_index]


class player(character):
    def __init__(self, filename):
        self._invulnerability_timer = 0.0
        super().__init__(filename)
        self.interaction_rect = pygame.Rect(
            0, 0, self.rect.width * 0.5, self.rect.height
        )

        self.weapon = weapon(self._properties['weapon']) \
            if 'weapon' in self._properties else None

        # Sprite used for "blinking" when damaged
        self._blink_image = pygame.Surface(
            (self._sprite_width, self._sprite_height)
        ).convert()
        self._blink_image.fill(ALPHA_COLOUR)
        self._blink_image.set_colorkey(ALPHA_COLOUR)

        # Attacking sprites
        self._attacking_sprites = {}
        self._attacking_sprites[direction.DOWN] = self._spritesheet.image_at(
            (
                self._frames * self._sprite_width, 0,
                self._sprite_width, self._sprite_height
            ), ALPHA_COLOUR
        )
        self._attacking_sprites[direction.LEFT] = self._spritesheet.image_at(
            (
                self._frames * self._sprite_width, self._sprite_height,
                self._sprite_width, self._sprite_height
            ), ALPHA_COLOUR
        )
        self._attacking_sprites[direction.RIGHT] = self._spritesheet.image_at(
            (
                self._frames * self._sprite_width, 2 * self._sprite_height,
                self._sprite_width, self._sprite_height
            ), ALPHA_COLOUR
        )
        self._attacking_sprites[direction.UP] = self._spritesheet.image_at(
            (
                self._frames * self._sprite_width, 3 * self._sprite_height,
                self._sprite_width, self._sprite_height
            ), ALPHA_COLOUR
        )

    @property
    def image(self):
        if self.invulnerable and int(self._invulnerability_timer * 10) % 2 == 0:
            return self._blink_image
        else:
            if self.attacking:
                if self._direction == direction.UP:
                    image = copy.copy(self.weapon.image)
                    image.blit(self._attacking_sprites[self._direction], (0, 0))
                else:
                    image = copy.copy(self._attacking_sprites[self._direction])
                    image.blit(self.weapon.image, (0, 0))
            else:
                image = super().image
            return image

    @property
    def movement_blocked(self):
        return super().movement_blocked or self.attacking

    @property
    def invulnerable(self):
        return self._invulnerability_timer > 0

    @property
    def attacking(self):
        try:
            return self.weapon.attacking
        except AttributeError:
            return False

    @property
    def hitbox(self):
        if self.attacking:
            return pygame.Rect(
                self.rect.centerx + self.weapon.hitbox.x,
                self.rect.centery + self.weapon.hitbox.y,
                self.weapon.hitbox.width,
                self.weapon.hitbox.height
            )
        else:
            return pygame.Rect(0, 0, 0, 0)

    @property
    def damage(self):
        return self.weapon.damage if self.weapon else 0

    def update_interaction_rect(self):
        self.interaction_rect.topleft = self._position[:]
        self.interaction_rect.size = (self.rect.width, self.rect.height)
        if self._direction == direction.UP:
            self.interaction_rect.height *= 0.5
            self.interaction_rect.y -= self.interaction_rect.height
        elif self._direction == direction.DOWN:
            self.interaction_rect.height *= 0.5
            self.interaction_rect.y += self.rect.height + self.interaction_rect.height
        elif self._direction == direction.LEFT:
            self.interaction_rect.width *= 0.5
            self.interaction_rect.x -= self.interaction_rect.width
        elif self._direction == direction.RIGHT:
            self.interaction_rect.width *= 0.5
            self.interaction_rect.x += self.rect.width + self.interaction_rect.width

    def update_invulerability(self, dt):
        self._invulnerability_timer -= dt
        if self._invulnerability_timer < 0:
            self._invulnerability_timer = 0.0

    def update(self, dt):
        super().update(dt)
        self.update_interaction_rect()
        self.update_invulerability(dt)
        self.weapon.update(dt)

    def move_back(self, dt):
        super().move_back(dt)
        self.update_interaction_rect()

    def take_damage(self, damage, knockback):
        if not self.invulnerable:
            self.health -= damage
            self.block_movement(KNOCKBACK_TIME)
            self._invulnerability_timer = INVULNERABILITY_TIME
            self.velocity[0] = knockback[0]
            self.velocity[1] = knockback[1]

    def attack(self):
        if not self.movement_blocked:
            self.stop_moving()
            self.weapon.attack(self._direction)


class npc(character):
    """NPC (Non-Player Character)
    """

    def __init__(self, filename, path):
        super().__init__(filename)

        self._path = path
        self._path_index = 0
        self._origin = self._path[self._path_index]
        if self.moving:
            self._goal = self._path[-1]
            self._path_incrementer = 1
            self._current_goal_index = self._path_index + self._path_incrementer
        else:
            self._current_goal_index = 0
        self._threshold = 1
        self.position = self._origin[0], self._origin[1]

        self._dialogue = self._properties['dialogue'] \
            if 'dialogue' in self._properties else []

    @property
    def dialogue(self):
        if self._dialogue:
            return random.choice(self._dialogue)
        else:
            return '...'

    @property
    def name(self):
        return self._name

    @property
    def moving(self):
        # Path with more than one node means the character is moving
        return len(self._path) > 1

    @property
    def current_goal(self):
        return self._path[self._current_goal_index]

    def is_close_enough(self, goal):
        x_matches = math.fabs(self.position[0] - goal[0]) < self._threshold
        y_matches = math.fabs(self.position[1] - goal[1]) < self._threshold

        return x_matches, y_matches

    def is_goal_hit(self, goal):
        x_matches, y_matches = self.is_close_enough(goal)
        goal_x_hit = (self.velocity[0] == 0 and x_matches) \
            or (self.velocity[0] > 0 and self.position[0] >= goal[0]) \
            or (self.velocity[0] < 0 and self.position[0] <= goal[0])
        goal_y_hit = (self.velocity[1] == 0 and y_matches) \
            or (self.velocity[1] > 0 and self.position[1] >= goal[1]) \
            or (self.velocity[1] < 0 and self.position[1] <= goal[1])

        return goal_x_hit, goal_y_hit

    def move_toward(self, goal):
        x_matches, y_matches = self.is_close_enough(goal)
        if not x_matches:
            #self.stop_moving_vertical()
            if goal[0] > self.position[0]:
                self.move_right()
            else:
                self.move_left()
        if not y_matches:
            #self.stop_moving_horizontal()
            if goal[1] > self.position[1]:
                self.move_down()
            else:
                self.move_up()

    def next_goal(self):
        self._path_index = self._current_goal_index
        next_goal_index = self._path_index + self._path_incrementer
        if not 0 <= next_goal_index < len(self._path):
            self._path_incrementer *= -1
            next_goal_index = self._path_index + self._path_incrementer
        self._current_goal_index = next_goal_index

    def update(self, dt):
        if self.moving:
            self.stop_moving()
            self.move_toward(self.current_goal)

        super().update(dt)

        if self.moving:
            goal_x_hit, goal_y_hit = self.is_goal_hit(
                self.current_goal
            )

            if goal_x_hit:
                self.position[0] = self.current_goal[0]
            if goal_y_hit:
                self.position[1] = self.current_goal[1]

            if goal_x_hit and goal_y_hit:
                self.next_goal()


class enemy(npc):
    def __init__(self, filename, path):
        super().__init__(filename, path)
        self._min_damage = self._properties['min_damage'] \
            if 'min_damage' in self._properties else 0
        self._max_damage = self._properties['max_damage'] \
            if 'max_damage' in self._properties else 0
        self._threat_range = self._properties['threat_range'] \
            if 'threat_range' in self._properties else 0
        self.knockback = self._properties['knockback'] \
            if 'knockback' in self._properties else 0
        self.threat_target = None

    @property
    def current_goal(self):
        if self.threat_target and self.in_threat_range(self.threat_target):
            return self.threat_target
        else:
            return super().current_goal

    @property
    def damage(self):
        return random.randint(self._min_damage, self._max_damage)

    def in_threat_range(self, target):
        delta_x = math.fabs(target[0] - self.position[0])
        delta_y = math.fabs(target[1] - self.position[1])
        return math.sqrt(delta_x**2 + delta_y**2) <= self._threat_range

    def take_damage(self, damage, knockback):
        self.health -= damage
        self.block_movement(KNOCKBACK_TIME)
        self.velocity[0] = knockback[0]
        self.velocity[1] = knockback[1]
