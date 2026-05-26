import pygame
from circleshape import CircleShape
from player import Player
from constants import LINE_WIDTH


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
