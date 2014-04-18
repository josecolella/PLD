#!/usr/bin/env python3
"""
Main Module
"""

import pygame
from models import *
from interaction import *
from A_Star import A_Star

pygame.init()  # Initialize Pygame
pygame.font.init()  # Font initializer
pygame.mixer.init()  # Music initializer

# Main theme music
# pygame.mixer.music.load("audio/laberynth.ogg")
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
FPS = 20
total_frames = 0

level1 = pygame.image.load('img/level1.png')
mainCharacter = MainCharacter(1 * 48, 10 * 64)

# Game Loop
while True:

    screen.blit(level1, (0, 0))  # blit the background

    # Robot.spawn(total_frames, FPS)
    # Robot.movement()

    mainCharacter.movement()

    # A_Star(screen, mainCharacter, total_frames, FPS)
    interaction(screen, mainCharacter)
    Tile.draw_tiles(screen)

    mainCharacter.draw(screen)
    # Robot.draw_zombies(screen)

    pygame.display.flip()
    clock.tick(FPS)
    total_frames += 1
