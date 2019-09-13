from data import UNICODE_CHARS
from exceptions import InvalidKingMoveError, InvalidBishopMoveError, InvalidKnightMoveError, InvalidRookMoveError, \
    InvalidPawnMoveError, CausingCheckError, ObstacleInDiagonalError, ObstacleInRowError, ObstacleInColumnError, \
    SameColorError, OutOfBordersError
from utils import is_same_column, is_same_row, position_to_row, position_to_column


class Piece:
    def __init__(self, color, position):
        self.piece_type = ''
        self.color = color
        self.position = position
        self.is_dead = False
        self.has_moved = False

    def print(self):
        char = UNICODE_CHARS[self.color][self.piece_type]
        print(char + '\t'.expandtabs(0), end='')

    def set_position(self, position):
        self.position = position

    def is_valid_move(self, board, to_position, is_validating):
        try:
            self.is_out_of_borders(to_position)
            self.is_same_color(board.get_piece(to_position))
            self.has_obstacle_in_column(board, to_position)
            self.has_obstacle_in_row(board, to_position)
            self.has_obstacle_in_diagonal(board, to_position)
            not is_validating and self.is_causing_checkmate(board, to_position)
        except OutOfBordersError:
            not is_validating and print('out of borders')
            return False
        except CausingCheckError:
            not is_validating and print('move causes checkmate')
            return False
        except ObstacleInDiagonalError:
            not is_validating and print('there is another piece in the way')
            return False
        except ObstacleInColumnError:
            not is_validating and print('there is another piece in the way')
            return False
        except ObstacleInRowError:
            not is_validating and print('there is another piece in the way')
            return False
        except SameColorError:
            not is_validating and print('location occupied by piece with the same color')
            return False
        return True

    @staticmethod
    def is_out_of_borders(position):
        if position < 0 or position > 63:
            raise OutOfBordersError
        return False

    def is_same_color(self, to_piece):
        if to_piece and to_piece.color == self.color:
            raise SameColorError
        return False

    def has_obstacle_in_column(self, board, to_position):
        from_col = position_to_column(self.position)
        to_col = position_to_column(to_position)
        if from_col != to_col:
            return False
        i = self.position
        end = to_position
        if self.position > to_position:
            i = to_position
            end = self.position
        i += 8
        while i < end:
            if board.get_piece(i):
                raise ObstacleInColumnError
            i += 8
        return False

    def has_obstacle_in_row(self, board, to_position):
        from_row = position_to_row(self.position)
        to_row = position_to_row(to_position)
        if from_row != to_row:
            return False
        i = self.position
        end = to_position
        if self.position > to_position:
            i = to_position
            end = self.position
        i += 1
        while i < end:
            if board.get_piece(i):
                raise ObstacleInRowError
            i += 1
        return False

    def has_obstacle_in_diagonal(self, board, to_position):
        diff = to_position - self.position
        if 0 not in [diff % 7, diff % 9]:
            return False

        from_row = position_to_row(self.position)
        to_row = position_to_row(to_position)
        from_col = position_to_column(self.position)
        to_col = position_to_column(to_position)
        addition = 9
        if to_row > from_row and to_col < from_col:
            addition = 7
        if to_row < from_row and to_col < from_col:
            addition = -9
        if to_row < from_row and to_col > from_col:
            addition = -7

        current_position = self.position + addition
        while current_position < to_position:
            if board.get_piece(current_position):
                raise ObstacleInDiagonalError
            current_position += addition

    def is_causing_checkmate(self, board, to_position):
        if self.piece_type == 'king':
            king_position = to_position
        else:
            king_piece = board.get_king_piece(self.color)
            king_position = king_piece.position

        old_position = self.position
        occupant_piece = board.get_piece(to_position)
        board.set_piece(self, to_position)
        is_valid = True
        for i in range(0, 64):
            piece = board.get_piece(i)
            try:
                if piece and piece.color is not self.color and piece.is_valid_move(board, king_position, True):
                    is_valid = False
                    break
            except Exception:
                continue
        board.set_piece(self, old_position)
        board.set_piece(occupant_piece, to_position)

        if not is_valid:
            raise CausingCheckError
        return False


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.piece_type = 'pawn'

    def is_valid_move(self, board, to_position, is_validating):
        if not super().is_valid_move(board, to_position, is_validating):
            return False
        to_piece = board.get_piece(to_position)
        diff = to_position - self.position
        if self.color == 'black':
            diff *= -1

        if not to_piece:
            if diff == 8 or (not self.has_moved and diff == 16):
                return True
        else:
            if to_piece.color != self.color and diff in [7, 9]:
                return True
        raise InvalidPawnMoveError


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.piece_type = 'rook'

    def is_valid_move(self, board, to_position, is_validating):
        if not super().is_valid_move(board, to_position, is_validating):
            return False
        diff = to_position - self.position
        if diff % 9 != 0 and diff % 7 != 0:
            raise InvalidRookMoveError
        return True


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.piece_type = 'knight'

    def is_valid_move(self, board, to_position, is_validating):
        if not super().is_valid_move(board, to_position, is_validating):
            return False
        diff = to_position - self.position
        if to_position < self.position:
            diff *= -1

        if diff not in [6, 10, 15, 17]:
            raise InvalidKnightMoveError
        return True


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.piece_type = 'bishop'

    def is_valid_move(self, board, to_position, is_validating):
        if not super().is_valid_move(board, to_position, is_validating):
            return False
        diff = abs((to_position % 8) - (self.position % 8))
        row_diff = abs(position_to_row(to_position) - position_to_row(self.position))
        if not diff == row_diff:
            raise InvalidBishopMoveError
        return True


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.piece_type = 'queen'

    def is_valid_move(self, board, to_position, is_validating):
        if not super().is_valid_move(board, to_position, is_validating):
            return False
        diff = abs((to_position % 8) - (self.position % 8))
        row_diff = abs(position_to_row(to_position) - position_to_row(self.position))
        if not (diff == row_diff
                or is_same_row(self.position, to_position) or is_same_column(self.position, to_position)):
            raise InvalidBishopMoveError
        return True


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.piece_type = 'king'

    def is_valid_move(self, board, to_position, is_validating):
        if not super().is_valid_move(board, to_position, is_validating):
            return False
        diff = to_position - self.position
        if to_position < self.position:
            diff *= -1

        if diff not in [1, 7, 8, 9]:
            raise InvalidKingMoveError
        return True
