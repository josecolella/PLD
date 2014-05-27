#!/usr/bin/env python3
"""
Game Module
"""

import pygame
from models import *
from gameoptions import *
from Interaction import *
from menu import show_menu


class Game:

    @staticmethod
    def start(screen2, screenheight, screenwidth, FPS, loadgame):
        """
        Method that initializes the game and the corresponding pieces of the game
        """
        width = 1024
        height = 768
        screen = pygame.Surface((width, height))
        menuShow = False
        # Main theme music
        pygame.mixer.music.load("audio/laberynth2.ogg")
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
        currentLevelList= LevelList(width,height,screen)
        allLevels = currentLevelList.allLevels()
        #if game state must jump
        if not loadgame:
            currentLevel = currentLevelList.buildLevelObject(next(iter(allLevels)))
        else:
            print("Loading Game")
            currentLevel = GameOption.loadGame(currentLevelList, allLevels)


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
        interaction = Interaction(screen, FPS, currentLevel)

        # Game Loop
        while True:
            if not menuShow:
                screen.blit(background, (0, 0))  # blit the background
                Treasure.draw(screen)
                #Robot.movement(screen)
                Laser.super_massive_jumbo_loop(screen)

                mainCharacter.movement(screen)

                #A_Star(screen, mainCharacter, total_frames, FPS)
                menuShow = interaction.interactionHandler()

                Door.draw(screen)
                mainCharacter.draw(screen)

                enemy.draw(screen)
                Robot.draw_robots(screen)
                Lever.allLevers.draw(screen)
            else:
                show_menu(screen, FPS)

            screen2.blit(pygame.transform.scale(
                screen, screen2.get_rect().size), (0, 0))
            pygame.display.flip()
            clock.tick(FPS)
            total_frames += 1

        pygame.quit()
