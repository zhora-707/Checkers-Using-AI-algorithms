import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, INFO_WIDTH
from checkers.game import Game


FPS = 60
GAMES = 10
WIN = pygame.display.set_mode((WIDTH + INFO_WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    for i in range(GAMES):
        game.start_game()
        while run:
            clock.tick(FPS)

            if game.winner():
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

            game.update()

    pygame.quit()


if __name__ == '__main__':
    main()
