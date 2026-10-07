"""
GameEngine: owns the targets and handles player clicks.

Moving targets (Task 2), combo scoring (Task 3), and a timed round (Task 4).
"""

import math
import random

import pygame

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
SPEEDS = [1.5, 3.0, 5.0]   # slow, medium, fast (pixels per frame)

BASE_POINTS = 10
HITS_PER_MULTIPLIER = 3
MAX_MULTIPLIER = 5

ROUND_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: new targets, score, combo, and timer."""
        self.targets = [self._random_target(SPEEDS[i % len(SPEEDS)])
                        for i in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 0
        self.game_over = False
        self.time_left = float(ROUND_SECONDS)
        self.round_start = pygame.time.get_ticks()

    def _random_target(self, speed=None):
        if speed is None:
            speed = random.choice(SPEEDS)
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        angle = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        wave_amp = random.choice([0.0, 0.0, 2.0])

        return Target(x, y, radius=TARGET_RADIUS, vx=vx, vy=vy, wave_amp=wave_amp)

    @property
    def multiplier(self):
        return min(1 + self.combo // HITS_PER_MULTIPLIER, MAX_MULTIPLIER)

    def _update_clock(self):
        """Recompute time_left from the real clock; end the round at zero."""
        if self.game_over:
            return
        elapsed = (pygame.time.get_ticks() - self.round_start) / 1000
        self.time_left = max(0.0, ROUND_SECONDS - elapsed)
        if self.time_left <= 0:
            self.game_over = True

    def handle_click(self, pos):
        # Refresh the clock first so a click arriving just after time ran out
        # (but before this frame's update) is still rejected.
        self._update_clock()
        if self.game_over:
            return

        target = check_hit(self.targets, pos)
        if target is not None:
            self.score += BASE_POINTS * self.multiplier
            self.combo += 1
            self.hits += 1
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            self.combo = 0
            self.misses += 1

    def update(self):
        self._update_clock()
        if self.game_over:
            return   # targets freeze where they were when time expired
        for target in self.targets:
            target.update(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)

        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Combo: x{self.multiplier}  ({self.combo} streak)", (10, 36))
        renderer.draw_text(surface, font, f"Hits: {self.hits}  Misses: {self.misses}", (10, 62))

        # Timer, right-aligned; turns red for the last 5 seconds
        timer_text = f"Time: {math.ceil(self.time_left)}"
        timer_color = (255, 90, 90) if self.time_left <= 5 else renderer.COLOR_TEXT
        timer_x = surface.get_width() - font.size(timer_text)[0] - 10
        renderer.draw_text(surface, font, timer_text, (timer_x, 10), timer_color)

        if self.game_over:
            renderer.draw_overlay(surface)
            renderer.draw_banner(surface, font, "TIME'S UP!", dy=-50)
            renderer.draw_banner(surface, font, f"Final score: {self.score}", dy=-10)
            total = self.hits + self.misses
            accuracy = round(100 * self.hits / total) if total else 0
            renderer.draw_banner(surface, font, f"Hits: {self.hits}   Accuracy: {accuracy}%", dy=25)
            renderer.draw_banner(surface, font, "Press R to play again", dy=70)