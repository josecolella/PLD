#!/usr/bin/env python3
# Module where the models are built
# This includes the characters, enemies, and objects of the game
import pygame
from random import randint
from levels import Level


class Character(pygame.Rect):

    """
    This class is an abstract concept of what all
    classes should contain
    """
    width, height = 32, 32

    def __init__(self, x, y):

        self.tx, self.ty = None, None
        pygame.Rect.__init__(self, x, y, Character.width, Character.height)

    def __str__(self):
        return str(self.get_number())

    def set_target(self, next_tile):
        if self.tx is None and self.ty is None:
            self.tx = next_tile.x
            self.ty = next_tile.y

    def get_number(self):

        return ((self.x / self.width) + Tile.H) + ((self.y / self.height) * Tile.V)

    def get_tile(self):

        return Tile.get_tile(self.get_number())

    def rotate(self, direction, original_img):

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                south = pygame.transform.rotate(original_img, 90)  # CCW
                self.img = pygame.transform.flip(south, False, True)

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = pygame.transform.rotate(original_img, 90)  # CCW

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = pygame.transform.flip(original_img, True, False)

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = original_img


class MainCharacter(Character):

    """
    This class represents the MainCharacter for the
    game
    """

    def __init__(self, x, y):
        """
        Initializes the main character in the specified
        x and y coordinates of the map
        """
        self.current = 0  # 0 -> pistol, 1 -> shotgun, 2 -> automatic
        self.direction = 'w'
        self.img = pygame.image.load('img/thief_w.png')

        Character.__init__(self, x, y)

    def movement(self):

        if self.tx is not None and self.ty is not None:  # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            vel = 8

            if X < 0:  # --->
                self.x += vel
            elif X > 0:  # <----
                self.x -= vel

            if Y > 0:  # up
                self.y -= vel
            elif Y < 0:  # dopwn
                self.y += vel

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    def draw(self, screen):

        screen.blit(self.img, (self.x, self.y))

        h = self.width / 2
        # img = MainCharacter.guns_img[self.current]

        if self.direction == 'w':
            pass
            # screen.blit(img, (self.x, self.y + h))

        elif self.direction == 'e':
            pass
            # img = pygame.transform.flip(img, True, False)
            # screen.blit(img, (self.x + h, self.y + h))

        elif self.direction == 's':
            pass
            # img = pygame.transform.rotate(img, 90)  # CCW
            # screen.blit(img, (self.x + h, self.y + h))

        elif self.direction == 'n':
            pass
            # south = pygame.transform.rotate(img, 90)
            # img = pygame.transform.flip(south, False, True)
            # screen.blit(img, (self.x + h, self.y - h))

    def rotate(self, direction):

        path = 'img/thief_'
        png = '.png'

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = pygame.image.load(path + self.direction + png)


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
    level1 = level.leve1()
    invalids.extend(level1)

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
            pass
            # if tile.type != 'empty' and tile not in Tile.level1:
            #     screen.blit(
            #         pygame.image.load('img/dark_gray_tile.png'), (tile.x, tile.y))
            # elif tile in Tile.level1:
            #     screen.blit(
            #         pygame.image.load('img/wall.png'), (tile.x, tile.y))
            # else:
            #     screen.blit(
            # pygame.image.load('img/light_gray_tile.png'), (tile.x, tile.y))
