import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    # Draw asteroid as a circle
    def draw(self, screen):
        # Draw circle using asteroid position and radius
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    # Move asteroid every frame using its velocity
    def update(self, dt):
        # Add movement based on velocity and delta time
        self.position += self.velocity * dt

    def split(self):

        # Remove original asteroid
        self.kill()

        # Stop splitting if asteroid is already at minimum size
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Log asteroid split event
        log_event("asteroid_split")

        # Generate random split angle
        angle = random.uniform(20, 50)

        # Create first velocity vector rotated clockwise
        first_rotation_vector = self.velocity.rotate(angle)

        # Create second velocity vector rotated counterclockwise
        second_rotation_vector = self.velocity.rotate(-angle)

        # Calculate radius for the new smaller asteroids
        radius_small = self.radius - ASTEROID_MIN_RADIUS

        # Create first smaller asteroid at current position
        asteroid_1 = Asteroid(
            self.position.x,
            self.position.y,
            radius_small,
        )

        # Create second smaller asteroid at current position
        asteroid_2 = Asteroid(
            self.position.x,
            self.position.y,
            radius_small,
        )

        # Assign velocity and increase speed by 20%
        asteroid_1.velocity = first_rotation_vector * 1.2

        # Assign velocity and increase speed by 20%
        asteroid_2.velocity = second_rotation_vector * 1.2
