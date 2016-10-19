class Board_Piece:
	def __init__(self):
		_xcount = 3
		_ycount = 2
		
		
	def decrement_count(self, player):
		if player:
			_xcount -= 1
		else:
			_ycount -=1