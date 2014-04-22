"""
This module is where all the interactions will be implemented.
Interactions encompass how the characters will respond to key strokes
"""


import pygame
from models import Tile, Laser
import sys


def interaction(screen, survivor, lever1, lever2):
    # Get mouse position
    isLevelPulled = False
    Mpos = pygame.mouse.get_pos()  # [x, y]
    Mx = Mpos[0] / Tile.width
    My = Mpos[1] / Tile.height

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("x: {} y: {}".format(Mx, My))

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_f:

                survivor.current += 1
                survivor.current %= len(Laser.imgs)

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
    elif keys[pygame.K_e]:  # Turn on lever
        if lever1.isNotActivated():
            lever1.turnOn(screen)
            Tile.set_door_open(survivor)
            isLevelPulled = True
                # survivor.x += survivor.width
    if keys[pygame.K_LEFT]:
        survivor.rotate('w')
        Laser(survivor.centerx, survivor.centery,
              -10, 0, 'w', survivor.get_bullet_type())

    elif keys[pygame.K_RIGHT]:
        survivor.rotate('e')
        Laser(survivor.centerx, survivor.centery,
              10, 0, 'e', survivor.get_bullet_type())

    elif keys[pygame.K_UP]:
        survivor.rotate('n')
        Laser(survivor.centerx, survivor.centery,
              0, -10, 'n', survivor.get_bullet_type())

    elif keys[pygame.K_DOWN]:
        survivor.rotate('s')
        Laser(survivor.centerx, survivor.centery,
              0, 10, 's', survivor.get_bullet_type())

    return isLevelPulled
