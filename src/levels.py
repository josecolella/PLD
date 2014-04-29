#!/usr/bin/env python3


class Level:

    """
    This class represents the different levels of the game and
    allows for scalability of the game
    """

    def __init__(self):
        """
        Creates a Level instance that has a list that determines
        the walls for the user. The initial wall are the outer boundaries
        for the game
        """
        # the initial points cover the top boundary, left boundary, right, and
        # bottom
        self.labyrinthList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                              14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                              26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                              38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                              50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
                              62, 63, 64, 1, 65, 129, 193, 257, 321, 385, 449,
                              513, 577, 641, 705, 769, 833, 897, 961, 1025, 1089,
                              1153, 1217, 1281, 1345, 1409, 1473, 1537, 1601, 1665,
                              1729, 1793, 1857, 1921, 1985, 2049, 2113, 2177, 2241,
                              2305, 2369, 2433, 2497, 2561, 2625, 2689, 2753, 2817,
                              2881, 2945, 3009, 64, 128, 192, 256, 320, 384, 448, 512,
                              576, 640, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216,
                              1280, 1344, 1408, 1472, 1536, 1600, 1664, 1728, 1792, 1856,
                              1920, 1984, 2048, 2112, 2176, 2240, 2304, 2368, 2432, 2496, 2560,
                              2624, 2688, 2752, 2816, 2880, 2944, 3008, 3072, 3009, 3010, 3011, 3012,
                              3013, 3014, 3015, 3016, 3017, 3018, 3019, 3020, 3021, 3022, 3023, 3024,
                              3025, 3026, 3027, 3028, 3029, 3030, 3031, 3032, 3033, 3034, 3035, 3036,
                              3037, 3038, 3039, 3040, 3041, 3042, 3043, 3044, 3045, 3046, 3047, 3048,
                              3049, 3050, 3051, 3052, 3053, 3054, 3055, 3056, 3057, 3058, 3059, 3060,
                              3061, 3062, 3063, 3064, 3065, 3066, 3067, 3068, 3069, 3070, 3071, 3072]

    def leve1(self):
        """
        This method returns the labyrith for level1
        """
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


class Level2:

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
        pass

    def build_static_background(self, bg_tile_map):
        """
        Creates the static background that remains unchanged while playing this level and returns it.
        Requires:
            bg_tile_map: a dictionary from char to tile images needed to build background.
        """
        pass

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
