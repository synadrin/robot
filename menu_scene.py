import pygame

from constants import *
from functions import *


class menu_item(object):
    def __init__(self, text, active, action):
        self.text = text
        self.active = active
        self.action = action


class menu_scene(object):
    def __init__(self, manager, filename, rect):
        self._manager = manager
        self._menu_items = []
        self.image = load_image(filename).convert()
        self.image.set_colorkey(ALPHA_COLOUR, pygame.RLEACCEL)
        self.rect = pygame.Rect(rect)
        self._active_choice_index = 0

    @property
    def active_choice_index(self):
        return self._active_choice_index

    @active_choice_index.setter
    def active_choice_index(self, value):
        difference = value - self._active_choice_index
        self._active_choice_index = value
        if self._active_choice_index >= len(self._menu_items):
            self._active_choice_index = 0
        elif self._active_choice_index < 0:
            self._active_choice_index = len(self._menu_items) - 1

        if self._menu_items \
            and self._menu_items[self._active_choice_index] \
            and not self._menu_items[self._active_choice_index].active:
            if difference > 0:
                self.active_choice_index += 1
            elif difference < 0:
                self.active_choice_index -= 1

    def pause(self):
        pass

    def resume(self):
        pass

    def handle_input(self, events, pressed_keys):
        for event in events:
            if event.type == R_INPUT_EVENT:
                if event.button == buttons.R_DOWN:
                    self.active_choice_index += 1
                if event.button == buttons.R_UP:
                    self.active_choice_index -= 1
                if event.button == buttons.R_A \
                    or event.button == buttons.R_START:
                    self.action(self.active_choice_index)

    def update(self, dt):
        pass

    def draw_cursor(self, surface):
        rect = pygame.Rect(self.rect)
        rect.x += TEXT_SIZE / 2
        rect.y += (self.active_choice_index + 1) * TEXT_SIZE
        pygame.draw.polygon(surface, TEXT_COLOUR,
            [
                [rect.x, rect.y],
                [rect.x + (TEXT_SIZE / 2), rect.y + (TEXT_SIZE / 2)],
                [rect.x, rect.y + TEXT_SIZE]
            ],
            0)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
        draw_text_box(surface, self.rect)
        active_text = []
        inactive_text = []
        for mi in self._menu_items:
            if mi.active:
                active_text.append(mi.text)
                inactive_text.append("")
            else:
                active_text.append("")
                inactive_text.append(mi.text)
        draw_text(surface, self.rect, active_text,
            TEXT_COLOUR)
        draw_text(surface, self.rect, inactive_text,
            TEXT_COLOUR_INACTIVE)
        self.draw_cursor(surface)

    def append(self, text, active, action):
        self._menu_items.append(menu_item(text, active, action))

    def action(self, index):
        action = self._menu_items[index].action
        if action and callable(action):
            action()
