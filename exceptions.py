class OutOfBordersError(Exception):
    pass


class SameColorError(Exception):
    pass


class ObstacleInColumnError(Exception):
    pass


class ObstacleInRowError(Exception):
    pass


class ObstacleInDiagonalError(Exception):
    pass


class CausingCheckError(Exception):
    pass


class InvalidPawnMoveError(Exception):
    pass


class InvalidRookMoveError(Exception):
    pass


class InvalidKnightMoveError(Exception):
    pass


class InvalidBishopMoveError(Exception):
    pass


class InvalidKingMoveError(Exception):
    pass


class InvalidQueenMoveError(Exception):
    pass
