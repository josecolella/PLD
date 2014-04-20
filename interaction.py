"""
This module is where all the interactions will be implemented.
Interactions encompass how the characters will respond to key strokes
"""


import pygame
from models import Tile
import sys


def interaction(screen, survivor):
    # Get mouse position
    Mpos = pygame.mouse.get_pos()  # [x, y]
    Mx = Mpos[0] / Tile.width
    My = Mpos[1] / Tile.height

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("x: {} y: {}".format(Mx, My))

    # Key events
    keys = pygame.key.get_pressed()

    # The event when the user presses w
    if keys[pygame.K_w]:  # North
        future_tile_number = survivor.get_number() - Tile.VerticalDifference
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                survivor.set_target(future_tile)
                survivor.rotate('n')
                # survivor.y -= survivor.height
    elif keys[pygame.K_s]:  # South
        future_tile_number = survivor.get_number() + Tile.VerticalDifference
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                survivor.set_target(future_tile)
                survivor.rotate('s')
                # survivor.y += survivor.height

    elif keys[pygame.K_a]:  # West
        future_tile_number = survivor.get_number() - Tile.HorizontalDifference

        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                survivor.set_target(future_tile)
                survivor.rotate('w')
                # survivor.x -= survivor.width

    elif keys[pygame.K_d]:  # East
        future_tile_number = survivor.get_number() + Tile.HorizontalDifference
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                survivor.set_target(future_tile)
                survivor.rotate('e')
                # survivor.x += survivor.width
    if keys[pygame.K_LEFT]:
        survivor.rotate('w')

    elif keys[pygame.K_RIGHT]:
        survivor.rotate('e')

    elif keys[pygame.K_UP]:
        survivor.rotate('n')

    elif keys[pygame.K_DOWN]:
        survivor.rotate('s')
