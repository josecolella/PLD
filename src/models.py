#!/usr/bin/env python3
# Module where the models are built
# This includes the characters, enemies, and objects of the game
import pygame
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

    colors = {
        'green': (0, 255, 0),
        'orange': (255, 165, 0),
        'red': (255, 0, 0),
        'blue': (0, 0, 255)
    }

    def __init__(self, boss):

        self.boss = boss
        self.image = pygame.Surface((self.boss.width * 2, 7))
        self.image.set_colorkey((0, 0, 0))  # black transparent
        self.color = Livebar.colors['green']
        pygame.draw.rect(
            self.image, self.color,
            (0, 0, self.boss.width * 2, 7), 1)

        self.rect = self.image.get_rect()
        self.rect.x = self.boss.x
        self.rect.y = self.boss.y
        pygame.draw.rect(
            self.image, Livebar.colors['blue'],
            (0, 0, self.boss.width / 2, 5), 1)

        self.oldpercent = 0

        pygame.Rect.__init__(
            self, self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self):
        self.percent = self.boss.health / self.boss.__class__.health
        if self.percent != self.oldpercent or self.boss.treasureCaptured:
            # fill black
            if self.percent != self.oldpercent and self.percent > 0:
                self.color = self.percentageColor()
            pygame.draw.rect(
            self.image, self.color,
            (0, 0, self.boss.width * 2, 7), 1)
            if self.boss.treasureCaptured:
                pygame.draw.rect(
                self.image, Livebar.colors['blue'],
                (0, 0, self.boss.width /2, 5), 1)
            pygame.draw.rect(
                self.image, (0, 0, 0), (1, 1, self.boss.width * 2 - 2, 5))
            pygame.draw.rect(self.image, self.color, (1, 1,
                                                       int(self.boss.width * 2 * self.percent), 5), 0)
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.centerx + 7
        self.rect.centery = self.boss.centery - \
            self.boss.height / 2 - 15

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.boss.treasureCaptured:
            screen.blit(pygame.transform.scale(self.image, (7, 7)), (self.rect.x + self.boss.width -4, self.rect.y - 15))
    def percentageColor(self):
        tup = None
        if self.percent >= 0.7:
            tup = Livebar.colors['green']
        elif self.percent >= 0.3 and self.percent < 0.7:
            tup = Livebar.colors['orange']
        elif self.percent >= 0.0 and self.percent < 0.3:
            tup = Livebar.colors['red']
        return tup


class Character(pygame.Rect):

    """
    This class is an abstract concept of what all
    classes should contain.
    """

    guns_img = (
        pygame.image.load("img/shotgun.png"),
        pygame.image.load("img/automatic.png")
    )

    width, height = Dimensions.width, Dimensions.height

    def __init__(self, x, y):

        self.tx, self.ty = None, None
        self.treasureCaptured = False
        self.currentGun = 0  # 0 -> shotgun, 1 -> automatic

        # Use cycle so that it iterates forever
        self.walking_west_images = itertools.cycle(
            (self.imgPath+'w_walk_l.png',
             self.imgPath+'w.png',
             self.imgPath+'w_walk_r.png'
             )
        )
        self.walking_east_images = itertools.cycle(
            (self.imgPath+'e_walk_l.png',
             self.imgPath+'e.png',
             self.imgPath+'e_walk_r.png'
             )
        )
        self.walking_north_images = itertools.cycle(
            (self.imgPath+'n_walk_l.png',
             self.imgPath+'n.png',
             self.imgPath+'n_walk_r.png'
             )
        )
        self.walking_south_images = itertools.cycle(
            (self.imgPath+'s_walk_l.png',
             self.imgPath+'s.png',
             self.imgPath+'s_walk_r.png'
             )
        )

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

    def rotate(self, direction):
        """
        Method created to manage the rotation of the Character
        and to set the appropriate image
        """
        png = '.png'

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                self.img = pygame.image.load(self.imgPath + self.direction + png)

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = pygame.image.load(self.imgPath + self.direction + png)

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = pygame.image.load(self.imgPath+self.direction + png)

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = pygame.image.load(self.imgPath+self.direction+png)


    # def rotate(self, direction, original_img):

    #     if direction == 'n':
    #         if self.direction != 'n':
    #             self.direction = 'n'
    #             south = pygame.transform.rotate(original_img, 90)  # CCW
    #             self.img = pygame.transform.flip(south, False, True)

    #     if direction == 's':
    #         if self.direction != 's':
    #             self.direction = 's'
    #             self.img = pygame.transform.rotate(original_img, 90)  # CCW

    #     if direction == 'e':
    #         if self.direction != 'e':
    #             self.direction = 'e'
    #             self.img = pygame.transform.flip(original_img, True, False)

    #     if direction == 'w':
    #         if self.direction != 'w':
    #             self.direction = 'w'
    #             self.img = original_img
    def movement(self, screen):
        """
        This method deals with everything related to the movement of the character.
        This method also manages the switch between the character walking with the left foot
        and then right foot to give the walk a realistic feel
        """
        if self.tx is not None and self.ty is not None:  # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            if X < 0:  # --->
                self.img = pygame.image.load(next(self.walking_east_images))
                self.x += self.velocity
            elif X > 0:  # <----
                self.img = pygame.image.load(next(self.walking_west_images))
                self.x -= self.velocity
            if Y > 0:  # up
                self.img = pygame.image.load(next(self.walking_north_images))
                self.y -= self.velocity
            elif Y < 0:  # dopwn
                self.img = pygame.image.load(next(self.walking_south_images))
                self.y += self.velocity
            screen.blit(self.img, (self.x, self.y))

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    def get_bullet_type(self):
        """
        get_bullet_type() -> str the current bullet
        """
        if self.currentGun == 0:
            return 'automatic'
        elif self.currentGun == 1:
            return 'shotgun'

    def changeGun(self):
        """
        Method that allows the character to change guns
        changeGun() -> switches to the next gun, so if the automatic gun
        was the current gun, then the shotgun is now the current gun and
        vice-versa
        """
        self.currentGun += 1
        self.currentGun %= len(Laser.imgs)

    def fireWest(self):
        """
        Method that allows the Character to fire the current gun to the left
        fireWest() -> Character will rotate west and fire
        """
        self.rotate('w')
        Laser(self.centerx, self.centery,
              -10, 0, 'w', self.get_bullet_type())

    def fireNorth(self):
        """
        Method that allows the Character to fire the current gun up
        fireWest() -> Character will rotate north and fire
        """
        self.rotate('n')
        Laser(self.centerx, self.centery,
              0, -10, 'n', self.get_bullet_type())

    def fireEast(self):
        """
        Method that allows the Character to fire the current gun east
        fireWest() -> Character will rotate east and fire
        """
        self.rotate('e')
        Laser(self.centerx, self.centery,
              10, 0, 'e', self.get_bullet_type())

    def fireSouth(self):
        """
        Method that allows the Character to fire the current gun down
        fireWest() -> Character will rotate down and fire
        """
        self.rotate('s')
        Laser(self.centerx, self.centery,
              0, 10, 's', self.get_bullet_type())

    def _move(self, direction, difference):
        """
        move(direction, difference) -> The Character moves to the direction
        that is specified by the direction string, by the amount
        that is specified by the difference if it is possible
        """
        future_tile_number = self.get_number() + difference
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile = Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                self.set_target(future_tile)
                self.rotate(direction)

    def moveEast(self):
        """
        moveEast() -> The Character will move east one tile
        """
        self._move('e', Tile.HorizontalDifference)

    def moveWest(self):
        """
        moveWest() -> The Character will move west one tile
        """
        self._move('w', - Tile.HorizontalDifference)

    def moveNorth(self):
        """
        moveNorth() -> The Character will move north one tile
        """
        self._move('n', - Tile.VerticalDifference)

    def moveSouth(self):
        """
        moveSouth() -> The Character will move south one tile
        """
        self._move('s', Tile.VerticalDifference)

    def draw(self, screen):
        """
        draw(screen) -> Displays the Character in the screen with it's healthbar
        """
        screen.blit(self.img, (self.x, self.y))
        self.healthbar.update()
        self.healthbar.draw(screen)

        h = self.width / 2
        img = Character.guns_img[self.currentGun]

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

        if self.health <= 0:
            self.__class__.List.remove(self)

    def satifiesWinConditions(self, coordinates):

        if self.treasureCaptured and (self.x, self.y) in coordinates:
            return True
        else:
            return False


class MainCharacter(Character):

    """
    This class represents the MainCharacter for the
    game
    """

    health = 100
    List = []

    def __init__(self, x, y):
        """
        Initializes the main character in the specified
        x and y coordinates of the map
        """
        self.health = MainCharacter.health
        self.healthbar = Livebar(self)
        self.description = "maincharacter"
        self.direction = 'w'
        self.velocity = 16
        self.imgPath = 'img/player_'
        self.img = pygame.image.load(self.imgPath+'w.png')

        Character.__init__(self, x, y)
        MainCharacter.List.append(self)

    @staticmethod
    def clear():
        MainCharacter.List.clear()


class Robot(Character):

    """
    The class that represents the robots that
    defend the Treasure
    """

    health = 100
    List = []
    original_img = pygame.image.load('img/guardian_s.png')
    robot_sound = itertools.cycle(
        ('audio/findseekanddestroy.ogg', 'audio/cmu_us_rms_arctic_clunits.ogg')
    )

    def __init__(self, x, y):
        self.health = Robot.health
        self.healthbar = Livebar(self)
        self.direction = 's'
        self.health = Robot.health
        self.img = Robot.original_img
        self.imgPath = 'img/guardian_'

        Character.__init__(self, x, y)

        Robot.List.append(self)

    @staticmethod
    def draw_robots(screen):
        for robot in Robot.List:
            robot.draw(screen)

    @staticmethod
    def movement(screen):
        for robot in Robot.List:
            # Target is set
            robot.movement(screen)

    '''
    def spawn(total_frames, FPS):
        if total_frames % (FPS * 3) == 0:

            sound = pygame.mixer.Sound(next(Robot.robot_sound))
            sound.play()

            tile_num = next(Robot.spawn_tiles_iter)
            spawn_node = Tile.get_tile(tile_num)
            Robot(spawn_node.x, spawn_node.y)
    '''
    @staticmethod
    def clear():
        Robot.List.clear()


class Enemy(Character):

    """
    This class represents the enemy that the MainCharacter will
    compete against to steal the Treasure
    """
    List = [] # A List of enemies
    health = 100

    def __init__(self, x, y):
        """
        Initializes the main character in the specified
        x and y coordinates of the map
        """
        self.health = Enemy.health
        self.healthbar = Livebar(self)
        self.description = "enemy"
        self.velocity = 4 # The enemy velocity
        self.direction = 'w'
        self.imgPath = 'img/thief_'
        self.img = pygame.image.load(self.imgPath+'w.png')

        Enemy.List.append(self)
        Character.__init__(self, x, y)

    @staticmethod
    def clear():
        Enemy.List.clear()


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

    @staticmethod
    def clear(self):
        Laser.List.clear()


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
        self.img = pygame.image.load(Treasure.treasure_img[0]).convert_alpha()
        self.isCaptured = False
        Treasure.List.append(self)


    @staticmethod
    def pickUpObject(player):
        """
        pickObject() -> The method that allows the Character to pick object
        """
        for treasure in Treasure.List:
            distance2 = (treasure.x-player.x)*(treasure.x-player.x)+(treasure.y-player.y)*(treasure.y-player.y)
            if distance2 < 4 * (treasure.width * treasure.width+ treasure.height*treasure.height):
                if not player.treasureCaptured:
                    player.treasureCaptured = True
                    treasure.isCaptured = True
                    treasure.showCaptured()

    @staticmethod
    def dropObject(player):
        """
        dropObject() -> The method that allows the Character to drop the object
        """
        for treasure in Treasure.List:
            if player.treasureCaptured:
                player.treasureCaptured = False
                treasure.x = player.x
                treasure.y = player.y
                treasure.img = pygame.image.load(Treasure.treasure_img[0])

    def showCaptured(self):
        self.img = pygame.image.load("img/light_gray_tile.png")

    def showNotCaptured(self):
        self.isCaptured = False

    @staticmethod
    def draw(screen):
        for treasure in Treasure.List:
            screen.blit(treasure.img, (treasure.x, treasure.y))

    @staticmethod
    def clear():
        Treasure.List.clear()


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
    # and another (64x16 = 1024 = screen.width)
    HorizontalDifference, VerticalDifference = 1, 64

    def __init__(self, x, y, Type):

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

    @staticmethod
    def clear():
        Tile.List.clear()
        Tile.total_tiles = 1


class Lever(pygame.sprite.Sprite):

    """The class for the lever object"""
    width = Dimensions.width
    height = Dimensions.height

    allLevers = pygame.sprite.Group()  # The group of levers

    def get_number(self):

        return ((self.rect.x / Lever.width) + Tile.HorizontalDifference) + ((self.rect.y / Lever.height) * Tile.VerticalDifference)

    def get_tile(self):

        return Tile.get_tile(self.get_number())

    def __init__(self, x, y, image, screen):
        pygame.sprite.Sprite.__init__(self)

        Lever.allLevers.add(self)
        self.image = pygame.image.load(image)
        self.animatedImages = itertools.cycle(
            (pygame.image.load(re.sub(r'\d', '1', image)),
             pygame.image.load(re.sub(r'\d', '2', image)),

             )
        )
        self.reverseAnimatedImages = itertools.cycle(
            (pygame.image.load(re.sub(r'\d', '1', image)),
             pygame.image.load(image),

             )
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        tile = self.get_tile()
        tile.walkable = False
        tile.type = 'solid'
        self.off = True

    def destroy(self):
        Lever.allLevers.remove(self)
        del self

    def turnOn(self):
        """
        turnOn() -> Method that is triggered when the MainCharacter or Enemy
        touch a deactivated Lever
        """
        self.off = False
        self.turnOnAnimation()

    def turnOnAnimation(self):
        self.image = next(self.animatedImages)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.time.delay(1000)
        self.image = next(self.animatedImages)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def turnOff(self):
        """
        turnOff() -> Method that is triggered when the MainCharacter or Enemy
        touch an activated Lever
        """
        self.off = True
        self.turnOffAnimation()

    def turnOffAnimation(self):
        self.image = next(self.reverseAnimatedImages)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.time.delay(1000)
        self.image = next(self.reverseAnimatedImages)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def isNotActivated(self):
        return self.off

    def toggle(self, doToggle=True):
        if self.isNotActivated():
            self.turnOn()
        else:
            self.turnOff()

        if hasattr(self, 'toggle_objects') and doToggle:
            for obj in self.toggle_objects:
                obj.toggle()

    @staticmethod
    def interactionToggleHandler(player):
        """
        Method that handles the interaction of toggling the lever when the instance
        of the player parameter is close to the lever

        Parameters
        ----------
        player : instance of a class that extends Character
           The instance of the player that is interacting with the game
        """
        for lever in Lever.allLevers:
                distance2 = (lever.rect.x-player.x)*(lever.rect.x-player.x)+(
                    lever.rect.y-player.y)*(lever.rect.y-player.y)
                if distance2 < 4 * (lever.width * lever.width+ lever.height*lever.height):
                    lever.toggle()

    @staticmethod
    def clear():
        Lever.allLevers.empty()


class Door(pygame.sprite.Sprite):
    """
    Represents the door object
    """
    open_door_image = pygame.image.load("img/brown_tile.png")
    closed_door_image = pygame.image.load("img/radioactive_tile.png")
    images = {
        'open': pygame.image.load("img/brown_tile.png"),
        'close': pygame.image.load("img/radioactive_tile.png")
    }
    List = []

    def get_number(self):

        return ((self.rect.x / self.rect.width) + Tile.HorizontalDifference) + ((self.rect.y / self.rect.height) * Tile.VerticalDifference)

    def get_tile(self):

        return Tile.get_tile(self.get_number())

    def __init__(self, x, y, toggled):
        pygame.sprite.Sprite.__init__(self)

        self.image = Door.closed_door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.toggled = toggled
        self.tile = self.get_tile()
        if self.toggled:
            self.tile.walkable = True
            self.tile.type = 'empty'
        else:
            self.tile.walkable = False
            self.tile.type = 'solid'

        Door.List.append(self)

    def toggle(self):
        self.toggled = not self.toggled

        self.toggleAction()

    def toggleAction(self):
        if self.toggled:
            self.image = Door.images['open']
        else:
            self.image = Door.images['close']

        if self.toggled:
            self.tile.walkable = True
            self.tile.type = 'empty'
        else:
            self.tile.walkable = False
            self.tile.type = 'solid'

        if hasattr(self, 'toggle_objects'):
            for obj in self.toggle_objects:
                obj.toggle()

    @staticmethod
    def draw(screen):
        for door in Door.List:
            screen.blit(door.image, (door.rect.x, door.rect.y))

    @staticmethod
    def clear():
        Door.List.clear()


class LevelList:
    """
    The object that represents all the levels in the game
    """

    def __init__(self, width, height, screen):
        """
        Creates a LevelList object that works with a certain width, height, and screen
        """
        self.width = width
        self.height = height
        self.screen = screen
        self.currentLevel = 1
        self.levels = {
            1: self.level1Representation(),
            2: self.level2Representation()
        }

    def allLevels(self):
        """
        Returns all the levels in the form of a tuple

        allLevels() -> tuple(dict, dict, ...)
        """
        return (i for i in self.levels.values())

    def level1Representation(self):
        """
        Returns the representation for the first level of the game

        level1Representation() -> dict with keys
            rep,
            objects,
            toggle_objects,
            tile_map, level,
            class_map, values,
            built_objects,
            coords,
            unwalkable
        """
        rep = Level.load_rep('level/level1.txt')
        objects = {
            'lever': {'l', 'm'},
            'door': {'p', 'q'},
            'player': {'j'},
            'enemy': {'e'},
            'object': {'a'},
            'robot': {'r'}
        }
        toggle_objects = {
            'l': {'p'},
            'm': {'q'}
        }
        tile_map = {
            'x': pygame.image.load('img/wall.png'),
            ',': pygame.image.load('img/dark_gray_tile.png'),
            '.': pygame.image.load('img/light_gray_tile.png'),
            '-': pygame.image.load('img/dark_red_tile.png')
        }
        level = Level(
            rep,
            objects,
            toggle_objects,
            self.width,
            self.height,
            Dimensions.width,
            Dimensions.height
        )
        class_map = {
            'lever': Lever,
            'robot': Robot,
            'enemy': Enemy,
            'player': MainCharacter,
            'door': Door,
            'object': Treasure
        }
        values = {
            'l':{'image':'img/lever_a_0.png', 'screen': self.screen},
            'm': {'image': 'img/lever_b_0.png', 'screen': self.screen},
            'p':{'toggled':False},
            'q': {'toggled': False},
            'j': {},
            'e': {},
            'a': {},
            'r': {}
        }

        coords = level.coordinates(['x'])
        unwalkable = {x for k in coords for x in coords[k]}

        level1Dict = {
          'levelIndex': 1,
          'rep': rep,
          'objects': objects,
          'toggle_objects': toggle_objects,
          'tile_map': tile_map,
          'level': level,
          'class_map': class_map,
          'values': values,
          'coords': coords,
          'unwalkable': unwalkable
        }
        return level1Dict

    def level2Representation(self):
        rep = Level.load_rep('level/level2.txt')
        objects = {
            'lever': {'l', 'm'},
            'door': {'p', 'q'},
            'player': {'j'},
            'enemy': {'e'},
            'object': {'a'},
            'robot': {'r'}
        }
        toggle_objects = {
            'l': {'p'},
            'm': {'q'}
        }
        tile_map = {
            'x': pygame.image.load('img/wall.png'),
            ',': pygame.image.load('img/dark_gray_tile.png'),
            '.': pygame.image.load('img/light_gray_tile.png'),
            '-': pygame.image.load('img/dark_red_tile.png')
        }
        level = Level(
            rep,
            objects,
            toggle_objects,
            self.width,
            self.height,
            Dimensions.width,
            Dimensions.height
        )
        class_map = {
            'lever': Lever,
            'robot': Robot,
            'enemy': Enemy,
            'player': MainCharacter,
            'door': Door,
            'object': Treasure
        }
        values = {
            'l':{'image':'img/lever_a_0.png', 'screen': self.screen},
            'm': {'image': 'img/lever_b_0.png', 'screen': self.screen},
            'p':{'toggled':False},
            'q': {'toggled': False},
            'j': {},
            'e': {},
            'a': {},
            'r': {}
        }

        coords = level.coordinates(['x'])
        unwalkable = {x for k in coords for x in coords[k]}

        level2Dict = {
          'levelIndex': 2,
          'rep': rep,
          'objects': objects,
          'toggle_objects': toggle_objects,
          'tile_map': tile_map,
          'level': level,
          'class_map': class_map,
          'values': values,
          'coords': coords,
          'unwalkable': unwalkable
        }
        return level2Dict

    def clearCurrentLevel(self):
        for key, value in self.levels[self.currentLevel]['class_map'].items():
            value.clear()

    def buildLevelObject(self, levelRepresentation):
        level = levelRepresentation['level']
        class_map = levelRepresentation['class_map']
        values = levelRepresentation['values']
        levelRepresentation['built_objects'] = level.build_objects(class_map, values)
        return levelRepresentation
