import os.path
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
