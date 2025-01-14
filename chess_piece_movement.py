from hexagons import *
import itertools

class Chessp():
    
    rook_moves = [Hex(1, -1, 0), Hex(-1, 1, 0), Hex(1, 0, -1), Hex(-1, 0, 1), Hex(0, 1, -1), Hex(0, -1, 1)]
    knight_moves = [Hex(1, 2, -3), Hex(2, 1, -3), Hex(-1, -2, 3), Hex(-2, -1, 3), Hex(1, -3, 2), Hex(2, -3, 1), Hex(-1, 3, -2), Hex(-2, 3, -1), Hex(-3, 1, 2), Hex(-3, 2, 1), Hex(3, -1, -2), Hex(3, -2, -1)]
    bishop_moves = [Hex(1, 1, -2), Hex(-1, -1, 2), Hex(1, -2, 1), Hex(-1, 2, -1), Hex(-2, 1, 1), Hex(2, -1, -1)]
    
    chess_pieces = []
    def __init__(self, type, object, pos, hm):
        
        self.type = type
        self.object = object
        self.position = pos  # In Hex
        self.first_move = hm
        Chessp.chess_pieces.append(self)
        
    def check(self, dire, i):
        return all(map(lambda x: -5 <= x * i <= 5, dire)) and Hex(dire[0] * i, dire[1] * i, dire[2] * i) not in map(lambda x: x.position, Chessp.chess_pieces)
        
    def p_move(self):
        """Gives all possible pawn moves"""
        
        valid_spaces = []
        pos = self.position
        if self.first_move and self.check(Hex(pos[0], pos[1] - 2, pos[2] + 2), 1):  # First move - can move 2 spaces forward
            valid_spaces.append(Hex(pos[0], pos[1] - 2, pos[2] + 2))
		if self.check(Hex(pos[0], pos[1] - 1, pos[2] + 1), 1):
            valid_spaces.append(Hex(pos[0], pos[1] - 1, pos[2] + 1))
        return valid_spaces
    
    def r_move(self):
        """Gives all possible rook moves"""

        valid_spaces = []
        for dire in Chessp.rook_moves:
            i = 1
            while self.check(dire, i):
                valid_spaces.append(Hex(dire[0] * i, dire[1] * i, dire[2] * i))
                i += 1
        return valid_spaces
        
    def b_moves(self):
        """Gives all possible bishop moves"""
        
        valid_spaces = []
        for dire in Chessp.bishop_moves:
            i = 1
            while self.check(dire, i):
                valid_spaces.append(Hex(dire[0] * i, dire[1] * i, dire[2] * i))
                i += 1
        return valid_spaces
        
    def n_move(self):
        """Gives all possible horsey moves"""
            
        valid_spaces = []
        for dire in Chessp.knight_moves:
            if self.check(dire, 1):
                valid_spaces.append(Hex(dire[0] * i, dire[1] * i, dire[2] * i))
        return valid_spaces
        
    def k_move(self):
        """Gives all possible king moves"""
           
        valid_spaces = []
        for dire in Chessp.rook_moves:
            if self.check(dire, 1):
                valid_spaces.append(Hex(dire[0] * i, dire[1] * i, dire[2] * i))
        return valid_spaces
        
    def q_move(self):
        """Gives all possible queen moves"""
        
        valid_spaces = r_move()
        for i in b_move():
            valid_spaces.append(i)
        return valid_spaces
