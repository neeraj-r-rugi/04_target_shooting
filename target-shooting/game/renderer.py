"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 25, 35)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, targets):
    surface.fill(COLOR_BG)
    for target in targets:
        pygame.draw.circle(surface, target.color, (int(target.x), int(target.y)), target.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(target.x), int(target.y)), target.radius, 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text, dy=0):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2,
                                 surface.get_height() // 2 + dy))
    surface.blit(surf, rect)
    
def draw_overlay(surface, alpha=170):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))
