from utils import GhostState, COLS, SQUARE_SIZE
from entities.ghosts.ghost import Ghost
from entities.pacman import PacMan
from maze import Node, maze


class Pinky(Ghost):

    def __init__(self, pacman: PacMan):
        super().__init__(pacman, 'pinky')
        self.pellet_threshold = 10

    def reset(self):
        super().reset(maze.pinky_start_node)
        # Pinky oscillates in the opposite direction of all other ghosts
        self.oscillate_direction = -1

    def _get_target_node(self) -> Node:
        if self.state == GhostState.SCATTER:
            # Scatter to top-right corner
            return Node(SQUARE_SIZE*COLS, 0)
        # Target 4 squares ahead of PacMan's current position
        return self.pacman.get_node_n_squares_ahead(4)
