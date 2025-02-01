from hexagons import *


class Chessp:

    black_pawn_move = Hex(0, 1, -1)
    black_pawn_take = [Hex(-1, 1, 0), Hex(1, 0, -1)]
    white_pawn_move = Hex(0, -1, 1)
    white_pawn_take = [Hex(1, -1, 0), Hex(-1, 0, 1)]
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

    def check(self, dire, i, chess_pieces: list, ignore_checkmate):
        # i told myself to make more readable code wth is this
        # print("using check", time.time())
        # if chess_pieces is None:
        #     chess_pieces = self.chess_pieces
        # # Lowk unustasin ja panin selle checki hoopis kõikidesse move funktsioonidesse oops
        return all(
            map(lambda x, y: -5 <= y + x * i <= 5, dire, self.position)
        ) and self.get_hex(dire, i) not in map(lambda x: x.position, chess_pieces)

    # , (
    #         not self._enemies_checking_post_move(dire, i)
    #         if not ignore_checkmate
    #         else True
    #     )

    def take_check(self, dire, i, chess_pieces: list, ignore_checkmate):
        return all(
            map(lambda x, y: -5 <= y + x * i <= 5, dire, self.position)
        ) and self.get_hex(dire, i) in map(
            lambda x: x.position if x.color is not self.color else None,
            chess_pieces,
        )

    # region
    # forgot purpose of this function
    # def check_if_king(self, dire, i):
    #     # Could be integrated into the check functions to waste less cycles
    #     for x in Chessp.chess_piecesx.position:
    #         if x.color is not self.color and x.type == "k":
    #             return True
    #     return False
    # endregion
    def get_hex(self, dire, i):
        """Get Hex dependinding on the direction, current position and direction multiplier"""

        q = self.position.q + dire[0] * i
        r = self.position.r + dire[1] * i
        s = self.position.s + dire[2] * i
        return Hex(q, r, s)

    def checked(self, v_spaces, dire, j, chess_pieces: list, ignore_checkmate):
        if self.take_check(dire, j, chess_pieces, ignore_checkmate):
            # Need to add a check to see whether the colors are different or not
            # Every object has a color to its name
            # sometimes idk
            for piece in chess_pieces:
                if (
                    piece.position == self.get_hex(dire, j)
                    and piece.color != self.color
                ):
                    taken = piece
                    break
            if taken.color != self.color:
                v_spaces.append(self.get_hex(dire, j))
                if taken.type == "k":
                    return v_spaces, True
        return v_spaces, False

    def _enemies_checking_post_move(self, pos: Hex) -> bool:
        # TODO: Add a check for situations where piece is taken away to prevent check cause i'm not sure if it exists
        alternate_chess_pieces = []
        for piece in self.chess_pieces:
            if piece == self:
                alternate_chess_pieces.append(
                    Chessp(
                        self.type,
                        self.color,
                        self.object,
                        pos,
                        self.first_move,
                        self.token,
                    )
                )
                # print("piece", alternate_chess_pieces[-1].position)
                # print("self", self.position)

            else:
                alternate_chess_pieces.append(piece)
        for piece in alternate_chess_pieces:
            if piece.color != self.color and piece.type != "k":
                _, king_check = eval(f"piece.{piece.type}_move(alternate_chess_pieces)")
                if king_check:
                    return True
        return False

    def check_if_2_pieces_overlapping(self, chess_pieces) -> bool:
        i = 0
        for piece in chess_pieces:
            if piece.position == self.position:
                i += 1
        # if i != 1:
        #     print("hey🫦🫦🫦🫦")
        return i != 1
        # return False

    def filter_for_check(self, valid_spaces: list[Hex], ignore_checkmate: bool):
        """Filters out moves that would put the king in check"""
        if ignore_checkmate:
            return
        # print("filtering", len(valid_spaces))
        spaces = valid_spaces.copy()
        for space in spaces:
            if self._enemies_checking_post_move(space):
                valid_spaces.remove(space)

    def p_move(self, type, chess_pieces: list):
        """Gives all possible pawn moves (both white and black)"""
        ignore_checkmate = True
        if chess_pieces is None:
            chess_pieces = self.chess_pieces
            ignore_checkmate = False

        if self.check_if_2_pieces_overlapping(
            chess_pieces
        ):  # fuck you thats why (short circuiting debugging reasons)
            return [], False

        valid_spaces = []
        pawn_move = eval(f"self.{type}_pawn_move")
        pawn_take = eval(f"self.{type}_pawn_take")
        if self.check(pawn_move, 1, chess_pieces, ignore_checkmate):
            valid_spaces.append(self.get_hex(pawn_move, 1))
            if self.first_move and self.check(
                pawn_move, 2, chess_pieces, ignore_checkmate
            ):  # First move - can move 2 spaces forward
                valid_spaces.append(self.get_hex(pawn_move, 2))

        # Check if pawn can take a piece
        king_check = False
        for pos in pawn_take:
            valid_spaces, is_king = self.checked(
                valid_spaces, pos, 1, chess_pieces, ignore_checkmate
            )
            king_check = True if not king_check and is_king else king_check
        self.filter_for_check(valid_spaces, ignore_checkmate)
        return valid_spaces, king_check

    def wp_move(self, chess_pieces: list = None):
        """Gives all possible white pawn moves"""

        return self.p_move("white", chess_pieces)

    def bp_move(self, chess_pieces: list = None):
        """Gives all possible black pawn moves"""

        return self.p_move("black", chess_pieces)

    def r_move(self, chess_pieces: list = None):
        """Gives all possible rook moves"""
        ignore_checkmate = True
        if chess_pieces is None:
            chess_pieces = self.chess_pieces
            ignore_checkmate = False

        if self.check_if_2_pieces_overlapping(chess_pieces):
            return [], False

        valid_spaces = []
        king_check = False
        for dire in Chessp.rook_moves:
            i = 1
            while self.check(dire, i, chess_pieces, ignore_checkmate):
                valid_spaces.append(self.get_hex(dire, i))
                i += 1
            valid_spaces, is_king = self.checked(
                valid_spaces, dire, i, chess_pieces, ignore_checkmate
            )
            king_check = True if not king_check and is_king else king_check
        self.filter_for_check(valid_spaces, ignore_checkmate)
        return valid_spaces, king_check

    def b_move(self, chess_pieces: list = None):
        """Gives all possible bishop moves"""
        ignore_checkmate = True
        if chess_pieces is None:
            chess_pieces = self.chess_pieces
            ignore_checkmate = False

        if self.check_if_2_pieces_overlapping(chess_pieces):
            return [], False

        valid_spaces = []
        king_check = False
        for dire in Chessp.bishop_moves:
            i = 1
            while self.check(dire, i, chess_pieces, ignore_checkmate):
                # print("bishop")
                valid_spaces.append(self.get_hex(dire, i))
                i += 1
            valid_spaces, is_king = self.checked(
                valid_spaces, dire, i, chess_pieces, ignore_checkmate
            )
            king_check = True if not king_check and is_king else king_check
        self.filter_for_check(valid_spaces, ignore_checkmate)
        return valid_spaces, king_check

    def n_move(self, chess_pieces: list = None):
        """Gives all possible horsey moves"""
        ignore_checkmate = True
        if chess_pieces is None:
            chess_pieces = self.chess_pieces
            ignore_checkmate = False

        if self.check_if_2_pieces_overlapping(chess_pieces):
            return [], False

        valid_spaces = []
        king_check = False
        for dire in Chessp.knight_moves:
            if self.check(dire, 1, chess_pieces, ignore_checkmate):
                valid_spaces.append(self.get_hex(dire, 1))
            valid_spaces, is_king = self.checked(
                valid_spaces, dire, 1, chess_pieces, ignore_checkmate
            )
            king_check = True if not king_check and is_king else king_check
        self.filter_for_check(valid_spaces, ignore_checkmate)
        return valid_spaces, king_check

    def k_move(self, chess_pieces: list = None):
        """Gives all possible king moves"""
        ignore_checkmate = True
        if chess_pieces is None:
            chess_pieces = self.chess_pieces
            ignore_checkmate = False

        if self.check_if_2_pieces_overlapping(chess_pieces):
            return [], False

        valid_spaces = []
        king_check = False
        for dire in Chessp.rook_moves:
            if self.check(dire, 1, chess_pieces, ignore_checkmate):
                valid_spaces.append(self.get_hex(dire, 1))
            valid_spaces, is_king = self.checked(
                valid_spaces, dire, 1, chess_pieces, ignore_checkmate
            )
        for dire in Chessp.bishop_moves:
            if self.check(dire, 1, chess_pieces, ignore_checkmate):
                valid_spaces.append(self.get_hex(dire, 1))
            valid_spaces, is_king = self.checked(
                valid_spaces, dire, 1, chess_pieces, ignore_checkmate
            )
            king_check = True if not king_check and is_king else king_check
        self.filter_for_check(valid_spaces, ignore_checkmate)
        return valid_spaces, king_check

    def q_move(self, chess_pieces: list = None):
        """Gives all possible queen moves"""
        valid_spaces, king_check = self.r_move(chess_pieces)
        b_moves, king_check2 = self.b_move(chess_pieces)
        king_check = king_check or king_check2
        for i in b_moves:
            valid_spaces.append(i)
        return valid_spaces, king_check
