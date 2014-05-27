import pygame
import sys
from models import Laser
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
        # Get mouse position
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

        # The event when the user presses w
        if keys[pygame.K_w]:  # North
            self.player.moveNorth()

        elif keys[pygame.K_s]:  # South
            self.player.moveSouth()

        elif keys[pygame.K_a]:  # West
            self.player.moveWest()

        elif keys[pygame.K_d]:  # East
            self.player.moveEast()

        elif keys[pygame.K_e]:  # Toggle lever
            for lever in Lever.allLevers:
                distance2 = (lever.rect.x-self.player.x)*(lever.rect.x-self.player.x)+(
                    lever.rect.y-self.player.y)*(lever.rect.y-self.player.y)
                if distance2 < 4*(lever.width*lever.width+
                                    lever.height*lever.height):
                    lever.toggle()

        if keys[pygame.K_LEFT]:
            self.player.rotate('w')
            Laser(self.player.centerx, self.player.centery,
                  -10, 0, 'w', self.player.get_bullet_type())

        elif keys[pygame.K_RIGHT]:
            self.player.rotate('e')
            Laser(self.player.centerx, self.player.centery,
                  10, 0, 'e', self.player.get_bullet_type())

        elif keys[pygame.K_UP]:
            self.player.rotate('n')
            Laser(self.player.centerx, self.player.centery,
                  0, -10, 'n', self.player.get_bullet_type())

        elif keys[pygame.K_DOWN]:
            self.player.rotate('s')
            Laser(self.player.centerx, self.player.centery,
                  0, 10, 's', self.player.get_bullet_type())

        return self.showMenu
