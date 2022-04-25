from checkers.checkers_game import CheckersGame
from checkers.checkers_pieces import CheckerPiece
from checkers.checkers_player import *

# Game settings
FPS = 60

# Initializing game window
GAME_WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Checkers')


# Game loop
def main():
    is_game_running = True
    clock = pg.time.Clock()
    game = CheckersGame()
    players = [RandomPlayer(FIRST_PLAYER_COLOR, game), MiniMaxPlayer(SECOND_PLAYER_COLOR, game, 1)]
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
            if game_status == FIRST_PLAYER_WIN:
                game_results["First"] += 1
            elif game_status == SECOND_PLAYER_WIN:
                game_results["Second"] += 1
            else:
                game_results["Tie"] += 1
            print(game_results)
            # is_game_running = False
            print("First player win!!!" if game_status == FIRST_PLAYER_WIN else "Second player win!!!"
                  if game_status == SECOND_PLAYER_WIN else "Tie!!!")
            game.reset()

    # Closing window
    pg.quit()


if __name__ == '__main__':
    main()
