#!/usr/bin/env python3
import pygame


class Level:

    """
    This class represents the different levels of the game and
    allows for scalability of the game
    """

    @staticmethod
    def cycle_check(toggle_objects):
        """
        Check if toggle chains in toggle_objects do not contain cycles
        A cycle would cause problems in non-reentrant functions and
        would exceed the maximum call depth when an object in that
        cycle calls its toggle method
        """
        h = []
        for x in toggle_objects: 
            for y in toggle_objects[x]:
                h.append((x, y))

        nh = [('a','a')]
        while len(nh)>0:
            nh = []
            for p in h:
                for q in h:
                    np = (p[0], q[1])
                    if p[1] == q[0] and np not in h and np not in nh:
                        nh.append(np)
            h.extend(nh)

        for x, y in h:
            if x == y:   # the toggle method of x would call itself after a while
                return False

        return True


    @staticmethod
    def unique_type_check(objects):
        """
        Check if names in objects have one unique type
        """
        names_with_type = set()
        r_objects = {}
        for k in self.objects:
            for l in self.objects[k]:
                names_with_type.add(l)
                try:
                    class_identifier = r_objects[l]
                except KeyError:
                    r_object[l] = k
                else:
                    if class_identifier != k:
                        return False

        return True


    @staticmethod
    def unrecognized_symbol_check(objects, rep, toggle_objects):
        """
        Check if names in rep and toggle_objects are declared in objects
        """
        names_with_type = set()
        for k in self.objects:
            for l in self.objects[k]:
                names_with_type.add(l)

        lines = len(rep)
        columns = len(rep[0])

        for y in range(lines):
            for x in range(columns):
                if self.rep[y][x] not in names_with_type:
                    return False

        if len(set(toggle_objects.keys()).difference_update(names_with_type))>0:        
            return False
        else:
            return True


    def __init__(self, rep, objects, toggle_objects, width, height, min_tile_w, min_tile_h):
        """
        Creates a Level instance from ascii text representation
        Requires:
            rep : list of ascii string (one for each row) representing
            the whole initial map.
            objects : a dictionary from class identifiers to object symbols used to recognize the ascii representation.
                Example: {'lever':{'l', 'm'}, 'door':{'p','q','r'}}.
                Meaning: 'l' and 'm' are 'lever' objects
                         'p', 'q', and 'r' are 'door' objects
                         The class associated to 'door' is not known yet.
            toggle_objects : a dictionary from chars to toggle affected chars
                Example: {'l':{'p'}, 'm':{'q', 'r'}}
                The lever whose char is 'l' in the representation toggles door 'p'.
                The lever whose char is 'm' toggles door 'q' and 'r'.
            min_tile_w : width of the smallest tile (cell width)
            min_tile_h : height of the smallest tile (cell height)
        """
        lines = len(rep)
        columns = len(rep[0])

        if min_tile_w * columns != width or min_tile_h * lines != height:
            raise RuntimeWarning("Tile-based surface dimensions do not match background dimensions")
        elif not unrecognized_symbol_check(objects, rep, toggle_objects):
            raise RuntimeWarning("Object symbol class identifier not declared")
        elif not unique_type_check(objects):
            raise RuntimeWarning("Object name does not have an unique class identifier")
        elif not cycle_check(toggle_objets):
            raise RuntimeWarning("Cycle in toggle chain")

        self.rep = rep
        self.objects = objects
        self.toggle_objects = toggle_objects
        self.width = width
        self.height = height
        self.min_tile_w = min_tile_w
        self.min_tile_h = min_tile_h


    def build_static_background(self, bg_tile_map, default='default'):
        """
        Creates the static background that remains unchanged while playing this level and returns it.
        Requires:
            bg_tile_map: a dictionary from char to tile images needed to build background.
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        background = pygame.Surface((self.width, self.height))
        #tile_rect = bg_tile_map['default'].get_rect()

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


    def build_objects(self, class_map, values):
        """
        Creates the objects involved in this level and returns then in a dictionary form.
        It creates a static "List" attribute for each class that groups all its instances.
        It builds each object and then appends it to its class "List".
        It also adds a toggle_affected attribute that relates toggle causing object to toggle affected object.
        Requires:
            class_map: a dictionary from class identifiers to class needed to build the objects.
            values : a dictionary from object symbol to **kwargs for instance creation
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
                    try:
                        model_class = class_map[class_identifier]
                    except KeyError:
                        raise RuntimeWarning("Missing class for '"+ class_identifier+"'")
                    else:
                        model_instance = model_class(self.values[self.rep[y][x]])  # **kwargs for instance creation
                        try:
                            class_map[class_identifier].List.append(model_instance)
                        except AttributeError:
                            class_map[class_identifier].List = [ model_instance ]

                        for obj in self.objects[class_identifier]:
                            if self.objects[class_identifier][obj] isinstance(set):   
                                # obj toggle propagates to these (maybe not constructed yet) objects
                                try:
                                    dependencies[self.rep[y][x]].update(self.objects[class_identifier][obj])
                                except KeyError:
                                    dependencies[obj] = set(self.objects[class_identifier][obj])

                        try:
                            built_models[class_identifier].append(model_instance)
                        except KeyError:
                            built_models[class_identifier] = [ model_instance ]


    def unwalkable_coordinates(self, ignore):
        """
        Returns the unwalkable coordinates not contained in ignore list
        """
        pass
