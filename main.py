#!/usr/bin/env python3
"""
Main Module
"""

import pygame
from models import *
from interaction import *

pygame.init()  # Initialize Pygame
pygame.font.init()  # Font initializer
pygame.mixer.init()  # Music initializer

# Main theme music
#pygame.mixer.music.load("audio/laberynth.ogg")
# pygame.mixer.music.play(-1)  # Continuous Loop

screenwidth = 1024
screenheight = 768

# Set screen with width and height
screen = pygame.display.set_mode((screenwidth, screenheight))


for y in range(0, screen.get_height(), 16):
    for x in range(0, screen.get_width(), 16):
        if Tile.total_tiles in Tile.invalids:
            Tile(x, y, 'solid')
        else:
            Tile(x, y, 'empty')


clock = pygame.time.Clock()  # Initialize Game Clock
FPS = 30
total_frames = 0


# Game Loop
while True:

    interaction(screen)
    Tile.draw_tiles(screen)
    pygame.display.flip()
    clock.tick(FPS)
    total_frames += 1
