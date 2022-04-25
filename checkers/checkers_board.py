from .checkers_pieces import *


class CheckersBoard:
    def __init__(self):
        self.board = []
        self.first_player_pieces_left = self.second_player_pieces_left = 8
        self.first_player_kings = self.second_player_kings = 0
        self.number_of_turn = 1
        self.turn_of_first_king = None
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
        for row in range(NUMBER_OF_ROWS // 2 - NUMBER_OF_EMPTY_ROWS // 2):
            self.board.append([])
            for column in range(NUMBER_OF_COLUMNS):
                if row % 2 != column % 2:
                    self.board[row].append(CheckerPiece(row, column, SECOND_PLAYER_COLOR))
                else:
                    self.board[row].append(None)

        # Empty rows
        for row in range(NUMBER_OF_ROWS // 2 - NUMBER_OF_EMPTY_ROWS // 2, NUMBER_OF_ROWS // 2 + NUMBER_OF_EMPTY_ROWS // 2):
            self.board.append([])
            for column in range(NUMBER_OF_COLUMNS):
                self.board[row].append(None)

        # Place first player pieces
        for row in range(NUMBER_OF_ROWS // 2 + NUMBER_OF_EMPTY_ROWS // 2, NUMBER_OF_ROWS):
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

        self.number_of_turn += 1

        if (first_player_piece_become_king or second_player_piece_become_king) and not self.turn_of_first_king:
            self.turn_of_first_king = self.number_of_turn

    def get_piece(self, row, column):
        return self.board[row][column]

    def get_valid_moves(self, piece):
        beaten_pieces = set()
        if piece.is_king:
            valid_movements = self.__get_valid_movements_for_king(piece.row, piece.column, piece.color)
        else:
            valid_movements = self.__get_valid_movements(piece.row, piece.column, piece.direction, piece.color,
                                                         beaten_pieces)
        if valid_movements == ([], []):
            return []

        return [(movement[0][0], movement[1]) for movement in valid_movements]

    def erase_pieces(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = None
            if piece.color == FIRST_PLAYER_COLOR:
                self.first_player_pieces_left -= 1
            else:
                self.second_player_pieces_left -= 1

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
                            beaten_pieces.add(beaten_piece)
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

    def __get_valid_movements_for_king(self, row, column, color):
        results = []

        self.__get_king_movement_in_column(row, column, results)

        self.__get_king_movement_in_diagonal(row, column, results)

        beats_result = []
        self.__get_king_beats_movement(row, column, color, set(), beats_result)

        if beats_result:
            self.__get_best_results(beats_result)
            results = beats_result

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

    def __get_king_movement_in_column(self, row, column, results):

        # Up king movement
        self.__calculate_king_movement_in_column(row + 2, NUMBER_OF_ROWS, 2, column, results)

        # Down king movement
        self.__calculate_king_movement_in_column(row - 2, -1, -2, column, results)

    def __get_king_movement_in_diagonal(self, row, column, results):
        # Up Left king movement
        self.__calculate_king_movement_in_diagonal(row + UP, -1, UP, column + LEFT, -1, LEFT, results)

        # Up Right king movement
        self.__calculate_king_movement_in_diagonal(row + UP, -1, UP, column + RIGHT, NUMBER_OF_COLUMNS, RIGHT, results)

        # Down Left king movement
        self.__calculate_king_movement_in_diagonal(row + DOWN, NUMBER_OF_ROWS, DOWN, column + LEFT, -1, LEFT, results)

        # Down Right king movement
        self.__calculate_king_movement_in_diagonal(row + DOWN, NUMBER_OF_ROWS, DOWN, column + RIGHT, NUMBER_OF_COLUMNS,
                                                   RIGHT, results)

    def __get_king_beats_movement(self, row, column, color, beaten_pieces, results):
        if beaten_pieces:
            results.append(([(row, column)], beaten_pieces))
        # Up Left king beats
        self.__beat_king(row, -1, column, -1, UP, LEFT, color, beaten_pieces.copy(), results)

        # Up Right king beats
        self.__beat_king(row, -1, column, NUMBER_OF_COLUMNS, UP, RIGHT, color, beaten_pieces.copy(), results)

        # Down Left king beats
        self.__beat_king(row, NUMBER_OF_ROWS, column, -1, DOWN, LEFT, color, beaten_pieces.copy(), results)

        # Down Right king beats
        self.__beat_king(row, NUMBER_OF_ROWS, column, NUMBER_OF_COLUMNS, DOWN, RIGHT, color, beaten_pieces.copy(),
                         results)

    def __beat_king(self, row, end_row, column, end_column, vertical_direction, horizontal_direction, color,
                    beaten_pieces, results):
        king_beats = self.__calculate_king_beats(row + vertical_direction, end_row, vertical_direction,
                                                 column + horizontal_direction, end_column, horizontal_direction, color)
        if king_beats:
            beaten_piece = king_beats[1][0]
            if beaten_piece not in beaten_pieces:
                beaten_pieces.add(beaten_piece)
                empty_fields = self.__get_empty_fields_after_piece(beaten_piece.row + vertical_direction, end_row,
                                                                   vertical_direction, beaten_piece.column +
                                                                   horizontal_direction, end_column,
                                                                   horizontal_direction)
                for field in empty_fields:
                    self.__get_king_beats_movement(field[0], field[1], color, beaten_pieces, results)

    def __calculate_king_movement_in_column(self, start, end, step, column, king_movement):
        for row in range(start, end, step):
            piece = self.board[row][column]
            if not piece:
                king_movement.append(([(row, column)], []))
            else:
                return

    def __calculate_king_movement_in_diagonal(self, start_row, end_row, step_row, start_column, end_column, step_column,
                                              king_movement):
        column = start_column
        for row in range(start_row, end_row, step_row):
            if column == end_column:
                return
            piece = self.board[row][column]
            if not piece:
                king_movement.append(([(row, column)], []))
            else:
                return
            column += step_column

    def __calculate_king_beats(self, start_row, end_row, step_row, start_column, end_column, step_column, color):
        column = start_column
        for row in range(start_row, end_row, step_row):
            if column == end_column:
                return None
            piece = self.board[row][column]
            if piece:
                if self.__can_beat(row + step_row, column + step_column, piece, color):
                    if not self.board[row + step_row][column + step_column]:
                        return [(row + step_row, column + step_column)], [piece]
                    else:
                        return None
                else:
                    return None
            column += step_column

    def __get_empty_fields_after_piece(self, start_row, end_row, step_row, start_column, end_column, step_column):
        empty_fields = []
        column = start_column
        for row in range(start_row, end_row, step_row):
            if column == end_column:
                return empty_fields
            piece = self.board[row][column]
            if not piece:
                empty_fields.append((row, column))
            else:
                return empty_fields
            column += step_column
        return empty_fields
