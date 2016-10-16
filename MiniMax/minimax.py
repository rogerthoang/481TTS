from Heuristic.heuristicX import heuristicX
from Heuristic.heuristicY import heuristicY
from sunfish import print_pos
import copy
#THINGS TO DO:
#-make sure minimax is implemented right (only tested at depth 1, check heuristic files for things to do)


def print_score_and_pos(score, new_position):
	print(score)
	if new_position is not None:
		print_pos(new_position)

#evaluate function that calls a heuristic function
#Note: a maximize player calls the mini side, so 
# Max  --------root
# Min  --------Leaf
#if the goal is to return a max value, player that was passed must be minimize,
#since player was switched by minimax
def evaluate(position, start_player):
	#print(position, player, node)
	if start_player:	
		return heuristicX(position, not start_player)
		
	else:
		return -heuristicY(position, not start_player)

#the function for performing minimax
#position = the position that was given either from main or new_position
#depth = how far we want to go (currently 1)
#player = maximize player or minimize
#node = contains a tuple that represents a pieces movement ex (89, 78)

def minimax(position, depth, player, start_player):
	test = []
	count = 0
	"""Returns a tuple (score, bestmove) for the position at the given depth"""
	if depth == 0: 
		return (evaluate(position, start_player), None)

	else: 
		#Maximizing player's section
		if player:
			bestscore = -float("inf")
			bestmove = None
			
			for node in position.gen_moves():
				copy_position = copy.deepcopy(position)
				new_position = copy_position.move(node)
				#new_position = new_position.rotate()
				score, move = minimax(new_position, depth - 1, False,  start_player)
				#print(score)
				print_score_and_pos(score, new_position)
				if score > bestscore: 
					bestscore = score
					bestmove = node
			return (bestscore, bestmove)
		
		else:
			#Minimizing player's section
			bestscore = float("inf")
			bestmove = None
			for node in position.gen_moves():
				copy_position = copy.deepcopy(position)
				new_position = copy_position.move(node)
				#new_position = new_position.rotate()
				score, move = minimax(new_position, depth - 1, True, start_player)
				#print(score)
				#print_score_and_pos(score, new_position)
				if score < bestscore: 
					#print("MINI")
					bestscore = score
					bestmove = node
			return (bestscore, bestmove)