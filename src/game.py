#!/usr/bin/env python3
"""
Game Module
"""

import pygame
from models import *
from interaction import *
from A_Star import A_Star
import json


class Game:

    @staticmethod
    def start(screen2, screenheight, screenwidth, FPS):
        """
        Method that initializes the game and the corresponding pieces of the game
        """
        width = 1024
        height = 768
        screen = pygame.Surface((width, height))
        # Main theme music
        pygame.mixer.music.load("audio/laberynth.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Continuous Loop


        # for y in range(0, screen.get_height(), 16):
        #     for x in range(0, screen.get_width(), 16):
        #         if Tile.total_tiles in Tile.invalids:
        #             Tile(x, y, 'solid')
        #         else:
        #             Tile(x, y, 'empty')

        clock = pygame.time.Clock()  # Initialize Game Clock
        total_frames = 0

        # level1 = pygame.image.load('img/level1.png')
        # Loads the initial level representation
        rep = Level.load_rep('level/level1.txt')

        objects = {'lever': {'l', 'm'},'door': {'p', 'q'},'player': {'j'},'enemy': {'e'},'object': {'a'},'robot': {'r'}}

        toggle_objects = {'l': {'p'}, 'm': {'q'}}
        tile_map = {'x': pygame.image.load('img/wall.png'),',': pygame.image.load('img/dark_gray_tile.png'), '.': pygame.image.load('img/light_gray_tile.png'), '-': pygame.image.load('img/dark_red_tile.png')}
        level = Level(rep, objects, toggle_objects, width, height,16,16)
        class_map = {'lever': Lever, 'robot': Robot, 'enemy': Enemy, 'player': MainCharacter, 'door': Door, 'object': Treasure}
        values = {'l':{'image':'img/lever_a_0.png'}, 'm': {'image': 'img/lever_b_0.png'}, 'p':{'toggled':False, 'numberTiles': 3}, 'q': {'toggled': False,'numberTiles':3}, 'j': {}, 'e': {}, 'a': {}, 'r': {}}
        level.build_objects(class_map, values)

        coords = level.coordinates(['x', 'p', 'q'])
        print(coords)
        # unwalkable = {x for k in coords for x in coords[k]}


        # mainCharacter = MainCharacter(1 * 48, 10 * 64)
        # enemy = Enemy(20 * 48, 10 * 64)
        # lever1 = Lever(5 * 48, 1 * 64, 'img/lever_a_0.png')
        # lever2 = Lever(15 * 48, 1 * 64, 'img/lever_b_0.png')
        # treasure = Treasure(64 * 6, 22 + 48)

        background = level.build_static_background(tile_map, default='.')

        # For testing purposes
        #background = pygame.Surface((screen.get_size()))
        #background.fill((255, 255, 255))
        #screen.blit(background, (0, 0))

        # Game Loop
        while True:
            screen.blit(background, (0, 0))  # blit the background
            # Treasure.draw(screen)
            # Tile.draw_tiles(screen, lever1, lever2)
            # if(len(Robot.List) < 2):
                # Robot.spawn(total_frames, FPS)
            # Robot.movement(screen)
            # Laser.super_massive_jumbo_loop(screen)

            # mainCharacter.movement(screen)

            #A_Star(screen, mainCharacter, total_frames, FPS)
            # leverPulled = interaction(
                # screen, mainCharacter, lever1, lever2, FPS)
            # if leverPulled:
                # Tile.draw_tiles(screen, lever1, lever2)

            # enemy.movement(screen)

            # mainCharacter.draw(screen)

            # enemy.draw(screen)
            # Robot.draw_robots(screen)
            # Lever.allLevers.draw(screen)
            #
            screen2.blit(pygame.transform.scale(
                screen, screen2.get_rect().size), (0, 0))
            pygame.display.flip()
            clock.tick(FPS)
            total_frames += 1

        pygame.quit()

    # def saveGame(mainCharacter, enemy, robots, treasure):

    #    mainCharacterPositions = {"x":mainCharacter.get_tile(), "y": mainCharacter}
    #    with open('game.json') as f:
