#!/usr/bin/env python3
# Module where the models are built
# This includes the characters, enemies, and objects of the game
import pygame
from random import randint


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
    TileImageTuple = ('radioactive_tile.png',
                      'brown_tile.png',
                      'dark_gray_tile.png',
                      'dark_red_tile.png',
                      'light_gray_tile.png',
                      'red_tile.png',
                      'sewer_tile.png'
                      )
    middlelevel = ["xxxxxxxxxxxxxxx",
                   "xs............x",
                   "x.........x...x",
                   "x.........x...x",
                   "x......x..x...x",
                   "x.....x...x...x",
                   "x..p.xxxxxx...x",
                   "x.....x.......x",
                   "x.x....x......x",
                   "x.x...........x",
                   "x.x...x.......x",
                   "x.x....x......x",
                   "x.xxxxxxx..n..x",
                   "x......x......x",
                   "x.....x.......x",
                   "xxxxxxxxxxxxxxx"]

    List = []
    # Determines the height and width of the labyrith tilek
    width, height = 16, 16
    total_tiles = 1
    H, V = 1, 22

    invalids = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 20, 21, 22,
                23, 26, 28, 29, 30, 32, 35, 36, 41, 44,
                45, 58, 59, 61, 62, 64, 66,
                67, 70, 77, 78, 88,
                89, 92, 94, 95, 99, 100, 102, 103, 105, 106, 107, 108, 110,
                111, 112, 113, 117, 119, 124, 128,
                133, 139, 141, 142, 143, 146, 152, 154,
                155, 156, 157, 158, 159, 168, 172, 174, 176,
                177, 181, 182, 184, 187, 188, 189, 190, 191, 192,
                194, 197, 198,
                199, 204, 206, 208, 209, 212, 214, 215, 220,
                221, 241, 242,
                243, 251, 264,
                265, 270, 273, 275, 278, 280, 281, 283, 285, 286,
                287, 288, 289, 290, 291, 292, 293, 294, 295, 296,
                297, 298, 299,
                300, 301, 302, 303, 304, 305, 306, 307, 308]

    def __init__(self, x, y, Type):

        self.parent = None
        self.H, self.G, self.F = 0, 0, 0

        self.type = Type
        self.number = Tile.total_tiles
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
            if not(tile.type == 'empty'):
                pygame.draw.rect(screen, [40, 40, 40], tile)
