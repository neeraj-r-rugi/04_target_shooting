"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import math
import random
import pygame

#Added a function to generate random RGB color values for targets as an extra task because it looks 
# fun lol
def get_random_number(min_value, max_value):
    """Return a random number between min_value and max_value."""
    return (random.uniform(min_value, max_value), random.uniform(min_value, max_value), random.uniform(min_value, max_value))

class Target:
    def __init__(self, x, y, radius=28, color=get_random_number(0, 255),
                 vx=0.0, vy=0.0, wave_amp=0.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx              # pixels per frame
        self.vy = vy
        self.wave_amp = wave_amp  # 0 = straight-line mover, >0 = wobbling mover
        self.phase = 0.0

    def get_bounding_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def update(self, width, height):
        """Move one frame and bounce off the edges of the play area."""
        self.x += self.vx
        self.y += self.vy

        # Wobble pattern: a sine-wave nudge on top of the straight-line motion
        if self.wave_amp:
            self.phase += 0.1
            self.y += math.sin(self.phase) * self.wave_amp

        # Bounce: clamp the circle's EDGE (not its center) to the bounds,
        # and force the velocity to point away from the wall.
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.vx = -abs(self.vx)

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.vy = -abs(self.vy)