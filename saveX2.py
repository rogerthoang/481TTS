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
	
	#print(position.pair_two_piece(rook_index, knight_index),
	#position.pair_two_piece(rook_index, t_king_index),
	#rook_index % 10 == 8 ,knight.knight_movement() == "R",
	#	 king_index % 10 == 8, 100 -king.king_stalk_rook())
	
	#if position.pair_two_piece(rook_index, t_king_index)\
	#and position.pair_two_piece(rook_index, king_index)\
	#and position.pair_two_piece(king_index, t_king_index):
	
	#if position.pair_two_piece(rook_index, t_king_index)\
	#and position.pair_two_piece(rook_index, king_index)\
	#and abs(rook_index % 10 - king_index % 10) == 0\
	#and king_index % 10 == rook_index % 10:
#		return 660

	#if position.pair_two_piece(rook_index, t_king_index)\
	#and position.pair_two_piece(rook_index, king_index)\
	#and king_index % 10 < rook_index % 10:
#		return 680

	#if position.pair_two_piece(rook_index, t_king_index)\
	#and position.pair_two_piece(rook_index, king_index):
		
	if position.pair_two_piece(rook_index, t_king_index)\
	and position.pair_two_piece(rook_index, king_index)\
	and king_index % 10 > rook_index % 10\
	and king.rook_follow_king().count(rook_index) == 1: 
		#print(king.rook_follow_king().count(rook_index) == 1)
		return 680
		
		
	if position.pair_two_piece(rook_index, t_king_index)\
	and position.pair_two_piece(rook_index, king_index):
		fake_king_rook = King(position, not player, rook_index)
	#	print(fake_king_rook.king_movement().count("K"), rook_index % 10 == king_index % 10)
		if fake_king_rook.king_movement().count("K") == 1\
		and rook_index % 10 > king_index % 10 and rook_index // 10 != king_index // 10:
			
			val1 = 670
			#return 670

	if position.pair_two_piece(rook_index, t_king_index)\
	and position.pair_two_piece(rook_index, king_index):
		fake_king_rook = King(position, not player, rook_index)
	#	print(fake_king_rook.king_movement().count("K"), rook_index % 10 == king_index % 10)
		if fake_king_rook.king_movement().count("K") == 1\
		and rook_index % 10 == king_index % 10 :
			
			val2 = 660 
			#return 660
		
	if val1 != 0 or val2 != 0:
		if val1 > val2:
			return val1
		else:
			return val2

	if position.pair_two_piece(rook_index, t_king_index)\
	and position.pair_two_piece(rook_index, king_index)\
	and abs(rook_index % 10 - king_index % 10) == 1\
	and king_index % 10 < rook_index % 10:
		return 650
	
	
	if position.pair_two_piece(rook_index, t_king_index)\
	and king.king_movement().count("R") == 1:
		return 600
	
	if position.pair_two_piece(rook_index, t_king_index)\
	and king.increase_movement(rook_index):
		return 450 + rook.trap_king()
	
	
	if position.pair_two_piece(rook_index, knight_index) \
	and position.pair_two_piece(rook_index, t_king_index) \
	and rook_index % 10 == 8 and knight.knight_movement().count("R") == 1\
	and king_index % 10 == 8:
		return 420 + (100 - king.king_stalk_rook())
	
	if position.pair_two_piece(rook_index, knight_index) \
	and position.pair_two_piece(rook_index, t_king_index) \
	and rook_index % 10 == 8 and knight.knight_movement().count("R") == 1:
		return 400 + (king_index % 10)
	
	
	if t_king_index and rook_index:
		if position.pair_two_piece(t_king_index, rook_index) and rook.check_king_space(10) \
		and rook_index % 10 == 8 and knight.knight_movement().count("R") == 1:
			return 300
	
	if t_king_index and rook_index:
		if position.pair_two_piece(t_king_index, rook_index) and rook.check_king_space(10) \
		and rook_index % 10 == 8:
			return 200 - knight.knight_follow_rook(rook_index)
			#return knight.knight_follow_rook(t_king_index)
	
	if rook.check_king_space(10):
		return rook.trap_king()
		
		

	
	return 0
			
		