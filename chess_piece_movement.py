from hexagons import *
import itertools

class Chessp():
	
	def __init__(self, type, object, pos, hm):
		
		self.type = type
		self.object = object
		self.position = pos  # In Hex
		self.first_move = hm
		
	def p_move(self):
		"""Checks if a pawn move is legal"""
		
		valid_spaces = []
		pos = self.position
		if self.first_move:
			valid_spaces.append(Hex(pos[0], pos[1] - 2, pos[2] + 2))
		valid_spaces.append(Hex(pos[0], pos[1] - 1, pos[2] + 1))
		return valid_spaces
	
	def r_move(self):
		"""Checks if a rook move is legal"""

		'''
		# Remove this - need to show the player all the possible moves, not whether a move is possible
		other_directions = [0, 1, 2]
		static_directions = [i for i in range(3) if self.position[i] - to_move[i] == 0]
		if len(static_directions) == 1:
			other_directions.remove(static_directions[0])
			if self.position[other_directions[0]] - to_move[other_directions[0]] == to_move[other_directions[1]] - self.position[other_directions[1]]:
				return True
		return False
		'''
	
		valid_spaces = []
		move_directions = itertools.permutations(['+', '-', '+ 0 *'], 3)  # Last one gives no change
		for dire in move_directions:
			i = 1
			enum_pos = list(enumerate(self.position))
			enum_range = range(len(enum_pos))
			while all(map(lambda x, y: -5 <= eval(f'{y} {dire[x]} {i}') <= 5, map(lambda x: enum_pos[x][0], enum_range), map(lambda x: enum_pos[x][0], enum_range))):
				q = eval(f'self.position.q {dire[0]} i')
				r = eval(f'self.position.r {dire[1]} i')
				s = eval(f'self.position.s {dire[2]} i')
				valid_spaces.append(Hex(q, r, s))
				i += 1
		return valid_spaces