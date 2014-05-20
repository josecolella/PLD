"""
This module represents the Artificial Intelligence for the game
"""

import pygame
import threading

class AB:
    def __init__(self, initial_state, depth):
        pass


    def __str__(self):
        pass


    def fathom(self):
        pass


    def max_depth_reached(self):
        pass


class A_star:
    def __init__(self, initial_state):
        pass


    def __str__(self):
        pass


    def search(self, target):
        pass


class Think(threading.Thread):
    def __init__(self, initial_state, depth):
        threading.Thread.__init__(self)
        self.level1 = A_star()
        self.level2 = AB(initial_state, depth)
        self.ready = threading.Event()
        self.access_lock = threading.Lock()


    def _reveal_plan(self, plan):
        self.access_lock.acquire()
        self.plan = plan
        self.access_lock.release()


    def run(self):
        while not self.level2.max_depth_reached():
            new_high_level_action = self.level2.fathom()
            new_plan = self.level1.search(new_high_level_action)
            self._reveal_plan(new_plan)

            if not self.ready.is_set():
                self.ready.set()


    def partial_plan(self):
        self.ready.wait()
        self.access_lock.acquire()
        plan = self.plan[:]
        self.access_lock.release()
        return plan


    def ready(self):
        return self.ready.is_set()



