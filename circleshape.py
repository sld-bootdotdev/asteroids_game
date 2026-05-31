import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_SPAWN_MARGIN


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:

        # Automatically add object to assigned sprite groups
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        # Store object position
        self.position: pygame.Vector2 = pygame.Vector2(x, y)

        # Default movement vector
        self.velocity = pygame.Vector2(0, 0)

        # Collision and drawing radius
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # Must be implemented by child classes
        pass

    def update(self, dt: float) -> None:
        # Must be implemented by child classes
        pass

    def wrap_around_screen(self) -> None:
        """Wrap object position around screen edges (toroidal world)."""
        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT

        # Don't immediately wrap freshly-spawned objects that sit just outside
        # the screen edge. Only wrap once an object moves beyond a safety
        # margin (based on the configured spawn margin).
        margin = ASTEROID_SPAWN_MARGIN

        if self.position.x < -margin or self.position.x > w + margin:
            self.position.x = self.position.x % w

        if self.position.y < -margin or self.position.y > h + margin:
            self.position.y = self.position.y % h

    def collides_with(self, other) -> bool:

        # Calculate distance between object centers
        distance = self.position.distance_to(other.position)

        # Objects collide when distance is less than or equal to combined radii
        return distance <= self.radius + other.radius
