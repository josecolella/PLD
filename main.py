#!/usr/bin/env python3
"""
Main Module
"""

import pygame
from models import *
from interaction import *
from A_Star import A_Star
from menu import show_menu

pygame.init()  # Initialize Pygame
pygame.font.init()  # Font initializer
pygame.mixer.init()  # Music initializer

# Main theme music
# pygame.mixer.music.load("audio/laberynth.ogg")
# pygame.mixer.music.play(-1)  # Continuous Loop

screenwidth = 1024
screenheight = 768
FPS = 20

# Set screen with width and height
screen = pygame.display.set_mode((screenwidth, screenheight))

# Start game menu and get user selections
selections = show_menu(screen, FPS)
''' This is a menu selections example:
{'game_music': False, 'play_game': True, 'game_sounds': True, 'unknown': False, 'show_credits': False, 'exit_game': False}
'''
# Process user selections
if selections['exit_game'] == True:
   pygame.quit()
   exit(0)


for y in range(0, screen.get_height(), 16):
    for x in range(0, screen.get_width(), 16):
        if Tile.total_tiles in Tile.invalids:
            Tile(x, y, 'solid')
        else:
            Tile(x, y, 'empty')


clock = pygame.time.Clock()  # Initialize Game Clock
total_frames = 0

level1 = pygame.image.load('img/level1.png')
mainCharacter = MainCharacter(1 * 48, 10 * 64)

# Game Loop
while True:

    screen.blit(level1, (0, 0))  # blit the background

    # Robot.spawn(total_frames, FPS)
    # Robot.movement()

    mainCharacter.movement()

    # A_Star(screen, mainCharacter, total_frames, FPS)
    interaction(screen, mainCharacter)
    Tile.draw_tiles(screen)

    mainCharacter.draw(screen)
    # Robot.draw_zombies(screen)

    pygame.display.flip()
    clock.tick(FPS)
    total_frames += 1
    
pygame.quit()
