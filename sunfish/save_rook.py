class Rook:
	def __init__(self, board, player, end):
		self._board = board
		self._player = player
		self._position = end

	def get_position(self):
		return self._position
		
	#loop through all possible rook moves to find if any pieces are in the rook's range
	def rook_piece_check(self):
		board_piece_list = []
		h_lower_limit, h_upper_limit = self.rook_hori_movement()

		#if maximize, look for possible pieces to eliminate
		if not self._player:
			for i in range(h_lower_limit, h_upper_limit + 1):
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "K" \
				and self._board.get_board_piece(i) != "N" and self._board.get_board_piece(i) != "R":
					board_piece_list.append(self._board.get_board_piece(i))
			
			
			v_lower_limit, v_upper_limit = self.rook_vert_movement()
			for i in range(v_lower_limit, v_upper_limit + 1, 10):
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "K" \
				and self._board.get_board_piece(i) != "N" and self._board.get_board_piece(i) != "R":
					board_piece_list.append(self._board.get_board_piece(i))
			
			
			if len(board_piece_list) > 0:
				return board_piece_list
					
	
			else:
				return []

		#if minimize, check if rook can attack your pieces		
		else:
			for i in range(h_lower_limit, h_upper_limit + 1):
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "k" \
				and self._board.get_board_piece(i) != "n" and self._board.get_board_piece(i) != "r":
					board_piece_list.append(self._board.get_board_piece(i))
			


			v_lower_limit, v_upper_limit = self.rook_vert_movement()
			for i in range(v_lower_limit, v_upper_limit + 1, 10):
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "k" \
				and self._board.get_board_piece(i) != "n" and self._board.get_board_piece(i) != "r":
					board_piece_list.append(self._board.get_board_piece(i))
			
			#print(board_piece_list)
			if len(board_piece_list) > 0:
				return board_piece_list
					
		
			else:
				return []

		return None

	#find the possible horizontal movement a rook can make
	def rook_hori_movement(self):
		#print(self._position)
		if self._position % 10 == 1:
			upper_limit = self._position + 7
			return self._position, upper_limit
		elif self._position % 10 == 8:
			lower_limit = self._position - 7
			return lower_limit, self._position
		else:
			current = self._position % 10
			upper = 8 - current
			lower = current - 1
			lower_limit = self._position - lower
			upper_limit = self._position + upper
			return lower_limit, upper_limit

	#find the possible vertical movement a rook can make
	def rook_vert_movement(self):
		if self._position / 10 == 2:
			lower_limit = self._position + 7
			return lower_limit, self._position

		elif self._position / 10 == 9:
			upper_limit = self._position - 7
			return self._position, upper_limit

		else:
			current = self._position % 10
			upper_limit = 90 + current
			lower_limit =  20 + current
			return lower_limit, upper_limit
	
	#check to see if the rook is safe from the opponent's king and knight
	def rook_safety(self):
		#Check to see if king is safe from all possible moves your opponent can make
		your_rook = self._position

		#MAXIMIZE only
		their_king = self._board.generic_find("k")
		
		if their_king is not None:
			from .King import King
			tk = King(self._board, not self._player, their_king)
			#piece = tk.king_movement()
			
			if tk.king_movement().count("R") == 1:
				return False
		
		their_knight = self._board.generic_find("n")
		
		if their_knight:
			from .Knight import Knight
			tn = Knight(self._board, not self._player, their_knight)
			#piece = tn.knight_movement()
			
			if tn.knight_movement().count("R") == 1:
				return False
		
		return True

	#pair king and rook together
	def paired_move(self):
		yk = self._board.generic_find("K")
		from Pieces.King import King
		your_king = King(self._board, not self._player, yk)
		return your_king.increase_movement(self._position)
	
	#determine where the two-piece king is and use algorithm to determine how much space is left
	#for the opponent king to move
	def trap_king(self):
		space = 0
		
		their_king = self._board.generic_find("k")
		their_knight = self._board.generic_find("n")
		
		hori_lower_limit, hori_upper_limit = self.rook_hori_movement()
		vert_lower_limit, vert_upper_limit = self.rook_vert_movement()

		h_axis_rook = self._position // 10
		v_axis_rook = self._position % 10

		h_axis_king = their_king // 10
		v_axis_king = their_king % 10
		
		if h_axis_rook > h_axis_king and v_axis_rook > v_axis_king:
			#use hori_lower and vert_lower

			space = hori_upper_limit - 28
			
			trim_board = (hori_upper_limit // 10) - 2
			
			space -= (trim_board * 2)
			
			cut_board = (9 - vert_lower_limit % 10)
			
			space -= (trim_board * cut_board)
			
			return 100 - space

		elif h_axis_rook > h_axis_king and v_axis_rook < v_axis_king:
			##use hor upper and vert_lower
			space = hori_upper_limit - 28
			
			trim_board = (hori_upper_limit // 10) - 2
			
			space -= (trim_board * 2)
			
			cut_board = (vert_lower_limit % 10)
			
			space -= (trim_board * cut_board)
			
			return 100 - space

		elif h_axis_rook < h_axis_king and v_axis_rook > v_axis_king:
			#use hori lower and vert upper
			space = 91 - hori_lower_limit 
			
			trim_board = abs((hori_upper_limit // 10) - 9)
			
			space -= (trim_board * 2)
			
			cut_board = (9 - vert_upper_limit % 10)
			
			space -= (trim_board * cut_board)
			
			return 100 - space

		elif h_axis_rook < h_axis_king and v_axis_rook < v_axis_king:
			#use hori upper and vert upper
			space = 91 - hori_lower_limit 
			
			trim_board = abs((hori_upper_limit // 10) - 9)
			
			space -= (trim_board * 2)
			
			cut_board = vert_upper_limit % 10
			
			space -= (trim_board * cut_board)
			
			return 100 - space
	
		else:
			return 0
	
	#check how much space the opponent king has
	def check_king_space(self, limit):
		space = self.trap_king()
		
		if (100 - space) < limit: #and (100-space) > 2:
			return True
		
		return False
	
	#Have the rook follow the king
	def king_follow(self):
		your_king = self._board.generic_find("K")
		
		from Pieces.King import King
		fake_rook_king = King(self._board, self._player, self._position)
		return fake_rook_king.increase_movement(your_king)
		
		
		
			
		