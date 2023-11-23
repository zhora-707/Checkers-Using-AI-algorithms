import time
import pygame
from checkers.constants import WIDTH, HEIGHT, INFO_WIDTH
from checkers.game import Game

FPS = 60
GAMES = 30 # specify number of games you want the bot to play
WIN = pygame.display.set_mode((WIDTH + INFO_WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def main():

    for game_num in range(1, GAMES + 1):
        game = Game(WIN, mode='ivi', algorithm_player_one='alpha-beta', algorithm_player_two='depth-limited') # player 1 is white always
        game.start_game(1, 4)

    pygame.quit()

if __name__ == '__main__':
    main()
