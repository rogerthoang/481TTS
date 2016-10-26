from Pieces.King import King
from Pieces.Knight import Knight
from Pieces.Rook import Rook

#heuristic for player Y
#position = configuration of chess board
def heuristicY(position):
	try:
		if position.is_checkmate():
			return 900000

		king_index = position.generic_find("K")
		knight_index = position.generic_find("N")
		max_rook_index = position.generic_find("r")
		max_king_index = position.generic_find("k")
		max_knight_index = position.generic_find("n")

		if king_index:
			king = King(position,  king_index)
		else:
			return -99999

		if knight_index:
			knight = Knight(position, knight_index)


		if max_rook_index:
			max_rook = Rook(position,  max_rook_index)

		if max_king_index:
			max_king = King(position,  max_king_index)


		if max_knight_index:
			max_knight = Knight(position,  max_knight_index)
		else:
			max_knight = None


		#check for king's safety, if this position is poor return a low value
		if not king.king_safety():
			return -1000

		if knight_index:
			if not knight.knight_safety():
				return -999

		#if minimize player can eliminate an opponent piece do it
		if position.check_board():
			return 99999

		if knight_index:
			if knight.knight_movement().count("r") == 1:
				return 157

		if king.king_movement().count("r") == 1 and knight_index:
			return 50 + (50 - abs(knight_index - max_rook_index))

		if king_index % 10 == 5 and knight_index and max_rook_index:
			return 20 + (5 - abs(king_index // 10 - 5)) + (5- abs(knight_index - max_rook_index))

		if knight_index and max_rook_index:
			return abs(knight_index % 10 - max_rook_index % 10) + abs(knight_index // 10 - max_rook_index // 10)\
			+ (5- abs(king_index // 10 - 5))

		elif max_rook_index:
			return abs(king_index % 10 - max_rook_index % 10) + abs(king_index // 10 - max_rook_index // 10)

		else:
			return abs(king_index // 10 - 5) + abs(king_index % 10 - 5)
	
	except:
		pass
	