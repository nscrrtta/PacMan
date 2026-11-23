from utils import Direction, FPS, SQUARE_SIZE, GHOST_OVERLAP_DISTANCE
from entities import Entity, PacMan, Ghost
from maze import maze
import random


class EntityMover:

    def __init__(self, pacman: PacMan, ghosts: list[Ghost]):
        self.pacman = pacman
        self.ghosts = ghosts

    def move_entities(self):
        # Move PacMan first, then ghosts
        self._move_entity(self.pacman)
        for ghost in self.ghosts:
            self._move_ghost(ghost)

    def oscillate_ghosts(self):
        for ghost in self.ghosts:
            self._oscillate_ghost(ghost, False)

    def _move_ghost(self, ghost: Ghost):
        if self.pacman.pellets_eaten < ghost.pellet_threshold:
            self._oscillate_ghost(ghost, False)
            return

        # Once a ghost is free to start moving, it must
        # first finish its current oscillation
        if ghost.is_oscillating:
            self._oscillate_ghost(ghost, True)
            return

        # Reduce speed of this ghost
        # if it is overlapping other ghosts
        px_offset = 0
        for other in self.ghosts:
            if self._is_trailing(ghost, other):
                px_offset -= 2

        self._move_entity(ghost, px_offset)

    def _oscillate_ghost(self, ghost: Ghost, stop_oscillating: bool):
        y_offset = abs(ghost.y - ghost.curr_node.y)

        if y_offset == 0 and stop_oscillating:
            ghost.is_oscillating = False
            ghost.set_direction()
            return

        ghost.direction = Direction.UP
        if ghost.oscillate_direction > 0:
            ghost.direction = Direction.DOWN

        if y_offset >= SQUARE_SIZE / 2:
            ghost.oscillate_direction *= -1
        ghost.y += ghost.oscillate_direction * 60 / FPS

    def _is_trailing(self, g1: Ghost, g2: Ghost) -> bool:
        """
        Return True if g1 overlaps with g2 and is trailing behind it.

        "Overlapping" means the two ghosts are alive, moving the same
        direction, and are within a certain distance to each other.
        """
        if g1 == g2:
            return False
        if g1.is_dead or g2.is_dead:
            return False
        if g1.is_scared() != g2.is_scared():
            return False
        if g1.direction != g2.direction:
            return False
        if g1.distance_to_entity(g2) > GHOST_OVERLAP_DISTANCE:
            return False

        dir = g1.direction
        if dir == Direction.UP:
            return g2.y < g1.y
        if dir == Direction.DOWN:
            return g2.y > g1.y
        if dir == Direction.LEFT:
            return g2.x < g1.x
        if dir == Direction.RIGHT:
            return g2.x > g1.x

    def _move_entity(self, entity: Entity, px_offset: int = 0):
        """
        Move an entity toward its next node (if it has one).
        The distance it moves is `px_array[px_index]` pixels.
        This method is called once per frame for each entity.
        """
        if not entity.is_moving():
            return

        # Total number of pixels the entity needs to move this frame
        px = entity.px_array[entity.px_index] + px_offset
        entity.increment_pixel_index()
        if px <= 0:
            return

        # If the entity's next node is closer than the number of
        # pixels it needs to move:

        #   1. move the entity to its next node
        #   2. determine its new next node and how many pixels are remaining
        #   3. repeat until the entity's next node is further than
        #      the number of pixels remaining
        #   4. move the remaining number of pixels toward the next node

        # This ensures the entity moves the correct number of pixels
        # this frame without skipping over any nodes

        d = self._distance_to_next_node(entity)
        while d <= px and entity.is_moving():
            self._move_toward_next_node(entity, d)
            if entity.next_node.is_portal():
                self._teleport_entity(entity)
            else:
                entity.set_next_node()
            entity.set_direction()

            px -= d
            d = self._distance_to_next_node(entity)
        self._move_toward_next_node(entity, px)

    def _distance_to_next_node(self, entity: Entity) -> int:
        if not entity.is_moving():
            return 0
        x, y = entity.next_node.x, entity.next_node.y
        return int(entity.distance_to(x, y))

    def _move_toward_next_node(self, entity: Entity, pixels: int):
        if not entity.is_moving():
            return

        dir = entity.direction
        if dir == Direction.UP:
            entity.y -= pixels
        elif dir == Direction.DOWN:
            entity.y += pixels
        elif dir == Direction.LEFT:
            entity.x -= pixels
        elif dir == Direction.RIGHT:
            entity.x += pixels

    def _teleport_entity(self, entity: Entity):
        from_ = entity.next_node

        portals = maze.portals.get(from_.portal_key)
        options = [node for node in portals if node != from_]

        to_ = random.choice(options)
        entity.move_to_node(to_)

        entity.next_node = None
        for node in to_.neighbours:
            if node is not None:
                entity.next_node = node
                break
