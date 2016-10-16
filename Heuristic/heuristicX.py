from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.Knight import Knight
from sunfish import print_pos

#THINGS TO DO:
#REIMPLEMENT heuristicX
#unsure if checkmate works

#heuristic for player X
#position = configuration of chess board
#player = maximize or minimize player

def heuristicX(position, player):
	if position.is_checkmate():
		return 800000
	
	val1 = 0
	val2 = 0
	#create a dictionary of values and weights for player X
	piece_values = {}
	piece_values["K"] = 7
	piece_values["N"] = 2
	piece_values["R"] = 11
	
	king_index = position.generic_find("K")
	rook_index = position.generic_find("R")
	knight_index = position.generic_find("N")
	t_king_index = position.generic_find("k")
	#print_pos(position)

	if king_index:
		king = King(position, not player, king_index)
		paired_combo = position.paired_combo(player)
		
	if rook_index:
		rook = Rook(position, player, rook_index)
		#what_piece = rook.rook_piece_check()
	
	if knight_index:
		knight = Knight(position, not player, knight_index)
	
	only_king, their_king = position.only_king()

	#if an opponent piece can be eliminated do it
	if position.check_board() and king.king_safety():
		return 99999

	if not king.king_safety():
		return -1000
	
	if not rook.rook_safety() and king.king_movement().count("R") != 1:
		return -5
	
	
	if king.increase_movement(rook_index) and king_index // 10 != rook_index // 10\
	and king_index // 10 > rook_index // 10:
		return 20
	
	if rook_index // 10 == 8:
		return 10
	
		
	return 0
			
		