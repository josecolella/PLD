"""
This module represents the Artificial Intelligence for the game
"""

import pygame
import multiprocessing
import threading
import heapq
import copy
import time


class MinimaxNode:
    def __init__(self, zone_coord, coord_zone, zone_ady, door_map, door_name, agent_map, objeto, lever_name, toggle, world, alfa, beta, minmax_layout, depth, horizont):
        self.agent_map = agent_map
        self.zone_coord = zone_coord
        self.coord_zone = coord_zone
        self.zone_ady = zone_ady
        self.door_map = door_map
        self.door_name = door_name
        self.agent_map = agent_map
        self.objeto = objeto
        self.lever_name = lever_name
        self.toggle = toggle
        self.world = copy.deepcopy(world)
        self.depth = depth
        self.horizont = horizont

        try:
            self.assets_not_engaged.pop()
        except IndexError:
            try:
                self.agent_playing = self.agents_not_engaged.pop()
            except IndexError:
                self.depth += 1
                self.agents_not_engaged = list(self.agent_map.keys())
                self.agent_playing = self.agents_not_engaged.pop()
                
            self.assets_not_engaged = list(self.agent_map[self.agent_playing].keys())
            self.assets_not_engaged.pop()
                
        self.minmax_layout = minmax_layout
        self.is_max_node = self.minmax_layout[self.agent_playing]
        self.h_value = 0
        self.alfa = alfa
        self.beta = beta
        
    def is_leaf(self):
        return self.depth == self.horizont
    

    def applicable_actions(self):
        l = []
        for asset in self.assets_not_engaged:
            zone = self.coord_zone[self.world[self.agent_map[self.agent_playing][asset]]['pos']]
            adyacent_zones = self.zone_ady[zone]
            for new_zone in adjacent_zones:
                for door_index in self.door_map[(zone, new_zone)]:
                    if self.world[door_index]['opened']:
                        l.append(('change_zone', self.agent_playing, asset, new_zone))
                        break
            
            l.append(('change_gun', self.agent_playing, asset))
            
            if not self.world[self.objeto]['captured'] and zone == self.coord_zone[self.world[self.objeto]['pos']]:
                l.append(('pick_up', self.agent_playing, asset))
                
            if self.world[self.objeto]['owner'] == (self.agent_playing, asset):
                l.append(('drop', self.agent_playing, asset))
                
            for agent_id in self.agent_map:
                for asset_id in self.agent_map[agent_id]:
                    if zone == self.coord_zone[self.world[self.agent_map[agent_id][asset_id]]['pos']]:
                        l.append(('hurt', self.agent_playing, asset, agent_id, asset_id))
            for lever in self.lever_name:
                for lever_index in self.lever_name[lever]:
                    if zone == self.coord_zone[self.world[lever_index]['pos']]:
                        l.append(('switch', self.agent_playing, asset, lever))
                        break
                        
        return l
        

    def generate_descendants(self, action_list):
        l = []
        for action in action_list:
            node = MinimaxNode(zone_coord, coord_zone, zone_ady, door_map, door_name, agent_map, objeto, lever_name, toggle, world, alfa, beta, minmax_layout, depth, horizont)
            if action[0] == 'change_zone':
                zone = self.coord_zone[node.world[self.agent_map[action[1]][action[2]]]['pos']]
                arbitrary_door_index = iter(self.door_map[(zone, action[3])]).next()
                side1 = node.world[arbitrary_door_index]['side1']
                
                if side1 in zone_coord[zone]:
                    new_pos = node.world[arbitrary_door_index]['side2']
                else:
                    new_pos = side1
                    
                node.world[self.agent_map[action[1]][action[2]]]['pos'] = new_pos
            elif action[0] == 'change_gun':
                bullet_t = node.world[self.agent_map[action[1]][action[2]]]['bullet_type']
                if bullet_t == 'automatic':
                    node.world[self.agent_map[action[1]][action[2]]]['bullet_type'] = 'shotgun'
                else:
                    node.world[self.agent_map[action[1]][action[2]]]['bullet_type'] = 'automatic'
            elif action[0] == 'pick_up':
                node.world[self.objeto]['captured'] = True
                node.world[self.objeto]['owner'] = (action[1], action[2])
            elif action[0] == 'drop':
                node.world[self.objeto]['captured'] = False
                node.world[self.objeto]['pos'] = node.world[self.agent_map[action[1]][action[2]]]['pos']
            elif action[0] == 'hurt':
                bullet_t = node.world[self.agent_map[action[1]][action[2]]]['bullet_type']
                victim_health = node.world[self.agent_map[action[3]][action[4]]]['health']
                victim_max_health = node.world[self.agent_map[action[3]][action[4]]]['max_health']
                
                if bullet_t == 'shotgun':
                    victim_health -= victim_max_health / 2
                else:
                    victim_health -= victim_max_health / 6 + 1
                    
                if victim_health <= 0.0:
                    node.world[self.agent_map[action[3]][action[4]]]['health'] = victim_max_health
                    node.world[self.agent_map[action[3]][action[4]]]['pos'] = node.world[self.agent_map[action[3]][action[4]]]['spawn_pos']
                else:
                    node.world[self.agent_map[action[3]][action[4]]]['health'] = victim_health
            elif action[0] == 'switch':
                for tog in self.toggle[action[3]]:
                    for door_index in self.door_name[tog]:
                        node.world[door_index]['opened'] = not node.world[door_index]['opened']
                        
            l.append(node)

        return l 


class AB(threading.Thread):

    def __init__(self, initial_state, depth):
        threading.Thread.__init__(self)    
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
        if parent is not None:
            self.g = parent.g+1
        else:
            self.g = 0
            
        self.h = min(( (abs(t[0]-self.asset_pos[0])+abs(t[1]-self.asset_pos[1]))//16 for t in self.target_points ))

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
        while n.parent is not None:
            x, y = (n.asset_pos[0] - n.parent.asset_pos[0], n.asset_pos[1] - n.parent.asset_pos[1])

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

        return path[::-1]
        

class A_star(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.load_event = threading.Event()
        self.stop_event = threading.Event()
        self.idle_event = threading.Event()

    def load(self, start_node):
        self.start_node = start_node
        self.load_event.set()
    
    def is_done(self):
        return self.idle_event.is_set()
        
    def get(self):
        return self.plan
    
    def stop(self):
        self.stop_event.set()
        self.load_event.set()
        self.join()

    def run(self):
        solution_found = False
        opened = []
                
        while not self.stop_event.is_set():
            while not solution_found and len(opened)>0 and not self.stop_event.is_set() and not self.load_event.is_set():
                actual = heapq.heappop(opened)
                solution_found = actual.is_solution()
                if not solution_found:
                    exp_nodes = actual.expand()
                    closed.append(actual)
                    for n in exp_nodes:
                        heapq.heappush(opened, n)
            
            if not self.stop_event.is_set():
                if self.load_event.is_set():
                    opened = [ self.start_node ]
                    closed = []
                    solution_found = False
                    plan = []
                    self.load_event.clear()        
                else:
                    if solution_found:
                        plan = actual.get_root_path()
                    else:
                        plan = []
                        
                    self.plan = plan[:]
                    self.idle_event.set()
                    self.load_event.wait()
                    self.idle_event.clear()


class Think(multiprocessing.Process):
    def __init__(self, agent_conn, child_conn, depth, agent_id):
        multiprocessing.Process.__init__(self)
        self.agent_conn = agent_conn
        self.child_conn = child_conn
        self.depth = depth
        self.plan_cc = 0
        self.agent_id = agent_id
        self.high_level_plan = [('switch', 0, 0, 'm'), ('change_zone', 0, 0, 3), ('pick_up', 0, 0), ('change_zone', 0, 0, 4), ('change_zone', 0, 0, 19)]
        self.a_star = A_star()


    def send_plan(self):
        self.agent_conn.send(self.plan)


    def run(self):
        thinking = True
        self.world = self.child_conn.recv()
        self.a_star.start()
        while thinking:
            if self.child_conn.poll():
                from_server = self.child_conn.recv()
                
                if isinstance(from_server, str):
                    if from_server == 'shutdown':
                        print("Shutting down AI core ...")
                        thinking = False
                        self.a_star.stop()
                elif isinstance(from_server, list):
                    pending_changes = from_server
            elif self.agent_conn.poll():
                from_agent = self.agent_conn.recv()
                
                if isinstance(from_agent[1], str):
                    if from_agent[0] == 0 and from_agent[1] == 'bored':
                        print("Bored received with cc="+str(from_agent[0])+". Sending nothing ...")
                        if hasattr(self, 'plan'):
                            self.agent_conn.send((1, self.plan))
      
            if thinking and self.plan_cc==0:
                # there is a high level inmediate action
                if len(self.high_level_plan) > 0:
                    action = self.high_level_plan.pop(0)
                    
                
                asset_id = 0
                asset_pos = (960, 640)
                target_points = {(720,64),(736,64)}
                allowed_area = {(688, 496), (896, 512), (656, 16), (608, 496), (992, 368), (640, 512), (928, 544), (960, 576), (912, 576), (960, 208), (944, 736), (960, 96), (960, 736), (896, 640), (848, 624), (752, 128), (816, 624), (960, 256), (800, 496), (816, 48), (704, 624), (720, 128), (672, 128), (848, 64), (992, 128), (736, 64), (976, 96), (976, 624), (656, 48), (928, 592), (912, 640), (944, 96), (736, 16), (960, 240), (992, 720), (880, 64), (752, 96), (832, 64), (976, 464), (784, 64), (976, 656), (992, 448), (720, 592), (848, 128), (928, 96), (800, 112), (992, 688), (736, 624), (944, 592), (896, 624), (752, 624), (976, 560), (928, 720), (832, 96), (960, 560), (976, 320), (912, 528), (784, 624), (992, 528), (944, 560), (896, 528), (864, 80), (992, 256), (928, 560), (960, 592), (704, 64), (944, 656), (960, 496), (896, 80), (848, 608), (752, 496), (704, 544), (896, 720), (944, 80), (928, 496), (816, 608), (688, 512), (960, 272), (848, 512), (720, 560), (960, 368), (832, 608), (704, 576), (976, 176), (720, 112), (672, 144), (960, 432), (832, 144), (816, 112), (992, 144), (736, 80), (816, 80), (688, 112), (768, 112), (976, 80), (848, 48), (720, 16), (672, 112), (752, 48), (704, 16), (784, 16), (976, 736), (992, 112), (864, 16), (736, 48), (688, 16), (768, 16), (640, 496), (976, 496), (800, 48), (672, 80), (992, 736), (960, 112), (832, 80), (896, 672), (912, 80), (672, 16), (976, 640), (992, 464), (720, 576), (928, 640), (624, 512), (976, 400), (912, 736), (800, 144), (960, 448), (944, 576), (960, 144), (896, 576), (976, 544), (992, 432), (928, 80), (800, 512), (976, 192), (960, 512), (976, 304), (912, 512), (784, 608), (992, 544), (944, 544), (832, 32), (960, 416), (800, 608), (912, 96), (768, 496), (960, 672), (944, 528), (688, 128), (960, 704), (656, 144), (704, 560), (864, 624), (736, 32), (960, 352), (992, 192), (736, 128), (960, 480), (704, 592), (736, 496), (976, 160), (720, 96), (960, 384), (784, 32), (992, 160), (864, 64), (736, 96), (816, 64), (688, 96), (896, 96), (768, 64), (976, 64), (848, 32), (864, 32), (752, 32), (720, 32), (704, 96), (656, 96), (976, 720), (816, 32), (656, 112), (976, 480), (912, 688), (800, 64), (672, 96), (880, 96), (960, 64), (896, 688), (912, 64), (704, 32), (992, 480), (928, 656), (768, 128), (976, 384), (912, 720), (992, 592), (976, 416), (944, 624), (960, 224), (896, 592), (976, 528), (992, 320), (816, 512), (992, 272), (960, 528), (992, 96), (912, 624), (992, 560), (912, 608), (928, 736), (944, 720), (816, 496), (896, 496), (960, 128), (800, 624), (960, 688), (944, 688), (880, 80), (960, 720), (656, 32), (896, 544), (704, 512), (656, 512), (976, 240), (864, 512), (992, 288), (912, 704), (752, 144), (992, 208), (864, 496), (736, 144), (944, 496), (816, 144), (976, 448), (720, 80), (672, 512), (992, 64), (992, 176), (736, 112), (720, 544), (656, 64), (896, 736), (976, 704), (832, 128), (912, 672), (800, 80), (992, 640), (976, 608), (960, 80), (704, 144), (768, 608), (784, 144), (656, 496), (992, 496), (848, 16), (928, 672), (768, 144), (752, 512), (608, 512), (992, 608), (944, 608), (752, 80), (912, 560), (768, 512), (976, 512), (992, 336), (928, 512), (704, 128), (752, 608), (960, 608), (976, 272), (752, 64), (944, 704), (992, 576), (944, 640), (992, 304), (928, 608), (976, 144), (960, 640), (704, 496), (944, 672), (624, 496), (832, 16), (976, 288), (784, 496), (720, 496), (848, 112), (704, 528), (928, 576), (976, 224), (704, 112), (960, 320), (656, 128), (992, 224), (880, 624), (816, 128), (896, 64), (976, 128), (848, 96), (720, 64), (960, 464), (864, 96), (944, 64), (816, 96), (768, 32), (672, 32), (784, 112), (784, 96), (976, 688), (720, 624), (832, 48), (912, 656), (928, 64), (800, 96), (992, 656), (848, 496), (960, 160), (896, 656), (768, 624), (784, 128), (976, 592), (992, 384), (928, 688), (656, 80), (976, 352), (736, 512), (992, 624), (832, 624), (960, 192), (960, 288), (992, 352), (928, 528), (960, 624), (976, 256), (912, 592), (976, 368), (896, 704), (928, 624), (688, 32), (960, 656), (832, 496), (912, 496), (864, 608), (800, 32), (800, 128), (960, 304), (864, 48), (880, 512), (832, 512), (704, 608), (976, 208), (720, 144), (672, 64), (960, 336), (992, 240), (880, 608), (896, 560), (688, 80), (688, 64), (848, 80), (720, 48), (880, 496), (752, 16), (704, 48), (784, 48), (976, 112), (992, 80), (992, 416), (816, 16), (688, 48), (768, 48), (800, 16), (672, 48), (992, 704), (752, 112), (960, 400), (704, 80), (784, 80), (976, 672), (720, 608), (688, 144), (976, 432), (848, 144), (768, 96), (720, 528), (736, 608), (960, 176), (896, 608), (992, 672), (976, 576), (992, 400), (720, 512), (928, 704), (832, 112), (768, 80), (960, 544), (976, 336), (912, 544), (784, 512), (672, 496), (992, 512), (944, 512)}
                start_node = A_starNode(None, asset_pos, asset_id, target_points, allowed_area)
                self.a_star.load(start_node)
                self.a_star.idle_event.wait()
                self.plan = self.a_star.get()
                print(self.plan)
                self.plan.extend([(0, 'changeGun'), (0, 'fireSouth')])
                self.plan_cc = (self.plan_cc+1)%2
                self.agent_conn.send((1, self.plan))
            else:
                time.sleep(0.2)


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
                                                                   
    def inform(self, action):
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
        self.agent_id = agent_id
        self.server = server
        self.List = []
        self.think_conn = think_conn                
        self.engaged = True
        self.action_done = True
        self.pos = 0
        self.plan = []
        self.plan_cc = 0

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
            self.plan_cc, self.plan = self.think_conn.recv()
            self.pos = 0
            self.engaged = True
            #print("Agent ID", self.agent_id, "is now engaged!")
                    
        if self.engaged:
            if self.pos == len(self.plan):
                self.think_conn.send((self.plan_cc, 'bored'))
                self.engaged = False
            elif self.action_done:
                action = self.plan[self.pos]
                self.action_done = False
                asset = self.List[action[0]]
                #print("Agent ID", self.agent_id, "is doing", action[1])

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
                elif action[1] == 'pickUp':
                    asset.pickUpObject()
                elif action[1] == 'drop':
                    asset.dropObject()
                elif action[1] == 'toggle':
                    asset.toggleObject()
                
                                                                         
    def inform(self, action):
        """
        This method does nothing.
        """
        pass    
    
    def actionCompleted(self):
        """
        The current action has been completed.
        """
        self.action_done = True
        self.server.update((self.agent_id, self.plan[self.pos][0], self.plan[self.pos][1]))
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
        self.pending_changes = []
        self.configured = False
        self.running = False
      

    def newAgent(self, depth):
        """
        Creates a new agent and prepares data structures.
        """
        think_conn, agent_conn = multiprocessing.Pipe()
        parent_conn, child_conn = multiprocessing.Pipe()
        agent = Agent(think_conn, len(self.core_list), self)
        think = Think(agent_conn, child_conn, depth, len(self.core_list))
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
        if self.configured and not self.running:
            for core in self.core_list:
                try:
                    core[1].start()
                except AttributeError:
                    pass 
                    
            for core in self.core_list:
                try:
                    core[2].send(self.config)
                except AttributeError:
                    pass
                    
            self.running = True

    def stopAll(self):
        """
        Order the shutdown of all AI cores running in the server.
        """
        if self.running:
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
                    
            self.running = False

    def configure(self, config):
        self.config = config
        self.configured = True

    def clear(self):
        self.core_list = []
        self.configured = False
        self.running = False

    def next(self):
        for agent, think, conn in self.core_list:
            agent.next()

    def update(self, action):
        '''
        '''
        self.pending_changes.append(action)
        
    def broadcast(self):
        '''
        '''
        if self.running and len(self.pending_changes)>0:
            for core in self.core_list:
                try:
                    core[2].send(self.pending_changes)
                except AttributeError:
                    pass
                                
            del self.pending_changes[:]

