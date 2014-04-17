#!/usr/bin/env python3
# Module where the models are built
# This includes the characters, enemies, and objects of the game
import pygame
from random import randint
from levels import Level


class MainCharacter(object):

    """
    This class represents the MainCharacter for the
    game
    """

    def __init__(self, arg):
        pass


class Robot(object):

    """
    The class that represents the robots that
    defend the Treasure
    """

    def __init__(self, arg):
        pass


class Enemy(object):

    """
    The class that represents the enemy that the
    user will be going up against
    """

    def __init__(self, arg):
        pass


class Laser(object):

    """
    The class that represents the laser that the MainCharacter
    can shoot to open portals
    """

    def __init__(self, arg):
        pass


class Treasure(object):

    """
    Class that represents the object that the MainCharacter has to
    steal
    """


class Tile(pygame.Rect):

    # The tuple of posible tile images
    TileImageTuple = (
        'img/wall.png',
        'img/light_gray_tile.png',
        'img/sewer_tile.png'
    )

    List = []
    # Determines the height and width of the labyrith tilek
    width, height = 16, 16
    total_tiles = 1
    H, V = 1, 22

    # The top boundary
    topColumnList = [i for i in range(65)]
    # The left boundary
    leftColumnList = [i * 64 + 1 for i in range(48)]
    # The right boundary
    rightColumnList = [i for i in range(64, 64 * 48 + 1, 64)]
    # the bottom boundary
    bottomColumnList = [i for i in range(48 * 64 - 63, 48 * 64 + 1)]
    invalids = []
    invalids.extend(topColumnList)
    invalids.extend(leftColumnList)
    invalids.extend(rightColumnList)
    invalids.extend(bottomColumnList)

    level = Level()
    invalids.extend(level.leve1())

    def __init__(self, x, y, Type):

        self.parent = None
        self.H, self.G, self.F = 0, 0, 0

        self.type = Type
        self.number = Tile.total_tiles
        self.randomImage = Tile.TileImageTuple[
            randint(0, len(Tile.TileImageTuple) - 1)]
        self.image = self.randomImage
        Tile.total_tiles += 1

        if Type == 'empty':
            self.walkable = True
        else:
            self.walkable = False

        pygame.Rect.__init__(self, (x, y), (Tile.width, Tile.height))

        Tile.List.append(self)

    @staticmethod
    def get_tile(number):
        for tile in Tile.List:
            if tile.number == number:
                return tile

    @staticmethod
    def draw_tiles(screen):
        for tile in Tile.List:
            if tile.type != 'empty':
                screen.blit(
                    pygame.image.load('img/dark_gray_tile.png'), (tile.x, tile.y))
            else:
                screen.blit(pygame.image.load(tile.image), (tile.x, tile.y))
