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
    def __init__(self, agent_conn, child_conn, initial_state, depth):
        multiprocessing.Process.__init__(self)
        self.level1 = A_star()
        self.level2 = AB(initial_state, depth)
        self.agent_conn = agent_conn
        #self.ready = threading.Event()
        #self.access_lock = threading.Lock()


    def send_plan(self):
        #self.access_lock.acquire()
        self.agent_conn.send(self.plan)
        #self.access_lock.release()


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
    def __init__(self, think_conn):
        self.think_conn = think_conn

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
        if self.think_conn.poll():
            self.plan = self.think_conn.recv()


class AgentServer:
    """
    This class holds a common processed view of the world where
    agents can act through their assets. It begins based on 
    initial level representation and evolves through events.
    This class is a singleton, use get() class method to retrieve
    the instance.
    """
    instance = None
    
    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    def __init__(self):
        self.core_list = []
      

    def newAgent(self):
        """
        Creates a new agent and prepares data structures.
        """
        think_conn, agent_conn = multiprocessing.Pipe()
        parent_conn, child_conn = multiprocessing.Pipe()
        agent = Agent(think_conn)
        think = Think(agent_conn, child_conn)
        self.core_list.append((agent, think, parent_conn))
        return agent

    def startAll(self):
        """
        Order the execution of all AI cores registered in the server.
        """
        for core in self.core_list:
            core[1].start()

    def stopAll(self):
        """
        Order the shutdown of all AI cores running in the server.
        """
        pass

    def moveEast(self):
        """
        moveEast() -> Notifies asset has moved east one tile
        """
        pass

    def moveWest(self):
        """
        moveWest() -> Notifies asset has moved west one tile
        """
        pass

    def moveNorth(self):
        """
        moveNorth() -> Notifies asset has moved north one tile
        """
        pass

    def moveSouth(self):
        """
        moveSouth() -> Notifies asset has moved south one tile
        """
        pass
        

    def changeGun(self):
        """
        Method that notifies that asset has changed guns
        changeGun() -> switches to the next gun, so if the automatic gun
        was the current gun, then the shotgun is now the current gun and
        vice-versa
        """
        pass

    def fireWest(self):
        """
        Method that notifies that asset has fired the current gun to the left
        """
        pass

    def fireNorth(self):
        """
        Method that notifies that asset has fired the current gun up
        """
        pass

    def fireEast(self):
        """
        Method that notifies that asset has fired the current gun east
        """
        pass

    def fireSouth(self):
        """
        Method that notifies that asset has fired the current gun down
        """
        pass       
        

