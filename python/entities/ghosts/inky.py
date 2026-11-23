from utils import GhostState, COLS, ROWS, SQUARE_SIZE
from entities.ghosts.blinky import Blinky
from entities.ghosts.ghost import Ghost
from entities.pacman import PacMan
from maze import Node, maze


class Inky(Ghost):

    def __init__(self, pacman: PacMan, blinky: Blinky):
        super().__init__(pacman, 'inky')
        self.pellet_threshold = 90

        # Inky is the only ghost whose movement
        # depends on the position of another ghost
        self.blinky = blinky

    def reset(self):
        super().reset(maze.inky_start_node)

    def _get_target_node(self) -> Node:
        if self.state == GhostState.SCATTER:
            # Scatter to bottom-right corner
            return Node(COLS*SQUARE_SIZE, ROWS*SQUARE_SIZE)

        # 1. Look at the point two squares ahead of PacMan
        # 2. Draw a vector from Blinky's position to that point
        # 3. Double the length of that vector to find the target node
        node = self.pacman.get_node_n_squares_ahead(2)
        x = 2 * node.x - self.blinky.x
        y = 2 * node.y - self.blinky.y
        return Node(x, y)
