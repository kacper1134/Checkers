import time

from checkers.checkers_board import CheckersBoard
from .checkers_constants import *


class CheckersGame:
    def __init__(self):
        self.__initialize_game()

    def update(self, window):
        self.board.draw_board(window)
        self.__draw_valid_moves(window)
        self.__draw_beaten_pieces(window)
        pg.display.update()

    def reset(self):
        time.sleep(1)
        self.__initialize_game()

    def select(self, row, column):
        if self.selected_piece:
            correct_move = self.__move_piece(row, column)

            if correct_move:
                self.current_turn = self.__get_next_turn()
                self.board.erase_pieces(self.beaten_pieces[self.selected_piece][(row, column)])
                self.selected_piece = None
                self.__calculate_valid_moves()
            else:
                self.selected_piece = None
                self.select(row, column)
        else:
            piece = self.board.get_piece(row, column)
            if piece and piece.color == self.current_turn:
                self.selected_piece = piece

    def get_status(self):
        king_tie_result = self.board.turn_of_first_king and self.board.number_of_turn - \
                          self.board.turn_of_first_king == 15
        if king_tie_result:
            return TIE

        if self.board.second_player_pieces_left == 0 or self.no_valid_moves and self.current_turn == SECOND_PLAYER_COLOR:
            return FIRST_PLAYER_WIN

        if self.board.first_player_pieces_left == 0 or self.no_valid_moves and self.current_turn == FIRST_PLAYER_COLOR:
            return SECOND_PLAYER_WIN

        return NOT_OVER

    def get_valid_moves(self):
        return self.valid_moves

    def get_all_pieces(self, color):
        pieces = set()
        for piece in self.valid_moves.keys():
            not_dead = any(piece in row for row in self.board.board)
            if piece.color == color and self.valid_moves[piece] and not_dead:
                pieces.add(piece)
        return pieces

    def computer_move_piece(self, row, column, piece):
        self.selected_piece = self.board.get_piece(piece.row, piece.column)
        self.__move_piece(row, column)
        self.current_turn = self.__get_next_turn()
        self.board.erase_pieces(self.beaten_pieces[self.selected_piece][(row, column)])
        self.selected_piece = None
        self.__calculate_valid_moves()

    def get_score_based_on_pieces_value(self, color):
        first_player_score = (self.board.first_player_pieces_left - self.board.first_player_kings) + \
                             self.board.first_player_kings * KING_VALUE
        second_player_score = (self.board.second_player_pieces_left - self.board.second_player_kings) + self.board.\
            second_player_kings * KING_VALUE
        if color == FIRST_PLAYER_COLOR:
            return first_player_score - second_player_score
        else:
            return second_player_score - first_player_score

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
        self.beaten_pieces = {piece: {} for row in self.board.board for piece in row if piece}
        self.no_valid_moves = True
        self.__calculate_valid_moves()

    def __calculate_valid_moves(self):
        self.no_valid_moves = True
        for row in self.board.board:
            for piece in row:
                if piece and piece.color == self.current_turn:
                    valid_moves = self.board.get_valid_moves(piece)
                    if valid_moves:
                        self.no_valid_moves = False

                    self.valid_moves[piece] = {valid_move[0] for valid_move in valid_moves}
                    self.beaten_pieces[piece]["all"] = {piece for valid_move in valid_moves
                                                        for piece in valid_move[1] if valid_move[1]}
                    for move in self.valid_moves[piece]:
                        self.beaten_pieces[piece][move] = {piece for valid_move in valid_moves
                                                           for piece in valid_move[1] if valid_move[1]
                                                           and valid_move[0] == move}

        self.__leave_only_best_moves()

    def __leave_only_best_moves(self):
        pieces = [piece for row in self.board.board for piece in row if piece and piece.color == self.current_turn]

        best_piece = (None, -1)
        for piece in pieces:
            for move in self.valid_moves[piece]:
                current_piece = (piece, len(self.beaten_pieces[piece][move]))
                if best_piece[1] < current_piece[1]:
                    best_piece = current_piece

        for piece in pieces:
            copy_valid_moves = self.valid_moves[piece].copy()
            for move in self.valid_moves[piece]:
                current_piece = (piece, len(self.beaten_pieces[piece][move]))
                if current_piece[1] != best_piece[1]:
                    copy_valid_moves.remove(move)
            self.valid_moves[piece] = copy_valid_moves

    def __draw_valid_moves(self, window):
        if self.selected_piece:
            for move in self.valid_moves[self.selected_piece]:
                x = move[1] * FIELD_SIZE + FIELD_SIZE // 2
                y = move[0] * FIELD_SIZE + FIELD_SIZE // 2
                pg.draw.circle(window, AVAILABLE_NEXT_MOVE_COLOR, (x, y), FIELD_SIZE // 4)

    def __draw_beaten_pieces(self, window):
        if self.selected_piece:
            for move in self.valid_moves[self.selected_piece]:
                for piece in self.beaten_pieces[self.selected_piece][move]:
                    x = piece.column * FIELD_SIZE + FIELD_SIZE // 2
                    y = piece.row * FIELD_SIZE + FIELD_SIZE // 2
                    pg.draw.circle(window, BEATEN_PIECE_COLOR, (x, y), FIELD_SIZE // 4 - PIECE_PADDING // 2)

    def __get_next_turn(self):
        return FIRST_PLAYER_COLOR if self.current_turn == SECOND_PLAYER_COLOR else SECOND_PLAYER_COLOR
