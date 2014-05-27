import pygame
import sys
from models import Laser, Lever
from gameoptions import GameOption


class Interaction:
    """
    Manages the key interaction with the player.
    """
    def __init__(self, screen, FPS, currentLevel):

        self.showMenu = False
        self.screen = screen
        self.fps = FPS
        self.currentLevel = currentLevel
        self.player = currentLevel['built_objects']['j'][0]

    def interactionHandler(self):
        """
        The handler that manages the user interaction with the game.
        All posible game keys are defined here and how they are managed
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # To change weapons
                if event.key == pygame.K_f:

                    self.player.currentGun += 1
                    self.player.currentGun %= len(Laser.imgs)
                # To save game
                if event.key == pygame.K_x:

                    GameOption.saveGame(self.currentLevel)

                if event.key == pygame.K_z:
                    self.showMenu = not self.showMenu

        # Key events
        keys = pygame.key.get_pressed()

        # Changing gun key
        if keys[pygame.K_f]:
            pass

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

        elif keys[pygame.K_e]:  # Toggle lever
            for lever in Lever.allLevers:
                distance2 = (lever.rect.x-self.player.x)*(lever.rect.x-self.player.x)+(
                    lever.rect.y-self.player.y)*(lever.rect.y-self.player.y)
                if distance2 < 4*(lever.width*lever.width+
                                    lever.height*lever.height):
                    lever.toggle()
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
