import random
from collections.abc import Callable

import pygame
from asteroid import Asteroid
from constants import *

# Type alias for asteroid spawn edge data
# Stores:
# 1. Movement direction vector
# 2. Function that returns spawn position
Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    # Define all possible asteroid spawn edges
    edges: list[Edge] = [
        (
            # Move right
            pygame.Vector2(1, 0),
            # Spawn outside left side of screen
            lambda y: pygame.Vector2(-ASTEROID_SPAWN_MARGIN, y * SCREEN_HEIGHT),
        ),
        (
            # Move left
            pygame.Vector2(-1, 0),
            # Spawn outside right side of screen
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_SPAWN_MARGIN,
                y * SCREEN_HEIGHT,
            ),
        ),
        (
            # Move down
            pygame.Vector2(0, 1),
            # Spawn above screen
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH,
                -ASTEROID_SPAWN_MARGIN,
            ),
        ),
        (
            # Move up
            pygame.Vector2(0, -1),
            # Spawn below screen
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH,
                SCREEN_HEIGHT + ASTEROID_SPAWN_MARGIN,
            ),
        ),
    ]

    def __init__(self) -> None:
        # Initialize sprite and add to containers
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Timer used to control asteroid spawn rate
        self.spawn_timer = 0.0

    def spawn(
        self,
        radius: float,
        position: pygame.Vector2,
        velocity: pygame.Vector2,
    ) -> None:

        # Create asteroid object
        asteroid = Asteroid(position.x, position.y, radius)

        # Set asteroid movement direction and speed
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:

        # Increase timer every frame
        self.spawn_timer += dt

        # Spawn asteroid after timer reaches limit
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:

            # Reset timer
            self.spawn_timer = 0

            # Pick random screen edge
            edge = random.choice(self.edges)

            # Random asteroid speed
            speed = random.randint(40, 100)

            # Create movement vector
            velocity = edge[0] * speed

            # Add random angle variation
            velocity = velocity.rotate(random.randint(-30, 30))

            # Generate random spawn position
            position = edge[1](random.uniform(0, 1))

            # Random asteroid size multiplier
            kind = random.randint(1, ASTEROID_KINDS)

            # Spawn asteroid
            self.spawn(
                ASTEROID_MIN_RADIUS * kind,
                position,
                velocity,
            )
