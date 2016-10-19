class King:
	def __init__(self, board, end):
		self._board = board
		self._position = end
		self._kings_moves = []
		
	def populate_moves(self):
		self._kings_moves = [self._position + 1, self._position - 1, 
						   self._position + 9, self._position + 10, self._position + 11,
						   self._position - 9, self._position - 10, self._position - 11]
		
	def ret_kings_moves(self):
		return self._kings_moves
	
	def ret_king_position(self):
		return self._position
	
	#check to see if anyone is in king's attack range
	def king_movement(self):
		board_piece_list = []
		#A king can only move in any direction by one
		self.populate_moves()
		
		for i in self._kings_moves:
			if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
			and self._board.get_board_piece(i) != "\n":
					board_piece_list.append(self._board.get_board_piece(i))
		
		if len(board_piece_list) > 0:
			return board_piece_list
					
		else:
			return []

		#if no one is close, return None
		return None	
	
	#Check to see if king is safe from all possible moves your opponent can make
	def king_safety(self):
		your_king = self._board.generic_find("K")
		rook = self._board.generic_find("r")

		if rook:
			from .Rook import Rook
			their_rook = Rook(self._board, rook)
			if their_rook.rook_piece_check().count("K") == 1:
				return False

		knight = self._board.generic_find("n")
		if knight:
			from .Knight import Knight
			their_knight = Knight(self._board, knight)
			if their_knight.knight_movement().count("K") == 1:
				return False

		king = self._board.generic_find("k")
		if king:
			their_king = King(self._board, king)
			if their_king.king_movement().count("K") == 1:
				return False   

		return True
	
	#NOT USED
	def king_stalk_rook(self):
		your_rook = self._board.generic_find("R")
		piece = self.king_movement()
		
		val = abs(self._position - your_rook)

		return val
	
	#create a 2-radii movement block around the king to check if the rook is there
	def increase_movement(self, your_rook):
		extended_list = [self._position - 18, self._position - 19, self._position - 20, self._position - 21, self._position - 22,
                         self._position - 8, self._position - 12, 
                         self._position - 2, self._position + 2,
                         self._position + 8, self._position + 12,
                         self._position + 18, self._position + 19, self._position + 20, self._position + 21, self._position + 22]
		
		for position in extended_list:
			if position == your_rook:
				return True
			
		return False
	
	#move king to optimal position to capture king, called when the opponent king has very little
	#space to move
	def hug_sides(self):
		if self._position // 10 == 2:
			return True
		elif self._position % 10 == 2:
			return True
		return False
	
	def rook_follow_king(self):
		your_rook = self._board.generic_find("R")
		their_king = self._board.generic_find("k")
		
		if your_rook // 10 < self._position // 10 \
		and self._position % 10 > their_king % 10:
			#top left
			return [self._position - 11, self._position - 10]
			
			
		elif your_rook // 10 < self._position // 10 \
		and self._position % 10 < their_king % 10:
			#top right
			return [self._position - 9, self._position - 10]
			
		elif your_rook // 10 > self._position // 10\
		and self._position % 10 > their_king % 10:
			#bottom leftt
			return [self._position + 9, self._position + 10]
			
		elif your_rook // 10 > self._position // 10\
		and self._position % 10 < their_king % 10:
			#bottom right
			return [self._position + 10, self._position + 11]
			
		else:
			return []
		
	#False is lower, True is upper
	def check_mated(self, king, knight, rook):
		viable_move_list = []
		limit = 0

		self.populate_moves()
		
		for position in self._kings_moves:
			if position // 10 > 1 and position // 10 < 10\
			and position % 10 > 0 and position % 10 < 9:
				viable_move_list.append(position)
		
		viable_move_list.append(self._position)
		
		if king:
			king.populate_moves()
			king_moves = king.ret_kings_moves()
			for position in king_moves:
				if viable_move_list.count(position) == 1:
					viable_move_list.pop(viable_move_list.index(position))
					
		if knight:
			knight.populate_moves()
			knight_moves = knight.ret_moves()
			for position in knight_moves:
				if viable_move_list.count(position) == 1:
					viable_move_list.pop(viable_move_list.index(position))
					
		if rook:
			rook_moves = []
			hori_lower, hori_upper = rook.rook_hori_movement()
			vert_lower, vert_upper = rook.rook_vert_movement()
			for num in range(hori_lower, hori_upper + 1):
				rook_moves.append(num)
				
			for num in range(vert_lower, vert_upper + 1, 10):
				rook_moves.append(num)
				
			for position in rook_moves:
				if viable_move_list.count(position) == 1:
					viable_move_list.pop(viable_move_list.index(position))

		if len(viable_move_list) == 0:
			return True
		else:
			return False		