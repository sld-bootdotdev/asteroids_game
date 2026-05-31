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

    # Player score
    score = 0
    # Combo/multiplier state
    combo_count = 0
    last_hit_time = 0.0
    # Note: combo constants are in `constants.py`

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

        # Render score HUD
        try:
            font = pygame.font.Font(None, 36)
            score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_surf, (10, 10))
            # Render combo multiplier when active
            if combo_count > 1:
                mult_surf = font.render(f"x{combo_count}", True, (255, 200, 0))
                screen.blit(mult_surf, (10 + score_surf.get_width() + 8, 10))
        except Exception:
            # If fonts aren't available for some reason, skip drawing the HUD
            pass

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
                    # Combo logic: increase combo if hits are close in time
                    now_s = pygame.time.get_ticks() / 1000.0
                    if now_s - last_hit_time <= COMBO_TIMEOUT_SECONDS:
                        combo_count = min(combo_count + 1, COMBO_MAX)
                    else:
                        combo_count = 1
                    last_hit_time = now_s

                    # Award points scaled by current combo multiplier
                    points = BASE_POINTS * combo_count
                    score += points
                    log_event(
                        "score", points=points, total=score, multiplier=combo_count
                    )
                    # Split asteroid into smaller asteroids
                    asteroid.split()
                    # Remove shot from all sprite groups
                    shot.kill()

        # Update display
        pygame.display.flip()

        # Limit FPS and calculate delta time
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
