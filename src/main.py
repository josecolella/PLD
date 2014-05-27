#!/usr/bin/env python3
"""
Main Module
"""
import pygame
from sys import exit
from game import Game
from menu import *
from gameoptions import *

if __name__ == '__main__':
    pygame.init()  # Initialize Pygame
    pygame.font.init()  # Font initializer
    pygame.mixer.init()  # Music initializer

    menu_sound = pygame.mixer.Sound("audio/menu.ogg")  # Menu music
    menu_sound.play(-1)

    screenwidth = 800
    screenheight = 600
    # Testing purpose
    # screenwidth = 1024
    # screenheight = 768

    FPS = 20

    # Set screen with width and height
    screen = pygame.display.set_mode((screenwidth, screenheight))
    # Set title for the window and icon for the game
    pygame.display.set_caption("Treasure Hunter")
    iconImg = pygame.image.load("img/icon.png")
    pygame.display.set_icon(iconImg)
    # Start game menu and get user selections
    menu = Menu() # Initialize Game Menu
    selections = menu.show_menu(screen, FPS) # Show InitialGameMenu
    # selections = show_menu(screen, FPS)
    ''' This is a menu selections example:
    {'game_music': False, 'play_game': True, 'load_game': False, 'game_sounds': True, 'unknown': False, 'show_credits': False, 'exit_game': False}
    '''
    print(selections)
    # Process user selections
    if selections['exit_game'] is True:
        pygame.quit()
        exit(0)
    elif selections['play_game'] is True:
        menu_sound.fadeout(1000)
        Game.start(screen, screenheight, screenwidth, FPS, loadgame=False)
    elif selections['load_game'] is True:
        menu_sound.fadeout(1000)
        Game.start(screen, screenheight, screenwidth, FPS, loadgame=True)
