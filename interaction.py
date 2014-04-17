"""
This module is where all the interactions will be implemented.
Interactions encompass how the characters will respond to key strokes
"""


import pygame
from models import Tile
import sys


def interaction(screen):
    # Get mouse position
    Mpos = pygame.mouse.get_pos()  # [x, y]
    Mx = Mpos[0] / Tile.width
    My = Mpos[1] / Tile.height

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in Tile.List:
                if tile.x == (Mx * Tile.width) and tile.y == (My * Tile.width):
                    tile.type = 'solid'
                    tile.walkable = False
                    break

    # Key events
    keys = pygame.key.get_pressed()

    # The event when the user presses w
    if keys[pygame.K_w]:  # North
        pass
    # The event when the user presses s
    if keys[pygame.K_s]:  # South
        pass

    # The event when the user presses a
    if keys[pygame.K_a]:  # West
        pass

    # The event when the user presses d
    if keys[pygame.K_d]:  # East
        pass

    # The event when the user presses space
    if keys[pygame.K_SPACE]:  # Space
        pass
