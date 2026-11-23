from utils import Direction


class Node:

    def __init__(self, x: float, y: float):
        # Center coordinates
        self.x, self.y = x, y

        # Some nodes are portals. Connected portals share
        # the same key, which is a lowercase letter
        self.portal_key: str | None = None

        # A node has up to four neighbours
        self.neighbours: list[Node | None] = [None] * 4

    def get_neighbour(self, direction: Direction) -> 'Node | None':
        return self.neighbours[direction.value]

    def set_neighbour(self, direction: Direction, node: 'Node | None'):
        self.neighbours[direction.value] = node

    def set_portal_key(self, key: str):
        self.portal_key = key

    def is_portal(self) -> bool:
        return self.portal_key is not None
