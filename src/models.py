#!/usr/bin/env python3
# Module where the models are built
# This includes the characters, enemies, and objects of the game
import pygame
from random import randint
from levels import Level
import itertools
import re


class Dimensions:

    """
    Class that defines the dimensions (height, and width) for the
    objects that are to be created in the game
    """
    width = 16
    height = 16


class Livebar(pygame.Rect):

    """
    This class represent the Character's healthbar
    """

    def __init__(self, boss):

        self.boss = boss
        self.image = pygame.Surface((self.boss.width * 2, 7))
        self.image.set_colorkey((0, 0, 0))  # black transparent
        pygame.draw.rect(
            self.image, (0, 255, 0), (0, 0, self.boss.width * 2, 7
                                      ), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.boss.x
        self.rect.y = self.boss.y
        self.oldpercent = 0

        pygame.Rect.__init__(
            self, self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self):
        self.percent = self.boss.health / self.boss.__class__.health
        if self.percent != self.oldpercent:
            # fill black
            pygame.draw.rect(
                self.image, (0, 0, 0), (1, 1, self.boss.width * 2 - 2, 5))
            pygame.draw.rect(self.image, (0, 255, 0), (1, 1,
                                                       int(self.boss.width * 2 * self.percent), 5), 0)  # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.centerx + 7
        self.rect.centery = self.boss.centery - \
            self.boss.height / 2 - 15

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Character(pygame.Rect):

    """
    This class is an abstract concept of what all
    classes should contain.
    """
    width, height = Dimensions.width, Dimensions.height

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

        return ((self.x / self.width) + Tile.HorizontalDifference) + ((self.y / self.height) * Tile.VerticalDifference)

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

    def _move(self, direction, difference):
        future_tile_number = self.get_number() + difference
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                self.set_target(future_tile)
                self.rotate(direction)

    def moveEast(self):
        self._move('e', Tile.HorizontalDifference)

    def moveWest(self):
        self._move('w', - Tile.HorizontalDifference)

    def moveNorth(self):
        self._move('n', - Tile.VerticalDifference)

    def moveSouth(self):
        self._move('s', Tile.VerticalDifference)


class MainCharacter(Character):

    """
    This class represents the MainCharacter for the
    game
    """

    guns_img = (
        pygame.image.load("img/shotgun.png"),
        pygame.image.load("img/automatic.png")
    )

    health = 100

    def __init__(self, x, y):
        """
        Initializes the main character in the specified
        x and y coordinates of the map
        """
        self.health = MainCharacter.health
        self.healthbar = Livebar(self)
        self.description = "maincharacter"
        self.current = 0  # 0 -> pistol, 1 -> shotgun, 2 -> automatic
        self.direction = 'w'
        self.img = pygame.image.load('img/player_w.png')
        # Use cycle so that it iterates forever
        self.walking_west_images = itertools.cycle(
            ('img/player_w_walk_l.png',
             'img/player_w.png',
             'img/player_w_walk_r.png'
             )
        )
        self.walking_east_images = itertools.cycle(
            ('img/player_e_walk_l.png',
             'img/player_e.png',
             'img/player_e_walk_r.png'
             )
        )
        self.walking_north_images = itertools.cycle(
            ('img/player_n_walk_l.png',
             'img/player_n.png',
             'img/player_n_walk_r.png'
             )
        )
        self.walking_south_images = itertools.cycle(
            ('img/player_s_walk_l.png',
             'img/player_s.png',
             'img/player_s_walk_r.png'
             )
        )

        Character.__init__(self, x, y)

    def get_bullet_type(self):
        """
        get_bullet_type() -> str the current bullet
        """

        if self.current == 0:
            return 'automatic'
        elif self.current == 1:
            return 'shotgun'

    def movement(self, screen):
        """
        This method deals with everything related to the movement of the character.
        This method also manages the switch between the character walking with the left foot
        and then right foot to give the walk a realistic feel
        """
        if self.tx is not None and self.ty is not None:  # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            vel = 8

            if X < 0:  # --->

                self.img = pygame.image.load(next(self.walking_east_images))
                self.x += vel
            elif X > 0:  # <----

                self.img = pygame.image.load(next(self.walking_west_images))
                self.x -= vel

            if Y > 0:  # up

                self.img = pygame.image.load(next(self.walking_north_images))
                self.y -= vel

            elif Y < 0:  # dopwn

                self.img = pygame.image.load(next(self.walking_south_images))
                self.y += vel

            screen.blit(self.img, (self.x, self.y))

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    def draw(self, screen):

        screen.blit(self.img, (self.x, self.y))
        self.healthbar.update()
        self.healthbar.draw(screen)

        h = self.width / 2
        img = MainCharacter.guns_img[self.current]

        if self.direction == 'w':
            screen.blit(img, (self.x, self.y + h))

        elif self.direction == 'e':
            img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x + h, self.y + h))

        elif self.direction == 's':
            img = pygame.transform.rotate(img, 90)  # CCW
            screen.blit(img, (self.x + h, self.y + h))

        elif self.direction == 'n':
            south = pygame.transform.rotate(img, 90)
            img = pygame.transform.flip(south, False, True)
            screen.blit(img, (self.x + h, self.y - h))

    def rotate(self, direction):
        """
        Method created to manage the rotation of the Character
        and to set the appropriate image
        """
        path = 'img/player_'
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


class Robot(Character):

    """
    The class that represents the robots that
    defend the Treasure
    """
    health = 100

    List = []
    spawn_tiles = (33 + 64 * 15, 36 + 64 * 15)
    spawn_tiles_iter = itertools.cycle(spawn_tiles)
    original_img = pygame.image.load('img/guardian_s.png')
    robot_sound = itertools.cycle(
        ('audio/findseekanddestroy.ogg', 'audio/cmu_us_rms_arctic_clunits.ogg')
    )
    health = 100

    def __init__(self, x, y):
        self.health = Robot.health
        self.healthbar = Livebar(self)
        self.direction = 's'
        self.health = Robot.health
        self.img = Robot.original_img
        self.walking_west_images = itertools.cycle(
            ('img/guardian_w_walk_l.png',
             'img/guardian_w_walk_c.png',
             'img/guardian_w_walk_r.png'
             )
        )
        self.walking_east_images = itertools.cycle(
            ('img/guardian_e_walk_l.png',
             'img/guardian_e_walk_c.png',
             'img/guardian_e_walk_r.png'
             )
        )
        self.walking_north_images = itertools.cycle(
            ('img/guardian_n_walk_l.png',
             'img/guardian_n_walk_c.png',
             'img/guardian_n_walk_r.png'
             )
        )
        self.walking_south_images = itertools.cycle(
            ('img/guardian_s_walk_l.png',
             'img/guardian_s_walk_c.png',
             'img/guardian_s_walk_r.png'
             )
        )

        Character.__init__(self, x, y)

        Robot.List.append(self)

    @staticmethod
    def draw_robots(screen):
        for robot in Robot.List:
            screen.blit(robot.img, (robot.x, robot.y))
            robot.healthbar.update()
            robot.healthbar.draw(screen)

            if robot.health <= 0:
                Robot.List.remove(robot)

    @staticmethod
    def movement(screen):
        for robot in Robot.List:
            # Target is set
            if robot.tx is not None and robot.ty is not None:

                X = robot.x - robot.tx
                Y = robot.y - robot.ty

                vel = 4
                if X < 0:  # --->
                    robot.img = pygame.image.load(
                        next(robot.walking_east_images))
                    robot.x += vel
                    robot.rotate('e', Robot.original_img)

                elif X > 0:  # <----
                    robot.img = pygame.image.load(
                        next(robot.walking_west_images))
                    robot.x -= vel
                    robot.rotate('w', Robot.original_img)

                if Y > 0:  # up
                    robot.img = pygame.image.load(
                        next(robot.walking_north_images))
                    robot.y -= vel
                    robot.rotate('n', Robot.original_img)

                elif Y < 0:  # dopwn
                    robot.img = pygame.image.load(
                        next(robot.walking_west_images))
                    robot.y += vel
                    robot.rotate('s', Robot.original_img)

                screen.blit(robot.img, (robot.x, robot.y))

                if X == 0 and Y == 0:
                    robot.tx, robot.ty = None, None

    @staticmethod
    def spawn(total_frames, FPS):
        if total_frames % (FPS * 3) == 0:

            sound = pygame.mixer.Sound(next(Robot.robot_sound))
            sound.play()

            tile_num = next(Robot.spawn_tiles_iter)
            spawn_node = Tile.get_tile(tile_num)
            Robot(spawn_node.x, spawn_node.y)


class Enemy(Character):

    """
    This class represents the enemy that the MainCharacter will
    compete against to steal the Treasure
    """
    guns_img = (
        pygame.image.load("img/shotgun.png"),
        pygame.image.load("img/automatic.png")
    )

    health = 100

    def __init__(self, x, y):
        """
        Initializes the main character in the specified
        x and y coordinates of the map
        """
        self.health = Enemy.health
        self.healthbar = Livebar(self)
        self.description = "enemy"
        self.current = 0  # 0 -> pistol, 1 -> shotgun, 2 -> automatic
        self.direction = 'w'
        self.img = pygame.image.load('img/thief_w.png')
        # Use cycle so that it iterates forever
        self.walking_west_images = itertools.cycle(
            ('img/thief_w_walk_l.png',
             'img/thief_w.png',
             'img/thief_w_walk_r.png'
             )
        )
        self.walking_east_images = itertools.cycle(
            ('img/thief_e_walk_l.png',
             'img/thief_e.png',
             'img/thief_e_walk_r.png'
             )
        )
        self.walking_north_images = itertools.cycle(
            ('img/thief_n_walk_l.png',
             'img/thief_n.png',
             'img/thief_n_walk_r.png'
             )
        )
        self.walking_south_images = itertools.cycle(
            ('img/thief_s_walk_l.png',
             'img/thief_s.png',
             'img/thief_s_walk_r.png'
             )
        )

        Character.__init__(self, x, y)

    def movement(self, screen):
        """
        This method deals with everything related to the movement of the character.
        This method also manages the switch between the character walking with the left foot
        and then right foot to give the walk a realistic feel
        """
        if self.tx is not None and self.ty is not None:  # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            vel = 4

            if X < 0:  # --->

                self.img = pygame.image.load(next(self.walking_east_images))
                self.x += vel
            elif X > 0:  # <----

                self.img = pygame.image.load(next(self.walking_west_images))
                self.x -= vel

            if Y > 0:  # up

                self.img = pygame.image.load(next(self.walking_north_images))
                self.y -= vel

            elif Y < 0:  # dopwn

                self.img = pygame.image.load(next(self.walking_south_images))
                self.y += vel

            screen.blit(self.img, (self.x, self.y))

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    def draw(self, screen):

        screen.blit(self.img, (self.x, self.y))
        self.healthbar.update()
        self.healthbar.draw(screen)

        h = self.width / 2
        img = Enemy.guns_img[self.current]

        if self.direction == 'w':
            screen.blit(img, (self.x, self.y + h))

        elif self.direction == 'e':
            img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x + h, self.y + h))

        elif self.direction == 's':
            img = pygame.transform.rotate(img, 90)  # CCW
            screen.blit(img, (self.x + h, self.y + h))

        elif self.direction == 'n':
            south = pygame.transform.rotate(img, 90)
            img = pygame.transform.flip(south, False, True)
            screen.blit(img, (self.x + h, self.y - h))

    def rotate(self, direction):
        """
        Method created to manage the rotation of the Character
        and to set the appropriate image
        """
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


class Laser(pygame.Rect):

    """
    The class that represents the laser that the MainCharacter
    can shoot to open portals
    """

    width, height = 3.5, 5
    List = []

    sounds = (
        'audio/fire.ogg',
        'audio/bullet.ogg'
    )

    imgs = {
        'shotgun': pygame.image.load('img/shotgun_b.png'),
        'automatic': pygame.image.load('img/automatic_b.png')
    }

    gun_dmg = {
        'shotgun': Robot.health / 2,
        'automatic': (Robot.health / 6) + 1
    }

    def __init__(self, x, y, velx, vely, direction, type_):

        if type_ == 'shotgun':

            try:

                dx = abs(Laser.List[-1].x - x)
                dy = abs(Laser.List[-1].y - y)

                if dx < 50 and dy < 50 and type_ == 'shotgun':
                    return

            except:
                pass

        self.type = type_
        if(self.type == 'shotgun'):
            sound = pygame.mixer.Sound(Laser.sounds[1])
        else:
            sound = pygame.mixer.Sound(Laser.sounds[0])
        sound.play()
        self.direction = direction
        self.velx, self.vely = velx, vely

        if direction == 'n':
            south = pygame.transform.rotate(Laser.imgs[type_], 90)  # CCW
            self.img = pygame.transform.flip(south, False, True)

        if direction == 's':
            self.img = pygame.transform.rotate(Laser.imgs[type_], 90)  # CCW

        if direction == 'e':
            self.img = pygame.transform.flip(Laser.imgs[type_], True, False)

        if direction == 'w':
            self.img = Laser.imgs[type_]

        pygame.Rect.__init__(self, x, y, Laser.width, Laser.height)

        Laser.List.append(self)

    def offscreen(self, screen):

        if self.x < 0:
            return True
        elif self.y < 0:
            return True
        elif self.x + self.width > screen.get_width():
            return True
        elif self.y + self.height > screen.get_height():
            return True
        return False

    @staticmethod
    def super_massive_jumbo_loop(screen):
        """
        super_massive_jumbo_loop(screen) -> Loop that deals with the removing
        of enemies, and bullets that are shot offscreen
        """
        for bullet in Laser.List:

            bullet.x += bullet.velx
            bullet.y += bullet.vely

            screen.blit(bullet.img, (bullet.x, bullet.y))

            if bullet.offscreen(screen):
                Laser.List.remove(bullet)
                continue

            for robot in Robot.List:
                if bullet.colliderect(robot):

                    """
                    The same bullet cannot be used to kill
                    multiple robot and as the bullet was
                    no longer in Laser.List error was raised
                    """

                    robot.health -= Laser.gun_dmg[bullet.type]
                    robot.healthbar.update()
                    robot.healthbar.draw(screen)

                    Laser.List.remove(bullet)
                    break

            for tile in Tile.List:

                if bullet.colliderect(tile) and not(tile.walkable):
                    try:
                        Laser.List.remove(bullet)
                    except:
                        break  # if bullet cannot be removed, then GTFO


class Treasure(pygame.Rect):

    """
    Class that represents the object that the MainCharacter has to
    steal
    """

    List = []
    treasure_img = (
        "img/object_1.png",
        "img/object_2.png",
        "img/object_3.png",
        "img/object_4.png",
    )

    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, Dimensions.width, Dimensions.height)
        self.img = pygame.image.load(Treasure.treasure_img[0])
        Treasure.List.append(self)

    @staticmethod
    def draw(screen):
        for treasure in Treasure.List:
            screen.blit(treasure.img, (treasure.x, treasure.y))


class Tile(pygame.Rect):

    # The tuple of posible tile images
    TileImageTuple = (
        'img/wall.png',
        'img/light_gray_tile.png',
        'img/sewer_tile.png',
        'img/radioactive_tile.png'
    )

    List = []
    # Determines the height and width of the labyrith tiles
    width, height = Dimensions.width, Dimensions.height
    # The total tiles of the labyrinth
    total_tiles = 1
    # The horizontal and vertical difference between one tile
    # and another
    HorizontalDifference, VerticalDifference = 1, 64
    # level = Level()
    # invalids = level.leve1()

    def __init__(self, x, y, Type, level):

        self.parent = None
        self.HorizontalDifference, self.G, self.F = 0, 0, 0

        self.type = Type
        self.number = Tile.total_tiles
        Tile.total_tiles += 1

        if Type == 'empty':
            self.walkable = True
        else:
            self.walkable = False

        pygame.Rect.__init__(self, (x, y), (Tile.width, Tile.height))

        # Add tile to list of tiles
        Tile.List.append(self)

    @staticmethod
    def get_tile(number):
        for tile in Tile.List:
            if tile.number == number:
                return tile

    @staticmethod
    def draw_tiles(screen):
        pass

    @staticmethod
    def set_door_open(character):
        if character.description == "maincharacter":
            for i in Tile.level.level1_player1_coordinates():
                tile = Tile.get_tile(i)
                Tile.List.remove(tile)

                tile.walkable = True
                tile.type = "empty"
                Tile.List.append(tile)

        elif character.description == "enemy":
            for i in Tile.level.level1_player2_coordinates():
                tile = Tile.get_tile(i)
                Tile.List.remove(tile)

                tile.walkable = True
                tile.type = "empty"
                Tile.List.append(tile)


class Lever(pygame.sprite.Sprite):

    """The class for the lever object"""
    width = Dimensions.width
    height = Dimensions.height

    allLevers = pygame.sprite.Group()  # The group of levers

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        Lever.allLevers.add(self)
        self.image = pygame.image.load(image)
        self.animatedImages = itertools.cycle(
            (pygame.image.load(re.sub(r'\d', '1', image)),
             pygame.image.load(re.sub(r'\d', '2', image)),
             pygame.image.load(image)

             )
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.off = True

    def destroy(self):
        Lever.allLevers.remove(self)
        del self

    def turnOn(self, screen):
        """
        turnOn() -> Method that is triggered when the MainCharacter or Enemy
        touch a Lever and this causes the lever to open the doors
        """
        self.off = False
        self.image = next(self.animatedImages)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.time.delay(1000)
        self.image = next(self.animatedImages)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def isNotActivated(self):
        return self.off


class Door(pygame.sprite.Sprite):
    """
    Represents the door object
    """
    open_door_image = "img/brown_tile.png"
    closed_door_image = "img/radioactive_tile.png"
    List = []

    def __init__(self, x, y, toggled, numberTiles):
        pygame.sprite.Sprite.__init__(self)

        self.image = Door.closed_door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.toggled = toggled
        self.numTiles = numberTiles
        Door.List.append(self)

    def toggle(self):
        self.toggled = not self.toggled
        if self.toggled:
            self.image = Door.open_door_image
        else:
            self.image = Door.closed_door_image

    def draw_door(self, screen):
        """
        This method draws the door with the corresponding number of tiles
        """
        for tile in range(self.numTiles):
            screen.blit(self.image, (self.rect.x + self.rect.width * tile, self.rect.y))

    @staticmethod
    def draw(screen):
        for door in Door.List:
            door.draw_door(screen)

