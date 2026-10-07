"""
hit_detection: figures out whether a click landed on a target.
"""
import pygame


def check_hit(targets, click_pos):
    click = pygame.Vector2(click_pos)
    for target in reversed(targets):
        if click.distance_to((target.x, target.y)) <= target.radius:
            return target
    return None
