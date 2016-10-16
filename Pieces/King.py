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