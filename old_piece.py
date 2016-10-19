from sunfish import print_pos
class King:
	def __init__(self, board, player, end):
		self._board = board
		self._player = player
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
		
		#if maximize player, look for minimize pieces
		if not self._player:
			#print(kings_moves)
			for i in self._kings_moves:
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "K" \
				and self._board.get_board_piece(i) != "N" and self._board.get_board_piece(i) != "R":
					board_piece_list.append(self._board.get_board_piece(i))
					
			if len(board_piece_list) > 0:
				return board_piece_list
					
		
			else:
				return []
		
		#otherwise, look for maximize player's pieces
		else:
			for i in self._kings_moves:
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "k" \
				and self._board.get_board_piece(i) != "n" and self._board.get_board_piece(i) != "r":
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

		#MAXIMIZE
		if your_king is not None and not self._player:
			knight = self._board.generic_find("n")
			
			king = self._board.generic_find("k")
	
			if king:
				their_king = King(self._board, not self._player, king)
				#piece = their_king.king_movement()
				#print(piece) 
				if their_king.king_movement().count("K") == 1:
					return False
		
			if knight:
				their_knight = Knight(self._board, not self._player, knight)
				if their_knight.knight_movement().count("K") == 1:
					return False
		
			return True

		#MINIMIZE
		else:
			rook = self._board.generic_find("r")
			#print("CHECKING")
			if rook:
				from .Rook import Rook
				their_rook = Rook(self._board, self._player, rook)
				#piece = their_rook.rook_piece_check()
				
				
				
				if their_rook.rook_piece_check().count("K") == 1:
					return False

			knight = self._board.generic_find("n")
			if knight:
				from .Knight import Knight
				their_knight = Knight(self._board, self._player, knight)
				#piece = their_knight.knight_movement()
				if their_knight.knight_movement().count("K") == 1:
					return False

			king = self._board.generic_find("k")
			if king:
				their_king = King(self._board, self._player, king)
				#piece = their_king.king_movement()

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
		#your_rook = self._board.generic_find("R")
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
	def check_mated(self, king, knight, rook):#, their_king):
		#print("CALLED")
		viable_move_list = []
		limit = 0
		#their_king.populate_moves()
		#their_king_moves = their_king.ret_kings_moves()
		#their_king_position = their_king.ret_kings_position()
		
		self.populate_moves()
		
		for position in self._kings_moves:#their_king_moves:
			if position // 10 > 1 and position // 10 < 10\
			and position % 10 > 0 and position % 10 < 9:
				viable_move_list.append(position)
		
		viable_move_list.append(self._position)
		#print(viable_move_list)
		#CONTINUE LATER CHECK MOVES
		
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
		
		
		
			
		class Knight:
	def __init__(self, board, player, end):
		self._board = board
		self._player = player
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
		
		if not self._player:
			for i in self._knight_moves:
				if self._board.get_board_piece(i) != "." and self._board.get_board_piece(i) != " " \
				and self._board.get_board_piece(i) != "\n" and self._board.get_board_piece(i) != "K" \
				and self._board.get_board_piece(i) != "N" and self._board.get_board_piece(i) != "R":
					#print("###########{}".format(self._board.get_board_piece(i)))
					board_piece_list.append(self._board.get_board_piece(i))
			#print(self.ret_moves())
			#print(board_piece_list)		
			if len(board_piece_list) > 0:
				return board_piece_list
					
			
			else:
				return []
		
		#otherwise, look for maximize player's pieces
		else:
			for i in self._knight_moves:
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
		
		
		
															