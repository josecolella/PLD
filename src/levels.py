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

        nh = [('a', 'a')]
        while len(nh) > 0:
            nh = []
            for p in h:
                for q in h:
                    np = (p[0], q[1])
                    if p[1] == q[0] and np not in h and np not in nh:
                        nh.append(np)
            h.extend(nh)

        for x, y in h:
            # the toggle method of x would call itself after a while
            if x == y:
                return False

        return True

    @staticmethod
    def unique_type_check(objects):
        """
        Check if names in objects have one unique type
        """
        r_objects = {}
        for k in objects:
            for l in objects[k]:
                try:
                    class_identifier = r_objects[l]
                except KeyError:
                    r_objects[l] = k
                else:
                    if class_identifier != k:
                        return False

        return True

    @staticmethod
    def unrecognized_symbol_check(objects, toggle_objects):
        """
        Check if names in toggle_objects are declared in objects
        """
        names_with_type = set()
        for k in objects:
            for l in objects[k]:
                names_with_type.add(l)

        if len(set(toggle_objects.keys()).difference(names_with_type)) > 0:
            return False
        else:
            return True

    @staticmethod
    def load_rep(filename):
        """
        Loads filename content and interprets it as list of ascii string (one for each row)
        Returns the result
        """
        f = open(filename, 'r')
        rep = []

        for row in f:
            rep.append(row.strip())

        f.close()
        return rep

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
            raise RuntimeWarning(
                "Tile-based surface dimensions do not match background dimensions")
        elif not Level.unrecognized_symbol_check(objects, toggle_objects):
            raise RuntimeWarning("Object symbol class identifier not declared")
        elif not Level.unique_type_check(objects):
            raise RuntimeWarning(
                "Object name does not have an unique class identifier")
        elif not Level.cycle_check(toggle_objects):
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
        This method returns the labyrith for level1
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        background = pygame.Surface((self.width, self.height))
        #tile_rect = bg_tile_map['default'].get_rect()

        for y in range(lines):
            for x in range(columns):
                # used for tiles whose size is a multiple of the smallest tile
                # dimensions
                if self.rep[y][x] != ' ':
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
                # tile symbol represents a model instance
                if self.rep[y][x] in r_objects:
                    class_identifier = r_objects[self.rep[y][x]]

                    try:
                        model_class = class_map[class_identifier]
                    except KeyError:
                        raise RuntimeWarning(
                            "Missing class for '" + class_identifier + "' identifier")
                    else:
                        try:
                            initialization = values[self.rep[y][x]]
                        except KeyError:
                            raise RuntimeWarning("Missing initialization values for '" + self.rep[
                                                 y][x] + "' symbol of class '" + class_identifier + "'")
                        else:
                            # will override object position if given
                            initialization['x'] = self.min_tile_w * x
                            initialization['y'] = self.min_tile_h * y
                            # **kwargs for instance creation
                            try:
                                model_instance = model_class(**initialization)
                            except Exception:
                                print(" ** An error occurred when building object '" + self.rep[y][x] +
                                      "' of class '" + class_identifier + "'")
                                raise
                            # try:
                            #    class_map[class_identifier].List.append(model_instance)
                            # except AttributeError:
                            #    class_map[class_identifier].List = [ model_instance ]

                            try:
                                built_models[self.rep[y][x]].append(
                                    model_instance)
                            except KeyError:
                                built_models[self.rep[y][x]] = [
                                    model_instance]

        for s in built_models:
            if s in self.toggle_objects:
                for obj in built_models[s]:
                    for tog in self.toggle_objects[s]:
                        try:
                            obj.toggle_aobjects.extend(built_models[tog])
                        except AttributeError:
                            obj.toggle_objects = list(built_models[tog])

        return built_models

    def coordinates(self, symbols):
        """
        Returns the coordinates that correspond to the
        specified symbols
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        coordinates = {}

        for y in range(lines):
            for x in range(columns):
                if self.rep[y][x] in symbols:
                    try:
                        coordinates[self.rep[y][x]].append(
                            (self.min_tile_w * x, self.min_tile_h * y))
                    except KeyError:
                        coordinates[self.rep[y][x]] = [
                            (self.min_tile_w * x, self.min_tile_h * y)]

        return coordinates

    def conn_map(self):
        """
        Returns an abstract view of represented map. This includes a
        connection graph whose nodes are zones and a door map.
        """
        pass

    def get_agent_server(self):
        """
        Returns an agent server for this level. Only one exists per level.
        """
        pass

    def generateMapMatrix(self):
        pass
