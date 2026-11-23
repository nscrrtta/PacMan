from utils.constants import *
import pygame


Colour = tuple[int, int, int]


class GameText:

    def __init__(self):
        pygame.font.init()
        half_square = SQUARE_SIZE / 2

        # Small text when PacMan eats a ghost (200)
        small_font = pygame.font.Font(FONT_FILE, SQUARE_SIZE // 2)

        # Large text (Score, Level, Paused, New Game, Ready!, Game Over!)
        large_font = pygame.font.Font(FONT_FILE, SQUARE_SIZE * 4 // 5)

        def large_text(text: str, colour: Colour, **rect_kwargs) -> Text:
            return Text(text, large_font, colour, **rect_kwargs)

        center = WINDOW_WIDTH / 2, half_square * 35 + SPACE_ABOVE
        self.ready     = large_text('Ready!',     YELLOW_TEXT_COLOUR, center=center)
        self.game_over = large_text('Game Over!', YELLOW_TEXT_COLOUR, center=center)

        center = WINDOW_WIDTH / 2, half_square * 3
        self.paused   = large_text('Paused',   WHITE_TEXT_COLOUR, center=center)
        self.new_game = large_text('New Game', WHITE_TEXT_COLOUR, center=center)

        topleft = half_square, half_square
        self.score_str = large_text('Score', WHITE_TEXT_COLOUR, topleft=topleft)

        topleft = half_square, SQUARE_SIZE * 7/4
        self.score_num = large_text('0' * 8, WHITE_TEXT_COLOUR, topleft=topleft)

        topright = WINDOW_WIDTH - half_square, half_square
        self.level_str = large_text('Level', WHITE_TEXT_COLOUR, topright=topright)

        topright = WINDOW_WIDTH - half_square, SQUARE_SIZE * 7/4
        self.level_num = large_text('001', WHITE_TEXT_COLOUR, topright=topright)

        self.ghost_bonus = Text('200', small_font, BONUS_TEXT_COLOUR)

    def update_score(self, score: int):
        self.score_num.set(f'{score:08}')

    def update_level(self, level: int):
        self.level_num.set(f'{level:03}')

    def move_ghost_bonus(self, x: float, y: float):
        self.ghost_bonus.rect.center = (x, y)


class Text:

    def __init__(self, text: str, font: pygame.font.Font, colour: Colour, **rect_kwargs):
        self.font = font
        self.colour = colour
        self.rect_kwargs = rect_kwargs
        self.text = None
        self.set(text)

    def set(self, text: str):
        if text == self.text:
            return
        self.text = text
        self.surface = self.font.render(text, True, self.colour)
        self.rect = self.surface.get_rect(**self.rect_kwargs)

    def draw(self, window: pygame.Surface):
        window.blit(self.surface, self.rect)
