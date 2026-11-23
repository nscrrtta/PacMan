from enum import Enum


class GameState(Enum):
    PAUSED = 0
    # PacMan has run out of lives
    GAME_OVER = 1
    # PacMan has eaten all pellets
    LEVEL_OVER = 2
    # PacMan has been hit by a ghost
    LEVEL_RESET = 3
    # PacMan is eating a ghost (brief pause)
    EATING_GHOST = 4
    # Level just started, waiting for PacMan to move
    PENDING = 5
    # None of the above (Default state)
    ACTIVE = 6


class GhostState(Enum):
    SCATTER = 0
    CHASE   = 1


class Direction(Enum):
    UP    = 0
    DOWN  = 1
    LEFT  = 2
    RIGHT = 3

    @property
    def opposite(self) -> 'Direction':
        return {
            Direction.UP:    Direction.DOWN,
            Direction.DOWN:  Direction.UP,
            Direction.LEFT:  Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }[self]
