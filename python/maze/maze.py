from utils import Direction, Colour, COLS, ROWS, SPACE_ABOVE, SQUARE_SIZE, MAZES_DIR, MAZE_COLOURS
from maze.borders import Borders
from maze.pellet import Pellet
from maze.node import Node


class Maze:
    """
    A graph of nodes for the current level. Updated for each level.
    All entities share a common instance of this class.
    """

    def __init__(self):
        # Count consecutive maze files: maze1.txt, maze2.txt, ...
        self.num_levels = 0
        while (MAZES_DIR / f'maze{self.num_levels + 1}.txt').is_file():
            self.num_levels += 1

    def build_maze(self, level: int):
        """
        Builds a maze (graph of nodes) from a txt file.
        """

        # Keep the level between 1 and self.num_levels
        level = (level - 1) % self.num_levels + 1

        with open(MAZES_DIR / f'maze{level}.txt', 'r') as f:
            self.txt_parsed = [
                # Every second char in each row is a space
                [char for i, char in enumerate(row) if i % 2 == 0]
                for row in f.read().split('\n')
            ]

        # For drawing maze borders
        colour = self._get_maze_colour(level)
        self.borders = Borders(self.txt_parsed, colour)

        # Key: (x, y) coordinates
        # Value: node located at (x, y)
        self.nodes: dict[tuple[float, float], Node] = {}

        # Key: lowercase letter
        # Value: portals (nodes) that are connected
        self.portals: dict[str, list[Node]] = {}

        # Pellets that PacMan eats
        self.pellets: list[Pellet] = []

        # Ghosts' home node
        self.ghost_home_center: Node | None = None

        # PacMan's starting position (list of one or two nodes)
        start: list[Node] = []

        # Gate to ghost home (a list of two nodes)
        gate: list[Node] = []

        for row in range(ROWS):
            for col in range(COLS):
                self.borders.build(row, col)

                # Center coordinates
                x = (col + 0.5) * SQUARE_SIZE
                y = (row + 0.5) * SQUARE_SIZE + SPACE_ABOVE
                node = Node(x, y)

                char = self.txt_parsed[row][col]

                if self._is_node(row, col):
                    self.nodes[(row, col)] = node

                if self._is_portal(row, col):
                    node.set_portal_key(char)
                    if char in self.portals:
                        self.portals[char].append(node)
                    else:
                        self.portals[char] = [node]

                if self._is_pellet(char):
                    pellet = Pellet(x, y, char == '*')
                    self.pellets.append(pellet)

                if self._is_start(char):
                    self.nodes[(row, col)] = node
                    start.append(node)

                if self._is_gate(row, col):
                    self.nodes[(row, col)] = node
                    gate.append(node)

        # Connect nodes
        for node in self.nodes.values():
            self._connect_node_to_neighbours(node)

        # Determine PacMan's starting node,
        # and connect it to the graph
        self._connect_start_node(start)

        # Determine the ghosts' starting nodes,
        # and connect them to the graph
        self._connect_ghost_home(gate)

    def _connect_node_to_neighbours(self, node: Node):
        if node.get_neighbour(Direction.UP) is None:
            up = self._find_closest_node(node, -1, 0)
            self._connect_UD_nodes(up, node)

        if node.get_neighbour(Direction.DOWN) is None:
            down = self._find_closest_node(node, 1, 0)
            self._connect_UD_nodes(node, down)

        if node.get_neighbour(Direction.LEFT) is None:
            left = self._find_closest_node(node, 0, -1)
            self._connect_LR_nodes(left, node)

        if node.get_neighbour(Direction.RIGHT) is None:
            right = self._find_closest_node(node, 0, 1)
            self._connect_LR_nodes(node, right)

    def _connect_start_node(self, start: list[Node]):
        self.pacman_start_node = start[0]
        if len(start) > 1:
            self.pacman_start_node = self._insert_middle_node(*start)

    def _connect_ghost_home(self, gate: list[Node]):
        # Node just outside of gate to ghost home
        entrance = self._insert_middle_node(*gate)

        # Middle of ghost home is 3 squares below entrance
        center = Node(entrance.x, entrance.y + SQUARE_SIZE * 3)

        # Right node of ghost home is 2 squares to the right
        right = Node(center.x + SQUARE_SIZE * 2, center.y)

        # Left node of ghost home is 2 squares to the left
        left = Node(center.x - SQUARE_SIZE * 2, center.y)

        self._connect_UD_nodes(entrance, center)
        self._connect_LR_nodes(center, right)
        self._connect_LR_nodes(left, center)

        self.ghost_home_entrance = entrance
        self.ghost_home_center = center

        self.blinky_start_node = entrance
        self.clyde_start_node = right
        self.pinky_start_node = center
        self.inky_start_node = left

    #
    # Helpers
    #

    def _find_closest_node(self, node: Node, dr: int, dc: int) -> Node | None:
        """
        Return closest node in a given direction, or None.
        """
        row = int((node.y - SPACE_ABOVE) // SQUARE_SIZE + dr)
        col = int(node.x // SQUARE_SIZE + dc)

        # Stop when at a node or no longer on a path
        while (row, col) not in self.nodes and self._is_path(row, col):
            row += dr
            col += dc

        return self.nodes.get((row, col))

    def _is_path(self, row: int, col: int) -> bool:
        if 0 <= row < ROWS and 0 <= col < COLS:
            char = self.txt_parsed[row][col]
            return char != 'X' and char != '='
        return False

    def _is_node(self, row: int, col: int) -> bool:
        """
        A node is a corner, intersection, or dead end in the maze.
        """
        # A node must also be a path
        if not self._is_path(row, col):
            return False

        can_move_up    = self._is_path(row - 1, col)
        can_move_down  = self._is_path(row + 1, col)
        can_move_left  = self._is_path(row, col - 1)
        can_move_right = self._is_path(row, col + 1)

        # Can move in 1, 3 or 4 directions (dead end or intersection)
        directions = [can_move_up, can_move_down, can_move_left, can_move_right]
        if directions.count(True) != 2:
            return True

        # Can move in 2 directions - must be corner
        return can_move_left != can_move_right \
           and can_move_down != can_move_up

    def _is_portal(self, row: int, col: int) -> bool:
        """
        A portal is a lowercase letter on the edge of the maze.
        """
        if row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1:
            return self.txt_parsed[row][col].islower()
        return False

    def _is_pellet(self, char: str) -> bool:
        return char == '.' or char == '*'

    def _is_start(self, char: str) -> bool:
        return char == 'S'

    def _is_gate(self, row: int, col: int) -> bool:
        if row == ROWS - 1:
            return False
        return self.txt_parsed[row + 1][col] == '='

    def _connect_LR_nodes(self, left: Node | None, right: Node | None):
        if left is not None:
            left.set_neighbour(Direction.RIGHT, right)
        if right is not None:
            right.set_neighbour(Direction.LEFT, left)

    def _connect_UD_nodes(self, up: Node | None, down: Node | None):
        if up is not None:
            up.set_neighbour(Direction.DOWN, down)
        if down is not None:
            down.set_neighbour(Direction.UP, up)

    def _insert_middle_node(self, a: Node, b: Node) -> Node:
        if a.y < b.y:
            return self._insert_middle_node_UD(a, b)
        if a.y > b.y:
            return self._insert_middle_node_UD(b, a)
        if a.x < b.x:
            return self._insert_middle_node_LR(a, b)
        if a.x > b.x:
            return self._insert_middle_node_LR(b, a)

    def _insert_middle_node_UD(self, up: Node, down: Node) -> Node:
        y = (up.y + down.y) / 2
        middle = Node(up.x, y)
        self._connect_UD_nodes(up, middle)
        self._connect_UD_nodes(middle, down)
        return middle

    def _insert_middle_node_LR(self, left: Node, right: Node) -> Node:
        x = (left.x + right.x) / 2
        middle = Node(x, left.y)
        self._connect_LR_nodes(left, middle)
        self._connect_LR_nodes(middle, right)
        return middle

    def _get_maze_colour(self, level: int) -> Colour:
        return MAZE_COLOURS[(level - 1) % len(MAZE_COLOURS)]


maze = Maze()
