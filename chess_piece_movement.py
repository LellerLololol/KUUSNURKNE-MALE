from hexagons import *
import itertools

class Chessp():
    
    white_pawn_move = Hex(0, -1, 1)
    black_pawn_move = Hex(0, 1, -1)
    rook_moves = [Hex(1, -1, 0), Hex(-1, 1, 0), Hex(1, 0, -1), Hex(-1, 0, 1), Hex(0, 1, -1), Hex(0, -1, 1)]
    knight_moves = [Hex(1, 2, -3), Hex(2, 1, -3), Hex(-1, -2, 3), Hex(-2, -1, 3), Hex(1, -3, 2), Hex(2, -3, 1), Hex(-1, 3, -2), Hex(-2, 3, -1), Hex(-3, 1, 2), Hex(-3, 2, 1), Hex(3, -1, -2), Hex(3, -2, -1)]
    bishop_moves = [Hex(1, 1, -2), Hex(-1, -1, 2), Hex(1, -2, 1), Hex(-1, 2, -1), Hex(-2, 1, 1), Hex(2, -1, -1)]

    chess_pieces = []
    def __init__(self, type, color, object, pos, hm):
        
        self.type = type
        self.color = color
        self.object = object
        self.position = pos  # In Hex
        self.first_move = hm
        Chessp.chess_pieces.append(self)
        
    def check(self, dire, i):
        # i told myself to make more readable code wth is this
        return all(map(lambda x, y: -5 <= y + x * i <= 5, dire, self.position)) and Hex(self.position.q + dire[0] * i, self.position.r + dire[1] * i, self.position.s + dire[2] * i) not in map(lambda x: x.position, Chessp.chess_pieces)
        
    def get_hex(self, dire, i):
        """Get Hex dependinding on the direction, current position and direction multiplier"""

        q = self.position.q + dire[0] * i
        r = self.position.r + dire[1] * i
        s = self.position.s + dire[2] * i
        return Hex(q, r, s)

    def p_move(self, type):
        """Gives all possible pawn moves (both white and black)"""
        
        valid_spaces = []
        pawn_move = eval(f'self.{type}_pawn_move')
        if self.check(pawn_move, 1):
            valid_spaces.append(self.get_hex(pawn_move, 1))
            if self.first_move and self.check(pawn_move, 2):  # First move - can move 2 spaces forward
                valid_spaces.append(self.get_hex(pawn_move, 2))
        return valid_spaces
    
    def wp_move(self):
        """Gives all possible white pawn moves"""

        return self.p_move('white')
    
    def bp_move(self):
        """Gives all possible black pawn moves"""

        return self.p_move('black')
    
    def r_move(self):
        """Gives all possible rook moves"""

        valid_spaces = []
        for dire in Chessp.rook_moves:
            i = 1
            while self.check(dire, i):
                valid_spaces.append(self.get_hex(dire, i))
                i += 1
        return valid_spaces
        
    def b_move(self):
        """Gives all possible bishop moves"""
        
        valid_spaces = []
        for dire in Chessp.bishop_moves:
            i = 1
            while self.check(dire, i):
                valid_spaces.append(self.get_hex(dire, i))
                i += 1
        return valid_spaces
        
    def n_move(self):
        """Gives all possible horsey moves"""
            
        valid_spaces = []
        for dire in Chessp.knight_moves:
            if self.check(dire, 1):
                valid_spaces.append(self.get_hex(dire, 1))
        return valid_spaces
        
    def k_move(self):
        """Gives all possible king moves"""
           
        valid_spaces = []
        for dire in Chessp.rook_moves:
            if self.check(dire, 1):
                valid_spaces.append(self.get_hex(dire, 1))
        return valid_spaces
        
    def q_move(self):
        """Gives all possible queen moves"""
        
        valid_spaces = self.r_move()
        for i in self.b_move():
            valid_spaces.append(i)
        return valid_spaces
