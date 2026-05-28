import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        # Spawn bullets using asteroid position and radius
        pygame.draw.circle(screen, "white", self.position, self.radius)

    # Move bullets every frame using its velocity
    def update(self, dt):
        # Add movement based on velocity and delta time
        self.position += self.velocity * dt
