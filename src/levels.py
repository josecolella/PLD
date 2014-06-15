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
        self.built_models = None

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

        self.built_models = built_models
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
                        coordinates[self.rep[y][x]].add(
                            (self.min_tile_w * x, self.min_tile_h * y))
                    except KeyError:
                        coordinates[self.rep[y][x]] = {
                            (self.min_tile_w * x, self.min_tile_h * y)
                        }

        return coordinates

    def conn_map(self):
        """
        Returns an abstract view of represented map. This includes a
        connection graph whose nodes are zones and a door map.
        """
        r_objects = {}
        for k in self.objects:  # create a "reversed" version of self.objects
            for l in self.objects[k]:
                r_objects[l] = k

        coords = self.coordinates(set(r_objects.keys()).union({'-'}))
        zone_coord = self.zone_coordinates()         # zone_coord
        coord_zone = {}                              # coord_zone
        for k in zone_coord:
            for v in zone_coord[k]:
                coord_zone[v] = k
        
        door_map = {}
        door_name = {}
        world = []
        for s in self.objects['door']:               # door_map
            for pos in coords[s]:                    # door_name
                for door in self.built_models[s]:
                    if pos == (door.rect.x, door.rect.y):
                        d = {'pos' : pos,
                            'opened' : door.toggled
                        }
                        try:
                            door_name[s].add(len(world))
                        except KeyError:
                            door_name[s] = {len(world)}
                                                    
                        north_pos = (door.rect.x, door.rect.y-self.min_tile_h)
                        try:
                            zone = coord_zone[north_pos]
                        except KeyError:
                            west_pos = (door.rect.x-self.min_tile_w, door.rect.y)
                            east_pos = (door.rect.x+self.min_tile_w, door.rect.y)
                            pair = (coord_zone[west_pos], coord_zone[east_pos])
                            d['side1'] = west_pos
                            d['side2'] = east_pos
                        else:
                            south_pos = (door.rect.x, door.rect.y+self.min_tile_h)
                            pair = (zone, coord_zone[south_pos])
                            d['side1'] = north_pos
                            d['side2'] = south_pos                            
                        finally:
                            if pair[0] != pair[1]:
                                try:
                                    door_map[pair].add(len(world))
                                except KeyError:
                                    if pair[::-1] in door_map:
                                        door_map[pair[::-1]].add(len(world))
                                    else:
                                        door_map[pair] = {len(world)}
                            
                        world.append(d)
                        
        zone_ady = {}                  # zone_ady
        inverse = []
        for a, b in door_map.keys():
            try:
                zone_ady[a].add(b)         
            except KeyError:
                zone_ady[a] = {b}
                
            inverse.append((b,a))
            
        for b, a in inverse:
            try:
                zone_ady[b].add(a)         
            except KeyError:
                zone_ady[b] = {a}
                
            door_map[(b,a)] = door_map[(a,b)]
        
        owner = (0,0)
        agent_map = {}                  # agent_map
        for model_name in ('robot', 'player', 'enemy'):
            for model in ( c for s in self.objects[model_name] for c in self.built_models[s] ):
                try:
                    ail = agent_map[model.agent.agent_id]
                except KeyError:
                    ail = agent_map[model.agent.agent_id] = {}
                finally:
                    ail[model.asset_id] = len(world)

                d = { 'pos' : (model.x, model.y),
                    'bullet_type' : model.get_bullet_type(),
                    'health' : model.health,
                    'max_health' : model.__class__.health,
                    'spawn_pos' : model.spawnPosition
                }

                world.append(d)
                
                if model.treasureCaptured:
                    owner = (model.agent.agent_id, model.asset_id)
        
        objeto = len(world)             # objeto
        treasure = self.built_models[list(self.objects['object'])[0]][0]
        d = {'pos' : (treasure.x, treasure.y),
            'captured' : treasure.isCaptured,
            'owner' : owner
        }
        world.append(d)
        
        lever_name = {}                 # lever_name
        for lever, symbol in ( (c, s) for s in self.objects['lever'] for c in self.built_models[s] ):
            d = {'pos' : (lever.rect.x, lever.rect.y),
                'toggled' : lever.off
            }
            
            try:
                lever_name[symbol].add(len(world))
            except KeyError:
                lever_name[symbol] = {len(world)}
                
            world.append(d)
            
        toggle = self.toggle_objects    # toggle
        
        exit_zone = { coord_zone[x] for x in coords['-'] }                  # exit_zone
                                        
        return {'zone_coord':zone_coord, 'coord_zone':coord_zone, 'zone_ady':zone_ady, 'door_map':door_map, 'door_name':door_name, 'agent_map':agent_map, 'objeto':objeto, 'lever_name':lever_name, 'toggle':toggle, 'exit_zone':exit_zone, 'world':world}
        


    def get_agent_server(self):
        """
        Returns an agent server for this level. Only one exists per level.
        """
        pass

    def zone_coordinates(self):
        """
        Returns cell based (tile) coordinates grouped by zones.
        Zones are detected automatically as areas delimited by doors or walls.
        """
        lines = len(self.rep)
        columns = len(self.rep[0])
        non_conducting = {'x'}
        non_conducting.update(self.objects['door'])
        m = [ [0]*columns for i in range(lines) ]
        zone_count = 1
        equivalent = set()
        coords = {}
        done = set()
        equiv_zone = {}
        zone_coords = {}


        for y in range(1,lines):
            for x in range(1,columns):
                if self.rep[y][x] not in non_conducting:
                    if self.rep[y-1][x] not in non_conducting or self.rep[y][x-1] not in non_conducting:
                        m[y][x] = max(m[y-1][x], m[y][x-1])
                        if m[y-1][x] != m[y][x-1] and m[y-1][x] != 0 != m[y][x-1]:
                            equivalent.add((m[y-1][x], m[y][x-1]))

                    else:
                        m[y][x] = zone_count
                        zone_count +=1

                    try:
                        coords[m[y][x]].add((self.min_tile_w * x, self.min_tile_h * y))
                    except KeyError:
                        coords[m[y][x]] = {(self.min_tile_w * x, self.min_tile_h * y)}


        for i in range(1, zone_count):
            if i not in done:
                changed = True
                equiv_zone[i] = {i}
                done.add(i)
                while changed:
                    zone_size = len(equiv_zone[i])
                    for z1, z2 in equivalent:
                        if z1 in equiv_zone[i]:
                            equiv_zone[i].add(z2)
                            done.add(z2)
                        elif z2 in equiv_zone[i]:
                            equiv_zone[i].add(z1)
                            done.add(z1)

                    if len(equiv_zone[i]) == zone_size:
                        changed = False
                    else:
                        changed = True


        for z1 in equiv_zone:
            zone_coords[z1] = set()

            for z2 in equiv_zone[z1]:
                zone_coords[z1].update(coords[z2])


        return zone_coords

