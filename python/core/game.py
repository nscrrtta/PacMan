from utils import GameState, Direction, GameText, FPS, EATING_DISTANCE
from entities import Ghost, PacMan, Blinky, Clyde, Inky, Pinky
from core.ghost_controller import GhostController
from core.entity_mover import EntityMover
from maze import Pellet, maze
import pygame


class Game:

    def __init__(self):
        self.pacman = PacMan()

        blinky = Blinky(self.pacman)
        clyde = Clyde(self.pacman)
        pinky = Pinky(self.pacman)
        inky = Inky(self.pacman, blinky)

        self.ghosts: list[Ghost] = [
            blinky,
            clyde,
            pinky,
            inky
        ]

        self.entity_mover = EntityMover(self.pacman, self.ghosts)
        self.ghost_controller = GhostController(self.ghosts)
        self.text = GameText()

        self._new_game()

    def _new_game(self):
        self.pacman_lives = 5
        self.level = 0
        self._set_score(0)
        self._new_level()

    def _new_level(self):
        self.level += 1
        self.text.update_level(self.level)

        self.pacman.pellets_eaten = 0
        self.ghost_controller.new_level()

        maze.build_maze(self.level)
        self._reset()

    def _reset(self):
        for ghost in self.ghosts:
            ghost.reset()
        if self.pacman_lives > 0:
            self.pacman.reset()
            self.state = GameState.PENDING
        else:
            self.state = GameState.GAME_OVER

    def update(self):
        """Advance the game by one frame."""

        # Power pellets blink in every state
        for pellet in maze.pellets:
            pellet.update()

        if self.state == GameState.PENDING \
        or self.state == GameState.GAME_OVER:
            self.entity_mover.oscillate_ghosts()
            return

        if self.state == GameState.LEVEL_OVER:
            self.level_over_frame_counter -= 1
            if self.level_over_frame_counter == 0:
                self._new_level()
            return

        if self.state == GameState.LEVEL_RESET:
            self.pacman.update()
            if not self.pacman.dying:
                self.pacman_lives -= 1
                self._reset()
            return

        if self.state == GameState.EATING_GHOST:
            self.eating_ghost_frame_counter -= 1
            if self.eating_ghost_frame_counter == 0:
                self.state = GameState.ACTIVE
            return

        if self.state != GameState.ACTIVE:
            return

        self.pacman.update()
        self.ghost_controller.update()

        # Check for collisions with scared ghosts
        self._ghost_collisions(is_scared=True)

        # Check for collisions with pellets.
        self._pellet_collisions()

        # Game state changed if PacMan ate the last pellet.
        # If the game is still going, check for collisions
        # with ghosts that aren't scared.
        if self.state == GameState.ACTIVE:
            self._ghost_collisions(is_scared=False)

        # Game state changed if PacMan collided with a ghost
        # that isn't scared. If the game is still going,
        # move each entity.
        if self.state == GameState.ACTIVE:
            self.entity_mover.move_entities()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self._key_down(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self._mouse_down(*event.pos)

    def _key_down(self, key: int):
        if key == pygame.K_ESCAPE:
            self._toggle_paused()
            return

        # States where direction-input is accepted
        states = [GameState.PENDING, GameState.PAUSED, GameState.ACTIVE]
        if self.state not in states:
            return

        key_dict = {
            pygame.K_UP:    Direction.UP,
            pygame.K_DOWN:  Direction.DOWN,
            pygame.K_LEFT:  Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT
        }

        if key in key_dict:
            self.pacman.queue_next_direction(key_dict[key])
            if self.pacman.is_moving():
                self.state = GameState.ACTIVE

    def _mouse_down(self, x: int, y: int):
        if self.state != GameState.PAUSED:
            if self.text.new_game.rect.collidepoint(x, y):
                self._new_game()

    def _pacman_hit_ghost(self, ghost: Ghost):
        if ghost.is_scared():
            self.state = GameState.EATING_GHOST
            self.eating_ghost_frame_counter = FPS

            self.text.move_ghost_bonus(self.pacman.x, self.pacman.y)
            self._set_score(self.score + 200)

            ghost.kill()
            return

        self.pacman.dying = True
        self.state = GameState.LEVEL_RESET

    def _pacman_ate_pellet(self, pellet: Pellet):
        self.pacman.pellets_eaten += 1
        self._set_score(self.score + 10)

        maze.pellets.remove(pellet)

        if len(maze.pellets) == 0:
            self.state = GameState.LEVEL_OVER
            self.level_over_frame_counter = 4 * FPS
        elif pellet.is_power_pellet:
            for ghost in self.ghosts:
                ghost.scare()

    def _pellet_collisions(self):
        """
        Check for collisions between PacMan and a pellet.
        PacMan can only eat one pellet per frame.
        """
        for pellet in maze.pellets:
            if self._in_eating_distance(pellet.x, pellet.y):
                self._pacman_ate_pellet(pellet)
                break

    def _ghost_collisions(self, is_scared: bool):
        """
        Check for collisions between PacMan and ghosts.
        PacMan can collide with multiple ghosts per frame.
        Stop once PacMan collides with a ghost that isn't scared.
        """
        for ghost in self.ghosts:
            if ghost.is_dead or ghost.is_scared() != is_scared:
                continue
            if self._in_eating_distance(ghost.x, ghost.y):
                self._pacman_hit_ghost(ghost)
                if not is_scared:
                    break

    def _in_eating_distance(self, x: float, y: float) -> bool:
        return self.pacman.distance_to(x, y) <= EATING_DISTANCE

    def _set_score(self, score: int):
        self.score = score
        self.text.update_score(score)

    def _toggle_paused(self):
        if self.state == GameState.ACTIVE:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.ACTIVE
