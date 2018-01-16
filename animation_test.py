import pygame
import pyscope

from constants import *
import spritesheet


'''
SPRITESHEET_FILENAME = 'robie-power-on.png'
SPRITE_WIDTH = 320
SPRITE_HEIGHT = 320
FRAMES = [
    [0, 2],
    [1, 0.1],
    [0, 1.5],
    [1, 0.1],
    [0, 1.5],
    [1, 0.1],
    [0, 0.1],
    [1, 0.1],
    [0, 0.1],
    [1, 0.1],
    [0, 0.1],
    [1, 0.1],
    [0, 0.1],
    [0, 0.1],
    [1, 0.1],
    [2, 0.25],
    [3, 0.25],
    [4, 0.25],
    [5, 10]
]
'''
SPRITESHEET_FILENAME = 'arm-swing.png'
SPRITE_WIDTH = 320
SPRITE_HEIGHT = 320
FRAMES = [
    [0, 2],
    [1, 0.1],
    [2, 0.1],
    [3, 0.1],
    [4, 0.1],
]
BACKGROUND_COLOUR = (51, 51, 51)


class animated_sprite(pygame.sprite.Sprite):
    def __init__(self, filename, width, height):
        pygame.sprite.Sprite.__init__(self)

        self._position = [0, 0]
        self._spritesheet = spritesheet.spritesheet(filename)
        self._frames = self._spritesheet.load_all(
            (0, 0, width, height),
            ALPHA_COLOUR
            )

        self._current_frame_index = 0;
        self.update_frame()

    @property
    def position(self):
        return list(self._position)
    
    @position.setter
    def position(self, value):
        self._position = list(value)
        self.update_frame()

    def update_frame(self):
        self._timeout = FRAMES[self._current_frame_index][1]
        self.image = self._frames[FRAMES[self._current_frame_index][0]]
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
    def next_frame(self):
        self._current_frame_index += 1
        if self._current_frame_index >= len(FRAMES):
            self._current_frame_index = 0
        self.update_frame()

    def update(self, dt):
        while (dt > 0):
            delta_t = dt
            if delta_t > self._timeout:
                delta_t = self._timeout

            self._timeout -= delta_t
            if self._timeout <= 0:
                self.next_frame()

            dt -= delta_t


class animation_test:
    def __init__(self, sprite):
        self._running = False
        self._sprite = sprite
        self._group = pygame.sprite.Group(self._sprite)
    
    def draw(self, surface):
        surface.fill(BACKGROUND_COLOUR)
        self._group.draw(surface)
    
    def handle_input(self):
        poll = pygame.event.poll

        event = poll()
        while event:
            if event.type == pygame.QUIT:
                self._running = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                    break

            event = poll()
    
    def update(self, dt):
        self._sprite.update(dt)
    
    def run(self):
        clock = pygame.time.Clock()
        self._running = True

        from collections import deque
        times = deque(maxlen=30)

        try:
            while self._running:
                dt = clock.tick(120) / 1000.
                times.append(clock.get_fps())

                self.handle_input()
                self.update(dt)
                self.draw(scope.screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self._running = False


if __name__ == "__main__":
    pygame.init()
    scope = pyscope.pyscope()
    pygame.display.set_caption('Animation Test')
    anim_sprite = animated_sprite(SPRITESHEET_FILENAME, SPRITE_WIDTH, SPRITE_HEIGHT)
    anim_sprite.position = [pygame.display.Info().current_w / 2 - (SPRITE_WIDTH / 2),
        pygame.display.Info().current_h / 2 - (SPRITE_HEIGHT / 2)]

    try:
        test = animation_test(anim_sprite)
        test.run()
    except:
        pygame.quit()
        raise
