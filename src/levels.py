#!/usr/bin/env python3


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
>>>>>>> dev
        """
        This method returns the labyrith for level1
        """
<<<<<<< HEAD
        # The labyrith
        self.labyrinthList.extend(
            [7, 22, 42, 57, 71, 86, 106, 121, 128, 129, 130, 131, 132, 133, 134, 135, 135, 150, 170, 185, 214, 234, 249, 250, 251, 252, 253, 254, 255, 256, 278, 298, 342, 362, 406, 426, 453, 453, 454, 455, 455, 455, 470, 490, 505, 505, 506, 507, 508, 509, 509, 517, 519, 519, 534, 554, 569, 573, 581, 583, 583, 598, 618, 633, 637, 645, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 662, 682, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 701, 709, 726, 746, 765, 773, 790, 810, 829, 837, 854, 874, 893, 901, 918, 938, 957, 965, 982, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 992, 998, 998, 999, 1000, 1001, 1002, 1021, 1029, 1056, 1062, 1085, 1093, 1120, 1126, 1149, 1157, 1184, 1190, 1213, 1221, 1248, 1254, 1277, 1285, 1312, 1318, 1341, 1349, 1376, 1382, 1405, 1413, 1435, 1435, 1436, 1437, 1438, 1439, 1440, 1440, 1446, 1446, 1447, 1448, 1449, 1450, 1451, 1451, 1469, 1477, 1499, 1507, 1507, 1515, 1533, 1541, 1563, 1571, 1571, 1579, 1597, 1605, 1627, 1630, 1630, 1631, 1632, 1633, 1634, 1635, 1635, 1636, 1637, 1638, 1639, 1639, 1643, 1661, 1669, 1691, 1694, 1703, 1707, 1725, 1733, 1755, 1758, 1767, 1771, 1789, 1797, 1819, 1822, 1831, 1835, 1853, 1861, 1883, 1886, 1895, 1899, 1917, 1925, 1926, 1927, 1928, 1929, 1930,
             1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1947, 1950, 1959, 1963, 1963, 1963, 1964, 1964, 1965, 1965, 1966, 1966, 1967, 1967, 1968, 1968, 1969, 1969, 1970, 1970, 1971, 1971, 1972, 1972, 1973, 1973, 1974, 1974, 1975, 1975, 1976, 1976, 1977, 1977, 1978, 1978, 1979, 1979, 1980, 1980, 1981, 1981, 2014, 2023, 2078, 2087, 2117, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2134, 2137, 2137, 2138, 2139, 2140, 2141, 2142, 2151, 2151, 2152, 2153, 2154, 2155, 2156, 2157, 2160, 2160, 2161, 2162, 2163, 2164, 2165, 2166, 2167, 2168, 2169, 2169, 2181, 2198, 2201, 2221, 2224, 2233, 2245, 2262, 2265, 2285, 2288, 2297, 2309, 2326, 2329, 2349, 2352, 2361, 2373, 2373, 2374, 2375, 2376, 2377, 2378, 2379, 2380, 2381, 2382, 2383, 2384, 2385, 2386, 2387, 2388, 2389, 2390, 2390, 2393, 2413, 2416, 2416, 2417, 2418, 2419, 2420, 2421, 2422, 2423, 2424, 2425, 2425, 2457, 2477, 2521, 2541, 2565, 2565, 2566, 2567, 2568, 2569, 2570, 2571, 2572, 2573, 2574, 2575, 2576, 2577, 2578, 2579, 2580, 2581, 2582, 2583, 2584, 2585, 2585, 2605, 2605, 2606, 2607, 2608, 2609, 2610, 2611, 2612, 2613, 2614, 2615, 2616, 2617, 2629, 2681, 2693, 2745, 2757, 2809, 2821, 2873, 2885, 2937, 2949, 3001, 3013, 3065, 3077, 3129])
        # Level 1 doors
        self.labyrinthList.extend([1948, 1949, 1960, 1961, 1962])
        return self.labyrinthList

    def leve1_door_coordinates(self):
        """
        level1_door_coordinates() -> List
        Returns a list of the door coordinates
        """
        return [1948, 1949, 1960, 1961, 1962]

    def level1_player1_coordinates(self):
        return [1948, 1949]

    def level1_player2_coordinates(self):
        return [1960, 1961, 1962]

=======
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
                                print(" ** An error occurred when building object '"+self.rep[y][x]+
                                      "' of class '"+class_identifier+"'")
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
                            obj.toggle_objects.extend(built_models[tog])
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
>>>>>>> dev
