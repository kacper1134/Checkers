from checkers.checkers_game import CheckersGame
from checkers.checkers_player import *
from checkers.checkers_button import *
import ctypes

# Game settings
FPS = 60

# Initializing game window
pg.init()
smallfont = pg.font.SysFont('Corbel', BUTTON_FONT_SIZE)
GAME_WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Checkers')


# Game loop
def main():
    is_game_running = True
    clock = pg.time.Clock()
    game = CheckersGame()
    players = choose_game_mode(GAME_WINDOW, clock, game)
    if not players:
        return
    
    current_player = 0
    game_results = {"First": 0, "Second": 0, "Tie": 0}
    while is_game_running:
        clock.tick(FPS)

        # Draw game board
        game.update(GAME_WINDOW)

        if not players[current_player].make_move():
            is_game_running = False

        if players[current_player].color != game.current_turn:
            current_player = (current_player + 1) % 2

        # Get game status
        game_status = game.get_status()

        if game_status != NOT_OVER:
            game.update(GAME_WINDOW)
            if game_status == FIRST_PLAYER_WIN:
                game_results["First"] += 1
            elif game_status == SECOND_PLAYER_WIN:
                game_results["Second"] += 1
            else:
                game_results["Tie"] += 1

            # is_game_running = False
            text = "First player win!!!" if game_status == FIRST_PLAYER_WIN else "Second player win!!!" \
                if game_status == SECOND_PLAYER_WIN else "Tie!!!"
            ctypes.windll.user32.MessageBoxW(0, text, "Game result", 0)
            game.reset()

    # Closing window
    pg.quit()


def choose_game_mode(window, clock, game):
    window.fill(USED_FIELD_COLOR)

    no_mode_selected = True
    buttons = Buttons(window)

    buttons.add_button(Button(0, 0, "Human Player", True))
    buttons.add_button(Button(2, 0, "Human Player", True))
    buttons.add_button(Button(0, 1, "Random Player"))
    buttons.add_button(Button(2, 1, "Random Player"))
    buttons.add_button(Button(0, 2, "MiniMax Player"))
    buttons.add_button(Button(2, 2, "MiniMax Player"))
    buttons.add_button(Button(BUTTONS_IN_ROW // 2, BUTTONS_IN_COLUMN - 1, "Confirm Choice", False, True))

    while no_mode_selected:
        clock.tick(FPS)
        buttons.draw(smallfont)

        for event in pg.event.get():
            # Quiting game event
            if event.type == pg.QUIT:
                pg.quit()
                return None

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                row, column = (mouse_position[0] // BUTTONS_WIDTH, mouse_position[1] // BUTTONS_HEIGHT)

                for button in buttons.get_buttons():
                    if row == button.row and column == button.column:
                        buttons.unselect(row)
                        button.select()
                        if button.confirm_button:
                            no_mode_selected = False

        pg.display.update()

    selected_buttons = buttons.get_selected_buttons()
    first_player_number = selected_buttons[0].column
    second_player_number = selected_buttons[1].column

    return [create_player(first_player_number, game, FIRST_PLAYER_COLOR),
            create_player(second_player_number, game, SECOND_PLAYER_COLOR)]


def create_player(number, game, color):
    if number == HUMAN_PLAYER:
        return HumanPlayer(color, game)
    if number == RANDOM_PLAYER:
        return RandomPlayer(color, game)
    if number == MINI_MAX_PLAYER:
        return MiniMaxPlayer(color, game, 4)


if __name__ == '__main__':
    main()
