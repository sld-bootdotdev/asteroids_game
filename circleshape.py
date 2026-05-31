import pygame


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

    def collides_with(self, other) -> bool:

        # Calculate distance between object centers
        distance = self.position.distance_to(other.position)

        # Objects collide when distance is less than or equal to combined radii
        return distance <= self.radius + other.radius
