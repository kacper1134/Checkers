import copy
import time

from .checkers_constants import *
import random


def get_row_and_column_from_mouse_position(position):
    x, y = position
    return y // FIELD_SIZE, x // FIELD_SIZE


class HumanPlayer:
    def __init__(self, color, game):
        self.color = color
        self.game = game

    def make_move(self):
        # Event loop
        for event in pg.event.get():
            # Quiting game event
            if event.type == pg.QUIT:
                return False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                row, column = get_row_and_column_from_mouse_position(mouse_position)
                self.game.select(row, column)
        return True


class RandomPlayer:
    def __init__(self, color, game):
        self.color = color
        self.game = game

    def make_move(self):
        valid_moves = self.game.get_valid_moves()
        pieces = self.game.get_all_pieces(self.color)

        if not pieces:
            return True

        piece = random.choice(list(pieces))

        move = random.choice(list(valid_moves[piece]))
        self.game.computer_move_piece(move[0], move[1], piece)
        time.sleep(0.5)

        return True


class MiniMaxPlayer:
    def __init__(self, color, game, maximum_number_of_moves_ahead):
        self.game = game
        self.color = color
        self.visited_nodes = 0
        self.maximum_number_of_moves_ahead = maximum_number_of_moves_ahead

    def make_move(self):
        self.visited_nodes = 0
        best_move = self.__get_best_move(copy.deepcopy(self.game), 0, None, None)
        self.game.computer_move_piece(best_move[0][0], best_move[0][1], best_move[2])
        print(f"Visited {self.visited_nodes} nodes")

        return True

    def __get_best_move(self, local_game, level, move, piece, alpha=MINUS_INFINITY, beta=PLUS_INFINITY):
        self.visited_nodes += 1
        # Make a move
        if move:
            local_game.computer_move_piece(move[0], move[1], piece)

        # Game ends or tree height is at its maximum
        if local_game.get_status() != NOT_OVER or level > self.maximum_number_of_moves_ahead:
            return move, local_game.get_score_based_on_pieces_value(self.color), piece

        pieces = local_game.get_all_pieces(local_game.current_turn)
        valid_moves = local_game.get_valid_moves()

        # Player turn - try to maximize result
        if local_game.current_turn == self.color:
            best_move = (None, MINUS_INFINITY, None)

            for piece in pieces:
                for move in valid_moves[piece]:
                    current_move = self.__get_best_move(copy.deepcopy(local_game), level + 1, move, piece, alpha, beta)
                    if current_move[1] > best_move[1]:
                        best_move = (move, current_move[1], piece)

                        if best_move[1] > alpha:
                            alpha = current_move[1]

                        if alpha >= beta:
                            return best_move

            return best_move

        # Another Player turn - try to minimize result
        else:
            best_move = (None, PLUS_INFINITY, None)

            for piece in pieces:
                for move in valid_moves[piece]:
                    current_move = self.__get_best_move(copy.deepcopy(local_game), level + 1, move, piece, alpha, beta)
                    if current_move[1] < best_move[1]:
                        best_move = (move, current_move[1], piece)

                        if best_move[1] < beta:
                            beta = current_move[1]

                        if alpha >= beta:
                            return best_move

            return best_move
