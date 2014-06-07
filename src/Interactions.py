import pygame
import sys
from models import Lever, Treasure
from gameoptions import GameOption

class Interaction:
    """
    Manages the key interaction with the player.
    """
    def __init__(self, screen, FPS, currentLevel):
        """
        Constructs the interactions that will be used to manage user interactions
        with the game.
        Parameters
        ----------
        - screen: pygame.Surface
        - FPS: The frames per second
        - currentLevel: The current level that the user will interact with
        """
        self.showGameMenu = False
        self.showHelpMenu = False
        self.screen = screen
        self.fps = FPS
        self.currentLevel = currentLevel
        self.player = currentLevel['built_objects']['j'][0]
        self.controlDefinition = (
            ('ESC', 'Show Menu'),
            ('r', 'Change Gun'),
            ('f', 'Pick Up'),
            ('g', 'Drop'),
            ('w', 'Move Up'),
            ('a', 'Move Left'),
            ('s', 'Move Down'),
            ('d', 'Move Right'),
            ('→', 'Shoot East'),
            ('↓', 'Shoot South'),
            ('↑', 'Shoot North'),
            ('←', 'Shoot West'),
            ('h', 'Close Help')
        )
        self.helpButton = {'h': 'Help'}

    def interactionHandler(self):
        """
        The handler that manages the user interaction with the game.
        All posible game keys are defined here and how they are managed
        interactionHandler() -> bool Whether to show the menu or not
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                GameOption.exitGame()

        # Key events
        keys = pygame.key.get_pressed()

        #  To show menu
        if keys[pygame.K_ESCAPE]:
            self.showGameMenu = True
        # Changing gun key
        if keys[pygame.K_r]:
            self.player.changeGun()

        if keys[pygame.K_h]:
            self.showHelpMenu = not self.showHelpMenu

        if keys[pygame.K_f]:
            Treasure.pickUpObject(self.player)
        elif keys[pygame.K_g]:
            Treasure.dropObject(self.player)

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

    def isUserCallingGameMenu(self):
        """
        isUserCallingGameMenu() -> True if the user is calling for the
        game menu, False otherwise
        """
        return self.showGameMenu

    def isUserCallingHelpScreen(self):
        """
        isUserCallingHelpScreen() -> True if user is calling for the
        help menu, False otherwise
        """
        return self.showHelpMenu
