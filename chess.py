from board import ChessBoard
from data import COLORS
from exceptions import InvalidPawnMoveError, InvalidBishopMoveError, InvalidRookMoveError, InvalidKnightMoveError, \
    InvalidKingMoveError
from utils import col_row_to_position


class Chess:
    def __init__(self):
        self.board = ChessBoard()

    def start(self):
        i = 0
        while True:
            # Print the board
            self.board.print()

            # Determine who's move it is
            color = COLORS[i]
            i = (i + 1) % 2

            print()
            print('It is ' + color + '\'s turn to move.')
            self.is_checkmate(color)
            piece = self.select_piece(color)
            self.handle_piece(piece)

    def select_piece(self, color):
        while True:
            try:
                square = input('Where is the piece you want to move? ')
                col = square[0].upper()
                row = int(square[1])
                position = col_row_to_position(col, row)
                piece = self.board.get_piece(position)

                if piece and piece.color == color:
                    can_move = False
                    for position in range(0, 64):
                        try:
                            if piece.is_valid_move(self.board, position, True):
                                can_move = True
                                break
                        except Exception:
                            continue
                    if can_move:
                        break
                    else:
                        print(piece.piece_type + ' has nowhere to move, select another piece')
                else:
                    print('Invalid square')
            except ValueError:
                print('Invalid square')
            except IndexError:
                print('Invalid square')
            except EOFError:
                print()
                print('----Program Exited----')
                exit()
        return piece

    def handle_piece(self, piece):
        while True:
            try:
                square = input('Where do you want to move ' + piece.piece_type + ' to? ')
                col = square[0].upper()
                row = int(square[1])
                position = col_row_to_position(col, row)
                if piece.is_valid_move(self.board, position, False):
                    self.board.move_piece(piece, position)
                    break
            except ValueError:
                print('Invalid square')
            except IndexError:
                print('Invalid square')
            except InvalidKingMoveError:
                print('king cannot move to there')
            except InvalidKnightMoveError:
                print('knight cannot move to there')
            except InvalidRookMoveError:
                print('rook cannot move to there')
            except InvalidBishopMoveError:
                print('bishop cannot move to there')
            except InvalidPawnMoveError:
                print('pawn cannot move to there')
            except EOFError:
                print('----Program Exited----')
                exit()

    def is_checkmate(self, color):
        has_valid_piece = False
        for piece_position in range(0, 64):
            piece = self.board.get_piece(piece_position)
            if not piece or piece.color is not color:
                continue
            for to_position in range(0, 64):
                try:
                    if piece.is_valid_move(self.board, to_position, True):
                        has_valid_piece = True
                        break
                except Exception:
                    continue
            if has_valid_piece:
                break
        if not has_valid_piece:
            print(color + ' has nowhere to go, CHECKMATE!')
            input('Press any key to exit')
            exit()
