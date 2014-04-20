#!/usr/bin/env python3
"""
Game Module
"""

import pygame
from models import *
from interaction import *
from A_Star import A_Star


class Game:

    @staticmethod
    def start(screen, screenheight, screenwidth, FPS):
        # Main theme music
        pygame.mixer.music.load("audio/laberynth.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Continuous Loop

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
        enemy = Enemy(20 * 48, 10 * 64)

        # For testing purposes
        # background = pygame.Surface((screen.get_size()))
        # background.fill((255, 255, 255))
        # screen.blit(background, (0, 0))

        # Game Loop
        while True:
            screen.blit(level1, (0, 0))  # blit the background
            Robot.spawn(total_frames, FPS)
            Robot.movement(screen)

            # A_Star(screen, mainCharacter, total_frames, FPS)
            interaction(screen, mainCharacter)
            mainCharacter.movement(screen)
            enemy.movement(screen)
            Tile.draw_tiles(screen)

            mainCharacter.draw(screen)
            enemy.draw(screen)
            Robot.draw_robots(screen)

            pygame.display.flip()
            clock.tick(FPS)
            total_frames += 1

        pygame.quit()
