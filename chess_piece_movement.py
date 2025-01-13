from hexagons import *
import itertools

class Chessp():

	# REWORK ALL MOVEMENTS
	# MOVEMENTS ARE IN STATIC DIRECTIONS - RECORD THE CHANGE AND STORE THEM IN A LIST
	# NO COMPLEX EXEC AND FOR NESTED FOR LOOPS
	
	chess_pieces = []
	def __init__(self, type, object, pos, hm):
		
		self.type = type
		self.object = object
		self.position = pos  # In Hex
		self.first_move = hm
		Chessp.chess_pieces.append(self)
		
	def p_move(self):
		"""Checks for legal pawn moves"""
		
		valid_spaces = []
		pos = self.position
		if self.first_move:
			valid_spaces.append(Hex(pos[0], pos[1] - 2, pos[2] + 2))
		valid_spaces.append(Hex(pos[0], pos[1] - 1, pos[2] + 1))
		return valid_spaces
	
	def r_move(self):
		"""Checks for legal rook moves"""
		
		valid_spaces = []
		move_directions = itertools.permutations(['+', '-', '+ 0 *'], 3)  # Last one gives no change
		for dire in move_directions:
			i = 1
			enum_pos = list(enumerate(self.position))
			enum_range = range(len(enum_pos))
			while all(map(lambda x, y: -5 <= eval(f'{y} {dire[x]} {i}') <= 5, map(lambda x: enum_pos[x][0], enum_range), map(lambda x: enum_pos[x][1], enum_range))):
				q = eval(f'self.position.q {dire[0]} i')
				r = eval(f'self.position.r {dire[1]} i')
				s = eval(f'self.position.s {dire[2]} i')
				if Hex(q, r, s) in map(lambda x: x.position, Chessp.chess_pieces):
					break
				valid_spaces.append(Hex(q, r, s))
				i += 1
		return valid_spaces
	
	def n_move(self):
		"""Checks for legal horsey moves"""

		# i wanted to do this with execs but they hate me and i hate them so this does work
		# globals()["{string}"] is a lifesaver
		# also if possible do find a way to kill the 9 """"errors""""
		valid_spaces = []
		directions = ['q', 'r', 's']
		q, r, s = None, None, None
		for dire in directions:
			others = list(directions)
			others.remove(dire)
			for signs in [['+', '-'], ['-', '+']]:
				exec(f'globals()["{dire}"] = {signs[0]}3 + self.position.{dire}')
				for horseys in [[2, 1], [1, 2]]:
					for pos, kw in enumerate(others):
						exec(f'globals()["{kw}"] = {signs[1]}{horseys[pos]} + self.position.{kw}')
					if Hex(q, r, s) not in map(lambda x: x.position, Chessp.chess_pieces) and all(map(lambda x: -5 <= x <= 5, [q, r, s])):
						valid_spaces.append(Hex(q, r, s))
		return valid_spaces

	def b_move(self):
		"""Checks for legal bishop moves"""

		valid_spaces = []
		directions = ['q', 'r', 's']
		q, r, s = None, None, None
		value_const = {'q': self.position.q, 'r': self.position.r, 's': self.position.s}
		signs = ['+', '-']
		for dire in directions:
			others = list(directions)
			others.remove(dire)
			for sign in signs:
				i = eval(f'{sign}1')
				while all(map(lambda x: -5 <= eval(f'{value_const}.get("{x}") + {i}') <= 5, directions)):
					stabiliser = 0
					for tj in others:
						exec(f'globals()["{tj}"] = {value_const}.get("{tj}") + {i}')
						print(r)  # This stays none - the valeus aren't changed for some reason
						stabiliser -= eval(f'{tj}')
					exec(f'globals()["{dire}"] = -values[0]-values[1]')
					if Hex(q, r, s) not in map(lambda x: x.position, Chessp.chess_pieces):
						valid_spaces.append(Hex(q, r, s))
					i += eval(f'{sign}1')
		return valid_spaces
