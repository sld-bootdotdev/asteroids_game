import pygame
from constants import *
from logger import log_state


def main():
    # Initialize Pygame
    pygame.init()
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create game clock
    clock = pygame.time.Clock()
    dt = 0.0

    while True:
        # Log current game state
        log_state()
        # Processing event queue
        for event in pygame.event.get():
            # Exit game when window is closed
            if event.type == pygame.QUIT:
                return
        # Fill screen with b1ack
        screen.fill("black")
        # Update display
        pygame.display.flip()
        # Limit FPS and calculate delta time
        dt = clock.tick(60) / 1000
        # print(dt)

    # print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    # print(f"Screen width: {SCREEN_WIDTH}")
    # print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
