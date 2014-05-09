"""
This module is where all the interactions will be implemented.
Interactions encompass how the characters will respond to key strokes
"""


import pygame
from models import Tile, Laser, Lever
import sys
from menu import show_menu


def interaction(screen, survivor, FPS):
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

                survivor.current += 1
                survivor.current %= len(Laser.imgs)

    # Key events
    keys = pygame.key.get_pressed()

    # The event when the user presses w
    if keys[pygame.K_w]:  # North
        survivor.moveNorth()

    elif keys[pygame.K_s]:  # South
        survivor.moveSouth()
        

    elif keys[pygame.K_a]:  # West
        survivor.moveWest()
       

    elif keys[pygame.K_d]:  # East
        survivor.moveEast()
        
    elif keys[pygame.K_e]:  # Toggle lever
        for lever in Lever.allLevers:
            distance2 = (lever.rect.x-survivor.x)*(lever.rect.x-survivor.x)+(
                lever.rect.y-survivor.y)*(lever.rect.y-survivor.y)

            if distance2 < 4*(lever.width*lever.width+
                                lever.height*lever.height):
                lever.toggle()
        #if lever1.isNotActivated():
        #   lever1.turnOn(screen)
        #   Tile.set_door_open(survivor)
        #   isLevelPulled = True
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


