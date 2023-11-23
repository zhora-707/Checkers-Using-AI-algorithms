import copy
import math
import time
import pygame
from .constants import *
from checkers.board import Board


class Game:
    # def __init__(self, win, mode='pvp'):
    #     self.win = win
    #     self.mode = mode
    def __init__(self, win, mode='ivi', algorithm_player_one='min-max', algorithm_player_two='min-max'):
        self.win = win
        self.mode = mode
        self.algorithm_player_one = algorithm_player_one
        self.algorithm_player_two = algorithm_player_two
        self.num_simulations = 1000
        self.max_depth = 3  # Set the maximum depth for iterative deepening

    def start_game(self, evaluation_functions=1, depth=3, algorithm='min-max', player_color=WHITE):
        self._init()
        self.heur_num = evaluation_functions
        self.depth = depth
        self.algorithm = algorithm
        self.player_one_color = player_color
        self.update()
        self._playmode()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.move_length = 0
        self.moves_to_draw = 15
        self.moves_number = 1

    def _playmode(self):
        match self.mode:
            case 'pvp':
                return
            case 'ivi':
                self._ivi()
            case 'pvi':
                self._pvi()

    def _ivi(self):
        if self.winner():
            return

        if self.turn == WHITE:
            algorithm = self.algorithm_player_one
        else:
            algorithm = self.algorithm_player_two

        if algorithm == 'min-max':
            _, (self.selected, move, to_skip) = self.board.minmax(self.turn,
                                                                  self.board.get_longest_move(self.turn),
                                                                  self.depth,
                                                                  self.heur_num)
        elif algorithm == 'alpha-beta':
            _, (self.selected, move, to_skip) = self.board.alpha_beta(self.turn,
                                                                      self.board.get_longest_move(self.turn),
                                                                      self.depth,
                                                                      -math.inf,
                                                                      math.inf,
                                                                      self.heur_num)
        elif algorithm == 'depth-limited':
            _, (self.selected, move, to_skip) = self.board.depth_limited_search(self.turn,
                                                                              self.board.get_longest_move(self.turn),
                                                                              self.depth,
                                                                              self.heur_num)


        # elif algorithm == 'monte-carlo':
        #     _, (self.selected, move, to_skip) = self.board.monte_carlo(
        #         self.turn, self.board.get_longest_move(self.turn), self.num_simulations)
        if move:
            self._moveAI(move[0], move[1], to_skip)

    def _pvi(self):
        if self.turn == self.player_one_color:
            return
        else:
            self._ivi()

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def winner(self):
        if self.moves_to_draw == 0:
            print(f'{DRAW} in {self.moves_number} moves')
            return True
        winner = self.board.winner(self.turn)
        if winner:
            if winner == WHITE:
                print(f'WHITE won in {self.moves_number} moves')
            else:
                print(f'RED won in {self.moves_number} moves')
            return True
        return False

    def reset(self):
        self.start_game(self.heur_num, self.depth, self.algorithm)

    def select(self, row, col):
        if col >= COLS:
            return False

        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, self.move_length)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            st, en = self.board.move(self.selected, row, col)
            com = '-'
            skipped = self.valid_moves[(row, col)]
            if skipped:
                com = 'x' * len(skipped)
                self.board.remove(skipped)
            if self.selected.king:
                self.moves_to_draw -= 1
            else:
                self.moves_to_draw = 15
            self.board.update_notation(f'{st} {com} {en}')
            self.change_turn()
            return True

        return False

    def _moveAI(self, row, col, skipped):
        st, en = self.board.move(self.selected, row, col)
        com = '-'
        if skipped:
            com = 'x' * len(skipped)
            self.board.remove(skipped)
        if self.selected.king:
            self.moves_to_draw -= 1
        else:
            self.moves_to_draw = 15
        self.board.update_notation(f'{st} {com} {en}')
        self.change_turn()


    def change_turn(self):
        self.valid_moves = {}
        self.update()
        if self.turn == RED:
            self.moves_number += 1
            self.turn = WHITE
            self.move_length = self.board.get_longest_move(WHITE)
        else:
            self.turn = RED
            self.move_length = self.board.get_longest_move(RED)
        self._playmode()