import math
from random import random
import pickle
from .constants import *
from .piece import Piece
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.can_move = True
        self.notation = []
        self.skipped_notation_moves = 1

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range((row + 1) % 2, COLS, 2):
                pygame.draw.rect(win, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                number = NUMBER_FONT.render(str(FIELD_NUMBERS[col][row]), True, WHITE)
                win.blit(number, ((row + 0.75) * SQUARE_SIZE, (col + 0.75) * SQUARE_SIZE))

    def draw_skeleton(self, win):
        win.fill(WHITE)
        pygame.draw.line(win, BLACK, (0, 0), (WIDTH + INFO_WIDTH, 0), 2)
        pygame.draw.line(win, BLACK, (0, 0), (0, HEIGHT), 2)
        pygame.draw.line(win, BLACK, (0, HEIGHT - 2), (WIDTH + INFO_WIDTH, HEIGHT - 2), 2)
        pygame.draw.line(win, BLACK, (WIDTH - 2, 0), (WIDTH - 2, HEIGHT), 2)
        pygame.draw.rect(win, WHITE, (WIDTH, 2, INFO_WIDTH - 2, HEIGHT - 4))

    def draw_notation(self, win):
        notation = NOTATION_FONT.render('Notation', True, BLACK)
        win.blit(notation, (WIDTH + 20, 10))

        for i, move in enumerate(self.notation):
            if i % 2 == 0:
                move_number = NOTATION_FONT.render(str(i // 2 + self.skipped_notation_moves) + '.', True, BLACK)
                win.blit(move_number, (WIDTH + 20, 30 + (i // 2) * 20))

                white_move = NOTATION_FONT.render(move, True, BLACK)
                win.blit(white_move, (WIDTH + 45, 30 + (i // 2) * 20))
            else:
                red_move = NOTATION_FONT.render(move, True, BLACK)
                win.blit(red_move, (WIDTH + 155, 30 + (i // 2) * 20))

    def draw(self, win):
        self.draw_skeleton(win)
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        self.draw_notation(win)

    def move(self, piece, row, col):
        st = FIELD_NUMBERS[piece.row][piece.col]
        en = FIELD_NUMBERS[row][col]
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        self.board[row][col].move(row, col)

        if row == ROWS - 1 and self.board[row][col].color == RED:
            self.board[row][col].make_king()
            self.red_kings += 1
        if row == 0 and self.board[row][col].color == WHITE:
            self.board[row][col].make_king()
            self.white_kings += 1
        return st, en

    def update_notation(self, move):
        self.notation.append(move)
        if len(self.notation) >= 72:
            self.notation = self.notation[2:]
            self.skipped_notation_moves += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_pieces(self, turn):
        pieces = []
        for row in self.board:
            for tile in row:
                if tile == 0:
                    continue
                if tile.color == turn:
                    pieces.append(tile)
        return pieces

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self, turn):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        if not self.can_move:
            if turn == WHITE:
                return RED
            else:
                return WHITE

        return None

    def get_valid_moves(self, piece, length=None):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.king:
            moves.update(self._traverse_left_king(row - 1, -1, -1, piece.color, left))
            moves.update(self._traverse_left_king(row + 1, ROWS, 1, piece.color, left))
            moves.update(self._traverse_right_king(row - 1, -1, -1, piece.color, right))
            moves.update(self._traverse_right_king(row + 1, ROWS, 1, piece.color, right))
        else:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left,
                                             True if piece.color == WHITE else False))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left,
                                             False if piece.color == WHITE else True))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right,
                                              True if piece.color == WHITE else False))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right,
                                              False if piece.color == WHITE else True))

        if length:
            correct_moves = {}
            for key, value in moves.items():
                if len(value) == length:
                    correct_moves[key] = value
            moves = correct_moves
        return moves

    def _traverse_left(self, start, stop, step, color, left, forward, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                elif forward:
                    moves[(r, left)] = last
                elif not forward and r != start:
                    moves[(r, left)] = last

                if last:
                    last += skipped
                    if step == -1:
                        row = max(r - 3, -1)
                        opposite = min(r + 3, ROWS)
                    else:
                        row = min(r + 3, ROWS)
                        opposite = max(r - 3, -1)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, forward, skipped=last))
                    moves.update(
                        self._traverse_left(r - step, opposite, -step, color, left - 1, not forward, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, forward, skipped=last))
                break
            elif current.color == color:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, forward, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                elif forward:
                    moves[(r, right)] = last
                elif not forward and r != start:
                    moves[(r, right)] = last

                if last:
                    last += skipped
                    if step == -1:
                        row = max(r - 3, -1)
                        opposite = min(r + 3, ROWS)
                    else:
                        row = min(r + 3, ROWS)
                        opposite = max(r - 3, -1)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, forward, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, forward, skipped=last))
                    moves.update(
                        self._traverse_right(r - step, opposite, -step, color, right + 1, not forward, skipped=last))
                break
            elif current.color == color:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            right += 1

        return moves

    def _traverse_left_king(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    continue
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    last += skipped
                    moves.update(
                        self._traverse_left_king(r - step, ROWS - stop - 1, -step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right_king(r + step, stop, step, color, left + 1, skipped=last))
            elif current.color == color or last:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            left -= 1

        return moves

    def _traverse_right_king(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= ROWS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    continue
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    last += skipped
                    moves.update(self._traverse_left_king(r + step, stop, step, color, right - 1, skipped=last))
                    moves.update(
                        self._traverse_right_king(r - step, ROWS - stop - 1, -step, color, right + 1, skipped=last))
            elif current.color == color or last:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            right += 1

        return moves

    def get_longest_move(self, color):
        longest = -1
        for row in self.board:
            for tile in row:
                if tile == 0:
                    continue
                if tile.color == color:
                    moves = self.get_valid_moves(tile)
                    if moves:
                        moves = dict(sorted(moves.items(), key=lambda k: len(k[1]), reverse=True))
                        longest_local = len(list(moves.values())[0])
                        if longest_local > longest:
                            longest = longest_local
        if longest == -1:
            self.can_move = False
        return longest

    def three_stage_function(self):
        if self.red_left + self.white_left > 19:
            EVALUATION_POINTS = OPENING_VALUES
        elif self.red_left + self.white_left > 8:
            EVALUATION_POINTS = MID_GAME_VALUES
        else:
            EVALUATION_POINTS = ENDGAME_VALUES

        evaluation = 0
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece != 0:
                    is_white = piece.color == WHITE
                    if not piece.king:
                        evaluation += EVALUATION_POINTS[i][j] if is_white else -EVALUATION_POINTS[-i - 1][-j - 1]
                    else:
                        evaluation += KING_VALUES[i][j] if is_white else -KING_VALUES[-i - 1][-j - 1]
        return round(evaluation, 2)

    def edge_function(self):
        evaluation = 0

        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece == 0:
                    continue
                is_white = piece.color == WHITE
                if not piece.king:
                    evaluation += EDGE_VALUES[i][j] if is_white else -EDGE_VALUES[-i - 1][-j - 1]
                else:
                    evaluation += KING_VALUES[i][j] if is_white else -KING_VALUES[-i - 1][-j - 1]
        return round(evaluation, 2)

    def minmax(self, turn, move_length, depth, evaluation_functions='1'):
        opposite = RED if turn == WHITE else WHITE
        best_val = -math.inf if turn == WHITE else math.inf
        best_move = None

        if depth == 0 or self.winner(turn):
            match evaluation_functions:
                case 1:
                    return self.three_stage_function(), None
                case 2:
                    return self.edge_function(), None
            return None, None

        for piece in self.get_pieces(turn):
            l_moves = self.get_valid_moves(piece, move_length)

            for move, skipped in l_moves.items():
                board = pickle.loads(pickle.dumps(self))
                board.move(piece, move[0], move[1])
                if skipped:
                    board.remove(skipped)
                eval, _ = board.minmax(opposite, board.get_longest_move(opposite), depth - 1, evaluation_functions)
                if turn == WHITE:
                    if eval > best_val:
                        best_val = eval
                        best_move = (piece, move, skipped)
                    elif eval == best_val:
                        if not best_move or (best_move and random() < 0.5):
                            best_val = eval
                            best_move = (piece, move, skipped)
                else:
                    if eval < best_val:
                        best_val = eval
                        best_move = (piece, move, skipped)
                    elif eval == best_val:
                        if not best_move or (best_move and random() < 0.5):
                            best_val = eval
                            best_move = (piece, move, skipped)
        return best_val, best_move

    def alpha_beta(self, turn, move_length, depth, alpha, beta, evaluation_functions='1'):
        opposite = RED if turn == WHITE else WHITE
        best_val = -math.inf if turn == WHITE else math.inf
        best_move = None

        if depth == 0 or self.winner(turn):
            match evaluation_functions:
                case 1:
                    return self.three_stage_function(), None
                case 2:
                    return self.edge_function(), None
            return None, None

        for piece in self.get_pieces(turn):
            l_moves = self.get_valid_moves(piece, move_length)

            for move, skipped in l_moves.items():
                board = pickle.loads(pickle.dumps(self))
                board.move(piece, move[0], move[1])
                if skipped:
                    board.remove(skipped)
                eval, _ = board.alpha_beta(opposite, board.get_longest_move(opposite), depth - 1, alpha, beta, evaluation_functions)

                if turn == WHITE:
                    if eval > best_val:
                        best_val = eval
                        best_move = (piece, move, skipped)
                    elif eval == best_val:
                        if not best_move or (best_move and random() < 0.5):
                            best_val = eval
                            best_move = (piece, move, skipped)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                else:
                    if eval < best_val:
                        best_val = eval
                        best_move = (piece, move, skipped)
                    elif eval == best_val:
                        if not best_move or (best_move and random() < 0.5):
                            best_val = eval
                            best_move = (piece, move, skipped)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return best_val, best_move

    def depth_limited_search(self, turn, move_length, depth, evaluation_functions='1'):
        opposite = RED if turn == WHITE else WHITE
        best_val = -math.inf if turn == WHITE else math.inf
        best_move = None

        if depth == 0 or self.winner(turn):
            match evaluation_functions:
                case 1:
                    return self.three_stage_function(), None
                case 2:
                    return self.edge_function(), None
            return None, None

        for piece in self.get_pieces(turn):
            l_moves = self.get_valid_moves(piece, move_length)

            for move, skipped in l_moves.items():
                board = pickle.loads(pickle.dumps(self))
                board.move(piece, move[0], move[1])
                if skipped:
                    board.remove(skipped)

                eval, _ = board.depth_limited_search(opposite, board.get_longest_move(opposite), depth - 1, evaluation_functions)

                if turn == WHITE and eval > best_val:
                    best_val = eval
                    best_move = (piece, move, skipped)
                elif turn == RED and eval < best_val:
                    best_val = eval
                    best_move = (piece, move, skipped)
                elif eval == best_val and random() < 0.5:
                    best_val = eval
                    best_move = (piece, move, skipped)
        return best_val, best_move


    # def monte_carlo(self, turn, move_length, num_simulations=1000):
    #     best_val = -math.inf if turn == WHITE else math.inf
    #     best_move = None
    #
    #     for piece in self.get_pieces(turn):
    #         l_moves = self.get_valid_moves(piece, move_length)
    #
    #         for move, skipped in l_moves.items():
    #             total_score = 0
    #
    #             for _ in range(num_simulations):
    #                 board = pickle.loads(pickle.dumps(self))
    #                 board.move(piece, move[0], move[1])
    #                 if skipped:
    #                     board.remove(skipped)
    #
    #                 score = board.simulate_random_games(turn, move_length)
    #                 total_score += score
    #
    #             avg_score = total_score / num_simulations
    #
    #             if turn == WHITE:
    #                 if avg_score > best_val:
    #                     best_val = avg_score
    #                     best_move = (piece, move, skipped)
    #             else:
    #                 if avg_score < best_val:
    #                     best_val = avg_score
    #                     best_move = (piece, move, skipped)
    #
    #     return best_val, best_move
    #
    # def simulate_random_games(self, turn, move_length):
    #     total_score = 0
    #
    #     for _ in range(move_length):
    #         winner = self.play_random_game(turn)
    #         if winner == turn:
    #             total_score += 1
    #
    #     return total_score
    #
    # def play_random_game(self, turn):
    #     current_turn = turn
    #
    #     while not self.winner(current_turn):
    #         pieces = self.get_pieces(current_turn)
    #         piece = random.choice(pieces) if pieces else None
    #
    #         if piece:
    #             valid_moves = self.get_valid_moves(piece)
    #             if valid_moves:
    #                 move, skipped = random.choice(list(valid_moves.items()))
    #
    #                 self.move(piece, move[0], move[1])
    #                 if skipped:
    #                     self.remove(skipped)
    #             else:
    #                 # If no valid moves, switch to the other player's turn
    #                 current_turn = RED if current_turn == WHITE else WHITE
    #         else:
    #             # If no pieces left for the current player, switch to the other player's turn
    #             current_turn = RED if current_turn == WHITE else WHITE
    #
    #     return current_turn

    def __str__(self):
        for row in self.board:
            for tile in row:
                if tile == 0:
                    print('-', end=' ')
                elif tile.color == WHITE:
                    print('w', end=' ')
                elif tile.color == RED:
                    print('r', end=' ')
            print()
        print()