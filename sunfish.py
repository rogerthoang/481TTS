#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import print_function
import re, sys, time
from itertools import count
from collections import OrderedDict, namedtuple
from MiniMax.minimax import *
import pc
import os
import time
from lockfile import LockFile


# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e8

# Mate value must be greater than 8*queen + 2*(rook+knight+bishop)
# King value is set to twice this value such that if the opponent is
# 8 queens up, but we got the king, we still exceed MATE_VALUE.
# When a MATE is detected, we'll set the score to MATE_UPPER - plies to get there
# E.g. Mate in 3 will be MATE_UPPER - 6
MATE_LOWER = 60000 - 8*2700
MATE_UPPER = 60000 + 8*2700

QS_LIMIT = 150
EVAL_ROUGHNESS = 20

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' ..n.k...\n'  #  20 - 29
    ' ........\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' ........\n'  #  80 - 89
    ' ....K.NR\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
)

###############################################################################
# Move and evaluation tables
###############################################################################

N, E, S, W = -10, 1, 10, -1
directions = {
    'P': (N, N+N, N+W, N+E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}

pst = {
    'P': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 198, 198, 198, 198, 198, 198, 198, 198, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 178, 198, 208, 218, 218, 208, 198, 178, 0,
        0, 178, 198, 218, 238, 238, 218, 198, 178, 0,
        0, 178, 198, 208, 218, 218, 208, 198, 178, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 198, 198, 198, 198, 198, 198, 198, 198, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'B': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 797, 824, 817, 808, 808, 817, 824, 797, 0,
        0, 814, 841, 834, 825, 825, 834, 841, 814, 0,
        0, 818, 845, 838, 829, 829, 838, 845, 818, 0,
        0, 824, 851, 844, 835, 835, 844, 851, 824, 0,
        0, 827, 854, 847, 838, 838, 847, 854, 827, 0,
        0, 826, 853, 846, 837, 837, 846, 853, 826, 0,
        0, 817, 844, 837, 828, 828, 837, 844, 817, 0,
        0, 792, 819, 812, 803, 803, 812, 819, 792, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'N': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 627, 762, 786, 798, 798, 786, 762, 627, 0,
        0, 763, 798, 822, 834, 834, 822, 798, 763, 0,
        0, 817, 852, 876, 888, 888, 876, 852, 817, 0,
        0, 797, 832, 856, 868, 868, 856, 832, 797, 0,
        0, 799, 834, 858, 870, 870, 858, 834, 799, 0,
        0, 758, 793, 817, 829, 829, 817, 793, 758, 0,
        0, 739, 774, 798, 810, 810, 798, 774, 739, 0,
        0, 683, 718, 742, 754, 754, 742, 718, 683, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'R': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'Q': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'K': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 60098, 60132, 60073, 60025, 60025, 60073, 60132, 60098, 0,
        0, 60119, 60153, 60094, 60046, 60046, 60094, 60153, 60119, 0,
        0, 60146, 60180, 60121, 60073, 60073, 60121, 60180, 60146, 0,
        0, 60173, 60207, 60148, 60100, 60100, 60148, 60207, 60173, 0,
        0, 60196, 60230, 60171, 60123, 60123, 60171, 60230, 60196, 0,
        0, 60224, 60258, 60199, 60151, 60151, 60199, 60258, 60224, 0,
        0, 60287, 60321, 60262, 60214, 60214, 60262, 60321, 60287, 0,
        0, 60298, 60332, 60273, 60225, 60225, 60273, 60332, 60298, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
}


###############################################################################
# Chess logic
###############################################################################
class Position(namedtuple('Position', 'board score wc bc ep kp')):
    """ A state of a chess game
    board -- a 120 char representation of the board
    score -- the board evaluation
    wc -- the castling rights, [west/queen side, east/king side]
    bc -- the opponent castling rights, [west/king side, east/queen side]
    ep - the en passant square
    kp - the king passant square
    """

    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            #print(i, p)
            if not p.isupper(): continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    # Stay inside the board, and off friendly pieces
                    if q.isspace() or q.isupper(): break
                    # Pawn move, double move and capture
                    if p == 'P' and d in (N, N+N) and q != '.': break
                    if p == 'P' and d == N+N and (i < A1+N or self.board[i+N] != '.'): break
                    if p == 'P' and d in (N+W, N+E) and q == '.' and j not in (self.ep, self.kp): break
                    # Move it
                    yield (i, j)
                    # Stop crawlers from sliding, and sliding after captures
                    if p in 'PNK' or q.islower(): break
                    # Castling, by sliding the rook next to the king
                    if i == A1 and self.board[j+E] == 'K' and self.wc[0]: yield (j+E, j+W)
                    if i == H1 and self.board[j+W] == 'K' and self.wc[1]: yield (j+W, j+E)

    def rotate(self):
        ''' Rotates the board, preserving enpassant '''
        return Position(
            self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
            119-self.ep if self.ep else 0,
            119-self.kp if self.kp else 0)

    def nullmove(self):
        ''' Like rotate, but clears ep and kp '''
        return Position(
            self.board[::-1].swapcase(), -self.score,
            self.bc, self.wc, 0, 0)

    def move(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        # Copy variables and reset ep and kp
        board = self.board
        wc, bc, ep, kp = self.wc, self.bc, 0, 0
        score = self.score + self.value(move)
        # Actual move
        board = put(board, j, board[i])
        board = put(board, i, '.')
        # Castling rights, we move the rook or capture the opponent's
        if i == A1: wc = (False, wc[1])
        if i == H1: wc = (wc[0], False)
        if j == A8: bc = (bc[0], False)
        if j == H8: bc = (False, bc[1])
        # Castling
        if p == 'K':
            wc = (False, False)
            if abs(j-i) == 2:
                kp = (i+j)//2
                board = put(board, A1 if j < i else H1, '.')
                board = put(board, kp, 'R')
        # Pawn promotion, double move and en passant capture
        if p == 'P':
            if A8 <= j <= H8:
                board = put(board, j, 'Q')
            if j - i == 2*N:
                ep = i + N
            if j - i in (N+W, N+E) and q == '.':
                board = put(board, j+S, '.')
        # We rotate the returned position, so it's ready for the next player
        return Position(board, score, wc, bc, ep, kp)
        #return Position(board, score, wc, bc, ep, kp).rotate()
    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        # Actual move
        score = pst[p][j] - pst[p][i]
        # Capture
        if q.islower():
            score += pst[q.upper()][119-j]
        # Castling check detection
        if abs(j-self.kp) < 2:
            score += pst['K'][119-j]
        # Castling
        if p == 'K' and abs(i-j) == 2:
            score += pst['R'][(i+j)//2]
            score -= pst['R'][A1 if j < i else H1]
        # Special pawn stuff
        if p == 'P':
            if A8 <= j <= H8:
                score += pst['Q'][j] - pst['P'][j]
            if j == self.ep:
                score += pst['P'][119-(j+S)]
        return score
    
######################################################################### 

    #this function returns the piece at index i
    def get_board_piece(self, i):
        return self.board[i]
	
    def find_board_piece(self, piece):
        count = 0
        try:
            for position in range(21, 99):
                #print(self.board[position], piece)
                if self.board[position] == piece:
                    return position
                
            return None
            
        except:
            pass
    
    def is_checkmate(self):
        if self.score <= -MATE_LOWER:
            return True
        else:
            return False
        
    #template function to find any piece you want
    #piece takes a string (ex. "K", "n")
    def generic_find(self, piece):
        this_piece = None
        for i in range(21, 99):
            if self.get_board_piece(i) == piece:
                this_piece = i
                
        return this_piece
       
    #Compare how many pieces are from the original and new board and if there is a 
    #difference a piece has been eliminated
    #config.TOTAL_PIECE is a global variable stored in config.py that tracks the total amount
    #of pieces on the board
    def check_board(self):
        piece_count = pc.TOTAL_PIECE
        
        count = 0
        for i in range(21, 99):
            if self.get_board_piece(i) == "K" or self.get_board_piece(i) == "N"\
            or self.get_board_piece(i) == "R" or self.get_board_piece(i) == "r"\
            or self.get_board_piece(i) == "k" or self.get_board_piece(i) == "n":
                count += 1

        if piece_count != count:
            return True
        
        return False     
    #check to see if only the opponent's king is left
    def only_king(self):
        their_knight = self.generic_find("n")
        their_king = self.generic_find("k")

        if their_knight is None and their_king:
            return True, their_king

        return False, None
    
    #check to see how much space the two-piece king has left to move in
    def kings_space(self, player):
        rook = self.generic_find("R")
        
        from Pieces.Rook import Rook
        your_rook = Rook(self, player, rook) 
        return your_rook.check_king_space(20)
    
    #Pair the king and rook together in order to trap the opponent
    def pair_two_piece(self, first_piece, second_piece):

        if abs(first_piece / 10 - second_piece / 10) < 3:
            return True
        
        return False
    
    #use a 2-radii move block to force a rook movement followed by a king movement
    def paired_combo(self, player):
        your_king = self.generic_find("K")
        your_rook = self.generic_find("R")
        
        from Pieces.King import King
        
        extended_list = [your_king - 18, your_king - 19, your_king - 20, your_king - 21, your_king - 22,
                         your_king - 8, your_king - 12, 
                         your_king - 2, your_king + 2,
                         your_king + 8, your_king + 12,
                         your_king + 18, your_king + 19, your_king + 20, your_king + 21, your_king + 22]
        
        yk = King(self, player, your_king)
        
        yk.populate_moves()
        
        king_moves = yk.ret_kings_moves()
        
        king_moves.extend(extended_list)

        for i in king_moves:
            if i == your_rook:
                return True
       
        return False
        

###############################################################################
# Search logic
###############################################################################

# lower <= s(pos) <= upper
Entry = namedtuple('Entry', 'lower upper')

# The normal OrderedDict doesn't update the position of a key in the list,
# when the value is changed.
class LRUCache:
    '''Store items in the order the keys were last added'''
    def __init__(self, size):
        self.od = OrderedDict()
        self.size = size

    def get(self, key, default=None):
        try: self.od.move_to_end(key)
        except KeyError: return default
        return self.od[key]

    def __setitem__(self, key, value):
        try: del self.od[key]
        except KeyError:
            if len(self.od) == self.size:
                self.od.popitem(last=False)
        self.od[key] = value

class Searcher:
    def __init__(self):
        self.tp_score = LRUCache(TABLE_SIZE)
        self.tp_move = LRUCache(TABLE_SIZE)
        self.nodes = 0

    def bound(self, pos, gamma, depth, root=True):
        """ returns r where
                s(pos) <= r < gamma    if gamma > s(pos)
                gamma <= r <= s(pos)   if gamma <= s(pos)"""
        self.nodes += 1

        # Depth <= 0 is QSearch. Here any position is searched as deeply as is needed for calmness, and so there is no reason to keep different depths in the transposition table.
        depth = max(depth, 0)

        # Sunfish is a king-capture engine, so we should always check if we
        # still have a king. Notice since this is the only termination check,
        # the remaining code has to be comfortable with being mated, stalemated
        # or able to capture the opponent king.
        if pos.score <= -MATE_LOWER:
            return -MATE_UPPER

        # Look in the table if we have already searched this position before.
        # We also need to be sure, that the stored search was over the same
        # nodes as the current search.
        entry = self.tp_score.get((pos, depth, root), Entry(-MATE_UPPER, MATE_UPPER))
        if entry.lower >= gamma and (not root or self.tp_move.get(pos) is not None):
            return entry.lower
        if entry.upper < gamma:
            return entry.upper

        # Here extensions may be added
        # Such as 'if in_check: depth += 1'

        # Generator of moves to search in order.
        # This allows us to define the moves, but only calculate them if needed.
        def moves():
            # First try not moving at all
            if depth > 0 and not root and any(c in pos.board for c in 'RBNQ'):
                yield None, -self.bound(pos.nullmove(), 1-gamma, depth-3, root=False)
            # For QSearch we have a different kind of null-move
            if depth == 0:
                yield None, pos.score
            # Then killer move. We search it twice, but the tp will fix things for us. Note, we don't have to check for legality, since we've already done it before. Also note that in QS the killer must be a capture, otherwise we will be non deterministic.
            killer = self.tp_move.get(pos)
            if killer and (depth > 0 or pos.value(killer) >= QS_LIMIT):
                yield killer, -self.bound(pos.move(killer), 1-gamma, depth-1, root=False)
            # Then all the other moves
            for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
                if depth > 0 or pos.value(move) >= QS_LIMIT:
                    yield move, -self.bound(pos.move(move), 1-gamma, depth-1, root=False)

        # Run through the moves, shortcutting when possible
        best = -MATE_UPPER
        for move, score in moves():
            best = max(best, score)
            if best >= gamma:
                # Save the move for pv construction and killer heuristic
                self.tp_move[pos] = move
                break

        # Stalemate checking is a bit tricky: Say we failed low, because
        # we can't (legally) move and so the (real) score is -infty.
        # At the next depth we are allowed to just return r, -infty <= r < gamma,
        # which is normally fine.
        # However, what if gamma = -10 and we don't have any legal moves?
        # Then the score is actaully a draw and we should fail high!
        # Thus, if best < gamma and best < 0 we need to double check what we are doing.
        # This doesn't prevent sunfish from making a move that results in stalemate,
        # but only if depth == 1, so that's probably fair enough.
        # (Btw, at depth 1 we can also mate without realizing.)
        if best < gamma and best < 0 and depth > 0:
            is_dead = lambda pos: any(pos.value(m) >= MATE_LOWER for m in pos.gen_moves())
            if all(is_dead(pos.move(m)) for m in pos.gen_moves()):
                in_check = is_dead(pos.nullmove())
                best = -MATE_UPPER if in_check else 0

        # Table part 2
        if best >= gamma:
            self.tp_score[(pos, depth, root)] = Entry(best, entry.upper)
        if best < gamma:
            self.tp_score[(pos, depth, root)] = Entry(entry.lower, best)

        return best

    # secs over maxn is a breaking change. Can we do this?
    # I guess I could send a pull request to deep pink
    # Why include secs at all?
    def _search(self, pos):
        """ Iterative deepening MTD-bi search """
        self.nodes = 0

        # In finished games, we could potentially go far enough to cause a recursion
        # limit exception. Hence we bound the ply.
        for depth in range(1, 1000):
            self.depth = depth
            # The inner loop is a binary search on the score of the position.
            # Inv: lower <= score <= upper
            # 'while lower != upper' would work, but play tests show a margin of 20 plays better.
            lower, upper = -MATE_UPPER, MATE_UPPER
            while lower < upper - EVAL_ROUGHNESS:
                gamma = (lower+upper+1)//2
                score = self.bound(pos, gamma, depth)
                # Test for debugging search instability
                if not lower <= score <= upper:
                    import tools
                    print(__file__, 'search instability?', lower, upper, 'gamma score', gamma, score, 'depth', depth, 'pos', tools.renderFEN(pos))
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score
            # We want to make sure the move to play hasn't been kicked out of the table,
            # So we make another call that must always fail high and thus produce a move.
            score = self.bound(pos, lower, depth)

            # Test for debugging tp_score
            assert score >= lower
            if self.tp_score.get((pos, depth, True)) is None:
                print("No score stored?", score)
                self.tp_score[(pos, depth, True)] = Entry(score, score)
            assert score == self.tp_score.get((pos, depth, True)).lower

            # Test for debugging tp_move
            arb_legal_move = lambda: next((m for m in pos.gen_moves() if not any(pos.move(m).value(m1) >= MATE_LOWER for m1 in pos.move(m).gen_moves())), None)
            if self.tp_move.get(pos) is None:
                print('No move stored? Score: {}'.format(score))
                self.tp_move[pos] = arb_legal_move()
            else:
                move = self.tp_move.get(pos)
                pos1 = pos.move(move)
                if any(pos1.value(m) >= MATE_LOWER for m in pos1.gen_moves()):
                    import tools
                    print('Returned illegal move? Score: {}'.format(score),
                            'move', tools.mrender(pos, move),
                            'pos', tools.renderFEN(pos))
                    self.tp_move[pos] = arb_legal_move()

            # Yield so the user may inspect the search
            yield

    def search(self, pos, secs):
        start = time.time()
        for _ in self._search(pos):
            if time.time() - start > secs:
                break
        # If the game hasn't finished we can retrieve our move from the
        # transposition table.
        return self.tp_move.get(pos), self.tp_score.get((pos, self.depth, True)).lower


###############################################################################
# User interface
###############################################################################

# Python 2 compatability
if sys.version_info[0] == 2:
    input = raw_input
    class NewOrderedDict(OrderedDict):
        def move_to_end(self, key):
            value = self.pop(key)
            self[key] = value
    OrderedDict = NewOrderedDict


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank


def render(i):
    rank, fil = divmod(i - A1, 10)
    return chr(fil + ord('a')) + str(-rank + 1)


def print_pos(pos):
    print()
    uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
    for i, row in enumerate(pos.board.split()):
        print(' ', 8-i, ' '.join(uni_pieces.get(p, p) for p in row))
    print('    a b c d e f g h \n\n')

#save player X's move to log
def save_X(pos, move, text_count):
    log_move = "X:{}:{}".format(pos.get_board_piece(move[0]), render(move[1]))
    test = render(move[1])
 
    lock = LockFile("log_X.txt")
    lock.acquire()
    with open("log_X.txt", "a") as log_X:
        log_X.write(str(text_count) + " " + log_move + "\n")
    lock.release()

#Player Y reads player X's move and saves it to their log
#It also makes the move that it read from player X
#returns the position after moving player X and text count
def read_X(pos, text_count, lines):
    t = lines
    while True:
        if os.path.exists("log_X.txt.lock") == False:
            with open("log_X.txt", "r") as log_X:
                l = len(log_X.readlines())
                log_X.seek(0)
                
                if t != l:
                    time.sleep(12)
                    for i in range(0, text_count):
                        info = log_X.readline()

                    #find the semicolons that seperate the needed elements
                    first_semi = info.find(":")
                    second_semi = info.find(":", first_semi +1)

                    #gather the piece and index of the move
                    piece = info[first_semi + 1:second_semi].strip()
                    position = info[second_semi + 1:].strip()

                    #get the index of the piece and revert the chess move to an index and make a tuple
                    start_index = pos.find_board_piece(piece)
                    end_index = parse(position)
                    read_move = (start_index, end_index)
                    
                    
                    #make the move using the tuple
                    pos = pos.move(read_move)
                    pos = show(pos, read_move, True)

                    #Save player X's move into player Y's log
                    with open("log_Y.txt", "a") as log_Y:
                        log_move = "X:{}:{}".format(piece, position)
                        log_Y.write(str(text_count) + " " + log_move + "\n")

                    break
    
    lines = l
    text_count += 1
    
    return pos, text_count, lines
        
#Player X reads player Y's move and saves it to their log
#It also makes the move that it read from player Y
#returns the position after moving player Y and the log counter
def read_Y(pos, text_count, lines):
    t = lines
    while True:
        if os.path.exists("log_Y.txt.lock") == False:    
            with open("log_Y.txt", "r") as log_Y:
                x = len(log_Y.readlines())
                log_Y.seek(0)
                if t != x:
                    time.sleep(12)
                    for i in range(0, text_count):
                        info = log_Y.readline()

                    #rotate the board to make the proper move
                    pos = pos.rotate()

                    #find the semicolons that seperate the needed elements
                    first_semi = info.find(":")
                    second_semi = info.find(":", first_semi +1)

                    #gather the information
                    piece = info[first_semi + 1:second_semi].strip()
                    position = info[second_semi + 1:].strip()

                    #turn the chess piece into an index and reverse the index to get a tuple
                    start_index = pos.find_board_piece(piece)
                    end_index = 119 - parse(position)
                    read_move = (start_index, end_index)

                    #make the move and rotate the board back
                    pos = pos.move(read_move)
                    pos = show(pos, read_move, False)
                    #pos = pos.rotate()


                    #save the player Y's move into player X's log
                    with open("log_X.txt", "a") as log_X:
                        log_move = "Y:{}:{}".format(piece, position)
                        log_X.write(str(text_count) + " " + log_move + "\n")

                    break
    lines = x
    text_count += 1
            
    return pos, text_count, lines

#function used to save Y's move to their log
def save_Y(pos, move, text_count):
    log_move = "Y:{}:{}".format(pos.get_board_piece(move[0]), render(119-move[1]))
    lock = LockFile("log_Y.txt")
    lock.acquire()
    with open("log_Y.txt", "a") as log_Y:
        log_Y.write(str(text_count) + " " + log_move + "\n")
    lock.release()

#function used to make the move, save the move to log and print the move
#pos = position of the board
#who = bool, True = max, False = min
#move = the move the minimax function returned
#text_count = counter the log file are using
#returns the new position after making the move
def showMove(pos, who, move, text_count):
    player = who
    
    #if max player
    if player:
        #save player X's move
        save_X(pos, move, text_count)
        
        #make the actual move
        pos = pos.move(move)
        
        pos = show(pos, move, player)
   
    #if min player
    else:
        #save player Y's move
        save_Y(pos, move, text_count)
        
        #make the actual move
        pos = pos.move(move)
        
        pos = show(pos, move, player)
        
    return pos

def show(pos, move, player):
    if player:
        #render the move and print it
        move_render = render(move[0]) + render(move[1])
        print("PLAYER X: {}".format(move_render))
        
        #print the board
        print_pos(pos)

    else:
        #render the move and print it
        move_render = render(119-move[0]) + render(119-move[1])
        print("PLAYER Y: {}".format(move_render))

        #rotate the board back and print it
        pos = pos.rotate()
        print_pos(pos)
     
    return pos

#driver function to play the game
#pos = position of the board
#who = bool, True = max player, False = min player
#text_count = counter for logs
#returns the position after the move of the player, false for game not ended and the log counter
def play(pos, who, text_count, lines):
    player = who
    if player:
        #Max player's move
        if pos.find_board_piece("k") == None:
            print("Player X has won!")
            return pos, True, text_count
        
        if pos.find_board_piece("K") == None:
            print("Player Y has won!")
            return pos, True, text_count
        
        if text_count > 1:
            pos, text_count, lines = read_Y(pos, text_count, lines)

        #given the current position, a depth, whos turn and checkmate, try to use minimax
        score, move = minimax(pos, 1, True, player)
       
        if score == 99999:
            pc.TOTAL_PIECE -= 1

        #engine check for player win    
        if pos.score <= -MATE_LOWER:
            print("PLAYER Y has won!")
            return pos, True, text_count

        if score == -1000:
            print("The game has ended in a draw.")
            return pos, True, text_count
        
        #call to make a move, save and show the move
        pos = showMove(pos, True, move, text_count)
        
        text_count += 1
        
    else:
        pos = pos.rotate()
        if pos.find_board_piece("k") == None:
            print("Player Y has won!")
            pos = pos.rotate()
            return pos, True, text_count
        
        pos = pos.rotate()
        if pos.find_board_piece("k") == None:
            print("Player X has won!")
            return pos, True, text_count
       
        
        #Minimizing PLAYER MOVE
        pos, text_count, lines = read_X(pos, text_count, lines)
    
        #rotate board for library to work properly
        pos = pos.rotate()
        
        #call minimax to determine the move
        score, move = minimax(pos, 1, False, player)
        
        if score == -99999:
            pc.TOTAL_PIECE -= 1
            
		#This engine's check for player win
        if pos.score <= -MATE_LOWER:
            print("Player X has won!")
            return pos, True, text_count
        
        if score == -1000:
            print("The game has ended in a draw.")
            return pos, True, text_count

        #call to make a move, save and show the move
        pos = showMove(pos, False, move, text_count)
        
        text_count += 1
        
    return pos, False, text_count, lines

def main():
    #initialize the various variables needed
    #count = how many rounds have passed, only increments after both player's have made a move
    #log_counters = counters used to represent the count in log_X and log_Y
    #end = bool used to determine if game has ended
    #pos' = initialize the board for both players
    count = 1
    x_log_counter = 1
    y_log_counter = 1
    end = False
    
    pos_X = Position(initial, 0, (True,True), (True,True), 0, 0)
    pos_Y = Position(initial, 0, (True,True), (True,True), 0, 0)
    
    #game limit is 100 turns or while the game has not ended
    while count < 101 and not end:
        pos_X, end, x_log_counter = play(pos_X, True, x_log_counter)
        pos_Y, end, y_log_counter = play(pos_Y, False, y_log_counter)
        count += 1
              
if __name__ == '__main__':
    main()

