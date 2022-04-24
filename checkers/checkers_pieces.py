from .checkers_constants import *


class CheckerPiece:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.is_king = False
        self.direction = UP if color == FIRST_PLAYER_COLOR else DOWN
        self.position = (0, 0)
        self.calculate_position()

    def calculate_position(self):
        x = FIELD_SIZE * self.column + FIELD_SIZE // 2
        y = FIELD_SIZE * self.row + FIELD_SIZE // 2
        self.position = (x, y)

    def become_king(self):
        self.is_king = True

    def draw(self, window):
        radius = FIELD_SIZE // 2 - PIECE_PADDING
        pg.draw.circle(window, PIECE_OUTLINE_COLOR, self.position, radius + PIECE_OUTLINE)
        pg.draw.circle(window, self.color, self.position, radius)
        if self.is_king:
            window.blit(CROWN_IMAGE, (self.position[0] - CROWN_IMAGE.get_width() // 2,
                                      self.position[1] - CROWN_IMAGE.get_height() // 2))

    def move(self, new_row, new_column):
        self.row = new_row
        self.column = new_column
        self.calculate_position()

    def get_row_and_column(self):
        return self.row, self.column

    # DELETE AFTER DEVELOPMENT
    def __repr__(self):
        return str(self.color)
