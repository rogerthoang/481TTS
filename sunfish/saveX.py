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
		m_knight = Knight(position, not player, knight_index)
	
	if t_king_index:
		their_king = King(position, not player, t_king_index)
		
	if t_knight_index:
		their_knight = Knight(position, not player, t_knight_index)
	

	#if an opponent piece can be eliminated do it
	if position.check_board() and (king.king_safety() or king.king_movement().count("k") == 1)\
	and (rook.rook_safety() or not rook.rook_safety() and king.king_movement().count("R") == 1)and (king.king_movement().count("R") == 1 or king.increase_movement(rook_index)):
		return 99999

	if their_king.check_mated(king, knight, rook) and king.king_safety()\
	and (king.king_movement().count("R") == 1 or knight.knight_movement().count("R") == 1\
		or rook.rook_safety()):
		return 1000
	
	if not king.king_safety():
		return -1000

	if not knight.knight_safety():
		return -1
	
	#print(rook.check_king_space(7) ,knight.knight_movement().count("k") == 1)
	#if rook.check_king_space(7) and knight.knight_movement().count("k") == 1:
	#	return 500
	
	if t_knight_index:
		if king.king_movement().count("R") == 1 and their_king.king_movement().count("R") == 1\
		and their_knight.knight_movement().count("R") == 0 and not rook.check_king_space(10):
			#print("?")
			return 200 + rook.trap_king() + \
		(10 - abs(king_index // 10 - rook_index // 10)) + \
		(10 - abs(knight_index // 10 - king_index // 10))+\
		(100 - abs(knight_index - king_index ))
		#(10 - abs(king_index // 10 - t_king_index // 10))
	
	if t_knight_index:
		if not rook.rook_safety() and their_knight.knight_movement().count("R") == 1:
			return -5
	
	if not rook.rook_safety() and king.king_movement().count("R") != 1:
		return -4
	
	#if not rook.rook_safety() and king.king_movement().count("R") == 1: and position.pair_two_piece(knight_index, t_king_index):
	#	return 1000 + rook.trap_king()+ (50 - abs(knight_index - t_king_index))
	
	#if not rook.rook_safety():
	#	return -3
	
	
	#print(king.increase_movement(rook_index), king.king_movement().count("R") == 1, their_king.increase_movement(rook_index), their_king.king_movement().count("r") == 1)
	if (t_king_index // 10 == 2 or t_king_index % 10 == 8\
		or t_king_index // 10 == 8 or t_king_index % 10 == 1)\
	and rook.check_king_space(10)\
	and (king.increase_movement(rook_index) or king.king_movement().count("R") == 1)\
	and (their_king.increase_movement(rook_index) or their_king.king_movement().count("R") == 1) and their_king.increase_movement(king_index):
		if knight.knight_movement().count("k") == 1:
			return 600 + rook.trap_king() 
		else:
			return 500 + rook.trap_king()+ (100 - abs(knight_index - t_king_index))
									   
	
	
	if rook.check_king_space(7) and king.king_movement().count("R") == 1\
	and their_king.increase_movement(king_index):
		#print("!")
		return 100 + rook.trap_king() +\
	(10 - abs(king_index // 10 - t_king_index // 10))\
	+ (10 - abs(king_index % 10 - t_king_index % 10))+\
	(100 - abs(knight_index - t_king_index))
	
	if rook.check_king_space(10) and king.increase_movement(t_king_index):
		#print("?")
		return 100 + rook.trap_king()
	
	

	#if their_king.increase_movement(rook_index) and king.increase_movement(t_king_index):
	#	return 111
	
	if king.increase_movement(t_king_index) and (t_king_index // 10 == 2 or t_king_index % 10 == 8\
												 or t_king_index // 10 == 8 or t_king_index % 10 == 1):
		return 40 + rook.trap_king() 
	
	if king.king_movement().count("R") == 1 :
		#return rook.trap_king() + (9 - abs((rook_index // 10 - t_king_index// 10) + abs(9 - (king_index - t_king_index) ) + abs(king_index - rook_index) ))
		#return rook.trap_king() + (50 - abs(rook_index - king_index)) + (50 - abs(king_index - t_king_index))
		if king_index // 10 < rook_index // 10 and rook_index % 10 == king_index % 10:
			#return rook.trap_king() #+ (100 - abs(knight_index - t_knight_index))
			#return 200 + (5 - abs(rook_index % 10 - t_king_index % 10))
			pass
		
		elif rook_index % 10 > t_king_index % 10:
			print("84")
			return rook.trap_king() + (10 - abs(king_index % 10 - t_king_index% 10 ))
		
		elif rook_index % 10 < t_king_index % 10:
			print("85")
			return rook.trap_king()+ (10 - abs(king_index % 10 - t_king_index% 10 )) + (10 - abs(king_index // 10 - t_king_index // 10 ))
		
		 
		
		
	if king.increase_movement(rook_index) and rook_index // 10 != 9\
	and rook_index % 10 < t_king_index % 10:
		return 20
	
	
	if rook_index // 10 == 8 and king_index // 10 == 9\
	and knight_index // 10 == 9:
		return 10
	
		
	return 0
			
		