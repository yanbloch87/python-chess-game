from piece import Pawn, Rook, Knight, Bishop, King, Queen

STARTING_POSITIONS = {
    0: Rook,
    56: Rook,
    1: Knight,
    57: Knight,
    2: Bishop,
    58: Bishop,
    3: Queen,
    59: Queen,
    4: King,
    60: King,
    5: Bishop,
    61: Bishop,
    6: Knight,
    62: Knight,
    7: Rook,
    63: Rook
}


class ChessBoard:
    def __init__(self):
        self.pieces = [None] * 64
        self.setup_game()

    def setup_game(self):
        for position in range(0, 8):
            self.pieces[position] = STARTING_POSITIONS[position]('white', position)
        for position in range(8, 16):
            self.pieces[position] = Pawn('white', position)
        for position in range(48, 56):
            self.pieces[position] = Pawn('black', position)
        for position in range(56, 64):
            self.pieces[position] = STARTING_POSITIONS[position]('black', position)

    def print(self):
        print(' ----------------------------------------')
        for row in reversed(range(0, 8)):
            print(row + 1, end='')
            print('| ', end='')
            for col in range(0, 8):
                piece = self.get_piece(row * 8 + col)
                if piece:
                    piece.print()
                else:
                    print('·\t'.expandtabs(1), end='')
                print(' | ', end='')
            print()
            print(' ----------------------------------------')
        print('   A\t   B\t   C\t   D\t   E\t   F\t   G\t   H\t'.expandtabs(1))

    def get_piece(self, position):
        return self.pieces[position]

    def get_king_piece(self, color):
        for piece in self.pieces:
            if piece and piece.piece_type == 'king' and piece.color == color:
                return piece
        raise ValueError

    def set_piece(self, piece, position):
        if piece is not None:
            self.pieces[piece.position] = None
            piece.set_position(position)
        self.pieces[position] = piece

    def move_piece(self, piece, position):
        existing_piece = self.pieces[position]
        if existing_piece is not None:
            existing_piece.is_dead = True
        piece.has_moved = True
        self.pieces[piece.position] = None
        self.pieces[position] = piece
        piece.set_position(position)
