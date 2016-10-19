class Knight:
	def __init__(self, board, end):
		self._board = board
		self._position = end
		self._knight_moves = []
	
	def populate_moves(self):
		self._knight_moves = [self._position + 8, self._position + 12,
						   self._position - 8, self._position - 12,
						   self._position + 21, self._position + 19,
						   self._position - 21, self._position - 19]
	def ret_position(self):
		return self._position
	
	def ret_moves(self):
		return self._knight_moves
	
	def knight_movement(self):
		self.populate_moves()
		board_piece_list = []
		#print(self._position, self._player)
		#print(self.ret_moves())
		
	
		for i in self._knight_moves:
			if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
			and self._board.get_board_piece(i) != "\n":
				board_piece_list.append(self._board.get_board_piece(i))
	
		if len(board_piece_list) > 0:
			return board_piece_list
						
		else:
			return []
		
		return None	
	
	def knight_safety(self):	
		max_knight = self._board.generic_find("n")
		max_king = self._board.generic_find("k")
		max_rook = self._board.generic_find("r")
		
		if max_knight:
			knight_piece = Knight(self._board, max_knight)
			if knight_piece.knight_movement().count("N") == 1:
				return False

		if max_king:
			from Pieces.King import King
			king_piece = King(self._board, max_king)
			if king_piece.king_movement().count("N") == 1:
				return False

		if max_rook:
			from Pieces.Rook import Rook
			rook_piece = Rook(self._board, max_rook)
			if rook_piece.rook_piece_check().count("N") == 1:
				return False

		return True
			
	def knight_follow_rook(self, piece):
		return abs(self._position - piece)
		
	def knight_corners(self, piece):
		knight_corners = [self._position + 11, self._position + 9,
						  self._position - 11, self._position - 9]
		
		for position in knight_corners:
			if piece == position:
				return True
			
		return False													