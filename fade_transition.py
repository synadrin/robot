import pygame

from constants import *
from functions import *


class fade_transition(object):
    def __init__(self, manager, time, colour):
        self._manager = manager
        self.finished = False
        self._colour = colour
        self._max_time = time
        self._timer = time
        self._fade_in = False
        self.from_scene = None
        self.to_scene = None

    @property
    def alpha(self):
        if self._fade_in:
            alpha_value = 255 * (self._timer / self._max_time)
        else:
            alpha_value = 255 * (1 - (self._timer / self._max_time))
        return alpha_value

    def pause(self):
        pass

    def resume(self):
        pass

    def end(self):
        self.finished = True

    def handle_input(self, events, pressed_keys):
        pass

    def update(self, dt):
        self._timer -= dt
        if self._timer <= (self._max_time / 2):
            self._fade_in = True
        if self._timer <= 0:
            self.end()

    def draw(self, surface):
        # Draw the scene under
        if self._fade_in:
            if self.to_scene:
                self.to_scene.draw(surface)
        else:
            if self.from_scene:
                self.from_scene.draw(surface)
        # Draw the fade
        fade_surface = pygame.Surface(
            (surface.get_width(), surface.get_height())
        )
        fade_surface.set_alpha(self.alpha)
        fade_surface.fill(self._colour)
        surface.blit(fade_surface, (0,0))
