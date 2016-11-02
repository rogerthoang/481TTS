from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.Knight import Knight

#heuristic for player X
#position = configuration of chess board

def heuristicX(position):
	try:
		if position.is_checkmate():
			return 800000

		king_index = position.generic_find("K")
		rook_index = position.generic_find("R")
		knight_index = position.generic_find("N")
		t_king_index = position.generic_find("k")
		t_knight_index = position.generic_find("n")

		if king_index:
			king = King(position, king_index)

		if rook_index:
			rook = Rook(position,  rook_index)

		if knight_index:
			knight = Knight(position, knight_index)

		if t_king_index:
			their_king = King(position, t_king_index)

		if t_knight_index:
			their_knight = Knight(position, t_knight_index)

		if king.king_movement().count("k") == 1 and king.king_safety():
			return 99999

		if rook_index and king_index:
			if rook.rook_piece_check().count("k") == 1 and rook.rook_safety() and not king.king_safety()\
			and king.king_movement().count("k") != 1:
				return 999

		#if minimize player can eliminate an opponent piece do it
		if rook_index:
			if position.check_board() and rook.rook_safety():
				return 99999

		#if an opponent piece can be eliminated do it
		if rook_index:
			if position.check_board() and (king.king_safety() or king.king_movement().count("k") == 1)\
			and (rook.rook_safety() or not rook.rook_safety() and king.king_movement().count("R") == 1):
				return 99999

		if knight_index and rook_index:
			if their_king.check_mated(king, knight, rook) and king.king_safety()\
			and (king.king_movement().count("R") == 1 or knight.knight_movement().count("R") == 1\
				or rook.rook_safety()):
				return 1000

		if not king.king_safety():
			return -1000

		if knight_index and rook_index:
			if not knight.knight_safety() and king.king_movement().count("N") == 0\
			and rook.rook_piece_check().count("N") == 0:
				return -1

		if t_knight_index and rook_index and knight_index:
			if king.king_movement().count("R") == 1 and their_king.king_movement().count("R") == 1\
			and their_knight.knight_movement().count("R") == 0 and not rook.check_king_space(t_king_index,10):
				return 200 + rook.trap_king(t_king_index) + \
			(10 - abs(king_index // 10 - rook_index // 10)) + \
			(10 - abs(knight_index // 10 - king_index // 10))+\
			(100 - abs(knight_index - king_index ))

		if t_knight_index and rook_index:
			if not rook.rook_safety() and their_knight.knight_movement().count("R") == 1:
				return -5

		if rook_index:
			if not rook.rook_safety() :
				return -4

		if t_king_index and rook_index and t_knight_index and knight_index:
			if (t_king_index // 10 == 2 or t_king_index % 10 == 8\
				or t_king_index // 10 == 8 or t_king_index % 10 == 1)\
			and rook.check_king_space(t_king_index, 10)\
			and (king.increase_movement(rook_index) or king.king_movement().count("R") == 1)\
			and (their_king.increase_movement(rook_index) or their_king.king_movement().count("R") == 1)\
			and their_king.increase_movement(king_index):
				if knight.knight_movement().count("k") == 1:
					return 500 + rook.trap_king(t_king_index) 
				else:
					return 500 + rook.trap_king(t_king_index) + (5 - abs(knight_index//10 - t_king_index//10))\
					+ (5 - abs(knight_index % 10 - t_king_index % 10))					   

		if rook_index and knight_index:
			if rook.check_king_space(t_king_index, 7) and king.king_movement().count("R") == 1\
			and their_king.increase_movement(king_index):
				if knight.knight_movement().count("k") == 1:
					return 300 + rook.trap_king(t_king_index)
				else:
					return 100 + rook.trap_king(t_king_index) +\
				(10 - abs(king_index // 10 - t_king_index // 10))\
				+ (10 - abs(king_index % 10 - t_king_index % 10))+\
				(100 - abs(knight_index - t_king_index))

		if rook_index:
			if king.king_movement().count("R") == 1 :
				if king_index // 10 < rook_index // 10 and rook_index % 10 == king_index % 10:
					pass

				elif rook_index % 10 > t_king_index % 10: 
					return rook.trap_king(t_king_index) + (10 - abs(king_index % 10 - t_king_index% 10 ))

				elif rook_index % 10 < t_king_index % 10:
					return rook.trap_king(t_king_index)+ (10 - abs(king_index % 10 - t_king_index% 10 ))\
					+ (10 - abs(king_index // 10 - t_king_index // 10 ))

		if rook_index:	 
			if king.increase_movement(rook_index) and rook_index // 10 != 9\
			and rook_index % 10 < t_king_index % 10:
				return 20

		if rook_index and knight_index:
			if rook_index // 10 == 8 and king_index // 10 == 9\
			and knight_index // 10 == 9:
				return 10
		
		if rook_index:
			return 4 - abs(rook_index // 10 - king_index // 10) + 4 - abs(rook_index % 10 - king_index % 10)
	
	except Exception as error:
		with open("error.txt", "a") as e:
			e.write(str(error) + "\n")
			
		return 1
		
	