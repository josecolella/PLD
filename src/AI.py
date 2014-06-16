"""
This module represents the Artificial Intelligence for the game
"""

import pygame
import multiprocessing
import threading
import heapq
import copy
import time
import traceback


class MinimaxNode:
    def __init__(self, zone_coord, coord_zone, zone_ady, door_map, door_name, agent_map, objeto, lever_name, toggle, world, alfa, beta, minmax_layout, depth, horizont):
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
            adjacent_zones = self.zone_ady[zone]
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
            node = MinimaxNode(self.zone_coord, self.coord_zone, self.zone_ady, self.door_map, self.door_name, self.agent_map, self.objeto, self.lever_name, self.toggle, self.world, self.alfa, self.beta, self.minmax_layout, self.depth, self.horizont)
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
        print("Thinking...")
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
                    closed.add(actual.asset_pos)
                    for n in exp_nodes:
                        if not n.asset_pos in closed:
                            heapq.heappush(opened, n)
            
            if not self.stop_event.is_set():
                if self.load_event.is_set():
                    opened = [ self.start_node ]
                    closed = set()
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
        self.plan = []
        self.agent_id = agent_id
        self.high_level_plan = [('switch', 0, 0, 'm'), ('change_zone', 0, 0, 3), ('pick_up', 0, 0), ('change_zone', 0, 0, 4), ('change_zone', 0, 0, 19)]
        self.a_star = A_star()
        self.required_star = False
        self.sended = True
        self.bored = False     
        self.reactive_mode = False   
        self.high_level_action_completed = True             
        self.pending_reactions = set()          

    def check_react(self, datafw, agent_id, fireEvent, threat_agent_id, threat_asset_id):
        print(" ** in check_react")
        threat_pos = datafw['world'][datafw['agent_map'][threat_agent_id][threat_asset_id]]['pos']
        threat_line = self.shooting_line(datafw, threat_agent_id, threat_asset_id)        
        l = []
        
        if fireEvent == "fireNorth":
            for asset_id in datafw['agent_map'][self.agent_id].keys():
                asset_line = self.shooting_line(datafw, self.agent_id, asset_id)
                safe = threat_line['north'].isdisjoint(asset_line['south'])
                asset_pos = datafw['world'][datafw['agent_map'][self.agent_id][asset_id]]['pos']
                evasion_pos = ((asset_pos[0]+16, asset_pos[1]), (asset_pos[0]-16, asset_pos[1]))
                distance = threat_pos[1] - asset_pos[1]
                l.append((safe, distance, evasion_pos))
            l.sort()
            safe, distance, evasion_pos = l[0]    
            threat_direction = 'north'                    
            evasion_movement = ('moveEast', 'moveWest')
            fire_response = 'fireSouth'
        elif fireEvent == "fireWest":
            for asset_id in datafw['agent_map'][self.agent_id].keys():
                asset_line = self.shooting_line(datafw, self.agent_id, asset_id)
                safe = threat_line['west'].isdisjoint(asset_line['east'])
                asset_pos = datafw['world'][datafw['agent_map'][self.agent_id][asset_id]]['pos']
                evasion_pos = ((asset_pos[0], asset_pos[1]+16), (asset_pos[0], asset_pos[1]-16))
                distance = threat_pos[0] - asset_pos[0]
                l.append((safe, distance, evasion_pos))
            l.sort()
            safe, distance, evasion_pos = l[0]
            threat_direction = 'west'
            evasion_movement = ('moveSouth', 'moveNorth')
            fire_response = 'fireEast'
        elif fireEvent == "fireSouth":
            for asset_id in datafw['agent_map'][self.agent_id].keys():
                asset_line = self.shooting_line(datafw, self.agent_id, asset_id)
                safe = threat_line['south'].isdisjoint(asset_line['north'])
                asset_pos = datafw['world'][datafw['agent_map'][self.agent_id][asset_id]]['pos']
                evasion_pos = ((asset_pos[0]+16, asset_pos[1]), (asset_pos[0]-16, asset_pos[1]))
                distance =  asset_pos[1] - threat_pos[1]
                l.append((safe, distance, evasion_pos))
            l.sort()
            safe, distance, evasion_pos = l[0]
            threat_direction = 'south'
            evasion_movement = ('moveEast', 'moveWest')
            fire_response = 'fireNorth'
        elif fireEvent == "fireEast":
            for asset_id in datafw['agent_map'][self.agent_id].keys():
                asset_line = self.shooting_line(datafw, self.agent_id, asset_id)
                safe = threat_line['east'].isdisjoint(asset_line['west'])
                asset_pos = datafw['world'][datafw['agent_map'][self.agent_id][asset_id]]['pos']
                evasion_pos = ((asset_pos[0], asset_pos[1]+16), (asset_pos[0], asset_pos[1]-16))
                distance = asset_pos[0] - threat_pos[0]
                l.append((safe, distance, evasion_pos))
            l.sort()
            safe, distance, evasion_pos = l[0]
            threat_direction = 'east'
            evasion_movement = ('moveSouth', 'moveNorth')
            fire_response = 'fireWest'
        print(" ** out check_react")
        return not safe, {'distance': distance, 'asset_id': asset_id, 'fire_response': fire_response, 'evasion_pos': evasion_pos, 'evasion_movement': evasion_movement, 'threat_line': threat_line, 'threat_direction': threat_direction}
                
    def react(self, datafw, distance, asset_id, fire_response, evasion_pos, evasion_movement, threat_line, threat_direction):
        plan = []
        asset_pos = datafw['world'][datafw['agent_map'][self.agent_id][asset_id]]['pos']
        asset_zone = datafw['coord_zone'][asset_pos]        

        if distance < 8*16:
            if datafw['world'][datafw['agent_map'][self.agent_id][asset_id]]['bullet_type'] == 'automatic':
                plan.append((asset_id, 'changeGun'))
                
            plan.append((asset_id, fire_response))
        else:
            if evasion_pos[0] not in threat_line[threat_direction] and evasion_pos[0] in datafw['zone_coord'][asset_zone]:
                plan.append((asset_id, evasion_movement[0]))
            elif evasion_pos[1] not in threat_line[threat_direction] and evasion_pos[1] in datafw['zone_coord'][asset_zone]:
                plan.append((asset_id, evasion_movement[1]))

        return plan

    def surrounding_coords(self, datafw, pos, diagonal=False):
        diffs = [(0,-16),(-16,0),(0,16),(16,0)]
        diags = ((16,-16),(-16,-16),(-16,16),(16,16))
        
        sc = set()
        if diagonal:
            diffs.extend(diags)
        
        for d in diffs:
            sc.add((pos[0]+d[0], pos[1]+d[1]))
            
        return sc.intersection(datafw['zone_coord'][datafw['coord_zone'][pos]])

    def accessible_coords(self, datafw, pos):
        zone = datafw['coord_zone'][pos]
        h = [ (zone, new_zone) for new_zone in datafw['zone_ady'][zone] ]

        nh = [None]
        while len(nh) > 0:
            nh = []
            for p in h:
                for q in h:
                    np = (p[0], q[1])
                    if p[1] == q[0] and np not in h and np not in nh:
                        nh.append(np)
            h.extend(nh)

        ac =  set()
        
        for z1, z2 in h:
            for door_index in datafw['door_map'][(z1, z2)]:
                if datafw['world'][door_index]['opened']:
                    ac.add(datafw['world'][door_index]['pos'])
                    ac.update(datafw['zone_coord'][z1])
                    ac.update(datafw['zone_coord'][z2])

        return ac
             
    def shooting_line(self, datafw, agent_id, asset_id, door_crossing = True):
        shooting_coords = {'north':set(), 'west':set(), 'south':set(), 'east':set()}
        direction_diff = {'north':{'w':0, 'h':-16}, 'west':{'w':-16, 'h':0}, 'south':{'w':0, 'h':16}, 'east':{'w':16, 'h':0}}
        asset_pos = datafw['world'][datafw['agent_map'][agent_id][asset_id]]['pos']

        if door_crossing:
            accessible_coords = self.accessible_coords(datafw, asset_pos)
        else:
            accessible_coords = datafw['zone_coord'][datafw['coor_zone'][pos]]

        for center in ((asset_pos[0], asset_pos[1]), (asset_pos[0]+16, asset_pos[1]+16)):
            for direction in ('north', 'west', 'south', 'east'):
                obstacle_not_reached = True
                line_pos = center
                while obstacle_not_reached:
                    line_pos = (line_pos[0]+direction_diff[direction]['w'], line_pos[1]+direction_diff[direction]['h'])
                    if line_pos in accessible_coords:
                        shooting_coords[direction].add(line_pos)
                    else:
                        obstacle_not_reached = False
           
        return shooting_coords

    def fire_handler(self, datafw, change):
        try:
            reaction_info = self.check_react(datafw, self.agent_id, change[2], change[0], change[1])
        except KeyError:
            print("Zone identification error. Disabling reaction...")
            traceback.print_exc()
        else:    
            print(" ** need_reaction =", reaction_info[0])
            if reaction_info[0]:   # do not know yet if world is in sync
                self.pending_reactions.add(change)   # will check again when world in sync
                if not self.reactive_mode:   # if there is not a reaction in course
                    self.plan = []   # cancel Agent operations in course
                    self.send_plan()   # make Agent send a "bored" request with sync information
                    self.reactive_mode = True
                    print("Reactive Mode = ON")
                    self.high_level_action_completed = False

    def movement_handler(self, datafw, change):
        direction_diff = {'north':{'w':0, 'h':-16}, 'west':{'w':-16, 'h':0}, 'south':{'w':0, 'h':16}, 'east':{'w':16, 'h':0}}    
        asset_pos = datafw['world'][datafw['agent_map'][change[0]][change[1]]]['pos']
        
        if change[2] == 'moveNorth':
            asset_pos = (asset_pos[0]+direction_diff['north']['w'], asset_pos[1]+direction_diff['north']['h'])
        elif change[2] == 'moveWest':
            asset_pos = (asset_pos[0]+direction_diff['west']['w'], asset_pos[1]+direction_diff['west']['h'])
        elif change[2] == 'moveSouth':
            asset_pos = (asset_pos[0]+direction_diff['south']['w'], asset_pos[1]+direction_diff['south']['h'])
        elif change[2] == 'moveEast':
            asset_pos = (asset_pos[0]+direction_diff['east']['w'], asset_pos[1]+direction_diff['east']['h'])

        datafw['world'][datafw['agent_map'][change[0]][change[1]]]['pos'] = asset_pos    

    def send_plan(self):
        self.plan_cc = (self.plan_cc+1)%2
        self.agent_conn.send((self.plan_cc, self.plan))
        print("Sended plan with cc=", self.plan_cc, " len=", len(self.plan))        
        self.bored = False
        self.sended = True
        self.plan = []


    def run(self):
        i = 0
        thinking = True
        world_in_sync = True
        datafw = self.child_conn.recv()
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

                    for change in pending_changes:
                        i += 1
                        if change[0] == self.agent_id and not world_in_sync:
                            world_in_sync = True
                            print("WORLD SYNCED")                 
                        
                        if isinstance(change[2], tuple):  # patch to solve incorrect FakeAgent positioning
                            datafw['world'][datafw['agent_map'][change[0]][change[1]]]['pos'] = change[2]
                            # the Character subclass instance tends to have a different position
                            # from the position in AI data structure
                        elif change[2] == 'moveEast':
                            self.movement_handler(datafw, change)
                        elif change[2] == 'moveWest':
                            self.movement_handler(datafw, change)
                        elif change[2] == 'moveNorth':
                            self.movement_handler(datafw, change)
                        elif change[2] == 'moveSouth':
                            self.movement_handler(datafw, change)
                        elif change[2] == 'changeGun':
                            bullet_t = datafw['world'][datafw['agent_map'][change[0]][change[1]]]['bullet_type']
                            if bullet_t == 'automatic':
                                datafw['world'][datafw['agent_map'][change[0]][change[1]]]['bullet_type'] = 'shotgun'
                            else:
                                datafw['world'][datafw['agent_map'][change[0]][change[1]]]['bullet_type'] = 'automatic'
                        elif change[2] == 'fireWest':
                            print(i, ":AI core:", change[2], "from agent", change[0], change[1])
                            self.fire_handler(datafw, change)
                        elif change[2] == 'fireNorth':
                            print(i, ":AI core:", change[2], "from agent", change[0], change[1])
                            self.fire_handler(datafw, change)
                        elif change[2] == 'fireEast':
                            print(i, ":AI core:", change[2], "from agent", change[0], change[1])
                            self.fire_handler(datafw, change)
                        elif change[2] == 'fireSouth':
                            print(i, ":AI core:", change[2], "from agent", change[0], change[1])
                            self.fire_handler(datafw, change)
                        elif change[2] == 'pickUp':
                            datafw['world'][datafw['objeto']]['captured'] = True
                            datafw['world'][datafw['objeto']]['owner'] = (change[0], change[1])
                        elif change[2] == 'drop':
                            datafw['world'][datafw['objeto']]['captured'] = False
                            datafw['world'][datafw['objeto']]['pos'] = datafw['world'][datafw['agent_map'][change[0]][change[1]]]['pos']
                        elif change[2] == 'toggle':
                            for lever_s in datafw['lever_name']:
                                for lever_index in datafw['lever_name'][lever_s]:
                                    lever_pos = datafw['world'][lever_index]['pos']
                                    asset_pos = datafw['world'][datafw['agent_map'][change[0]][change[1]]]['pos']
                                    distance2 = (lever_pos[0]-asset_pos[0])*(lever_pos[0]-asset_pos[0])+(
                                        lever_pos[1]-asset_pos[1])*(lever_pos[1]-asset_pos[1])
                                    if distance2 < 4 * 512:
                                        print("AI core: guessing", change[2], "affected", lever_s)
                                        for tog in datafw['toggle'][lever_s]:
                                            for door_index in datafw['door_name'][tog]:
                                                print("Made toggle of", tog, "door ;)")
                                                datafw['world'][door_index]['opened'] = not datafw['world'][door_index]['opened']
                            
            elif self.agent_conn.poll():
                from_agent = self.agent_conn.recv()
                
                if isinstance(from_agent[1], tuple):
                    if from_agent[1][0] == 'bored':
                        print("Bored received with cc="+str(from_agent[0])+" expected "+str(self.plan_cc))                
                        if from_agent[0] == self.plan_cc:   # plan control code
                            self.bored = True
                            self.sended = False
                            world_in_sync = from_agent[1][1]
                            print("WORLD_IN_SYNC=", world_in_sync)
                            if not self.reactive_mode:
                                self.high_level_action_completed = True

                        else:
                            self.high_level_action_completed = True
      
            if thinking and world_in_sync:
                if self.bored:
                    if self.reactive_mode:
                        if len(self.pending_reactions)==0:
                            self.reactive_mode = False
                            print("Reactive Mode =OFF")
                        else:
                            reaction = self.pending_reactions.pop()               
                            try:
                                reaction_info = self.check_react(datafw, self.agent_id, reaction[2], reaction[0], reaction[1])   # threat persist?
                            except KeyError:
                                print("Zone identification error. Disabling reaction...")
                                traceback.print_exc()
                            else:
                                print(" ** need_reaction (synced)=", reaction_info[0])    
                                if reaction_info[0]:
                                    self.plan=self.react(datafw, **reaction_info[1])   # reactive was splitted into two parts
                                    self.send_plan()              
                    elif not self.high_level_action_completed or len(self.high_level_plan)>0:
                        self.bored = False
                        if len(self.high_level_plan)>0 and self.high_level_action_completed:
                            action = self.high_level_plan.pop(0)
                        else:
                            print("Resolving (again)", action)
                            
                        print("Resolving", action)
                        if action[0] == 'change_gun':
                            self.plan = []
                            self.plan.append((action[2], action[0]))
                            self.required_star = False
                        elif action[0] == 'change_zone':
                            agent_id = action[1]
                            asset_id = action[2]
                            new_zone = action[3]
                            asset_pos = datafw['world'][datafw['agent_map'][agent_id][asset_id]]['pos']
                            asset_zone = datafw['coord_zone'][asset_pos]
                            targets = set()
                            doors = set()
                            for door_index in datafw['door_map'][(asset_zone, new_zone)]:
                                doors.add(datafw['world'][door_index]['pos'])
                                targets.add(datafw['world'][door_index]['side1'])
                                targets.add(datafw['world'][door_index]['side2'])                                
                            allowed_area = datafw['zone_coord'][asset_zone].union(targets)
                            targets.difference_update(datafw['zone_coord'][asset_zone])
                            allowed_area.update(doors)
                            start_node = A_starNode(None, asset_pos, asset_id, targets, allowed_area)
                            self.a_star.load(start_node)
                            self.plan = []                                  
                            self.required_star = True
                        elif action[0] == 'pick_up':
                            agent_id = action[1]
                            asset_id = action[2]                        
                            pos = datafw['world'][datafw['objeto']]['pos']
                            targets = self.surrounding_coords(datafw, pos, diagonal=True)
                            asset_pos = datafw['world'][datafw['agent_map'][agent_id][asset_id]]['pos'] 
                            allowed_area = datafw['zone_coord'][datafw['coord_zone'][pos]]
                            datafw['world'][datafw['objeto']]['captured'] = True
                            datafw['world'][datafw['objeto']]['owner'] = (agent_id, asset_id)
                            start_node = A_starNode(None, asset_pos, asset_id, targets, allowed_area)
                            self.a_star.load(start_node)
                            self.plan = [(asset_id, 'pickUp')]
                            self.required_star = True
                        elif action[0] == 'drop':
                            self.plan = [(action[2], action[0])]
                            self.required_star = False
                        elif action[0] == 'hurt':
                            pass
                        elif action[0] == 'switch':
                            agent_id = action[1]
                            asset_id = action[2]
                            lever_s = action[3]
                            targets = set()
                            for lever_index in datafw['lever_name'][lever_s]:
                                pos = datafw['world'][lever_index]['pos']
                                targets.update(self.surrounding_coords(datafw, pos, diagonal=True))
                            asset_pos = datafw['world'][datafw['agent_map'][agent_id][asset_id]]['pos'] 
                            allowed_area = datafw['zone_coord'][datafw['coord_zone'][asset_pos]]
                            start_node = A_starNode(None, asset_pos, asset_id, targets, allowed_area)
                            self.a_star.load(start_node)
                            self.plan = [(asset_id, 'toggle')]
                            self.required_star = True
                            
                elif not self.sended:
                    if not self.required_star:                 
                        self.send_plan()
                    elif self.a_star.is_done():
                        plan = self.a_star.get()
                        self.plan[:0] = plan
                        self.send_plan()                            

                time.sleep(0.01)                
                            

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
        self.last_action = action
    
    
    def actionCompleted(self, actually_done=True):
        """
        The current action has been completed.
        """
        if actually_done:
            if self.last_action[1][:4] == 'move':  # patch to solve incorrect FakeAgent positioning
                model = self.List[self.last_action[0]]
                self.server.update((self.agent_id, self.last_action[0], (model.x, model.y)))
            else:
                self.server.update((self.agent_id, self.last_action[0], self.last_action[1]))
        
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
            #print("Agent ID", self.agent_id, "is now engaged! ->", self.plan)
                    
        if self.engaged:
            if self.pos == len(self.plan):
                self.think_conn.send((self.plan_cc, ('bored', self.action_done)))
                self.engaged = False
            elif self.action_done:
                action = self.plan[self.pos]
                self.action_done = False
                asset = self.List[action[0]]
                self.last_command = action[1]
                self.last_asset = action[0]
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
    
    def actionCompleted(self, actually_done=True):
        """
        The current action has been completed.
        """
        self.action_done = True
        if actually_done:
            print("Agent ID", self.agent_id, "did", self.last_command)
            self.server.update((self.agent_id, self.last_asset, self.last_command))
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

