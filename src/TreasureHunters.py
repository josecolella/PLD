import pygame
from game import Game
from menu import *
from gameoptions import *


class TreasureHunters(object):
    """
    This class represents the global game which includes the
    menu. Create to encapsulate the initialization of the game
    """

    menu_music = "audio/menu.ogg"

    @staticmethod
    def start():
        """
        Initializes all the pygame methods, window, etc
        that need to be called on tostart the game
        """
        # Initialize Pygame
        pygame.init()
        # Font initializer
        pygame.font.init()
        # Music initializer
        pygame.mixer.init()
        # Menu music
        menu_sound = pygame.mixer.Sound(TreasureHunters.menu_music)
        menu_sound.play(-1)

        screenwidth = 800
        screenheight = 600

        FPS = 20

        # Set screen with width and height
        screen = pygame.display.set_mode((screenwidth, screenheight))
        # Set title for the window and icon for the game
        pygame.display.set_caption("Treasure Hunter")
        iconImg = pygame.image.load("img/icon.png")
        pygame.display.set_icon(iconImg)
        # Start game menu and get user selections
        # Initialize Game Menu
        menu = Menu()
        # Show InitialGameMenu
        selections = menu.show_menu(screen, FPS)
        print(selections)
        musicOption = {
            'game_music': selections['game_music']
        }
        # Process user selections
        if selections['play_game'] is True:
            menu_sound.fadeout(1000)
            newGame = Game(FPS, musicOption, loadgame=False)
            newGame.start(screen)
            # Game.start(screen)
        elif selections['load_game'] is True:
            menu_sound.fadeout(1000)
            loadedGame = Game(FPS, musicOption, loadgame=True)
            loadedGame.start(screen)
        elif selections['exit_game'] is True:
            GameOption.exitGame()
