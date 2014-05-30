import pygame
import sys
from models import Lever


class Interaction:
    """
    Manages the key interaction with the player.
    """
    def __init__(self, screen, FPS, currentLevel):
        """

        """
        self.showMenu = False
        self.screen = screen
        self.fps = FPS
        self.currentLevel = currentLevel
        self.player = currentLevel['built_objects']['j'][0]

    def interactionHandler(self):
        """
        The handler that manages the user interaction with the game.
        All posible game keys are defined here and how they are managed
        interactionHandler() -> bool Whether to show the menu or not
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key events
        keys = pygame.key.get_pressed()

        #  To show menu
        if keys[pygame.K_ESCAPE]:
            self.showMenu = True
        # Changing gun key
        if keys[pygame.K_f]:
            self.player.changeGun()
        # Movement and shooting keys
        # West
        if keys[pygame.K_w]:
            self.player.moveNorth()
        # South
        elif keys[pygame.K_s]:
            self.player.moveSouth()
        #West
        elif keys[pygame.K_a]:
            self.player.moveWest()
        #East
        elif keys[pygame.K_d]:
            self.player.moveEast()
        # Toggle lever
        elif keys[pygame.K_e]:
            Lever.interactionToggleHandler(self.player)
        # Fire Left
        if keys[pygame.K_LEFT]:
            self.player.fireWest()
        # Fire Right
        elif keys[pygame.K_RIGHT]:
            self.player.fireEast()
        # Fire North
        elif keys[pygame.K_UP]:
            self.player.fireNorth()
        # Fire South
        elif keys[pygame.K_DOWN]:
            self.player.fireSouth()

        return self.showMenu
