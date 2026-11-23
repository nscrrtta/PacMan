from utils import GhostState, FPS, STANDARD_SPEED, SCARED_SPEED, DEAD_SPEED
from entities.entity import Entity
from entities.pacman import PacMan
from maze import Node, maze
import random


class Ghost(Entity):

    def __init__(self, pacman: PacMan, name: str):
        super().__init__()
        self.pacman = pacman

        # Each ghost has a different pellet threshold
        self.pellet_threshold = 0

        # Used to pick this ghost's images (e.g. pngs/blinky_U.png)
        self.name = name

        self.state = GhostState.SCATTER

    def reset(self, start_node: Node):
        # Set to True once a ghost leaves home for the first time.
        # Blinky is the exception (starts outside the ghost home).
        self.left_home = start_node == maze.ghost_home_entrance

        self.revive()

        # Ghosts oscillate up/down until:
        # 1. PacMan has started moving, and
        # 2. PacMan eats enough pellets
        #
        # This is the y-direction they are currently moving in.
        # (Switches back and forth between 1 and -1).
        self.oscillate_direction = 1
        self.is_oscillating = True

        self.next_node = self._get_next_node(start_node, None)
        super().reset(start_node)

    def kill(self):
        """
        Called when PacMan has eaten this ghost.
        """
        self.set_speed(DEAD_SPEED)
        self.scared_timer = 0
        self.is_dead = True

    def revive(self):
        """
        Called when a dead ghost reaches the ghost home,
        when the scared timer runs out, or when the level resets.
        """
        self.set_speed(STANDARD_SPEED)
        self.scared_timer = 0
        self.is_dead = False

    def scare(self):
        """
        Called when PacMan eats a power pellet.
        Slow down speed, set 10 second timer,
        and reverse direction.
        """
        if self.is_dead or self._in_ghost_home():
            return
        self.set_speed(SCARED_SPEED)
        self.scared_timer = 10 * FPS
        self.reverse()

    def is_scared(self) -> bool:
        return self.scared_timer > 0 and not self.is_dead

    def set_next_node(self):
        self.next_node = self._get_next_node(self.next_node, self.curr_node)

    def _get_next_node(self, ref_node: Node, prev_node: Node | None) -> Node | None:
        self.curr_node = ref_node

        if ref_node == maze.ghost_home_center:
            self.revive()
            self.left_home = True
            return maze.ghost_home_entrance

        options: list[Node] = []
        for node in ref_node.neighbours:
            # Rules:
            # 1. Can only move to ghost_home_center
            #    if dead, or never left ghost home.
            # 2. Cannot return to previous node
            if node == maze.ghost_home_center:
                if self.is_dead or not self.left_home:
                    return node
            elif node is not None and node != prev_node:
                options.append(node)

        # If at a dead end, reverse direction
        if not options:
            return prev_node

        if self.is_scared():
            return random.choice(options)

        target = maze.ghost_home_center
        if not self.is_dead:
            target = self._get_target_node()

        # Find the closest node to <target>
        min_distance = float('inf')
        closest_node: Node | None = None
        for node in options:
            dx = node.x - target.x
            dy = node.y - target.y
            distance = dx**2 + dy**2
            if distance < min_distance:
                min_distance = distance
                closest_node = node

        return closest_node

    def _in_ghost_home(self) -> bool:
        at_home = self.curr_node == maze.ghost_home_center
        return at_home or not self.left_home

    def _get_target_node(self) -> Node:
        """
        Return the node this ghost is heading toward.
        Each ghost subclass must override this.
        """
        raise NotImplementedError
