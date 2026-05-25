import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Current ship rotation angle

    def triangle(self) -> list[pygame.Vector2]:
        # Direction where the ship is facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Side direction used to build triangle width
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        # Front point of the ship
        a = self.position + forward * self.radius

        # Bottom left point
        b = self.position - forward * self.radius - right

        # Bottom right point
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        # Draw player triangle on screen
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        # Change player rotation over time
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        # Get currently pressed keys
        keys = pygame.key.get_pressed()

        # Rotate left
        if keys[pygame.K_a]:
            self.rotate(-dt)

        # Rotate right
        if keys[pygame.K_d]:
            self.rotate(dt)
