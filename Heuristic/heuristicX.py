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
	t_knight_index = position.generic_find("n")
	#print_pos(position)

	if king_index:
		king = King(position, not player, king_index)
		paired_combo = position.paired_combo(player)
		
	if rook_index:
		rook = Rook(position, player, rook_index)
		#what_piece = rook.rook_piece_check()
	
	if knight_index:
		knight = Knight(position, player, knight_index)
	
	if t_king_index:
		their_king = King(position, not player, t_king_index)
		
	if t_knight_index:
		their_knight = Knight(position, not player, t_knight_index)
	
	#only_king, their_king = position.only_king()

	#if an opponent piece can be eliminated do it
	#if position.check_board() and king.king_safety():
	#	return 99999

	if not king.king_safety():
		return -1000
	#print(player)
	#print(rook.rook_safety(), their_knight.knight_movement(), their_knight.knight_movement().count("R") == 1)
	#print(their_knight.knight_movement().count("R") == 1)
	
	if not rook.rook_safety() and their_knight.knight_movement().count("R") == 1:
		return -5
	
	if not rook.rook_safety() and king.king_movement().count("R") != 1:
		return -5
	
	
	
	if not knight.knight_safety():
		return -1
	
	
	
	if rook.check_king_space(6):
		return 100 + (100 - abs(knight_index // 10 - t_king_index // 10))
	
	if king.increase_movement(t_king_index) and t_king_index // 10 == 2 or t_king_index % 10 == 8:
		return 40 + rook.trap_king()
	
	if rook_index // 10 > king_index // 10 and king.increase_movement(t_king_index):
		return 122
	
	if their_king.increase_movement(rook_index) and king.increase_movement(t_king_index):
		return 111
	
	if king.king_movement().count("R") == 1 :
		return rook.trap_king() + (9 - abs((rook_index // 10 - t_king_index// 10) + abs(9 - (king_index - t_king_index) )) )
	

	if king.increase_movement(rook_index) and rook_index // 10 != 9\
	and rook_index % 10 < t_king_index % 10:
		return 20
	
	
	if rook_index // 10 == 7 and king_index // 10 == 9\
	and knight_index // 10 == 9:
		return 10
	
		
	return 0
			
		