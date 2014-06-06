#!/usr/bin/env python3
"""
Game Module
"""

import pygame
from models import *
from gameoptions import *
from Interactions import *
from menu import *


class Game:

    music = {
        'main_theme': 'audio/laberynth2.ogg',
        'object_taken': 'audio/laberynth.ogg'
    }

    def __init__(self, FPS, loadgame):
        self.width = 1024
        self.height = 768
        self.screen = pygame.Surface((self.width, self.height))
        self.FPS = FPS
        self.loadgame = loadgame

    def playMainThemeMusic(self):
        # Main theme music
        pygame.mixer.music.load(Game.music['main_theme'])
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)  # Continuous Loop

    def initializeLoadedGame(self, currentLevel):
        for toggleObject, toggleEffect, in currentLevel['toggle_objects'].items():
            print("{} -> {}".format(toggleObject, toggleEffect))
            if not currentLevel['built_objects'][toggleObject][0].off:
                #  Get all elements affected by the toggling
                # toggle the object
                for effectObj in toggleEffect:
                    currentLevel['built_objects'][effectObj][0].toggle()

                lever = currentLevel['built_objects'][toggleObject][0]

                lever.toggle()
                lever.turnOnAnimation()

    def start(self, screen2):
        """
        Method that initializes the game and the corresponding pieces of the game
        """
        self.playMainThemeMusic()
        menuShow = False
        pauseMenu = Menu()
        levelContinue = True
        gameNotEnd = True

        clock = pygame.time.Clock()  # Initialize Game Clock
        total_frames = 0
        level = 1

        # Game Start
        while gameNotEnd:

            # premature tile creation to preserve tile invariant
            # invariant: relation between tile number and tile position
            for y in range(0, self.screen.get_height(), 16):
                for x in range(0, self.screen.get_width(), 16):
                    Tile(x, y, 'empty')

            # Loads the initial level representation
            currentLevelList = LevelList(self.width, self.height, self.screen)

            #if game state must jump
            if not self.loadgame:
                currentLevel = currentLevelList.buildLevelObject(currentLevelList.levels[level])
            else:
                currentLevel = GameOption.loadGame(currentLevelList, currentLevelList.levels[level])
                self.initializeLoadedGame(currentLevel)

            winCoordinates = currentLevel['level'].coordinates(('-',))['-']
            # make unbuildable and unwalkable objects unwalkable (walls)
            for y in range(0, self.screen.get_height(), 16):
                for x in range(0, self.screen.get_width(), 16):
                    if (x, y) in currentLevel['unwalkable']:
                        tile_number = ((x / 16) + Tile.HorizontalDifference) + (
                            (y / 16) * Tile.VerticalDifference)
                        tile = Tile.get_tile(tile_number)
                        tile.walkable = False
                        tile.type = 'solid'

            mainCharacter = currentLevel['built_objects']['j'][0]
            enemy = currentLevel['built_objects']['e'][0]

            background = currentLevel['level'].build_static_background(currentLevel['tile_map'], default='.')
            interaction = Interaction(self.screen, self.FPS, currentLevel)
            levelContinue = False

            # Game Loop
            while not levelContinue:
                if not menuShow:
                    self.screen.blit(background, (0, 0))  # blit the background
                    Treasure.draw(self.screen)
                    Laser.super_massive_jumbo_loop(self.screen)

                    mainCharacter.movement(self.screen)

                    interaction.interactionHandler()
                    menuShow = interaction.isUserCallingGameMenu()

                    Message.text_to_screen(self.screen, 'Health: {0}'.format(mainCharacter.health),0, -1)
                    # show general game information
                    if interaction.isUserCallingHelpScreen():
                        Message.showGeneralGameInformation(self.screen, interaction.controlDefinition)
                    else:
                        Message.showGeneralGameInformation(self.screen, interaction.helpButton)

                    if mainCharacter.satifiesWinConditions(winCoordinates):
                        currentLevelList.clearCurrentLevel()
                        levelContinue = True
                        level += 1
                        # Show message
                        # Reset del nivel -> If won se mueve al proximo nivel, else se recarga el nivel
                    Door.draw(self.screen)
                    mainCharacter.draw(self.screen)

                    enemy.draw(self.screen)
                    Robot.draw_robots(self.screen)
                    Lever.allLevers.draw(self.screen)
                else:
                    selections = pauseMenu.show_menu(screen2, self.FPS, "pauseMenu")
                    if selections['exit_game'] is True:
                        pygame.quit()
                        exit(0)
                    elif selections['resume_game'] is True:
                        menuShow = False
                        interaction.showGameMenu = False
                    elif selections['save_game'] is True:
                        GameOption.saveGame(currentLevel)
                        print('Game Saved')

                screen2.blit(pygame.transform.scale(
                    self.screen, screen2.get_rect().size), (0, 0))
                pygame.display.flip()
                clock.tick(self.FPS)
                total_frames += 1

        GameOption.exitGame()
