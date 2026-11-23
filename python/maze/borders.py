from utils import Colour, COLS, ROWS, SPACE_ABOVE, SQUARE_SIZE
import pygame
import math


class Borders:
    """
    For drawing borders of maze.
    """

    def __init__(self, txt_parsed: list[list[str]], colour: Colour):
        self.txt_parsed = txt_parsed
        self.colour = colour

        self.edges: list[Edge] = []
        self.corners: list[Corner] = []

    def build(self, row: int, col: int):
        if self._is_path(row, col):
            return
        elif self._is_edge(row, col):
            self._build_edge(row, col)
        elif self._is_corner(row, col):
            self._build_corner(row, col)

    def _is_path(self, row: int, col: int) -> bool:
        if 0 <= row < ROWS and 0 <= col < COLS:
            char = self.txt_parsed[row][col]
            return char != 'X' and char != '='
        return False

    def _is_edge(self, row: int, col: int) -> bool:
        return [
            self._is_path(row - 1, col),
            self._is_path(row + 1, col),
            self._is_path(row, col - 1),
            self._is_path(row, col + 1)
        ].count(True) == 1

    def _is_corner(self, row: int, col: int) -> bool:
        return self._is_path(row - 1, col - 1) \
            or self._is_path(row - 1, col + 1) \
            or self._is_path(row + 1, col - 1) \
            or self._is_path(row + 1, col + 1)

    def _build_edge(self, row: int, col: int):
        x = SQUARE_SIZE * col
        y = SQUARE_SIZE * row + SPACE_ABOVE

        # Determine if edge is gate to ghost home
        gate = self.txt_parsed[row][col] == '='

        w = 4 if gate else 1
        h = SQUARE_SIZE

        # If path above
        if self._is_path(row - 1, col):
            y += SQUARE_SIZE / 2
            vertical = False

        # If path below
        elif self._is_path(row + 1, col):
            y += SQUARE_SIZE / 2 - w
            vertical = False

        # If path left
        elif self._is_path(row, col - 1):
            x += SQUARE_SIZE / 2
            vertical = True

        # If path right
        elif self._is_path(row, col + 1):
            x += SQUARE_SIZE / 2 - w
            vertical = True

        if vertical:
            w, h = h, w

        edge = Edge(pygame.Rect(x, y, h, w), gate)
        self.edges.append(edge)

    def _build_corner(self, row: int, col: int):
        x = SQUARE_SIZE * col
        y = SQUARE_SIZE * row + SPACE_ABOVE

        # . .
        # X .
        if self._is_path(row - 1, col + 1) \
        and self._is_path(row, col + 1) \
        and self._is_path(row - 1, col):
            angle = 0

        # . .
        # . X
        elif self._is_path(row - 1, col - 1) \
        and self._is_path(row, col - 1) \
        and self._is_path(row - 1, col):
            angle = 90

        # . X
        # . .
        elif self._is_path(row + 1, col - 1) \
        and self._is_path(row, col - 1) \
        and self._is_path(row + 1, col):
            angle = 180

        else: angle = 270

        # X X
        # . X
        if self._is_path(row + 1, col - 1) \
        and not self._is_path(row + 1, col) \
        and not self._is_path(row, col - 1):
            x += 1
            y -= 1
            angle = 0

        # X X
        # X .
        elif self._is_path(row + 1, col + 1) \
        and not self._is_path(row + 1, col) \
        and not self._is_path(row, col + 1):
            x -= 1
            y -= 1
            angle = 90

        # X .
        # X X
        if self._is_path(row - 1, col + 1) \
        and not self._is_path(row - 1, col) \
        and not self._is_path(row, col + 1):
            x -= 1
            y += 1
            angle = 180

        # . X
        # X X
        elif self._is_path(row - 1, col - 1) \
        and not self._is_path(row - 1, col) \
        and not self._is_path(row, col - 1):
            x += 1
            y += 1
            angle = 270

        if angle == 90 or angle == 180:
            x += SQUARE_SIZE
        if angle == 90 or angle == 0:
            y += SQUARE_SIZE

        corner = Corner(x, y, angle)
        self.corners.append(corner)

class Edge:

    def __init__(self, rect: pygame.Rect, gate: bool):
        self.rect = rect
        self.gate = gate

class Corner:

    def __init__(self, x: int, y: int, angle: int):
        radius = SQUARE_SIZE / 2
        self.rect = pygame.Rect(
            x - radius,
            y - radius,
            radius * 2,
            radius * 2
        )
        self.start_angle = math.radians(angle)
        self.end_angle = math.radians(angle + 90)
