#!/usr/bin/env python3
import pygame


class Level:

    """
    This class represents the different levels of the game and
    allows for scalability of the game
    """

    def __init__(self, rep, effects, toggle):
        """
        Creates a Level instance from ascii text representation.
        Requires:
            rep : list of ascii string (one for each row) representing
            the whole map.
            effects : a dictionary with object name keys that associates
            them to chars and handles their toggle relations.
            Example: {'lever':{'l':{'p'}, 'm':{'q','r'}}, 'door':{'p','q','r'}}.
            The lever whose char is 'l' in the representation toggles door 'p'.
            The lever whose char is 'm' toggles door 'q' and 'r'.
            toggle : a dictionary from char to True/False toggle state
        """
        self.rep = rep
        self.effects = effects

    def build_static_background(self, bg_tile_map, width, height):
        """
        Creates the static background that remains unchanged while playing this level and returns it.
        Requires:
            bg_tile_map: a dictionary from char to tile images needed to build background.
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        background = pygame.Surface((width, height))
        tile_rect = bg_tile_map['default'].get_rect()
        # length = screenrect.width / columns
        # height = screenrect.height / lines

        # wallblock = createblock(length, height, (20, 0, 50))
        # nextblock = createblock(length, height, (255, 50, 50))
        # prevblock = createblock(length, height, (255, 50, 255))
        # endblock = createblock(length, height, (100, 100, 100))
        # randomblock = createblock(length, height, (0, 0, 200))

        # background = background0.copy()

        for y in range(lines):
            for x in range(columns):
                if self.rep[y][x] in bg_tile_map:
                    background.blit(
                        bg_tile_map[self.rep[y][x]], (tile_rect.width * x, tile_rect.height * y))
                else:
                    background.blit(
                        bg_tile_map['default'], (tile_rect.width * x, tile_rect.height * y))

        return background

    def build_objects(self, class_map):
        """
        Creates the objects involved in this level and returns then in a dictionary form.
        It creates a static "List" attribute for each class that groups all its instances.
        It builds each object and then appends it to its class "List".
        It also adds an attribute that relates toggle causing class to toggle affected class.
        Requires:
            class_map: a dictionary from char to class needed to build the objects.
        """
        pass

    def unwalkable_coordinates(self, ignore):
        """
        Returns the unwalkable coordinates not contained in ignore list
        """
        pass
