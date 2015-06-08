import random
from simplegraph import SimpleGraph
from collections import defaultdict
import re
import pprint
import string

movesArr = ['U', 'D', 'L', 'R', 'F', 'B', 'u', 'd', 'l', 'r', 'f', 'b']
traditional_moves = ['U', 'D', 'L', 'R', 'F', 'B']
inverse_moves = ['u', 'd', 'l', 'r', 'f', 'b']
roll_towards = string.maketrans('UFDBufdb','FDBUfdbu')

def sgn(cycle):
	# Simple O(n) time algorithm to calculate sgn
	n = len(cycle)
	visited = [False]*n
	sgn = 1

	for k in range(n):
		if not visited[k]:         
			next = k
			small_cycle_length = 0
			while not visited[next]: 
				small_cycle_length += 1
				visited[next] =  True
				next = cycle[next] - 1
			if small_cycle_length%2 == 0: sgn = -sgn;
	return sgn

def inverse(moves):
	return moves.swapcase()[::-1] # [::-1] = .reverse()

def conjugate(operation, basis): #P'IP
	return inverse(basis) + operation + basis

def simplify(movestr):
	for inverse in inverse_moves: #Expand
		movestr = movestr.replace(inverse, inverse.upper()*3)
	while True:
		oldmoves = movestr
		for move in traditional_moves: #Cancel
			movestr = movestr.replace(move*4, "")
		if movestr == oldmoves: break
	for move in traditional_moves:	#Simplify
		movestr = movestr.replace(move*3, move.lower())
	return movestr

def in_place(array, i):
	return array[i] == i

def commutator(first, second):
		return first + second + inverse(first) + inverse(second) 

def asIfRolledTowards(s):
	return s.translate(roll_towards)

flip_0_2 = "RlBRlDRlFFrLDrLBrLUU"
flip_10_0 = "RlURlBRlDDrLBrLUrLFF" #asIfRolledTowards(flip_0_2)
flip_10_8	= asIfRolledTowards(flip_10_0)
flip_8_2 = asIfRolledTowards(flip_10_8)

class RubiksCube(object):
	moves = movesArr
	traditional_moves = traditional_moves
	inverse_moves = inverse_moves

	cube_permutations = [ "U", #2, 3, 4, 1
												"D", #8, 5, 6, 7
												"FF", #(7, 6, 3, 4, 5, 2, 1, 8)
												"BB", 
												"LL", 
												"RR", 
												"RRuFbRRfBuRR" 
												]

	flip_two_edges = "RUDBBUUbUBUBBdru" 	# flip 1 and 2
	twist_two_corners = "LdlfdFUfDFLDlu" 	# twist 1 and 2
	cycle_three_edges = "RRuFbRRfBuRR" 		# 0, 1, 2 [ ORDER 3 ]
	cycle_left_three_edges = "LLUfBLLFbULL"	# 0, 2, 3 [ ORDER 3 ]
	cycle_three_corners = "fUBuFUbu" 			#	1, 2, 4 [Rotates all +1]
	swap_two_corners_and_two_edges = "rURurUFRbRBRfRR" # Corners 1, 2: Edges 3, 4: Rotates inverse of twist_two_corners
	monotwist = "fRFr"*2
	monoswap = "DFffDDFFdf"

	right_face_edges = set((1,5,6,9))
	down_face_edges = set((11,8,9,10))
	up_face_edges = set((0,1,2,3))
	left_face_edges = set((4,11,7,3))
	front_face_edges = set((2,7,10,6))
	back_face_edges = set((0,5,4,8))

	# """
	# This function isn't actually necessary because it calculates the same immutable thing every time an object
	# is instantiated. I will use this to generate it once, then I will write it as a class literal afterward"
	# """
	def gen_move_corners(self):
		self.move_corners = defaultdict(lambda: {})
		corner_graph = SimpleGraph(set(self.corner_locations))
		self.move_edges = defaultdict(lambda: {})
		edge_graph = SimpleGraph(set(self.edge_locations))
		for operation in self.cube_permutations:
			self.clear()
			self.do(operation)
			inverse_str = simplify(inverse(operation))
			for i in range(len(self.corner_locations)):
				if in_place(self.corner_locations, i): continue
				self.move_corners[self.corner_locations[i]][i] = operation
				self.move_corners[i][self.corner_locations[i]] = inverse_str
				corner_graph.add_edge(i, self.corner_locations[i])
			for i in range(len(self.edge_locations)):
				if in_place(self.edge_locations,i): continue
				self.move_edges[self.edge_locations[i]][i] = operation
				self.move_edges[i][self.edge_locations[i]] = inverse_str
				edge_graph.add_edge(i, self.edge_locations[i])
		self.clear()
		for i in self.corner_locations:
			for j in self.corner_locations:
				if j not in self.move_corners[i] and i != j: 
					start, mid, end = corner_graph.bfs(i, j) # We know it will be a path of 2
					self.move_corners[start][end] = self.move_corners[start][mid] + self.move_corners[mid][end]

		# for key, value in self.move_corners.items():
		# 	print key
		# 	print value

	def clear(self):
		self.corner_locations = (0,1,2,3,4,5,6,7) 
		self.edge_locations	= (0,1,2,3,4,5,6,7,8,9,10,11) 
		self.corner_orientations =(0,0,0,0,0,0,0,0) 
		self.edge_orientations=(0,0,0,0,0,0,0,0,0,0,0,0)	
		self.history = ""
		return self

	def is_solved(self):
		return (self.corner_locations == (0,1,2,3,4,5,6,7) and \
				self.edge_locations	== (0,1,2,3,4,5,6,7,8,9,10,11) and \
				self.corner_orientations ==(0,0,0,0,0,0,0,0) and \
				self.edge_orientations==(0,0,0,0,0,0,0,0,0,0,0,0))

	def simplify(cls, moves):
		return simplify(moves)

	def inverse(cls, moves):
		return inverse(moves) 

	def __init__(self):
		self.clear()
		self.gen_move_corners()

	def is_valid(self):
		# A configuration (sigma,tau,x,y) is valid iff 	sgn(sigma) = sgn(tau)
		#																								sum(x) = 0 mod 3
		#																								sum(y) = 0 mod 3
		if (sgn(self.corner_locations) != sgn(self.edge_locations)): return False
		if (sum(self.corner_orientations)%3 != 0):	return False
		if (sum(self.edge_orientations)%2 != 0):	return False
		return True

	def callMethod(self, name):
		getattr(self, name)()

	def do(self, moves):
		moveArr = list(simplify(moves))
		for move in moveArr:
			if move.isupper():
				self.callMethod(move)
			else:
				for i in range(3):
					self.callMethod(move.upper())
		self.history = simplify(self.history + moves)
		self.normalize()
		return self

	def randomMoves(self, n):
		for i in range(n):
			self.randomMove()

	def randomMove(self):
		move = self.moves[random.randint(0,len(self.moves)-1)]
		self.do(move)
		return move

	def scramble(self):
		for i in range(30): self.randomMove()
		self.normalize()
		return self

	def D(self): 
		x = self.corner_orientations
		y = self.edge_orientations
		s = self.corner_locations
		t = self.edge_locations
		self.corner_locations = (s[0], s[1], s[2], s[3], s[7], s[4], s[5], s[6])
		self.corner_orientations = (x[0], x[1], x[2], x[3], x[7], x[4], x[5], x[6])
		self.edge_locations = (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[9], t[10], t[11], t[8])
		self.edge_orientations = (y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[9], y[10], y[11], y[8])
		return self

	def U(self):
		x = self.corner_orientations
		y = self.edge_orientations
		s = self.corner_locations
		t = self.edge_locations
		self.corner_locations = (s[1], s[2], s[3], s[0], s[4], s[5], s[6], s[7])
		self.corner_orientations = (x[1], x[2], x[3], x[0], x[4], x[5], x[6], x[7])
		self.edge_locations = (t[3], t[0], t[1], t[2], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11])
		self.edge_orientations = (y[3], y[0], y[1], y[2], y[4], y[5], y[6], y[7], y[8], y[9], y[10], y[11])
		return self

	def R(self):
		x = self.corner_orientations
		y = self.edge_orientations
		s = self.corner_locations
		t = self.edge_locations
		self.corner_locations = (s[0], s[6], s[1], s[3], s[4], s[5], s[7], s[2])
		self.corner_orientations = (x[0], x[6]+1, x[1]+2, x[3], x[4], x[5], x[7]+2, x[2]+1)
		self.edge_locations = (t[0], t[6], t[2], t[3], t[4], t[1], t[9], t[7], t[8], t[5], t[10], t[11])
		self.edge_orientations = (y[0], y[6], y[2], y[3], y[4], y[1], y[9], y[7], y[8], y[5], y[10], y[11])
		return self

	def L(self): 
		x = self.corner_orientations
		y = self.edge_orientations
		s = self.corner_locations
		t = self.edge_locations
		self.corner_locations = (s[3], s[1], s[2], s[4], s[5], s[0], s[6], s[7])
		self.corner_orientations = (x[3] + 2,x[1],x[2],x[4] + 1,x[5] + 2,x[0] + 1,x[6], x[7])
		self.edge_locations = (t[0], t[1], t[2], t[4], t[11], t[5], t[6], t[3], t[8], t[9], t[10], t[7])
		self.edge_orientations = (y[0], y[1], y[2], y[4], y[11], y[5], y[6], y[3], y[8], y[9], y[10], y[7])
		return self

	def F(self):
		x = self.corner_orientations
		y = self.edge_orientations
		s = self.corner_locations
		t = self.edge_locations
		self.corner_locations = (s[5], s[0], s[2], s[3], s[4], s[6], s[1], s[7])
		self.corner_orientations = (x[5] + 1,x[0] + 2,x[2], x[3], x[4], x[6] + 2,x[1] + 1, x[7])
		self.edge_locations = (t[0], t[1], t[7], t[3], t[4], t[5], t[2], t[10], t[8], t[9], t[6], t[11])
		self.edge_orientations = (y[0], y[1], y[7] + 1, y[3], y[4], y[5], y[2] + 1, y[10] + 1, y[8], y[9], y[6] + 1, y[11])
		return self

	def B(self):
		x = self.corner_orientations
		y = self.edge_orientations
		s = self.corner_locations
		t = self.edge_locations
		self.corner_locations = (s[0], s[1], s[7], s[2], s[3], s[5], s[6], s[4])
		self.corner_orientations = (x[0], x[1], x[7] + 1, x[2] + 2, x[3] + 1, x[5], x[6], x[4] + 2)
		self.edge_locations = (t[5], t[1], t[2], t[3], t[0], t[8], t[6], t[7], t[4], t[9], t[10], t[11])
		self.edge_orientations = (y[5] + 1, y[1], y[2], y[3], y[0] + 1, y[8] + 1, y[6], y[7], y[4] + 1, y[9], y[10], y[11])
		return self

	def toString(self):
		return str(self.corner_locations) + "\n" + \
							str(self.edge_locations) + "\n" + \
							str(self.corner_orientations)  + "\n" + \
							str(self.edge_orientations)

	def normalize(self):
		x = list(self.corner_orientations)
		y = list(self.edge_orientations)
		for i in range(len(self.corner_orientations)):
			x[i] = self.corner_orientations[i] % 3
		for i in range(len(self.edge_orientations)):
			y[i] = self.edge_orientations[i] % 2
		self.corner_orientations = tuple(x)
		self.edge_orientations = tuple(y)
		return self

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			self.normalize()
			other.normalize()
			if 	self.edge_locations == other.edge_locations and \
					self.corner_locations == other.corner_locations and \
					self.edge_orientations == other.edge_orientations and \
					self.corner_orientations == other.corner_orientations:
					return True
			else:
				return False
		else:
		  return False

	def __ne__(self, other):
		return not self.__eq__(other)


	def solve_four_bottom_corners(self):
		# These swaps will trash the top layers, but are great for bottom corners
		rotate_pos_5 = "FUBD"
		rotate_pos_7 = "RRuR"

		# Very slow first attempt (as in many moves)
		# Place 5
		ind = self.corner_locations.index(5)
		if ind > 3:
			if 		ind == 4: self.do("D")
			elif 	ind == 6: self.do("d")
			elif	ind == 7: self.do("DD")
		else:
			while self.corner_locations[0] != 5: self.do("U") # Because we know how to move 0 -> 5
			self.do("L")
		if self.corner_orientations[5] == 1: self.do(rotate_pos_5) 
		elif self.corner_orientations[5] == 2: self.do(inverse(rotate_pos_5))

		# Place 7
		ind = self.corner_locations.index(7)
		if ind > 3:
			if 		ind == 4: self.do("B")
			elif 	ind == 6: self.do("r")
		else:
			while self.corner_locations[2] != 7: self.do("U") # Because we know how to move 6 -> 7
			self.do("R")
		if self.corner_orientations[7] == 2: self.do(rotate_pos_7)
		elif self.corner_orientations[7] == 1: self.do(inverse(rotate_pos_7))

		# Place 6
		idx = self.corner_locations.index(6)
		ori = self.corner_orientations[idx]
		if idx != 6 or ori != 0:
			if idx == 6:
				if ori == 1: 		self.do("Rur")
				elif ori == 2: 	self.do("fUF")
			elif idx == 4: self.do("bUB")
			if self.corner_locations.index(6) < 4:
				while self.corner_locations[1] != 6: self.do("U")
				ori = self.corner_orientations[1]
				if ori == 0:	
					self.do("URuur")
					ori = self.corner_orientations[1]
				if ori == 1: 		self.do("fuF")
				elif ori == 2: 	self.do("RUr")

		# Place 4
		idx = self.corner_locations.index(4)
		ori = self.corner_orientations[idx]
		if idx != 4 or ori != 0:
			if idx == 4:
				if ori == 1: 		self.do("Lul")
				elif ori == 2: 	self.do("bUB")
			if self.corner_locations.index(4) < 4:
				while self.corner_locations[3] != 4: self.do("U")
				ori = self.corner_orientations[3]
				if ori == 0:	
					self.do("ULuul")
					ori = self.corner_orientations[3]
				if ori == 1: 		self.do("buB")
				elif ori == 2: 	self.do("LUl")
		return self




		#if 0 in x[4:]:
	
	def place_top_four_corners(self):
		# This will trash edges and top orientations but that's okay in this stage
		swap_corners_1_2 = "RUrufuF"
		# Place 3
		while self.corner_locations[3] != 3: self.do("U")
		# Fairly few cases
		if self.corner_locations[:4] == (0,1,2,3): return self
		if self.corner_locations[1] == 1:
			three_way = swap_corners_1_2 + "u" + swap_corners_1_2 + "U" + swap_corners_1_2
			self.do(three_way)
		if self.corner_locations[1] == 2:	self.do(swap_corners_1_2)
		if self.corner_locations[1] == 0:	self.do(conjugate(swap_corners_1_2, "U"))
		if self.corner_locations[1] == 2: self.do(swap_corners_1_2)
		return self

	def twist_top_four_corners(self):
		twist_tlf1_trf2	=	"LdlfdFUfDFLDlu"
		if self.corner_orientations[0] == 2: self.do(twist_tlf1_trf2)
		elif self.corner_orientations[0] == 1: self.do(inverse(twist_tlf1_trf2))
		if self.corner_orientations[1] == 2: self.do(conjugate(twist_tlf1_trf2, "u"))
		elif self.corner_orientations[1] == 1: self.do(conjugate(inverse(twist_tlf1_trf2), "u"))
		if self.corner_orientations[2] == 2: self.do(conjugate(twist_tlf1_trf2, "UU"))
		elif self.corner_orientations[2] == 1: self.do(conjugate(inverse(twist_tlf1_trf2), "UU"))
		return self

	def solve_three_ledges(self):
		ledges = [4,11,7]	# We use only 5 macros, which manipulate the bottom-front and top-right positions

		solutions = ["urLFRl", "URRLLdRRLL", "uRlBLr", "URlBBrLU", "uRlBBRRLLFRlUU"]
		for i in range(len(ledges)):
			basis = "L"*(i+1)
			self.do(basis)
			goal = ledges[i]
			idx = self.edge_locations.index(goal)
			faces = self.get_edge_faces(goal)
			move = ""
			if "L" in faces:
				if idx == 4: move = "ubU"
				elif idx == 7: move = "Ufu"
				elif idx == 11: move = "D"
			elif "R" in faces:
				if idx == 5: move = "r"
				if idx == 9: move = "RR"
				if idx == 6: move = "R"
			elif "B" in faces:
				if idx == 8: move = "DD"
				elif idx == 0: move = "LUl"
			elif "F" in faces and idx == 2: move = "lFFL"
			basis += move
			self.do(move)
			idx = self.edge_locations.index(goal)
			if idx == 10 and self.edge_orientations[idx]==1: self.do(solutions[0])
			elif idx == 10 and self.edge_orientations[idx]==0: self.do(solutions[1])
			elif idx == 1 and self.edge_orientations[idx]==1: self.do(solutions[2])
			elif idx == 1 and self.edge_orientations[idx]==0: self.do(solutions[3])
			elif idx == 3 and self.edge_orientations[idx]==1: self.do(solutions[4])
			self.do(inverse(basis))
		return self

	def solve_four_redges(self):
		solutions = ["UrLfRl", "uRRLLDRRLL", "URlbLr", "uRlBBrLu", "URlBBRRLLfRlUU"]
		ledges = [1,6,9,5]	# We use only 5 macros, which manipulate the bottom-front and top-right positions
		for i in range(len(ledges)):
			basis = "R"*i
			self.do(basis)
			goal = ledges[i]
			idx = self.edge_locations.index(goal)
			faces = self.get_edge_faces(goal)
			move = ""
			if "L" in faces:
				if idx == 4: move = "L" 
				elif idx == 7: move = "l"
				elif idx == 11: move = "LL"
			elif "R" in faces:
				if idx == 5: self.do(commutator("r", self.cycle_three_edges)) #move = "UBu"
				if idx == 9: self.do(commutator("RR", self.cycle_three_edges))
				if idx == 6: self.do(commutator("R", self.cycle_three_edges)) #move = "uFU"
			elif "B" in faces:
				if idx == 8: move = "DD"
				elif idx == 0: self.do(inverse(self.cycle_three_edges))# cycle move = "r"
			elif "F" in faces and idx == 2: self.do(self.cycle_three_edges)
			basis += move
			self.do(move)
			idx = self.edge_locations.index(goal)
			if idx == 10 and self.edge_orientations[idx]==1: self.do(solutions[0])
			elif idx == 10 and self.edge_orientations[idx]==0: self.do(solutions[1])
			elif idx == 3 and self.edge_orientations[idx]==1: self.do(solutions[2])
			elif idx == 3 and self.edge_orientations[idx]==0: self.do(solutions[3])
			elif idx == 1 and self.edge_orientations[idx]==1: self.do(solutions[4])
			self.do(inverse(basis))
		return self

	def solve_last_ledge(self):
		idx = self.edge_locations.index(3)
		if idx == 10: self.do("uRlbbRldRRLL")
		elif idx == 8: self.do("UrLffrLDRRLL")
		elif idx == 0: self.do(inverse(self.cycle_left_three_edges))
		elif idx == 2: self.do(self.cycle_left_three_edges)
		if self.edge_orientations[3] == 1: self.do("FUdLLUUDDRurDDUULLDufU")
		return self

	def flip_midges(self):
		# Take easy path first, if it exists
		if self.edge_orientations[0] == 1 and self.edge_orientations[10] == 1: self.do(flip_10_0)
		if self.edge_orientations[0] == 1 and self.edge_orientations[2] == 1: self.do(flip_0_2)
		if self.edge_orientations[10] == 1 and self.edge_orientations[2] == 1: self.do(flip_10_0)
		if self.edge_orientations[2] == 1 and self.edge_orientations[8] == 1: self.do(flip_10_0)
		if self.edge_orientations[0] == 1 and self.edge_orientations[10] == 1: self.do(flip_10_0)

		# Takes more moves, but works 100% of the time
		if self.edge_orientations[0] == 1: self.do(flip_10_0)
		if self.edge_orientations[10] == 1: self.do(flip_10_8)
		if self.edge_orientations[8] == 1: self.do(flip_8_2)
		if self.edge_orientations[2] == 1: self.do(flip_0_2)
		return self

	def place_midges(self):
		if self.is_solved(): return self
		swap_two_horizontally = "UURRLLDDRRLL"
		midge_back_cycle = "UURlBBrL"
		midge_cycle = 'lRBBLrUU'

		if not self.edge_locations[10] == 10: # If the 10 isn't positioned, put it in 8
			while self.edge_locations[8] != 10: self.do(midge_cycle)
			# Then put swap it into 10
			self.do(swap_two_horizontally)

		# Now we just need to solve 2,8,0
		if self.edge_locations[2] == 0: self.do(midge_cycle)
		elif self.edge_locations[2] == 8: self.do(midge_back_cycle)

		return self

	def whereis(self, corner):
		idx = self.corner_locations.index(corner)
		print str(corner)+" at position (" + str(idx) + ") with orientation: " + str(self.corner_orientations[idx])

	def get_edge_faces(self, name):
		faces = []
		edge = self.edge_locations.index(name)
		if edge in self.back_face_edges: faces.append("B")
		elif edge in self.front_face_edges: faces.append("F")
		if edge in self.down_face_edges: faces.append("D")
		elif edge in self.up_face_edges: faces.append("U")
		if edge in self.left_face_edges: faces.append("L")
		elif edge in self.right_face_edges: faces.append("R")
		return faces

	def solve(self):
		if not self.is_valid():
			print "This is not a valid cube and cannot be solved"
			return False
		self.solve_four_bottom_corners()
		self.place_top_four_corners()
		self.twist_top_four_corners()
		self.solve_three_ledges()
		self.solve_four_redges()
		self.solve_last_ledge()
		self.flip_midges()
		self.place_midges()
		return self

	def loadPosition(self, sigma, tau, x, y):
		self.corner_locations = sigma
		self.edge_locations	= tau
		self.corner_orientations = x
		self.edge_orientations =	y
		return self
