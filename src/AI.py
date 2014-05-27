"""
This module represents the Artificial Intelligence for the game
"""

import pygame
import multiprocessing


class MinimaxNode:
    pass


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


class Think(multiprocessing.Process):
    #The following class code is deprecated (thread oriented ...)
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


class Agent:
    """
    This class is a front end that manages the interaction between
    a game character and it's AI core running in a separate process.
    It captures events from the agent assets and sends them to the 
    agent server. When a response is available, it makes the agent assets
    execute their AI core commands.
    """
    def __init__(self):
        pass

    def addAsset(self, asset):
        """
        Add asset to this agent and send event to the server in order
        to make visible this change to the other agent cores.
        """
        pass

    def delAsset(self):
        """
        Remove asset from this agent and send event to the server in order
        to make visible this change to the other agent cores.
        """
        pass

    def start(self):
        """
        Order the execution of the AI core associated to this agent.
        """
        pass

    def stop(self):
        """
        Order the shutdown of the AI core associated to this agent.
        """
        pass

    def next(self):
        """
        Executes next command of the plan (if previous is complete).
        """
        pass


class AgentServer:
    """
    This class holds a common processed view of the world where
    agents can act through their assets. It begins based on 
    initial level representation and evolves through events.
    """
    def __init__(self):
        pass

    def newAgent(self):
        """
        Creates a new agent and prepares data structures.
        """
        pass

    def startAll(self):
        """
        Order the execution of all AI cores registered in the server.
        """
        pass

    def stopAll(self):
        """
        Order the shutdown of all AI cores running in the server.
        """
        pass


