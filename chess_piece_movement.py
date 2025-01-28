from hexagons import *


class Chessp:

    white_pawn_move = Hex(0, 1, -1)
    white_pawn_take = [Hex(-1, 1, 0), Hex(1, 0, -1)]
    black_pawn_move = Hex(0, -1, 1)
    black_pawn_take = [Hex(1, -1, 0), Hex(-1, 0, 1)]
    rook_moves = [
        Hex(1, -1, 0),
        Hex(-1, 1, 0),
        Hex(1, 0, -1),
        Hex(-1, 0, 1),
        Hex(0, 1, -1),
        Hex(0, -1, 1),
    ]
    knight_moves = [
        Hex(1, 2, -3),
        Hex(2, 1, -3),
        Hex(-1, -2, 3),
        Hex(-2, -1, 3),
        Hex(1, -3, 2),
        Hex(2, -3, 1),
        Hex(-1, 3, -2),
        Hex(-2, 3, -1),
        Hex(-3, 1, 2),
        Hex(-3, 2, 1),
        Hex(3, -1, -2),
        Hex(3, -2, -1),
    ]
    bishop_moves = [
        Hex(1, 1, -2),
        Hex(-1, -1, 2),
        Hex(1, -2, 1),
        Hex(-1, 2, -1),
        Hex(-2, 1, 1),
        Hex(2, -1, -1),
    ]

    chess_pieces = []

    def __init__(self, type, color, object, pos, first_move, id):

        self.type = type
        self.color = color
        self.object = object
        self.position = pos  # In Hex
        self.first_move = first_move
        self.token = id

    def deinit(self):
        self.chess_pieces.remove(self)
        self.position = Hex(-10, 10, 0)

    def check(self, dire, i):
        # i told myself to make more readable code wth is this
        return all(
            map(lambda x, y: -5 <= y + x * i <= 5, dire, self.position)
        ) and self.get_hex(dire, i) not in map(
            lambda x: x.position, Chessp.chess_pieces
        )

    def take_check(self, dire, i):
        return all(
            map(lambda x, y: -5 <= y + x * i <= 5, dire, self.position)
        ) and self.get_hex(dire, i) in map(
            lambda x: x.position if x.color is not self.color else None,
            Chessp.chess_pieces,
        )

    def check_if_king(self, dire, i):
        # Could be integrated into the check functions to waste less cycles
        for x in Chessp.chess_piecesx.position:
            if x.color is not self.color and x.type == "k":
                return True
        return False

    def get_hex(self, dire, i):
        """Get Hex dependinding on the direction, current position and direction multiplier"""

        q = self.position.q + dire[0] * i
        r = self.position.r + dire[1] * i
        s = self.position.s + dire[2] * i
        return Hex(q, r, s)

    def checked(self, v_spaces, dire, j):
        if self.take_check(dire, j):
            # Need to add a check to see whether the colors are different or not
            # Every object has a color to its name
            # sometimes idk
            for piece in self.chess_pieces:
                if piece.position == self.get_hex(dire, j):
                    taken = piece
                    break
            if taken.color != self.color:
                v_spaces.append(self.get_hex(dire, j))
        return v_spaces, taken.type == "k"

    def enemies_checking_king_post_move(self, dire, j) -> bool:
        for piece in self.chess_pieces:
            if piece.color != self.color and piece.type != "k":
                _, king_check = eval(f"piece.{piece.type}_move()")
                if king_check:
                    return True
        return False

    def p_move(self, type):
        """Gives all possible pawn moves (both white and black)"""

        valid_spaces = []
        pawn_move = eval(f"self.{type}_pawn_move")
        pawn_take = eval(f"self.{type}_pawn_take")
        if self.check(pawn_move, 1):
            valid_spaces.append(self.get_hex(pawn_move, 1))
            if self.first_move and self.check(
                pawn_move, 2
            ):  # First move - can move 2 spaces forward
                valid_spaces.append(self.get_hex(pawn_move, 2))

        # Check if pawn can take a piece
        for pos in pawn_take:
            valid_spaces, is_king = self.checked(valid_spaces, pos, 1)
            king_check = True if not king_check and is_king else king_check
        return valid_spaces, king_check

    def wp_move(self):
        """Gives all possible white pawn moves"""

        return self.p_move("white")

    def bp_move(self):
        """Gives all possible black pawn moves"""

        return self.p_move("black")

    def r_move(self):
        """Gives all possible rook moves"""

        valid_spaces = []
        for dire in Chessp.rook_moves:
            i = 1
            while self.check(dire, i):
                valid_spaces.append(self.get_hex(dire, i))
                i += 1
            valid_spaces, is_king = self.checked(valid_spaces, dire, i)
            king_check = True if not king_check and is_king else king_check
        return valid_spaces, king_check

    def b_move(self):
        """Gives all possible bishop moves"""

        valid_spaces = []
        for dire in Chessp.bishop_moves:
            i = 1
            while self.check(dire, i):
                valid_spaces.append(self.get_hex(dire, i))
                i += 1
            valid_spaces, is_king = self.checked(valid_spaces, dire, i)
            king_check = True if not king_check and is_king else king_check
        return valid_spaces, king_check

    def n_move(self):
        """Gives all possible horsey moves"""

        valid_spaces = []
        for dire in Chessp.knight_moves:
            if self.check(dire, 1):
                valid_spaces.append(self.get_hex(dire, 1))
            valid_spaces, is_king = self.checked(valid_spaces, dire, 1)
            king_check = True if not king_check and is_king else king_check
        return valid_spaces, king_check

    def k_move(self):
        """Gives all possible king moves"""

        valid_spaces = []
        for dire in Chessp.rook_moves:
            if self.check(dire, 1):
                valid_spaces.append(self.get_hex(dire, 1))
            valid_spaces, is_king = self.checked(valid_spaces, dire, 1)
        for dire in Chessp.bishop_moves:
            if self.check(dire, 1):
                valid_spaces.append(self.get_hex(dire, 1))
            valid_spaces, is_king = self.checked(valid_spaces, dire, 1)
            king_check = True if not king_check and is_king else king_check
        return valid_spaces, king_check

    def q_move(self):
        """Gives all possible queen moves"""

        valid_spaces, king_check = self.r_move()
        b_moves, king_check2 = self.b_move()
        king_check = king_check or king_check2
        for i in b_moves:
            valid_spaces.append(i)
        return valid_spaces, king_check
