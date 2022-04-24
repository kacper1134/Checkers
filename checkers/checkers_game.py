from checkers.checkers_board import CheckersBoard
from .checkers_constants import *


class CheckersGame:
    def __init__(self, window):
        self.__initialize_game()
        self.window = window

    def update(self):
        self.board.draw_board(self.window)
        self.__draw_valid_moves()
        pg.display.update()

    def reset(self):
        self.__initialize_game()

    def select(self, row, column):
        if self.selected_piece:
            correct_move = self.__move_piece(row, column)
            self.selected_piece = None
            if correct_move:
                self.current_turn = self.__get_next_turn()
                self.__calculate_valid_moves()
            else:
                self.select(row, column)
        else:
            piece = self.board.get_piece(row, column)
            if piece and piece.color == self.current_turn:
                self.selected_piece = piece

    def __move_piece(self, row, column):
        piece = self.board.get_piece(row, column)
        correct_move = not piece and (row, column) in self.valid_moves[self.selected_piece]
        if correct_move:
            self.board.move_piece(self.selected_piece, row, column)
        return correct_move

    def __initialize_game(self):
        self.selected_piece = None
        self.board = CheckersBoard()
        self.current_turn = FIRST_PLAYER_COLOR
        self.valid_moves = {}
        self.__calculate_valid_moves()

    def __calculate_valid_moves(self):
        for row in self.board.board:
            for piece in row:
                if piece and piece.color == self.current_turn:
                    self.valid_moves[piece] = self.board.get_valid_moves(piece)

    def __draw_valid_moves(self):
        if self.selected_piece:
            for move in self.valid_moves[self.selected_piece]:
                x = move[1] * FIELD_SIZE + FIELD_SIZE // 2
                y = move[0] * FIELD_SIZE + FIELD_SIZE // 2
                pg.draw.circle(self.window, AVAILABLE_NEXT_MOVE_COLOR, (x, y), FIELD_SIZE // 4)

    def __get_next_turn(self):
        return FIRST_PLAYER_COLOR if self.current_turn == SECOND_PLAYER_COLOR else SECOND_PLAYER_COLOR