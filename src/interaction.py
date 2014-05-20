"""
This module is where all the interactions will be implemented.
Interactions encompass how the characters will respond to key strokes
"""


import pygame
from models import Tile, Laser, Lever
import sys
from menu import show_menu
from gameoptions import *


def interaction(screen, currentLevel, FPS):
    """
    Menu that defines the key interactions in the game and how the
    screen will respond to the events
    """
    # Get mouse position

    Mpos = pygame.mouse.get_pos()  # [x, y]
    Mx = Mpos[0] / Tile.width
    My = Mpos[1] / Tile.height

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # To change weapons
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_f:

                currentLevel['built_objects']['j'][0].currentGun += 1
                currentLevel['built_objects']['j'][0].currentGun %= len(Laser.imgs)

            if event.key == pygame.K_x:

                GameOption.saveGame(currentLevel)

            if event.key == pygame.K_z:

                GameOption.loadGame(currentLevel)

    # Key events
    keys = pygame.key.get_pressed()

    # The event when the user presses w
    if keys[pygame.K_w]:  # North
        currentLevel['built_objects']['j'][0].moveNorth()

    elif keys[pygame.K_s]:  # South
        currentLevel['built_objects']['j'][0].moveSouth()

    elif keys[pygame.K_a]:  # West
        currentLevel['built_objects']['j'][0].moveWest()

    elif keys[pygame.K_d]:  # East
        currentLevel['built_objects']['j'][0].moveEast()

    elif keys[pygame.K_e]:  # Toggle lever
        for lever in Lever.allLevers:
            distance2 = (lever.rect.x-currentLevel['built_objects']['j'][0].x)*(lever.rect.x-currentLevel['built_objects']['j'][0].x)+(
                lever.rect.y-currentLevel['built_objects']['j'][0].y)*(lever.rect.y-currentLevel['built_objects']['j'][0].y)
            if distance2 < 4*(lever.width*lever.width+
                                lever.height*lever.height):
                lever.toggle()

    if keys[pygame.K_LEFT]:
        currentLevel['built_objects']['j'][0].rotate('w')
        Laser(currentLevel['built_objects']['j'][0].centerx, currentLevel['built_objects']['j'][0].centery,
              -10, 0, 'w', currentLevel['built_objects']['j'][0].get_bullet_type())

    elif keys[pygame.K_RIGHT]:
        currentLevel['built_objects']['j'][0].rotate('e')
        Laser(currentLevel['built_objects']['j'][0].centerx, currentLevel['built_objects']['j'][0].centery,
              10, 0, 'e', currentLevel['built_objects']['j'][0].get_bullet_type())

    elif keys[pygame.K_UP]:
        currentLevel['built_objects']['j'][0].rotate('n')
        Laser(currentLevel['built_objects']['j'][0].centerx, currentLevel['built_objects']['j'][0].centery,
              0, -10, 'n', currentLevel['built_objects']['j'][0].get_bullet_type())

    elif keys[pygame.K_DOWN]:
        currentLevel['built_objects']['j'][0].rotate('s')
        Laser(currentLevel['built_objects']['j'][0].centerx, currentLevel['built_objects']['j'][0].centery,
              0, 10, 's', currentLevel['built_objects']['j'][0].get_bullet_type())
