import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup
import pyscope

from constants import *
from functions import *
import character


class QuestGame(object):
    """ This class is a basic game.

    This class will load data, create a pyscroll group, a hero object.
    It also reads input and moves the Hero around the map.
    Finally, it uses a pyscroll group to render the map and Hero.
    """
    filename = get_map(MAP_FILENAME)

    def __init__(self):

        # true while running
        self.running = False

        # load data from pytmx
        tmx_data = load_pygame(self.filename)

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(map_data,
            scope.screen.get_size(), clamp_camera=True, tall_sprites=1)
        self.map_layer.zoom = 2

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.hero = character.character(HERO_SPRITESHEET,
            SPRITE_WIDTH, SPRITE_HEIGHT, HERO_MOVE_SPEED)

        # put the hero in tile named "player_start"
        player_start = tmx_data.get_object_by_name('player_start')
        self.hero.position = [player_start.x, player_start.y]

        # add our hero to the group
        self.group.add(self.hero)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        self.npcs = list()
        for object in tmx_data.objects:
            if object.type == 'wall':
                self.walls.append(pygame.Rect(
                    object.x, object.y,
                    object.width, object.height))
            elif object.type == 'sprite':
                # Load sprite from JSON
                target_x = int(object.target_x) * tmx_data.tilewidth
                target_y = int(object.target_y) * tmx_data.tileheight
                npc = character.npc(object.name, [object.x, object.y], [target_x, target_y])
                self.npcs.append(npc)
                self.group.add(npc)

        # List used for displaying lines of text
        self._text_set = []

    def draw_text(self, surface):
        if self._text_set:
            vertical_offset = surface.get_height() * (1 - DIALOG_HEIGHT)
            dialog_box = pygame.Rect(0, vertical_offset, surface.get_width(), 
                surface.get_height() * DIALOG_HEIGHT)
            y = vertical_offset + TEXT_SIZE
            x = TEXT_SIZE
            font = pygame.font.Font(pygame.font.get_default_font(), TEXT_SIZE)

            pygame.draw.rect(surface, DIALOG_BACKGROUND, dialog_box, 0)
            pygame.draw.rect(surface, DIALOG_BORDER, dialog_box, DIALOG_BORDER_THICKNESS)
            for line in self._text_set:
                text = font.render(line, 1, TEXT_COLOUR, TEXT_BACKGROUND)
                surface.blit(text, (x, y))
                y += text.get_height()

    def draw(self, surface):

        # center the map/screen on our Hero
        self.group.center(self.hero.rect.center)

        # draw the map and all sprites
        self.group.draw(surface)

        # Draw text
        self.draw_text(surface)

    def handle_input(self):
        """ Handle pygame input events
        """
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

                elif event.key == K_EQUALS:
                    self.map_layer.zoom += .25

                elif event.key == K_MINUS:
                    value = self.map_layer.zoom - .25
                    if value > 0:
                        self.map_layer.zoom = value

                elif event.key == K_SPACE:
                    #TODO: Interaction
                    index = self.hero.interaction_rect.collidelist(self.npcs)
                    if index > -1:
                        self._text_set.append(self.npcs[index].name + ': '
                            + self.npcs[index].dialogue)

            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                scope.resize(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

            event = poll()

        # using get_pressed is slightly less accurate than testing for events
        # but is much easier to use.
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.hero.move_up()
        elif pressed[K_DOWN]:
            self.hero.move_down()
        else:
            self.hero.stop_moving_vertical()

        if pressed[K_LEFT]:
            self.hero.move_left()
        elif pressed[K_RIGHT]:
            self.hero.move_right()
        else:
            self.hero.stop_moving_horizontal()

    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)
        # Check if NPCs are colliding with the hero
        for npc in self.npcs:
            if npc.feet.colliderect(self.hero.feet):
                npc.move_back(dt)
                self.hero.move_back(dt)

    def run(self):
        """ Run the game loop
        """
        clock = pygame.time.Clock()
        self.running = True

        from collections import deque
        times = deque(maxlen=30)

        try:
            while self.running:
                dt = clock.tick(120) / 1000.
                times.append(clock.get_fps())

                self.handle_input()
                self.update(dt)
                self.draw(scope.screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    scope = pyscope.pyscope()
    pygame.display.set_caption(DISPLAY_NAME)

    try:
        game = QuestGame()
        game.run()
    except:
        pygame.quit()
        raise
