import pygame
from constants import *
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_event
import sys


def main():
    # Initialize Pygame
    pygame.init()

    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create game clock
    clock = pygame.time.Clock()

    # Delta time keeps movement and rotation consistent across different FPS
    dt = 0.0

    # Store objects that need update logic every frame
    updatable = pygame.sprite.Group()

    # Store objects that should be rendered on the screen
    drawable = pygame.sprite.Group()

    # Store all asteroid objects
    asteroids = pygame.sprite.Group()

    # Store all shots objects
    shots = pygame.sprite.Group()

    # Tell Player which sprite groups new player objects should join automatically
    Player.containers = (updatable, drawable)

    # Tell Asteroid which groups new asteroid objects should join automatically
    Asteroid.containers = (asteroids, updatable, drawable)

    # Tell Shot which groups new shots objects should join automatically
    Shot.containers = (shots, updatable, drawable)

    # Tell AsteroidField to join only the updatable group
    # AsteroidField updates/spawns asteroids but does not draw anything itself
    AsteroidField.containers = (updatable,)

    # Create asteroid spawner object
    asteroid_field = AsteroidField()

    # Create player object
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        # Log current game state
        log_state()

        # Processing event queue
        for event in pygame.event.get():
            # Exit game when window is closed
            if event.type == pygame.QUIT:
                return

        # Update all objects in the updatable group
        # Pass dt so movement and rotation stay framerate independent
        updatable.update(dt)

        # Fill screen with black before drawing new frame
        screen.fill("black")

        for obj in asteroids:
            print(type(obj))
            # Check if asteroid collides with the player
            if obj.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Loop through every object stored in the drawable group
        for obj in drawable:
            # Call each object's draw method to render it on the screen
            obj.draw(screen)

        # Check every asteroid against every shot
        for asteroid in asteroids:
            # Loop through all active shots
            for shot in shots:
                # Check if shot collided with asteroid
                if asteroid.collides_with(shot):
                    # Log asteroid hit event
                    log_event("asteroid_shot")
                    # Remove asteroid from all sprite groups
                    asteroid.kill()
                    # Remove shot from all sprite groups
                    shot.kill()

        # Update display
        pygame.display.flip()

        # Limit FPS and calculate delta time
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
