import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOT_SPEED,
    PLAYER_SHOT_COOLDOWN_SECONDS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Current ship rotation angle
        self.cooldown = 0

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
        # Reduce cooldown timer by elapsed frame time
        self.cooldown -= dt

        # Get currently pressed keys
        keys = pygame.key.get_pressed()

        # Rotate left
        if keys[pygame.K_a]:
            self.rotate(-dt)

        # Rotate right
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Move forward
        if keys[pygame.K_w]:
            self.move(dt)

        # Move backward
        if keys[pygame.K_s]:
            self.move(-dt)

        # Shoot
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Wrap player around screen after movement
        try:
            self.wrap_around_screen()
        except Exception:
            pass

    def move(self, dt):
        # Base direction vector
        unit_vector = pygame.Vector2(0, 1)

        # Rotate direction based on player rotation
        rotated_vector = unit_vector.rotate(self.rotation)

        # Convert direction into movement with speed and frame time
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt

        # Move player position
        self.position += rotated_with_speed_vector

    def shoot(self):

        # Prevent shooting while weapon is on cooldown
        if self.cooldown > 0:
            return
        # Reset cooldown timer after firing
        self.cooldown = PLAYER_SHOT_COOLDOWN_SECONDS

        # Create new shot at player position
        shot = Shot(self.position.x, self.position.y)

        # Create base forward direction vector
        velocity = pygame.Vector2(0, 1)

        # Rotate shot direction to match player rotation
        velocity = velocity.rotate(self.rotation)

        # Apply shot movement speed
        velocity *= PLAYER_SHOT_SPEED

        # Give shot its movement velocity
        shot.velocity = velocity
