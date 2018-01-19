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
