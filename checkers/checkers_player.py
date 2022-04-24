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
        pieces = []

        for piece in valid_moves.keys():
            not_dead = any(piece in row for row in self.game.board.board)
            if piece.color == self.color and valid_moves[piece] and not_dead:
                pieces.append(piece)

        piece = random.choice(pieces)

        move = random.choice(list(valid_moves[piece]))
        self.game.computer_move_piece(move[0], move[1], piece)
        time.sleep(0.3)

        return True
