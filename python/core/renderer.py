from entities import Ghost, PacMan
from maze import Borders, maze
from core.game import Game
from utils import *
import pygame
import math


# Angle PacMan's mouth faces, for each direction
mouth_angles = {
    Direction.UP:    270,
    Direction.DOWN:  90,
    Direction.LEFT:  180,
    Direction.RIGHT: 0
}


class GameRenderer:

    def __init__(self, window: pygame.Surface, game: Game):
        self.window = window
        self.game = game

        # When alive/dead, a ghost's eyes point in the
        # direction they are moving. When scared, the
        # image is the same regardless of direction.
        self.scared_image = self._load_image('scared_ghost')
        self.dead_images  = self._load_image_dict('eyes')
        self.alive_images = {
            ghost.name: self._load_image_dict(ghost.name)
            for ghost in game.ghosts
        }

    def draw(self):
        self.window.fill(BG_COLOUR)

        self._draw_borders(maze.borders)

        for pellet in maze.pellets:
            if pellet.visible:
                center = (pellet.x, pellet.y)
                pygame.draw.circle(self.window, PELLET_COLOUR, center, pellet.radius)
        for ghost in self.game.ghosts:
            self._draw_ghost(ghost)
        self._draw_pacman(self.game.pacman)

        self._draw_text()

        for i in range(self.game.pacman_lives):
            self._draw_life(i)

    def _draw_borders(self, borders: Borders):
        colour = borders.colour

        # Maze flashes at the end of a level
        if self.game.state == GameState.LEVEL_OVER:
            i = self.game.level_over_frame_counter % FPS
            if i >= FPS / 2:
                colour = FLASH_COLOUR

        for edge in borders.edges:
            edge_colour = GATE_COLOUR if edge.gate else colour
            pygame.draw.rect(self.window, edge_colour, edge.rect)
        for corner in borders.corners:
            pygame.draw.arc(self.window, colour, corner.rect, corner.start_angle, corner.end_angle)

    def _draw_ghost(self, ghost: Ghost):
        image = self.alive_images[ghost.name][ghost.direction]
        if ghost.is_scared():
            use_scared_image = True
            if ghost.scared_timer < FPS:
                # Flash when nearing end of scared state
                use_scared_image = ghost.scared_timer % 4 > 0
            if use_scared_image:
                image = self.scared_image
        elif ghost.is_dead:
            image = self.dead_images[ghost.direction]
        rect = image.get_rect(center=(ghost.x, ghost.y))
        self.window.blit(image, rect)

    def _draw_pacman(self, pacman: PacMan):
        x, y = pacman.x, pacman.y

        # If alive but not moving, draw full circle
        if not pacman.dying and not pacman.is_moving():
            pygame.draw.circle(self.window, PACMAN_COLOUR, (x, y), PACMAN_RADIUS)
            return

        # Draw with mouth open, depending on direction facing
        a = mouth_angles[pacman.direction]
        start_angle = int(a + pacman.mouth_angle // 2)
        end_angle = int(a - pacman.mouth_angle // 2 + 360)
        self._draw_wedge(x, y, PACMAN_RADIUS, start_angle, end_angle)

    def _draw_life(self, i: int):
        radius = SQUARE_SIZE * 3 // 5
        x = SQUARE_SIZE * (1.5 * i + 1)
        y = WINDOW_HEIGHT - SQUARE_SIZE * 5/4
        self._draw_wedge(x, y, radius, 225, 495)

    def _draw_wedge(self, x: float, y: float, radius: int, start_angle: int, end_angle: int):
        for angle in range(start_angle, end_angle):
            rad = (angle % 360) * math.pi / 180
            for r in range(radius + 1):
                px = int(x + r * math.cos(rad))
                py = int(y + r * math.sin(rad))
                self.window.set_at((px, py), PACMAN_COLOUR)

    def _draw_text(self):
        text = self.game.text
        state = self.game.state

        if state == GameState.PAUSED:
            text.paused.draw(self.window)
        else:
            text.new_game.draw(self.window)

        if state == GameState.GAME_OVER:
            if not self.game.pacman.dying:
                text.game_over.draw(self.window)
        elif state == GameState.EATING_GHOST:
            text.ghost_bonus.draw(self.window)
        elif state == GameState.PENDING:
            text.ready.draw(self.window)

        text.score_str.draw(self.window)
        text.score_num.draw(self.window)
        text.level_str.draw(self.window)
        text.level_num.draw(self.window)

    def _load_image_dict(self, name: str) -> dict[Direction, pygame.Surface]:
        return {
            Direction.UP:    self._load_image(f'{name}_U'),
            Direction.DOWN:  self._load_image(f'{name}_D'),
            Direction.LEFT:  self._load_image(f'{name}_L'),
            Direction.RIGHT: self._load_image(f'{name}_R')
        }

    def _load_image(self, file_name: str) -> pygame.Surface:
        image = pygame.image.load(IMAGES_DIR / f'{file_name}.png')
        return pygame.transform.scale_by(image, SQUARE_SIZE / IMAGE_SQUARE_SIZE)
