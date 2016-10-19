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
	
	king_index = position.generic_find("K")
	rook_index = position.generic_find("R")
	knight_index = position.generic_find("N")
	t_king_index = position.generic_find("k")
	t_knight_index = position.generic_find("n")

	if king_index:
		king = King(position, not player, king_index)
		paired_combo = position.paired_combo(player)
		
	if rook_index:
		rook = Rook(position, player, rook_index)
	else:
		return 0
	
	if knight_index:
		knight = Knight(position, player, knight_index)
		#m_knight = Knight(position, not player, knight_index)
	else:
		knight = None
	
	if t_king_index:
		their_king = King(position, not player, t_king_index)
		
	if t_knight_index:
		their_knight = Knight(position, not player, t_knight_index)
	

	#if an opponent piece can be eliminated do it
	if position.check_board() and (king.king_safety() or king.king_movement().count("k") == 1)\
	and (rook.rook_safety() or not rook.rook_safety() and king.king_movement().count("R") == 1):#and (king.king_movement().count("R") == 1 or king.increase_movement(rook_index)):
		return 99999

	if their_king.check_mated(king, knight, rook) and king.king_safety()\
	and (king.king_movement().count("R") == 1 or knight.knight_movement().count("R") == 1\
		or rook.rook_safety()):
		return 1000
	
	if not king.king_safety():
		return -1000

	if not knight.knight_safety():
		return -1
	
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
	
	#if rook.check_king_space(5):
	#	return 750 + rook.trap_king() + (100 - abs(knight_index - t_king_index))#+\
		#(5-abs(knight_index // 10 - king_index // 10)) + (5-abs(knight_index % 10 - king_index % 10))
	
	#if rook.check_king_space(7):
	#	return 650 + rook.trap_king()
	
	
	if (t_king_index // 10 == 2 or t_king_index % 10 == 8\
		or t_king_index // 10 == 8 or t_king_index % 10 == 1)\
	and rook.check_king_space(10)\
	and (king.increase_movement(rook_index) or king.king_movement().count("R") == 1)\
	and (their_king.increase_movement(rook_index) or their_king.king_movement().count("R") == 1) and their_king.increase_movement(king_index):
		if knight.knight_movement().count("k") == 1:
			#print("A")
			return 500 + rook.trap_king() 
		else:
			#print("B")
			return 500 + rook.trap_king() + (5 - abs(knight_index//10 - t_king_index//10)) + (5 - abs(knight_index % 10 - t_king_index % 10))#+\
			#(5-abs(rook_index // 10 - t_king_index // 10)) + (5-abs(rook_index % 10 - t_king_index % 10))
									   
	
	if rook.check_king_space(7) and king.king_movement().count("R") == 1\
	and their_king.increase_movement(king_index):
		#print("!")
		if knight.knight_movement().count("k") == 1:
			#print("?")
			return 300 + rook.trap_king()
		else:
			#print("#")
			return 100 + rook.trap_king() +\
		(10 - abs(king_index // 10 - t_king_index // 10))\
		+ (10 - abs(king_index % 10 - t_king_index % 10))+\
		(100 - abs(knight_index - t_king_index))
	

	if king.king_movement().count("R") == 1 :
		if king_index // 10 < rook_index // 10 and rook_index % 10 == king_index % 10:
			pass
		
		elif rook_index % 10 > t_king_index % 10:
			#print("84")
			return rook.trap_king() + (10 - abs(king_index % 10 - t_king_index% 10 ))
		
		elif rook_index % 10 < t_king_index % 10:
			#print("85")
			return rook.trap_king()+ (10 - abs(king_index % 10 - t_king_index% 10 )) + (10 - abs(king_index // 10 - t_king_index // 10 ))
		
		 
	if king.increase_movement(rook_index) and rook_index // 10 != 9\
	and rook_index % 10 < t_king_index % 10:
		return 20
	
	
	if rook_index // 10 == 8 and king_index // 10 == 9\
	and knight_index // 10 == 9:
		return 10
	
		
	return 0
			
		