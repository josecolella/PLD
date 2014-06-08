"""
This module represents the Artificial Intelligence for the game
"""

import pygame
import multiprocessing
import heapq


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


class A_starNode:
    def __init__(self, parent, asset_pos, asset_id, target_points, allowed_area):
        self.parent = parent
        self.asset_pos = asset_pos
        self.asset_id = asset_id
        self.target_points = target_points
        self.allowed_area = allowed_area
        self.g = parent.g+1
        self.h = min(( abs(t[0]-self.asset_pos[0])+abs(t[1]-self.asset_pos[1]) for t in self.target_points ))
        
    def __lt__(self, other):
        return (self.g+self.h) < (other.g+other.h)
        
    def expand(self):
        exp_nodes = []
        ldiff = [(0,16),(0,-16),(16,0),(-16,0)]
        list_fp = [ (self.asset_pos[0]+d[0], self.asset_pos[1]+d[1]) for d in ldiff ]
        for future_pos in list_fp:
            if future_pos in self.allowed_area:
                exp_nodes.append(A_starNode(self, future_pos, self.asset_id, self.target_points, self.allowed_area))
     
        return exp_nodes
           
    def is_solution(self):
        return self.asset_pos in self.target_points
        
    def get_root_path(self):
        path = []
        n = self                            
        while n is not None:
            x, y = n.asset_pos - n.parent.asset_pos                                            

            if x == 0:
                if y > 0:
                    path.append((self.asset_id, 'moveSouth'))
                else:
                    path.append((self.asset_id, 'moveNorth'))
            else:
                if x > 0:
                    path.append((self.asset_id, 'moveEast'))
                else:
                    path.append((self.asset_id, 'moveWest'))
                    
            n = n.parent
            
        return reversed(path)
        

class A_star:
    def __init__(self, start_node):
        self.opened = []
        self.closed = []
        self.start_node = start_node

    def search(self):
        plan = []
        actual = self.start_node
        solution_found = actual.is_solution()
        
        while not solution_found and len(self.opened)>0:
            actual = heapq.heappop(self.opened)
            solution_found = actual.is_solution()
            if not solution_found:
                exp_nodes = actual.expand()
                self.closed.append(actual)
                for n in exp_nodes:
                    heapq.heappush(self.opened, n)
                
        if solution_found:
            plan = actual.get_root_path()
            
        return plan


class Think(multiprocessing.Process):
    #The following class code is deprecated (thread oriented ...)
    def __init__(self, agent_conn, child_conn, depth):
        multiprocessing.Process.__init__(self)
        #self.level1 = A_star()
        #self.level2 = AB(initial_state, depth)
        self.agent_conn = agent_conn
        self.child_conn = child_conn
        self.depth = depth
        #self.ready = threading.Event()
        #self.access_lock = threading.Lock()


    def send_plan(self):
        #self.access_lock.acquire()
        self.agent_conn.send(self.plan)
        #self.access_lock.release()


    def run(self):
        thinking = True
        
        while thinking:
            if self.agent_conn.poll():
                from_agent = self.agent_conn.recv()
                
                if isinstance(from_agent, str):
                    if from_agent == 'bored':
                        print("Bored received. Sending nothing ...")
                        #self.agent_conn.send([ (0, 'fireNorth') * 40 ])
                        
            if self.child_conn.poll():
                from_server = self.child_conn.recv()
                
                if isinstance(from_server, str):
                    if from_server == 'shutdown':
                        print("Shutting down AI core ...")
                        thinking = False
                elif isinstance(from_conn, tuple):
                    pass
                    
            if thinking:
                pass
            '''        
            while not self.level2.max_depth_reached():
                new_high_level_action = self.level2.fathom()
                new_plan = self.level1.search(new_high_level_action)
                self._reveal_plan(new_plan)

                if not self.ready.is_set():
                    self.ready.set()
            '''

    '''
    def partial_plan(self):
        self.ready.wait()
        self.access_lock.acquire()
        plan = self.plan[:]
        self.access_lock.release()
        return plan


    def ready(self):
        return self.ready.is_set()
    '''

class FakeAgent:
    """
    This class notifies world changes caused by non-AI agent to the AgentServer.
    This class has the same Agent methods but some of them do nothing.
    """
    def __init__(self, agent_id, server):
        self.agent_id = agent_id
        self.server = server
        self.List = []

    def addAsset(self, asset):
        """
        Add asset to this agent and send event to the server in order
        to make visible this change to the other agent cores.
        """
        asset_id = len(self.List)
        self.List.append(asset)
        return asset_id

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
        This method does nothing.
        """
        pass                                                           

    def actionCompleted(self):
        """
        The current action has been completed.
        """
        pass
        
    def updateHealth(self, asset_id, health):
        pass


class Agent:
    """
    This class is a front end that manages the interaction between
    a game character and it's AI core running in a separate process.
    It captures events from the agent assets and sends them to the 
    agent server. When a response is available, it makes the agent assets
    execute their AI core commands.
    """
    def __init__(self, think_conn, agent_id, server):
        self.think_conn = think_conn
        self.agent_id = agent_id
        self.server = server
        self.engaged = True
        self.action_done = True
        self.pos = 0
        self.plan = []
        self.List = []

    def addAsset(self, asset):
        """
        Add asset to this agent and send event to the server in order
        to make visible this change to the other agent cores.
        """
        asset_id = len(self.List)
        self.List.append(asset)
        return asset_id

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
        Executes next command of the plan (if previous action has been completed).
        """
        if self.think_conn.poll():
            self.plan = self.think_conn.recv()
            self.pos = 0
            self.engaged = True
            print("Agent ID", self.agent_id, "is now engaged!")
                    
        if self.engaged:
            if self.pos == len(self.plan):
                self.think_conn.send('bored')
                self.engaged = False
            elif self.action_done:
                action = self.plan[self.pos]
                self.action_done = False
                asset = self.List[action[0]]
                print("Agent ID", self.agent_id, "is doing", action[1])

                if action[1] == 'moveEast':
                    asset.moveEast()
                elif action[1] == 'moveWest':
                    asset.moveWest()
                elif action[1] == 'moveNorth':
                    asset.moveNorth()
                elif action[1] == 'moveSouth':
                    asset.moveSouth()
                elif action[1] == 'changeGun':
                    asset.changeGun()
                elif action[1] == 'fireWest':
                    asset.fireWest()
                elif action[1] == 'fireNorth':
                    asset.fireNorth()
                elif action[1] == 'fireEast':
                    asset.fireEast()
                elif action[1] == 'fireSouth':
                    asset.fireSouth()                                                            

    def actionCompleted(self):
        """
        The current action has been completed.
        """
        self.action_done = True
        self.pos += 1
        
    def updateHealth(self, asset_id, health):
        print("Update Health request from agent", self.agent_id, "- asset", asset_id, "with value", health)

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
      

    def newAgent(self, depth):
        """
        Creates a new agent and prepares data structures.
        """
        think_conn, agent_conn = multiprocessing.Pipe()
        parent_conn, child_conn = multiprocessing.Pipe()
        agent = Agent(think_conn, len(self.core_list), self)
        think = Think(agent_conn, child_conn, depth)
        self.core_list.append((agent, think, parent_conn))
        return agent

    def newFakeAgent(self):
        """
        Creates a new fake agent and prepares data structures.
        """
        agent = FakeAgent(len(self.core_list), self)
        self.core_list.append((agent, None, None))
        return agent

    def startAll(self):
        """
        Order the execution of all AI cores registered in the server.
        """
        for core in self.core_list:
            try:
                core[1].start()
            except AttributeError:
                pass 

    def stopAll(self):
        """
        Order the shutdown of all AI cores running in the server.
        """
        for core in self.core_list:
            try:
                core[2].send('shutdown')
            except AttributeError:
                pass
                
        for core in self.core_list:
            try:
                core[1].join()
            except AttributeError:
                pass

    def configure(self):
        pass

    def clear(self):
        self.core_list = []

    def next(self):
        for agent, think, conn in self.core_list:
            agent.next()

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
        

