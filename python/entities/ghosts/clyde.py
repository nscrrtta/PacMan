from utils import GhostState, ROWS, SQUARE_SIZE
from entities.ghosts.ghost import Ghost
from entities.pacman import PacMan
from maze import Node, maze


class Clyde(Ghost):

    def __init__(self, pacman: PacMan):
        super().__init__(pacman, 'clyde')
        self.pellet_threshold = 60

    def reset(self):
        super().reset(maze.clyde_start_node)

    def _get_target_node(self) -> Node:
        scatter_node = Node(0, ROWS*SQUARE_SIZE)

        if self.state == GhostState.SCATTER:
            # Scatter to bottom-left corner
            return scatter_node

        d = self.distance_to_entity(self.pacman)

        # Chase PacMan
        if d > 8 * SQUARE_SIZE:
            return Node(self.pacman.x, self.pacman.y)
        # Run from PacMan
        return scatter_node
