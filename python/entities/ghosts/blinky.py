from entities.ghosts.ghost import Ghost
from entities.pacman import PacMan
from utils import GhostState
from maze import Node, maze


class Blinky(Ghost):

    def __init__(self, pacman: PacMan):
        super().__init__(pacman, 'blinky')
        self.pellet_threshold = 0

    def reset(self):
        super().reset(maze.blinky_start_node)

    def _get_target_node(self) -> Node:
        if self.state == GhostState.SCATTER:
            # Scatter to top-left corner
            return Node(0, 0)
        # Chase PacMan
        return Node(self.pacman.x, self.pacman.y)
