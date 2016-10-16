from Pieces.King import King
from Pieces.Knight import Knight

#NEED TO DO:
#-Improve King's AI (can avoid being in danger, but moves away unintelligently)
#-Program the knight to move smartly
#-Unsure if checkmate works

#heuristic for player Y
#position = configuration of chess board
#player = maximize or minimize player
#node = the tuple that contains the player's move
def heuristicY(position, player):
	if position.is_checkmate():
		return 900000
	
	#create a dictionary of piece and value for player Y
	piece_values = {}
	piece_values["K"] = 5
	piece_values["N"] = 1
	
	king_index = position.generic_find("K")
	knight_index = position.generic_find("N")
	
	if king_index:
		king = King(position, player, king_index)
	
	if knight_index:
		knight = Knight(position, player, knight_index)
	
	#check for king's safety, if this position is poor return a low value
	if not king.king_safety():
		return 1
	
	#if minimize player can eliminate an opponent piece do it
	if position.check_board():
		return 99999
	
	return 5
	
	
	