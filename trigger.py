import pygame


class trigger(pygame.Rect):

    def __init__(self, x, y, width, height, properties):
        super().__init__(x, y, width, height)
        self._name = properties['name'] if 'name' in properties else ''
        self.on_enter = properties['on_enter'] \
            if 'on_enter' in properties else None
        self.on_exit = properties['on_exit'] \
            if 'on_exit' in properties else None
        self.on_interact = properties['on_interact'] \
            if 'on_interact' in properties else None
        self.message_text = properties['message_text'] \
            if 'message_text' in properties else None
