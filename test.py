from termcolor import colored
from solver import RubiksCube
from simplegraph import SimpleGraph
import random

def passes(message, result):
	if result:
		print message + ": " + colored('passed', 'green')
	else: 
		print message + ": " + colored('FAILED', 'red')

class Tester(object):
	def __init__(self):
		self.test_number = 0
		self.passing = True
		self.error_msg = ""

	def evaluate(self, test, failmsg=""):
		self.test_number += 1
		if failmsg == "": failmsg = "Test " + str(self.test_number)
		if test: return self.passing, self.error_msg
		if self.passing:	self.passing = False
		self.error_msg = self.error_msg + "\n" + failmsg + ": " + colored('FAILED', 'red')
		return self.passing, self.error_msg

def randomMoveValidityTest(n):
	tester = Tester()
	cube = RubiksCube()
	passing = True
	for i in range(n):
		move = cube.randomMove()
		tester.evaluate(cube.is_valid(), "Move number: " + str(i) + ":" + str(move) + "\n" + cube.normalize().toString())
	passes("Random move validity test", tester.passing)
	if not tester.passing: print tester.error_msg

def randomMoveEqualityTest(n):
	tester = Tester()
	cube1 = RubiksCube()
	cube2 = RubiksCube()
	for i in range(n):
		move = cube1.randomMove()
		cube2.do(move)
		cube1 != cube2
		msg = cube1.toString() + "\n does not equal \n "+ cube2.toString()
		tester.evaluate(cube1 == cube2, msg)
	passes("Random moves equality check", tester.passing)
	if not tester.passing: print tester.error_msg

def simpleEqualityTest():
	cube = RubiksCube()
	solved = RubiksCube()
	passes("Starting Configuration Equality Check", cube == solved)
	#cube.do(["D", "Dinv", "U", "Uinv", "F", "Finv", "B", "Binv", "L", "Linv", "R", "Rinv"])
	cube.do("UDLRFBbfrldu")
	passes("Inverse Configuration Equality Check", cube == solved)

def simpleGraphTest():
	cube = RubiksCube()
	corners = SimpleGraph()
	corners.build_from_corners(cube.corner_locations)
	tester = Tester()
	tester.evaluate(len(corners.bfs(0,3)) == 2, "len(corners.bfs(0,3)) == 2")
	tester.evaluate(len(corners.bfs(0,2)) == 3, "len(corners.bfs(0,2)) == 3")
	tester.evaluate(len(corners.bfs(0,7)) == 4, "len(corners.bfs(0,7)) == 4")
	tester.evaluate(len(corners.bfs(0,1)) == 2, "len(corners.bfs(0,1)) == 2")
	passes("Simple Graph test: ", tester.passing)
	if not tester.passing: print tester.error_msg

def simplificationTest():
	tester = Tester()
	tester.evaluate(RubiksCube().simplify("UDLRFBbfrldu") == "", '"UDLRFBbfrldu" == ""')
	tester.evaluate(RubiksCube().simplify("bfrlduUDLRFB") == "", '"bfrlduUDLRFB" == ""')
	tester.evaluate(RubiksCube().simplify("uUu") == "u", '"uUu" == "u"')
	tester.evaluate(RubiksCube().simplify("BbB") == "B", '"BbB" == "B"')
	tester.evaluate(RubiksCube().simplify("") == "", '"" == ""')
	passes("Simplification test", tester.passing)
	if not tester.passing: print tester.error_msg

def multiplyByInverseTest(n, k):
	moves = RubiksCube().moves
	tester = Tester()
	for i in range(n):
		move = ""
		while random.random() > 1./k: #Average length k
			move = move + random.choice(moves)
		inverse = RubiksCube().inverse(move)
		tester.evaluate(RubiksCube().simplify(move + inverse) == "", '"' + move + inverse + '" == ""')
		tester.evaluate(RubiksCube().simplify(move + inverse) == "", '"' + inverse + move + '" == ""')
	passes("Inverse Multiplication Test", tester.passing)
	if not tester.passing: print tester.error_msg

def solveBottomCorners(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		msg = "Solve bottom corners of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		tester.evaluate(cube.corner_locations[4:] == (4,5,6,7) and cube.corner_orientations[4:] == (0,0,0,0), msg)
		cube.clear()
	passes("Solve bottom four corners", tester.passing)
	if not tester.passing: print tester.error_msg

def placeTopCorners(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		msg = "Place top corners of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		tester.evaluate(cube.corner_locations[:4] == (0,1,2,3), msg)
		cube.clear()
	passes("Place top four corners", tester.passing)
	if not tester.passing: print tester.error_msg

def twistTopCorners(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		cube.twist_top_four_corners()
		msg = "Twist top corners of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		tester.evaluate(cube.corner_orientations[:4] == (0,0,0,0), msg)
		cube.clear()
	passes("Twist top four corners", tester.passing)
	if not tester.passing: print tester.error_msg

def solveLedges(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		cube.twist_top_four_corners()
		cube.solve_three_ledges()
		msg = "Solve ledges of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		passed = True
		for i in (4,11,7):
			if cube.edge_locations[i] != i or cube.edge_orientations[i] != 0: passed = False
		tester.evaluate(passed, msg)
		cube.clear()
	passes("Solve ledges", tester.passing)
	if not tester.passing: print tester.error_msg

def solveRedges(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		cube.twist_top_four_corners()
		cube.solve_three_ledges()
		cube.solve_four_redges()
		msg = "Solve redges of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		passed = True
		for i in (1,5,6,9,4,11,7):
			if cube.edge_locations[i] != i or cube.edge_orientations[i] != 0: passed = False
		tester.evaluate(passed, msg)
		cube.clear()
	passes("Solve redges", tester.passing)
	if not tester.passing: print tester.error_msg

def solveLastLedge(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		cube.twist_top_four_corners()
		cube.solve_three_ledges()
		cube.solve_four_redges()
		cube.solve_last_ledge()
		msg = "Solve last ledge of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		passed = True
		for i in (1,5,6,9,4,11,7,3):
			if cube.edge_locations[i] != i or cube.edge_orientations[i] != 0: passed = False
		tester.evaluate(passed, msg)
		cube.clear()
	passes("Solve last ledge", tester.passing)
	if not tester.passing: print tester.error_msg

def flipMidges(n):
	tester = Tester()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		cube.twist_top_four_corners()
		cube.solve_three_ledges()
		cube.solve_four_redges()
		cube.solve_last_ledge()
		cube.flip_midges()
		msg = "Flip midges of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		passed = True
		for i in (1,5,6,9,4,11,7,3):
			if cube.edge_locations[i] != i or cube.edge_orientations[i] != 0: passed = False
		for i in (0,2,8,10):
			if cube.edge_orientations[i] != 0: passed = False
		tester.evaluate(passed, msg)
		cube.clear()
	passes("Flip midges", tester.passing)
	if not tester.passing: print tester.error_msg

def placeMidges(n):
	tester = Tester()
	solved = RubiksCube()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		cube.solve_four_bottom_corners()
		cube.place_top_four_corners()
		cube.twist_top_four_corners()
		cube.solve_three_ledges()
		cube.solve_four_redges()
		cube.solve_last_ledge()
		cube.flip_midges()
		cube.place_midges()
		msg = "Place midges of: \n" + prescramble + "\ninstead got:\n" + cube.toString()
		tester.evaluate(cube == solved, msg)
		cube.clear()
	passes("Place midges", tester.passing)
	if not tester.passing: print tester.error_msg

def testSolution(n):
	tester = Tester()
	solved = RubiksCube()
	cube = RubiksCube()
	for i in range(n):
		cube.scramble()
		prescramble = cube.toString()
		solution = cube.solve().history
		newcube = RubiksCube()
		newcube.loadPosition(cube.corner_locations, cube.edge_locations, cube.corner_orientations, cube.edge_orientations)
		newcube.do(solution)

		msg = "Solve: \n" + prescramble + "\ngot:\n" + cube.toString()
		tester.evaluate(newcube == solved, msg)
		cube.clear()
	passes("Full solution", tester.passing)
	if not tester.passing: print tester.error_msg
