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
        # screen = pygame.Surface((1024,768))
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
        lever1 = Lever(5 * 48, 1 * 64, 'img/lever_a_0.png')
        lever2 = Lever(15 * 48, 1 * 64, 'img/lever_b_0.png')
        # For testing purposes
        # background = pygame.Surface((screen.get_size()))
        # background.fill((255, 255, 255))
        # screen.blit(background, (0, 0))

        
        # Game Loop
        while True:
            screen.blit(level1, (0, 0))  # blit the background
            Tile.draw_tiles(screen)
            Robot.spawn(total_frames, FPS)
            Robot.movement(screen)
            Laser.super_massive_jumbo_loop(screen)

            mainCharacter.movement(screen)

            # A_Star(screen, mainCharacter, total_frames, FPS)
            leverPulled = interaction(screen, mainCharacter, lever1, lever2)
            if leverPulled:
                Tile.draw_tiles(screen)

            enemy.movement(screen)

            mainCharacter.draw(screen)
            enemy.draw(screen)
            Robot.draw_robots(screen)
            Lever.allLevers.draw(screen)
            # screen2.blit(pygame.transform.scale(screen, screen2.get_rect().size), (0,0))
            pygame.display.flip()
            clock.tick(FPS)
            total_frames += 1

        pygame.quit()
