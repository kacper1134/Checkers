from .checkers_pieces import *


class CheckersBoard:
    def __init__(self):
        self.board = []
        self.first_player_pieces_left = self.second_player_pieces_left = 8
        self.first_player_kings = self.second_player_kings = 0
        self.number_of_turn = 1
        self.create_pieces()

    def draw_board(self, window):
        # Draw square fields
        window.fill(USED_FIELD_COLOR)
        for row in range(NUMBER_OF_ROWS):
            for col in range(row % 2, NUMBER_OF_COLUMNS, 2):
                pg.draw.rect(window, UNUSED_FIELD_COLOR, (col * FIELD_SIZE, row * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))

        # Draw pieces
        for row in range(NUMBER_OF_ROWS):
            for column in range(NUMBER_OF_COLUMNS):
                if self.board[row][column]:
                    self.board[row][column].draw(window)

    def create_pieces(self):
        # Place second player pieces
        for row in range(NUMBER_OF_ROWS // 2 - 2):
            self.board.append([])
            for column in range(NUMBER_OF_COLUMNS):
                if row % 2 != column % 2:
                    self.board[row].append(CheckerPiece(row, column, SECOND_PLAYER_COLOR))
                else:
                    self.board[row].append(None)

        # Empty rows
        for row in range(NUMBER_OF_ROWS // 2 - 2, NUMBER_OF_ROWS // 2 + 2):
            self.board.append([])
            for column in range(NUMBER_OF_COLUMNS):
                self.board[row].append(None)

        # Place first player pieces
        for row in range(NUMBER_OF_ROWS // 2 + 2, NUMBER_OF_ROWS):
            self.board.append([])
            for column in range(NUMBER_OF_COLUMNS):
                if row % 2 != column % 2:
                    self.board[row].append(CheckerPiece(row, column, FIRST_PLAYER_COLOR))
                else:
                    self.board[row].append(None)

    def move_piece(self, piece, row, column):
        previous_row, previous_column = piece.get_row_and_column()
        piece.move(row, column)
        self.board[previous_row][previous_column] = None
        self.board[row][column] = piece

        first_player_piece_become_king = row == 0
        second_player_piece_become_king = row == NUMBER_OF_ROWS - 1

        if first_player_piece_become_king:
            self.first_player_kings += 1
            piece.become_king()
        if second_player_piece_become_king:
            self.second_player_kings += 1
            piece.become_king()

    def get_piece(self, row, column):
        return self.board[row][column]

    def get_valid_moves(self, piece):
        beaten_pieces = []
        valid_movements = self.__get_valid_movements(piece.row, piece.column, piece.direction, piece.color,
                                                     beaten_pieces)
        if valid_movements == ([], []):
            return []
        return [(movement[0][0], movement[1]) for movement in valid_movements]

    def erase_pieces(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = None

    def __get_valid_movements(self, row, column, direction, color, beaten_pieces):
        reversed_direction = self.__get_reverse_vertical_direction(direction)

        next_up_row = row + direction
        next_down_row = row + reversed_direction
        next_left_column = column + LEFT
        next_right_column = column + RIGHT

        can_move_up_left = self.__can_move_to_field(next_up_row, next_left_column)
        can_move_up_right = self.__can_move_to_field(next_up_row, next_right_column)
        can_move_down_left = self.__can_move_to_field(next_down_row, next_left_column)
        can_move_down_right = self.__can_move_to_field(next_down_row, next_right_column)

        results = []
        vertical_directions = [direction, reversed_direction]
        horizontal_directions = [LEFT, RIGHT]
        can_move = [can_move_up_left, can_move_up_right, can_move_down_left, can_move_down_right]
        next_rows = [next_up_row, next_up_row, next_down_row, next_down_row]
        next_columns = [next_left_column, next_right_column, next_left_column, next_right_column]
        index = 0

        for vertical_direction in vertical_directions:
            for horizontal_direction in horizontal_directions:
                if can_move[index]:
                    result = self.__move(next_rows[index], next_columns[index], vertical_direction,
                                         horizontal_direction, color, not beaten_pieces, direction)
                    if result:
                        row, column, beaten_piece = result
                        if beaten_piece and beaten_piece not in beaten_pieces:
                            beaten_pieces.append(beaten_piece)
                            move_result = self.__get_valid_movements(row, column, direction, color,
                                                                     beaten_pieces.copy())
                            if move_result == ([], []):
                                results.append(([(row, column)], [beaten_piece]))
                            else:
                                for r in move_result:
                                    r[1].append(beaten_piece)
                                    r[0].append((row, column))
                                    results.append(r)
                        elif not beaten_piece:
                            results.append(([(row, column)], []))
                index += 1

        if not results:
            return [], []
        return self.__get_best_results(results)

    def __get_reverse_vertical_direction(self, direction):
        return UP if direction == DOWN else DOWN

    def __move(self, row, column, vertical_direction, horizontal_direction, color, not_beat_series,
               up_direction, can_go_down=False):
        piece: CheckerPiece = self.board[row][column]
        if not piece:
            if (vertical_direction == up_direction or can_go_down) and not_beat_series:
                return row, column, None
            return None
        else:
            next_row = piece.row + vertical_direction
            next_column = piece.column + horizontal_direction

            if self.__can_beat(next_row, next_column, piece, color) and not self.board[next_row][next_column]:
                return next_row, next_column, piece

    def __get_best_results(self, results):
        maximum_number_of_beats = max(results, key=lambda result: len(result[1]))
        return [result for result in results if len(result[1]) == len(maximum_number_of_beats[1])]

    def __can_beat(self, row, column, piece, color):
        return self.__can_move_to_field(row, column) and piece.color != color

    def __can_move_to_field(self, row, column):
        return row != -1 and row != NUMBER_OF_ROWS and column != -1 and column != NUMBER_OF_COLUMNS
