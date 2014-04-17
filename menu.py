#!/usr/bin/env python3
"""
Module that creates the game menu
"""
import pygame


def write(screen, text, x, y,
                   size=15, color=(255, 255, 255), font_type = 'comicneueangular'):
    try:
        text = str(text)
        font = pygame.font.SysFont(
            font_type, size)
        text = font.render(text, True, color)
        text = font.convert_alpha()
        screen.blit(text, (x, y))
    except Exception:
        print("Font Error, saw it coming")
