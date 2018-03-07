import pygame

from constants import *
from functions import *


class text_scene(object):
    def __init__(self, manager, text_list, rect):
        self._manager = manager
        if isinstance(text_list, list):
            self._text_list = text_list
        else:
            self._text_list = [text_list]
        self.rect = rect

    def pause(self):
        pass

    def resume(self):
        pass

    def handle_input(self, events, pressed_keys):
        for event in events:
            if event.type == R_INPUT_EVENT:
                if event.button == buttons.R_A:
                    self._manager.pop()

    def update(self, dt):
        pass

    def draw(self, surface):
        draw_text_box(surface, self.rect)
        draw_text(surface, self.rect, self._text_list,
            TEXT_COLOUR)
