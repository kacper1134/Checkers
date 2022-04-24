import pygame as pg

# Game sizes
WIDTH, HEIGHT = 500, 500
NUMBER_OF_ROWS, NUMBER_OF_COLUMNS = 8, 8
FIELD_SIZE = WIDTH // NUMBER_OF_COLUMNS

PIECE_PADDING = FIELD_SIZE // 7
PIECE_OUTLINE = FIELD_SIZE // 25

# Colors used for game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_BROWN = (153, 103, 60)
DARK_BROWN = (54, 34, 4)
SILVER = (150, 156, 148)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FIRST_PLAYER_COLOR = WHITE
SECOND_PLAYER_COLOR = BLACK
UNUSED_FIELD_COLOR = LIGHT_BROWN
USED_FIELD_COLOR = DARK_BROWN
AVAILABLE_NEXT_MOVE_COLOR = BLUE
PIECE_OUTLINE_COLOR = SILVER
BEATEN_PIECE_COLOR = RED

# Direction
UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1

# Images
CROWN_IMAGE = pg.image.load('assets/crown.png')
CROWN_IMAGE = pg.transform.scale(CROWN_IMAGE, (WIDTH // 16, HEIGHT // 28))
