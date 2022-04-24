from checkers.checkers_game import *

# Game settings
FPS = 60

# Initializing game window
GAME_WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Checkers')


def get_row_and_column_from_mouse_position(position):
    x, y = position
    return y // FIELD_SIZE, x // FIELD_SIZE


# Game loop
def main():
    is_game_running = True
    clock = pg.time.Clock()
    game = CheckersGame(GAME_WINDOW)

    while is_game_running:
        clock.tick(FPS)

        # Event loop
        for event in pg.event.get():
            # Quiting game event
            if event.type == pg.QUIT:
                is_game_running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                row, column = get_row_and_column_from_mouse_position(mouse_position)
                game.select(row, column)

        # Draw game board
        game.update()

        # Get game status
        game_status = game.get_status()

        if game_status != NOT_OVER:
            is_game_running = False
            print("First player win!!!" if game_status == FIRST_PLAYER_WIN else "Second player win!!!"
            if game_status == SECOND_PLAYER_WIN else "Tie!!!")

    # Closing window
    pg.quit()


if __name__ == '__main__':
    main()
