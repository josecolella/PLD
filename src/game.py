#!/usr/bin/env python3
"""
Game Module
"""

import pygame
from models import *
from gameoptions import *
from Interactions import *
from menu import *
from AI import AgentServer
from time import sleep


class Game:
    """
    Class that represents the actual game. Initializes the interactions,
    manages the user interaction with the game, as well as the control over
    the levels, saving, loading, and exiting.
    """
    music = {
        'main_theme': 'audio/laberynth.ogg',
        'object_taken': 'audio/laberynth2.ogg'
    }


    def __init__(self, FPS, soundOptions, loadgame):
        """
        Constructs the class with a Frame-Per-Second, and if the game
        is to be loaded
        """
        print(soundOptions)
        self.width = 1024
        self.height = 768
        self.screen = pygame.Surface((self.width, self.height))
        self.FPS = FPS
        self.loadgame = loadgame
        self.soundOptions = soundOptions

    def playMainThemeMusic(self):
        """
        Manages the playing of the main theme music for the game
        """
        # Main theme music
        pygame.mixer.music.load(Game.music['main_theme'])
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)  # Continuous Loop

    def playObjectTakenMusic(self):
        pygame.mixer.music.load(Game.music['object_taken'])
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)

    def pauseMainThemeMusic(self):
        """
        pauseMainThemeMusic() -> pauses music
        """
        pygame.mixer.music.pause()

    def resumeMainThemeMusic(self):
        """
        resumeMainThemeMusic() -> resumes the music from the spot that it was
        paused
        """
        pygame.mixer.music.unpause()

    def restartMainThemeMusic(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.stop()

    def initializeLoadedGame(self, currentLevel):
        """
        Helper method created to initialize games that are to be loaded
        from file
        """

        self._initializeLoadedToggleObjects(currentLevel)
        self._initializeLoadedTreasure(currentLevel)

    def _initializeLoadedTreasure(self, currentLevel):
        """
        Helper method used to initialize the treasure in the map,
        and if any of the characters have control of the treasure
        """
        for treasureIdentifier in currentLevel['objects']['object']:
            for treasure in currentLevel['built_objects'][treasureIdentifier]:
                if treasure.isCaptured:
                    treasure.showCaptured()

    def _initializeLoadedToggleObjects(self, currentLevel):
        for toggleObject, toggleEffect, in currentLevel['toggle_objects'].items():
            if not currentLevel['built_objects'][toggleObject][0].off:
                #  Get all elements affected by the toggling
                # toggle the object
                for effectObj in toggleEffect:
                    currentLevel['built_objects'][effectObj][0].toggle()

                lever = currentLevel['built_objects'][toggleObject][0]

                lever.toggle()
                lever.turnOnAnimation()

    def nextLevel(self, currentLevelList, levelContinue, level):
        currentLevelList.clearCurrentLevel()
        levelContinue = True
        level += 1
        self.loadgame = False
        if self.soundOptions['game_music']:
            self.restartMainThemeMusic()
        return levelContinue, level

    def start(self, screen2):
        """
        Method that initializes the game and the corresponding pieces
        of the game
        """
        # Whether to show the pause Menu
        menuShow = False
        # Whether to continue the level
        levelContinue = True
        # Whether the game continues
        gameNotEnd = True
        # Inialize the pause menu
        pauseMenu = Menu()

        clock = pygame.time.Clock()  # Initialize Game Clock
        total_frames = 0
        level = 1

        # Game Start
        while gameNotEnd:
            if self.soundOptions['game_music']:
                self.playMainThemeMusic()
            # premature tile creation to preserve tile invariant
            # invariant: relation between tile number and tile position
            for y in range(0, self.screen.get_height(), 16):
                for x in range(0, self.screen.get_width(), 16):
                    Tile(x, y, 'empty')

            # Loads the initial level representation
            currentLevelList = LevelList(self.width, self.height, self.screen)
            try:
                #if game state must jump
                if not self.loadgame:
                    currentLevel = currentLevelList.buildLevelObject(currentLevelList.levels[level])
                else:
                    currentLevel = GameOption.loadGame(currentLevelList)
                    level = currentLevel['levelIndex']
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
                AI_server = AgentServer.get()  # The server must be configured at this point
                AI_server.startAll()
                levelContinue = False

                # Game Loop
                while not levelContinue:
                    if not menuShow:
                        # blit the background
                        self.screen.blit(background, (0, 0))
                        Treasure.draw(self.screen)
                        Laser.charactersShotDamageHandler(self.screen)

                        mainCharacter.movement(self.screen)

                        interaction.interactionHandler()
                        menuShow = interaction.isUserCallingGameMenu()
                        if menuShow:
                            self.pauseMainThemeMusic()
                        # apply interaction of all AI cores
                        AI_server.next()

                        Message.text_to_screen(self.screen, 'Health: {0}'.format(mainCharacter.health),0, -1)
                        # show general game information
                        if interaction.isUserCallingHelpScreen():
                            Message.showGeneralGameInformation(self.screen, interaction.controlDefinition)
                        else:
                            Message.showGeneralGameInformation(self.screen, interaction.helpButton)

                        if mainCharacter.satifiesWinConditions(winCoordinates):
                            level, levelContinue = self.nextLevel(currentLevelList, levelContinue, level)

                        Door.draw(self.screen)
                        mainCharacter.draw(self.screen)

                        enemy.draw(self.screen)
                        Robot.draw_robots(self.screen)
                        Lever.allLevers.draw(self.screen)
                    else:
                        selections = pauseMenu.show_menu(screen2, self.FPS, "pauseMenu")
                        if selections['exit_game'] is True:
                            GameOption.exitGame()
                        elif selections['resume_game'] is True:
                            menuShow = False
                            self.resumeMainThemeMusic()
                            interaction.showGameMenu = False
                        elif selections['save_game'] is True:
                            GameOption.saveGame(currentLevel)
                            print('Game Saved')

                    screen2.blit(pygame.transform.scale(
                        self.screen, screen2.get_rect().size), (0, 0))
                    pygame.display.flip()
                    clock.tick(self.FPS)
                    total_frames += 1
            except KeyError:  # Max Levels reached
                print('Here')
                currentLevelList.clearCurrentLevel()
                self.screen.blit(pygame.image.load("img/dead.jpg"), (0, 0))
                pygame.display.update()
                sleep(4.0)
                GameOption.exitGame()

        GameOption.exitGame()
