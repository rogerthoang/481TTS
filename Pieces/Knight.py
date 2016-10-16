class Knight:
	def __init__(self, board, player, end):
		self._board = board
		self._player = player
		self._position = end
		
	def ret_position(self):
		return self._position
	
	def knight_movement(self):
		board_piece_list = []
			
		knight_movement = [self._position + 8, self._position + 12,
						   self._position - 8, self._position - 12,
						   self._position + 21, self._position + 19,
						   self._position - 21, self._position - 19]
		if not self._player:
			for i in knight_movement:
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "K" \
				and self._board.get_board_piece(i) != "N" and self._board.get_board_piece(i) != "R":
					#print("###########{}".format(self._board.get_board_piece(i)))
					board_piece_list.append(self._board.get_board_piece(i))
					
			if len(board_piece_list) > 0:
				return board_piece_list
					
		
			else:
				return []
		
		#otherwise, look for maximize player's pieces
		else:
			for i in knight_movement:
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "k" \
				and self._board.get_board_piece(i) != "n" and self._board.get_board_piece(i) != "r":
					board_piece_list.append(self._board.get_board_piece(i))
					
					#print("FOUND KING at {0} {1}".format(self._board.get_board_piece(i), i))
					#print("FOUND : {0} at {1} which is {2}".format(board_piece_list, i, self._board.get_board_piece(i)))
			#print(board_piece_list)		
			if len(board_piece_list) > 0:
				return board_piece_list
					
		
			else:
				return []
		
		#if no one is close, return False, None
		return None	
	
	def knight_safety(self):
		if not self._player:
			their_knight = self._board.generic_find("n")
			their_king = self._board.generic_find("k")
			if their_knight:
				knight_piece = Knight(self._board, not self._player, their_knight)

				if knight_piece.knight_movement().count("N") == 1:
					return False
			
			if their_king:
				from Pieces.King import King
				king_piece = King(self._board, not self._player, their_king)
				if king_piece.king_movement().count("N") == 1:
					return False
			
			return True
		
		else:
			max_knight = self._board.generic_find("n")
			max_king = self._board.generic_find("k")
			max_rook = self._board.generic_find("r")
			
			if max_knight:
				knight_piece = Knight(self._board, not self._player, max_knight)
				what_piece = knight_piece.knight_movement()
				if knight_piece.knight_movement().count("N") == 1:
					return False
			
			if max_king:
				from Pieces.King import King
				king_piece = King(self._board, not self._player, max_king)
				what_piece = king_piece.king_movement()
				if king_piece.king_movement().count("N") == 1:
					return False
			
			if max_rook:
				from Pieces.Rook import Rook
				rook_piece = Rook(self._board, not self._player, max_rook)
				what_piece = rook_piece.rook_piece_check()
				if rook_piece.rook_piece_check().count("N") == 1:
					return False
			
			return True
			
	def knight_follow_rook(self, piece):
		return abs(self._position - piece)
		
		
		
															