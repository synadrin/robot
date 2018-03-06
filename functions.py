import os.path
from enum import Enum
import math

import pygame

from constants import *


# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


# make loading maps a little easier
def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename + '.tmx')


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


def draw_text_box(surface, rect):
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
