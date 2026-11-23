from utils import Direction, FPS, STANDARD_SPEED
from maze import Node
import math


class Entity:

    def __init__(self):
        self.curr_node: Node | None = None
        self.next_node: Node | None = None

    def reset(self, curr_node: Node):
        """
        Called when a new level begins
        or a level in progress resets.
        """
        self.move_to_node(curr_node)
        self.set_speed(STANDARD_SPEED)
        self.set_direction()

    def move_to_node(self, node: Node):
        self.curr_node = node
        self.x, self.y = node.x, node.y

    def set_next_node(self):
        """
        Called when an entity reaches its next node
        and needs to determine its new next node.
        """
        raise NotImplementedError

    def set_speed(self, pixels: int):
        """
        Set an entity's speed (`pixels` per second)
        """
        self.px_array = self._get_px_array(pixels)
        self.px_per_sec = pixels
        self.px_index = 0

    def set_direction(self):
        if not self.is_moving():
            return
        elif self.next_node.y < self.y:
            self.direction = Direction.UP
        elif self.next_node.y > self.y:
            self.direction = Direction.DOWN
        elif self.next_node.x < self.x:
            self.direction = Direction.LEFT
        elif self.next_node.x > self.x:
            self.direction = Direction.RIGHT

    def increment_pixel_index(self):
        self.px_index = (self.px_index + 1) % len(self.px_array)

    def distance_to_entity(self, entity: 'Entity') -> float:
        return self.distance_to(entity.x, entity.y)

    def distance_to(self, x: float, y: float) -> float:
        dx, dy = self.x - x, self.y - y
        return math.sqrt(dx ** 2 + dy ** 2)

    def reverse(self):
        self.next_node, self.curr_node = \
        self.curr_node, self.next_node
        self.set_direction()

    def is_moving(self) -> bool:
        return self.next_node is not None

    def _get_px_array(self, pixels: int) -> list[int]:
        """
        Return a list with length = FPS, where arr[i]
        is how many pixels an entity will move in frame i.

        The sum of the values in the array will be equal
        to `pixels`, so `pixels` is the number of pixels
        an entity moves per second.
        """
        return self._px_per_frame_array(pixels, FPS)

    def _px_per_frame_array(self, pixels: int, frames: int) -> list[int]:
        """
        Divide `pixels` as evenly as possible in a list
        with length = `frames`.

        Ex: `pixels` = 15, `frames` = 6:
        Return [2, 3, 2, 3, 2, 3]
        """
        pos = [i * pixels // frames for i in range(frames + 1)]
        return [pos[i + 1] - pos[i] for i in range(frames)]
