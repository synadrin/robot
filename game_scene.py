import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from constants import *
from functions import *
import spritesheet
import character
import trigger
import pathfinding


class game_scene(object):
    def __init__(self, manager, engine):
        self._manager = manager
        self._engine = engine

        # True when waiting on the player input (dialogue, menu, etc)
        self._waiting = False

        # Load images for UI
        self._ui_spritesheet = spritesheet.spritesheet('ui.png')
        self._ui_images = self._ui_spritesheet.load_all(
            (0, 0, DEFAULT_SPRITE_WIDTH, DEFAULT_SPRITE_HEIGHT),
            ALPHA_COLOUR
        )

        # Load the default map
        self.load_map(
            DEFAULT_MAP,
            MAP_ENTRANCE,
            self._engine.screen.get_size()
        )

    def load_map(self, name, entrance_name, display_size):
        filename = get_map(name)

        # load data from pytmx
        tmx_data = load_pygame(filename)

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(
            map_data,
            display_size,
            clamp_camera=True,
            tall_sprites=1
        )
        self.map_layer.zoom = 2

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # put the hero in tile with name matching entrance_name
        player_start = tmx_data.get_object_by_name(entrance_name)
        self._engine.hero.position = [player_start.x, player_start.y]

        # add our hero to the group
        self.group.add(self._engine.hero)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        self.npcs = list()
        self.enemies = list()
        self.triggers = list()
        temp_npcs = list()
        # Also a pathfinding grid
        self.pathfinding_grid = pathfinding.weighted_grid(
            tmx_data.width, tmx_data.height)
        for object in tmx_data.objects:
            if object.type == 'wall':
                self.walls.append(pygame.Rect(
                    object.x, object.y,
                    object.width, object.height))
                # Add walls to the pathfinding grid
                grid_x = int(object.x / tmx_data.tilewidth)
                grid_y = int(object.y / tmx_data.tileheight)
                grid_width = int(object.width / tmx_data.tilewidth)
                grid_height = int(object.height / tmx_data.tileheight)
                for y in range(0, grid_height):
                    for x in range(0, grid_width):
                        self.pathfinding_grid.walls.append(
                            (grid_x + x, grid_y + y))
            elif object.type == 'npc' or object.type == 'enemy':
                # Process NPCs and enemies after walls are determined
                temp_npcs.append(object)
            elif object.type == 'trigger':
                self.triggers.append(trigger.trigger(
                    object.x, object.y,
                    object.width, object.height,
                    object.properties))

        # Process NPCs and enemies
        for object in temp_npcs:
            target_grid_x = int(object.target_x)
            target_grid_y = int(object.target_y)
            target_x = target_grid_x * tmx_data.tilewidth
            target_y = target_grid_y * tmx_data.tileheight
            origin_grid_x = int(object.x / tmx_data.tilewidth)
            origin_grid_y = int(object.y / tmx_data.tileheight)
            # Pathfinding
            came_from, cost_so_far = pathfinding.a_star_search(
                self.pathfinding_grid,
                (origin_grid_x, origin_grid_y),
                (target_grid_x, target_grid_y))
            path = pathfinding.reconstruct_path(
                came_from,
                (origin_grid_x, origin_grid_y),
                (target_grid_x, target_grid_y))
            path = [
                (t[0] * tmx_data.tilewidth, t[1] * tmx_data.tileheight)
                for t in path]
            # Load sprite from JSON
            if object.type == 'npc':
                npc = character.npc(object.name, path)
                self.npcs.append(npc)
                self.group.add(npc)
            elif object.type == 'enemy':
                enemy = character.enemy(object.name, path)
                self.enemies.append(enemy)
                self.group.add(enemy)

    def interaction(self):
        index = self._engine.hero.interaction_rect.collidelist(self.npcs)
        # NPC
        if index > -1:
            self.display_text(self.npcs[index].name + ': '
                + self.npcs[index].dialogue)
        else:
            # Events, objects
            index = self._engine.hero.interaction_rect.collidelist(self.triggers)
            if index > -1:
                trigger = self.triggers[index]
                if trigger.on_interact == 'message':
                    self.display_text(trigger.message_text)
                elif trigger.on_interact == 'load_map':
                    self.load_map(
                        trigger.map_name,
                        trigger.entrance_name,
                        self._engine.screen.get_size()
                    )

    def draw_text(self, surface):
        if self._text_set:
            vertical_offset = surface.get_height() * (1 - DIALOG_HEIGHT)
            dialog_box = pygame.Rect(0, vertical_offset, surface.get_width(), 
                surface.get_height() * DIALOG_HEIGHT)
            y = vertical_offset + TEXT_SIZE
            x = TEXT_SIZE
            font = pygame.font.Font(pygame.font.get_default_font(), TEXT_SIZE)

            draw_text_box(surface, dialog_box)
            for line in self._text_set:
                text = font.render(line, 1, TEXT_COLOUR, TEXT_BACKGROUND)
                surface.blit(text, (x, y))
                y += text.get_height()

    def draw_ui(self, surface):
        # Health
        full_count = int(self._engine.hero.health / 2)
        half_count = self._engine.hero.health % 2
        empty_count = int((self._engine.hero.max_health - self._engine.hero.health) / 2)
        for i in range(0, full_count):
            #x = surface.get_width() - ((i / 2 + 1) * self._ui_images[0].get_width())
            x = i * self._ui_images[2].get_width()
            y = 0
            surface.blit(
                self._ui_images[2], (x, y)
            )
        for i in range(0, half_count):
            x = (i + full_count) * self._ui_images[1].get_width()
            y = 0
            surface.blit(
                self._ui_images[1], (x, y)
            )
        for i in range(0, empty_count):
            x = (i + full_count + half_count) * self._ui_images[0].get_width()
            y = 0
            surface.blit(
                self._ui_images[0], (x, y)
            )

    def display_text(self, text):
        self._waiting = True
        if isinstance(text, list):
            self._text_set = text
        else:
            self._text_set = [text]

    def clear_text(self):
        self._waiting = False
        self._text_set = None

    def _button_action(self):
        if self._waiting:
            #TODO: Move to next action
            self.clear_text()
            if self._engine.hero.dead:
                self.running = False
        else:
            self.interaction()

    def _button_attack(self):
        self._engine.hero.attack()

    def _button_up(self):
        print("UP")

    def _button_down(self):
        print("DOWN")

    def _button_left(self):
        print("LEFT")

    def _button_right(self):
        print("RIGHT")

    def handle_input(self, events, pressed_keys):
        poll = pygame.event.poll

        event = poll()
        while event:
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break

#                elif event.key == K_EQUALS:
#                    self.map_layer.zoom += .25
#
#                elif event.key == K_MINUS:
#                    value = self.map_layer.zoom - .25
#                    if value > 0:
#                        self.map_layer.zoom = value
#
#                elif event.key == K_SPACE:
#                    self._button_action()
#
#                elif event.key == K_x:
#                    self._button_attack()
#
#            # this will be handled if the window is resized
#            elif event.type == VIDEORESIZE:
#                scope.resize(event.w, event.h)
#                self.map_layer.set_size((event.w, event.h))
#
            event = poll()
#
#        # using get_pressed is slightly less accurate than testing for events
#        # but is much easier to use.
#        if not self._waiting:
#            pressed = pygame.key.get_pressed()
#            if pressed[K_UP]:
#                self._engine.hero.move_up()
#            elif pressed[K_DOWN]:
#                self._engine.hero.move_down()
#            else:
#                self._engine.hero.stop_moving_vertical()
#
#            if pressed[K_LEFT]:
#                self._engine.hero.move_left()
#            elif pressed[K_RIGHT]:
#                self._engine.hero.move_right()
#            else:
#                self._engine.hero.stop_moving_horizontal()

    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
#                if not self._waiting:
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)
        # Check if NPCs are colliding with the hero
        for npc in self.npcs:
            if npc.feet.colliderect(self._engine.hero.feet):
                npc.move_back(dt)
                self._engine.hero.move_back(dt)
        for enemy in self.enemies:
            if enemy.alive and enemy.rect.colliderect(self._engine.hero.hitbox):
                enemy.take_damage(
                    self._engine.hero.damage,
                    calculate_knockback(
                        self._engine.hero.position, enemy.position,
                        self._engine.hero.weapon.knockback
                    )
                )
                if enemy.dead:
                    enemy.remove(self.group)
            elif enemy.alive and enemy.feet.colliderect(self._engine.hero.feet):
                enemy.move_back(dt)
                self._engine.hero.take_damage(
                    enemy.damage,
                    calculate_knockback(
                        enemy.position, self._engine.hero.position, enemy.knockback
                    )
                )
            enemy.threat_target = self._engine.hero.position
        # If the player is dead, game over
        if self._engine.hero.dead:
            self.game_over()

    def draw(self, surface):
        # center the map/screen on our Hero
        self.group.center(self._engine.hero.rect.center)

        # draw the map and all sprites
        self.group.draw(surface)

        # Draw user interface
        self.draw_ui(surface)

        # Draw text
        self.draw_text(surface)
