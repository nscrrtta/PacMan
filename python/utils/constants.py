from pathlib import Path


#
# Files
#

ROOT_DIR = Path(__file__).resolve().parents[2]

# Maze files: maze1.txt, maze2.txt, ...
MAZES_DIR = ROOT_DIR / 'mazes'

# Ghost images
IMAGES_DIR = ROOT_DIR / 'pngs'

FONT_FILE = ROOT_DIR / 'font' / 'PressStart2P-Regular.ttf'

#
# Game size
#

SQUARE_SIZE = 24

# Square size (in pixels) the ghost images were drawn for
IMAGE_SQUARE_SIZE = 24

# Number of rows in maze
ROWS = 31

# Number of columns in maze
COLS = 28

# Space above maze
SPACE_ABOVE = SQUARE_SIZE * 3

# Space below maze
SPACE_BELOW = SQUARE_SIZE * 2

# Dimensions of window
WINDOW_WIDTH = COLS * SQUARE_SIZE
WINDOW_HEIGHT = ROWS * SQUARE_SIZE + SPACE_ABOVE + SPACE_BELOW

# How close (in pixels) two ghosts must be
# for them to be considered overlapping
GHOST_OVERLAP_DISTANCE = 25

# Pellet sizes
SMALL_PELLET_RADIUS = 3
LARGE_PELLET_RADIUS = 8

# PacMan size (must be an integer)
PACMAN_RADIUS = SQUARE_SIZE * 2 // 3

# How close (in pixels) PacMan must be to a pellet or ghost
# to eat it (or for the ghost to eat PacMan).
EATING_DISTANCE = PACMAN_RADIUS

#
# Game speed
#

FPS = 60

# Standard speed for PacMan and ghosts (pixels/second)
STANDARD_SPEED = 120

# Ghost speed when scared (pixels/second)
SCARED_SPEED = 60

# Ghost speed when dead (pixels/second)
DEAD_SPEED = 200

#
# Colours
#

BG_COLOUR     = (10, 10, 10)
PACMAN_COLOUR = (255, 255, 0)
PELLET_COLOUR = (245, 187, 156)

# Ghost house gate, and the maze borders while flashing at the end of a level
GATE_COLOUR  = (255, 255, 255)
FLASH_COLOUR = (255, 255, 255)

# Text
BONUS_TEXT_COLOUR  = (0, 0, 255)     # Points for eating a ghost (200)
WHITE_TEXT_COLOUR  = (255, 255, 255) # Score, Level, Paused, New Game
YELLOW_TEXT_COLOUR = (255, 255, 0)   # Ready!, Game Over!

# Maze border colour for each level (repeats after the last one)
MAZE_COLOURS = [
    (0,   0,   255),
    (127, 0,   255),
    (255, 0,   127),
    (255, 127, 100),
    (0,   255, 127),
    (0,   255, 255),
    (0,   127, 255)
]
