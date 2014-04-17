#!/usr/bin/env python3

import numpy as np


class Level:

    """
    This class represents the different levels of the game and
    allows for scalability of the game
    """

    def __init__(self):
        """
        Creates a Level instance that has a list that determines
        the walls for the user
        """
        self.labyrinthList = []

    def leve1(self):
        """
        This method returns the labyrith for level1
        """
        # The labyrith
        self.labyrinthList = [i * 64 + 7 for i in range(3)]
        self.labyrinthList.extend([i * 64 + 22 for i in range(10)])
        self.labyrinthList.extend([i * 64 + 7 for i in range(7, 10)])
        self.labyrinthList.extend([i + (64 * 10) for i in range(7, 23)])
        self.labyrinthList.extend([i + (64 * 2) for i in range(8)])
        self.labyrinthList.extend([i + (64 * 7) for i in range(5, 8)])
        self.labyrinthList.extend([i * 64 + 5 for i in range(7, 30)])
        self.labyrinthList.extend([i + (64 * 30) for i in range(5, 28)])
        self.labyrinthList.extend([i * 64 + 22 for i in range(33, 38)])
        self.labyrinthList.extend([i + (64 * 33) for i in range(5, 23)])
        self.labyrinthList.extend([i + (64 * 37) for i in range(5, 23)])
        self.labyrinthList.extend([i * 64 + 5 for i in range(33, 38)])
        self.labyrinthList.extend([i + (64 * 40) for i in range(5, 26)])
        self.labyrinthList.extend([i * 64 + 7 for i in range(7, 10)])
        self.labyrinthList.extend([i * 64 + 5 for i in range(40, 49)])
        self.labyrinthList.extend([i * 64 + 25 for i in range(33, 41)])
        self.labyrinthList.extend([i + (64 * 33) for i in range(25, 31)])
        # self.labyrinthList.extend([i + (64 * 33) for i in range(32, 39)])
        self.labyrinthList.extend([i * 64 + 30 for i in range(25, 33)])
        self.labyrinthList.extend([i * 64 + 27 for i in range(22, 31)])
        self.labyrinthList.extend([i + (64 * 22) for i in range(27, 33)])
        self.labyrinthList.extend([i + (64 * 25) for i in range(30, 35)])

        # self.labyrinthList.extend([i * 64 + 57 for i in range(3)])
        # self.labyrinthList.extend([i * 64 + 42 for i in range(10)])
        # self.labyrinthList.extend([i * 64 + 57 for i in range(7, 10)])
        # self.labyrinthList.extend([i + (64 * 10) for i in range(42, 58)])
        return np.array(self.labyrinthList)

