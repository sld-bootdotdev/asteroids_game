# Asteroids (Pygame)

An Asteroids-style arcade game built with Python and `pygame` as part of the Boot.dev curriculum.

## Core architecture

This project keeps the game loop intentionally simple and leans on `pygame.sprite.Group` to organize the simulation:

- `main.py` is the entry point. It initializes Pygame, creates the window, constructs sprite groups, and runs the frame loop (`events -> update -> collision checks -> draw -> flip`).
- `constants.py` defines all tuning knobs (screen size, speeds, cooldowns, radii, etc.) so gameplay changes don’t require hunting through code.
- `circleshape.py` provides a shared base for “things that collide”. Entities store `position` and `radius`, and collision is circle-based (fast and good enough for Asteroids).
- `player.py` implements the ship as a triangle. It tracks `rotation`, moves by rotating a forward vector, and spawns `Shot` sprites with a cooldown.
- `asteroid.py` implements asteroids that move and can split into smaller asteroids when hit.
- `asteroidfield.py` is a spawner/updater responsible for creating new asteroids over time (so the game doesn’t have to manually “manage waves”).
- `shot.py` defines projectiles with a velocity and lifetime-style behavior.

The key pattern is “entities are sprites”: each entity is responsible for its own `update()` and (when drawable) `draw()` behavior, and `main.py` coordinates how groups are updated and rendered.

## Requirements

- Python `>= 3.13` (see `.python-version`)
- `pygame==2.6.1` (declared in `pyproject.toml`)

## Run the game

### Option A: `uv` (recommended)

1) Install dependencies:

```bash
uv sync
```

1) Run:

```bash
uv run python main.py
```

### Option B: `venv` + `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install "pygame==2.6.1"
python main.py
```

## Notes

- The game logs snapshots to `game_state.jsonl` and events to `game_events.jsonl` (JSON Lines format) for the first ~16 seconds of gameplay.
