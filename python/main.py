from utils import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from core import Game, GameRenderer
import pygame


pygame.init()
pygame.display.set_caption('PacMan by Nick Sciarretta')

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

game = Game()
renderer = GameRenderer(window, game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game.handle_event(event)

    clock.tick(FPS)
    game.update()
    renderer.draw()
    pygame.display.update()

pygame.quit()
