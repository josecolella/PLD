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

        clock = pygame.time.Clock()  # Initialize Game Clock
        total_frames = 0

        # premature tile creation to preserve tile invariant
        # invariant: relation between tile number and tile position
        for y in range(0, screen.get_height(), 16):
            for x in range(0, screen.get_width(), 16):
                Tile(x, y, 'empty')


        # Loads the initial level representation
        currentLevelList = LevelList(width, height, screen)

        # levelIterator = levelList.levelsList
        currentLevel = next(iter(currentLevelList.allLevels()))


        # make unbuildable and unwalkable objects unwalkable (walls)
        for y in range(0, screen.get_height(), 16):
            for x in range(0, screen.get_width(), 16):
                if (x, y) in currentLevel['unwalkable']:
                    tile_number = ((x / 16) + Tile.HorizontalDifference) + (
                        (y / 16) * Tile.VerticalDifference)
                    tile = Tile.get_tile(tile_number)
                    tile.walkable = False
                    tile.type = 'solid'

        mainCharacter = currentLevel['built_objects']['j'][0]
        enemy = currentLevel['built_objects']['e'][0]

        background = currentLevel['level'].build_static_background(currentLevel['tile_map'], default='.')


        # Game Loop
        while True:
            screen.blit(background, (0, 0))  # blit the background
            Treasure.draw(screen)
            #Robot.movement(screen)
            Laser.super_massive_jumbo_loop(screen)

            mainCharacter.movement(screen)

            #A_Star(screen, mainCharacter, total_frames, FPS)
            interaction(
                    screen, mainCharacter, FPS)



            Door.draw(screen)
            mainCharacter.draw(screen)

            enemy.draw(screen)
            Robot.draw_robots(screen)
            Lever.allLevers.draw(screen)
            screen2.blit(pygame.transform.scale(
                screen, screen2.get_rect().size), (0, 0))
            pygame.display.flip()
            clock.tick(FPS)
            total_frames += 1

        pygame.quit()

    # def saveGame(mainCharacter, enemy, robots, treasure):

    #    mainCharacterPositions = {"x":mainCharacter.get_tile(), "y": mainCharacter}
    #    with open('game.json') as f:
