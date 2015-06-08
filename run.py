import test
import solver
from solver import RubiksCube
from termcolor import colored
import math 

light = (1, 'blue', 'light')
moderate = (10, 'yellow', 'moderate')
heavy = (100, 'red', 'heavy')
power, color, stress = heavy

print "Testing Rubiks Cube Solver"
print 				"Test stress level:                      " + colored(stress, color) 
print colored("------------------------------------------------", 'grey')
test.randomMoveValidityTest(int(math.log(power)*1000))
test.simpleEqualityTest()
test.randomMoveEqualityTest(int(math.log(power)*1000))
test.simpleGraphTest()
test.simplificationTest()
test.multiplyByInverseTest(power*100, 7)
test.solveBottomCorners(power*100)
test.placeTopCorners(power*100)
test.twistTopCorners(power*100)
test.solveLedges(power*10)
test.solveRedges(power*10)
test.solveLastLedge(power*10)
test.flipMidges(power*10)
test.placeMidges(power*10)
test.testSolution(power*100)

def execute_macro(operation):
	cube = RubiksCube()
	cube.do(getattr(RubiksCube(), operation)).normalize()
	print operation + ": "
	print cube.toString()

pos1 = ((6, 1, 3, 4, 5, 2, 0, 7),(3, 2, 1, 4, 6, 7, 5, 9, 10, 11, 0, 8),(1, 2, 0, 0, 2, 1, 0, 0),(0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0))
pos2 = ((1, 6, 3, 2, 4, 7, 0, 5),(8, 7, 1, 4, 0, 9, 5, 6, 3, 10, 11, 2),(0, 1, 1, 1, 2, 1, 2, 1),(0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1))
pos3 = ((2, 1, 4, 0, 6, 7, 5, 3),(10, 4, 11, 1, 9, 3, 8, 5, 6, 7, 0, 2),(1, 1, 0, 1, 1, 1, 1, 0),(1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1))
pos4 = ((1, 7, 3, 0, 4, 2, 5, 6),(2, 7, 11, 9, 8, 10, 0, 3, 5, 4, 1, 6),(0, 2, 0, 0, 2, 2, 2, 1),(0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0))
pos5 = ((1, 0, 3, 6, 5, 4, 2, 7),(7, 8, 3, 5, 0, 9, 6, 10, 4, 2, 1, 11),(0, 0, 0, 2, 1, 2, 2, 2),(1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1))
pos6 = ((2, 5, 6, 0, 3, 4, 1, 7),(10, 11, 5, 7, 1, 6, 8, 3, 4, 9, 0, 2),(0, 2, 1, 2, 0, 2, 1, 1),(0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1))# for operation in RubiksCube().cube_permutations:
pos7 = ((3, 6, 5, 0, 4, 1, 2, 7),(1, 3, 9, 6, 4, 8, 5, 0, 10, 11, 2, 7),(1, 1, 0, 2, 2, 2, 2, 2),(0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1))
pos8 = ((5, 4, 3, 0, 6, 1, 2, 7),(8, 10, 6, 4, 0, 3, 9, 11, 2, 1, 5, 7),(0, 1, 0, 1, 1, 1, 0, 2),(0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0))
pos9 = ((3, 4, 7, 5, 0, 2, 6, 1),(7, 9, 1, 11, 2, 5, 4, 8, 6, 3, 0, 10),(1, 1, 0, 0, 1, 0, 1, 2),(1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0))
pos10 = ((5, 2, 7, 4, 1, 3, 6, 0),(11, 5, 9, 8, 1, 2, 6, 0, 10, 3, 7, 4),(1, 0, 1, 2, 1, 0, 2, 2),(0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1))
pos11 = ((7, 0, 6, 3, 2, 4, 1, 5),(4, 5, 3, 1, 7, 2, 10, 9, 0, 6, 11, 8),(1, 1, 0, 2, 1, 2, 0, 2),(1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0))
pos12 = ((0, 3, 7, 5, 4, 2, 6, 1),(2, 9, 4, 0, 8, 10, 7, 6, 3, 5, 1, 11),(2, 1, 2, 2, 1, 0, 0, 1),(0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0))
pos13 = ((1, 4, 0, 7, 3, 5, 2, 6),(10, 2, 0, 4, 7, 6, 1, 3, 8, 11, 5, 9),(2, 1, 2, 0, 2, 1, 2, 2),(1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0))
pos14 = ((7, 5, 3, 1, 6, 0, 4, 2),(0, 10, 11, 6, 5, 3, 8, 1, 4, 7, 9, 2),(1, 2, 1, 1, 2, 2, 2, 1),(0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0))
# 	cube = RubiksCube()
# 	cube.do(operation).normalize()
# 	print operation + ": "
# 	print cube.toString()



# execute_macro("twist_two_corners")
# execute_macro("flip_two_edges")
# for macro in ["flip_two_edges",	"twist_two_corners",	"cycle_three_edges", "cycle_three_corners", "swap_two_corners_and_two_edges"]:
# 	execute_macro(macro)

# cubewe()
#print cube.toString()



