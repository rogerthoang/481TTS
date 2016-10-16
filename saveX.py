from Pieces.Rook import Rook
from Pieces.King import King
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
	
	#print_pos(position)

	if king_index:
		king = King(position, not player, king_index)
		paired_combo = position.paired_combo(player)
		
	if rook_index:
		rook = Rook(position, player, rook_index)
		what_piece = rook.rook_piece_check()
	
	only_king, their_king = position.only_king()

	if their_king:
		tk= King(position, not player, their_king)
	
	#if an opponent piece can be eliminated do it
	if position.check_board():
		return 99999

	if not king.king_safety():
		return -1000
	
	if not rook.rook_safety():
		return -5
	
	if what_piece == "n":
		return piece_values["R"] * 2
	
	
	if paired_combo and only_king and king.hug_sides() and king.increase_movement(their_king):
		return 7777
	
	if paired_combo and only_king and rook.check_king_space(5):
		if king.hug_sides():
			return 222
	
	if paired_combo and only_king and rook.check_king_space(5):
		if tk.increase_movement(king_index):
			return 200
	
	if paired_combo and only_king and tk.increase_movement(rook_index) and king.king_movement() == "R":
		return 111

	if paired_combo and only_king and king.king_movement() == "R":
		return rook.trap_king()
	
	if paired_combo and only_king and king.king_movement() == "R":
		return 50
	
	if only_king and position.pair_row_king_rook():
		return 48
	
	if what_piece == "k":
		return piece_values["R"] * 3
	else:
		return 0

	
	return piece_values[piece]
			
		