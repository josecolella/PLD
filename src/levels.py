#!/usr/bin/env python3
import pygame


class Level:

    """
    This class represents the different levels of the game and
    allows for scalability of the game
    """

    def __init__(self, rep, objects, values, min_tile_w, min_tile_h):
        """
        Creates a Level instance from ascii text representation.
        Requires:
            rep : list of ascii string (one for each row) representing
            the whole map.
            objects : a dictionary with object name keys that associates
            them to chars and handles their toggle relations.
                Example: {'lever':{'l':{'p'}, 'm':{'q','r'}}, 'door':{'p','q','r'}}.
                The lever whose char is 'l' in the representation toggles door 'p'.
                The lever whose char is 'm' toggles door 'q' and 'r'.
            values : a dictionary from char to dictionary for instance creation
            min_tile_w : width of the smallest tile
            min_tile_h : height of the smallest tile
        """
        self.rep = rep
        self.objects = objects
        self.values = values
        self.min_tile_w = min_tile_w
        self.min_tile_h = min_tile_h


    def build_static_background(self, bg_tile_map, width, height, default='default'):
        """
        Creates the static background that remains unchanged while playing this level and returns it.
        Requires:
            bg_tile_map: a dictionary from char to tile images needed to build background.
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        background = pygame.Surface((width, height))
        #tile_rect = bg_tile_map['default'].get_rect()

        if self.min_tile_w*columns > width or self.min_tile_h*lines > height:
            print(" ** The text representation using current\n    tiles does not fit screen dimensions!")
            print(" ** WARNING: Using black background instead")
        else:
            for y in range(lines):
                for x in range(columns):
                    if self.rep[y][x] != ' ':   # used for tiles whose size is a multiple of the smallest tile dimensions
                        if self.rep[y][x] in bg_tile_map:
                            background.blit(
                                bg_tile_map[self.rep[y][x]], (self.min_tile_w * x, self.min_tile_h * y))
                        else:
                            background.blit(
                                bg_tile_map[default], (self.min_tile_w * x, self.min_tile_h * y))

        background = background.convert()
        return background


    def build_objects(self, class_map):
        """
        Creates the objects involved in this level and returns then in a dictionary form.
        It creates a static "List" attribute for each class that groups all its instances.
        It builds each object and then appends it to its class "List".
        It also adds an attribute that relates toggle causing class to toggle affected class.
        Requires:
            class_map: a dictionary from object names to class needed to build the objects.
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        r_objects = {}
        built_models = {}

        for k in self.objects:  # create a "reversed" version of self.objects
            for l in self.objects[k]:
                r_objects[l] = k

        for y in range(lines):
            for x in range(columns):
                if self.rep[y][x] in r_objects:  # tile symbol represents a model instance
                    class_identifier = r_objects[self.rep[y][x]]
                    self.values['x'] = self.min_tile_w * columns  # will override object position if given
                    self.values['y'] = self.min_tile_h * height
                    model_instance = class_map[class_identifier](self.values)  # **kwargs for constructor
                    try:
                        class_map[class_identifier].List.append(model_instance)
                    except AttributeError:
                        class_map[class_identifier].List = [ model_instance ]

                    try:
                        built_models[class_identifier].append(model_instance)
                    except KeyError:
                        built_models[class_identifier] = [ model_instance ]

        # TODO: propagation of toggle effects through toggle_ao attribute (idea: call x.toggle() for x in toggle_ao)
        # TODO: width and height size check


    def unwalkable_coordinates(self, ignore):
        """
        Returns the unwalkable coordinates not contained in ignore list
        """
        pass
