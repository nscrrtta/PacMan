from utils import Direction, FPS, SQUARE_SIZE
from entities.entity import Entity
from maze import Node, maze


class PacMan(Entity):

    def __init__(self):
        super().__init__()
        self.pellets_eaten = 0

    def reset(self):
        # While PacMan is moving, players can "queue" his next move.
        # The next time PacMan reaches a node, he will change
        # direction based on the move in this queue.
        #
        # If there is no move queued, he will continue moving
        # in the same direction (if possible).
        #
        # There can only be one move queued at a time.
        self.move_queue: list[Direction] = []

        self.next_node = None
        super().reset(maze.pacman_start_node)

        # Variables for chewing animation
        self.chew_frames = SQUARE_SIZE * FPS // self.px_per_sec
        self.frame_counter = 0
        self.mouth_angle = 0.0

        # True while PacMan's death animation is active
        self.dying = False

    def set_next_node(self):
        self.curr_node = self.next_node
        self.next_node = self._get_next_node()

    def _get_next_node(self) -> Node | None:
        if self.move_queue:
            direction = self.move_queue[0]
            node = self._get_neighbour(direction)
            if node is not None:
                self.move_queue.pop()
                return node
        # Continue moving in the same direction, if possible
        return self._get_neighbour(self.direction)

    def _get_neighbour(self, direction: Direction) -> Node | None:
        # If PacMan is moving (self.next_node is not None)
        # use self.next_node as the reference node.
        #
        # Otherwise, if PacMan is stationary,
        # use self.curr_node as the reference node.
        ref_node = self.next_node or self.curr_node
        return ref_node.get_neighbour(direction)

    def queue_next_direction(self, direction: Direction):
        """
        Queue the direction PacMan will move in once he
        reaches the node he is currently moving to.
        """
        self.move_queue = [direction]

        # If PacMan is not moving, immediately set self.next_node
        if not self.is_moving():
            self.next_node = self._get_neighbour(direction)
            self.move_queue.pop()
            self.set_direction()
        elif direction == self.direction.opposite:
            self.move_queue.pop()
            self.reverse()

    def get_node_n_squares_ahead(self, n: int) -> Node:
        x, y = self.x, self.y
        if self.direction == Direction.UP:
            y -= SQUARE_SIZE * n
        elif self.direction == Direction.DOWN:
            y += SQUARE_SIZE * n
        elif self.direction == Direction.LEFT:
            x -= SQUARE_SIZE * n
        elif self.direction == Direction.RIGHT:
            x += SQUARE_SIZE * n
        return Node(x, y)

    def update(self):
        # Dying animation
        if self.dying:
            self.mouth_angle += FPS / 15
            if self.mouth_angle >= 360:
                self.dying = False
        # Chewing animation
        elif self.is_moving():
            self.frame_counter += 1
            self.frame_counter %= self.chew_frames

            # Calculate mouth_angle
            half = self.chew_frames / 2
            # 1 ... 0.5 ... 0 ... 0.5 ... 1 ...
            factor = abs(self.frame_counter - half) / half
            # 120° when mouth fully open
            self.mouth_angle = 120 * factor
