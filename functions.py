import os.path
from enum import Enum
import math

import pygame

from constants import *


# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


# Makes loading resources easier
def get_resource_name(filename):
    return os.path.join(RESOURCES_DIR, filename)


# make loading maps a little easier
def get_map(filename):
    return get_resource_name(filename + '.tmx')


# make loading images a little easier
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))


def calculate_knockback(source, target, knockback_value):
    delta_x = target[0] - source[0]
    delta_y = target[1] - source[1]
    distance = math.sqrt(delta_x**2 + delta_y**2)
    return [
        knockback_value * delta_x / distance,
        knockback_value * delta_y / distance
    ]


def rect_adjustment(surface, rect):
    if isinstance(rect, tuple):
        x, y, w, h = rect
        # Assume values (0 < x,y,w,h <= 1) are fractions of the whole window
        if x > 0 and x <= 1:
            x = x * surface.get_width()
        if y > 0 and y <= 1:
            y = y * surface.get_height()
        if w > 0 and w <= 1:
            w = w * surface.get_width()
        if h > 0 and h <= 1:
            h = h * surface.get_height()
        rect = (x, y, w, h)
        return pygame.Rect(rect)

    return rect


def draw_text_box(surface, rect):
    rect = rect_adjustment(surface, rect)

    # Edges
    ## Top
    pygame.draw.rect(surface, DIALOG_BORDER, (
            rect.x + DIALOG_BORDER_THICKNESS,
            rect.y,
            rect.width - (2 * DIALOG_BORDER_THICKNESS),
            DIALOG_BORDER_THICKNESS
        ), 0)
    ## Right
    pygame.draw.rect(surface, DIALOG_BORDER, (
            rect.x + rect.width - DIALOG_BORDER_THICKNESS,
            rect.y + DIALOG_BORDER_THICKNESS,
            DIALOG_BORDER_THICKNESS,
            rect.height - (2 * DIALOG_BORDER_THICKNESS)
        ), 0)
    ## Bottom
    pygame.draw.rect(surface, DIALOG_BORDER, (
            rect.x + DIALOG_BORDER_THICKNESS,
            rect.y + rect.height - DIALOG_BORDER_THICKNESS,
            rect.width - (2 * DIALOG_BORDER_THICKNESS),
            DIALOG_BORDER_THICKNESS
        ), 0)
    ## Left
    pygame.draw.rect(surface, DIALOG_BORDER, (
            rect.x,
            rect.y + DIALOG_BORDER_THICKNESS,
            DIALOG_BORDER_THICKNESS,
            rect.height - (2 * DIALOG_BORDER_THICKNESS)
        ), 0)
    # Corners
    ## Top Left
    pygame.draw.circle(surface, DIALOG_BORDER, (
            rect.x + DIALOG_BORDER_THICKNESS,
            rect.y + DIALOG_BORDER_THICKNESS,
        ), DIALOG_BORDER_THICKNESS, 0)
    ## Top Right
    pygame.draw.circle(surface, DIALOG_BORDER, (
            rect.x + rect.width - DIALOG_BORDER_THICKNESS,
            rect.y + DIALOG_BORDER_THICKNESS,
        ), DIALOG_BORDER_THICKNESS, 0)
    ## Bottom Left
    pygame.draw.circle(surface, DIALOG_BORDER, (
            rect.x + DIALOG_BORDER_THICKNESS,
            rect.y + rect.height - DIALOG_BORDER_THICKNESS,
        ), DIALOG_BORDER_THICKNESS, 0)
    ## Bottom Right
    pygame.draw.circle(surface, DIALOG_BORDER, (
            rect.x + rect.width - DIALOG_BORDER_THICKNESS,
            rect.y + rect.height - DIALOG_BORDER_THICKNESS,
        ), DIALOG_BORDER_THICKNESS, 0)
    # Fill
    pygame.draw.rect(surface, DIALOG_BACKGROUND, (
            rect.x + DIALOG_BORDER_THICKNESS,
            rect.y + DIALOG_BORDER_THICKNESS,
            rect.width - (2 * DIALOG_BORDER_THICKNESS),
            rect.height - (2 * DIALOG_BORDER_THICKNESS)
        ), 0)


def draw_text(surface, rect, text_list, colour):
    rect = rect_adjustment(surface, rect)

    y = rect.y + TEXT_SIZE
    x = TEXT_SIZE
    font = pygame.font.Font(pygame.font.get_default_font(), TEXT_SIZE)

    for line in text_list:
        text = font.render(line, 1, colour, TEXT_BACKGROUND)
        surface.blit(text, (x, y))
        y += text.get_height()


# Input configuration
R_INPUT_EVENT = pygame.USEREVENT + 1
## Buttons
class buttons(Enum):
    R_UP = 1
    R_RIGHT = 2
    R_DOWN = 3
    R_LEFT = 4
    R_A = 5
    R_B = 6
    R_START = 7
    R_SELECT = 8

## Map from keyboard/joystick to buttons
keyboard_map = {
    pygame.K_UP: buttons.R_UP,
    pygame.K_RIGHT: buttons.R_RIGHT,
    pygame.K_DOWN: buttons.R_DOWN,
    pygame.K_LEFT: buttons.R_LEFT,
    pygame.K_z: buttons.R_B,
    pygame.K_x: buttons.R_A,
    pygame.K_RETURN: buttons.R_START,
    pygame.K_RSHIFT: buttons.R_SELECT,
}
joystick_map = {
}
