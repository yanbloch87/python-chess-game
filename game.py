# https://codegolf.stackexchange.com/questions/148587/is-it-a-valid-chess-move
from chess import Chess


def run():
    game = Chess()
    try:
        game.start()
    except Exception as e:
        print('Unhandled exception')
        print(e)
        exit(1)


run()
