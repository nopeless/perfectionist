

# v10
# fixed dictionary *FINALLY*
# added various features such as
# * BoardManager



from copy import Error
from numpy.core.numerictypes import _minvals

from numpy.lib.function_base import select
from typing import List
import itertools
from itertools import repeat
import numpy as np
import pprint
import heapq
import copy

import numpy
import time




SIZE=48
X=6
Y=8
FEVER=10


# B -> P -> B



class Path:
	def __init__(self, sel:int, tar:int) -> None:
		self.sel=sel
		self.tar=tar
	def __repr__(self) -> str:
		return f"({self.sel} => {self.tar})"

class BoardLoc:
	def __init__(self, lost:int, id:int) -> None:
		self.lost=lost
		self.id=id
	def __repr__(self) -> str:
		return f"({self.lost}, {self.id})"

class B_Path:
	def __init__(self, loc:BoardLoc, paths:List[Path]=[]) -> None:
		self.loc=loc
		self.paths=paths[:]
	def __repr__(self) -> str:
		return f"<B_Path {self.loc} {self.paths}>"


# a board location can be None
class Board:
	table = np.fromfile("v9_fevertime_table", np.uint8, -1)
	pre_calc_table = np.fromfile(
		"nCrTable0-31x0-31", np.uint32, -1).reshape([32, 32])
	
	def __init__(self, board:np.ndarray, count:np.int8=SIZE, last_board:BoardLoc=None) -> None:
		self.board=board
		self.last_board=last_board
		self.count=count
		self.hash=hash(board.tobytes())
		
	def __repr__(self):
		i=0
		outstr="-"*(X*3+2)+"\n"
		for yy in range(Y):
			outstr+="|"
			for xx in range(X):
				xx,yy
				outstr+=str(self.board[i]).rjust(2, " ")+" "
				i+=1
			outstr+="|\n"
		outstr+="-"*(X*3+2)
		return outstr

	def get_fever_score(self) -> int:
		# basically, get its feverscore
		# this only works if the count of the board is less or equal to 10
		fb=np.full(16, 0, np.uint8)
		for tile in self.board:
			if tile != 0: fb[tile]+=1
		fb[0]=10-sum(fb)
		return self.table[self.id_from_stacked(fb)]
	
	@staticmethod
	def nHr(n, r):
		return Board.pre_calc_table[n+r-1, r]

	@staticmethod
	def id_from_stacked(board):
		count=10
		id=0
		ln=15
		for loc in range(15, -1, -1):
			if board[loc]==0: continue
			for _ in repeat(None, board[loc]): 
				count-=1
				for s in range(ln+1, loc+1, -1):
					id += Board.nHr(s, count)
				ln = loc
		return id

	def get_valid_moves(self, loc:BoardLoc):
		# returns valid moves
		# format
		# [
		# 	0: [Path, Path,...]
		# 	1: B_Path
		# 	...
		# ]
		# 
		# since the incides are the loses, we need 16 of them
		rt=[[]] + [B_Path(loc) for _ in repeat(None, 15)]
		# ^ from v8.1 fevertime logic.py
		# a good way to start the board
		one_index=[]
		after_zeros=np.full(SIZE, False, np.bool)
		min_val=np.int32(0)
		for row_idx in range(0, SIZE, X):
			for select_index, select_tile in zip(range(row_idx, row_idx+X), self.board[row_idx:row_idx+X]):
				if select_tile==0: continue
				# print("ENTER")
				for line in [zip(range(select_index+1, row_idx+X), self.board[select_index+1:row_idx+X]), zip(range(select_index+X, SIZE, X), self.board[select_index+X:SIZE:X])]:
					# pprint.pprint(line)
					# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
					for target_index, target_tile in line:
						if target_tile == 0: continue
						if select_tile == 1:
							one_index.append(select_index)
							if target_tile != 1:
								rt[1].paths.append(Path(target_index, select_index))
						else:
							if select_tile == target_tile:
								# print(f"added {select_tile} {target_tile}|{select_index} {target_index}")
								rt[0].append(Path(select_index, target_index))
							else:
								# 4 2
								# 2
								min_val=min(select_tile, target_tile)
								if select_tile==target_tile+target_tile:
									if not after_zeros[select_index]:
										rt[min_val].paths.append(Path(select_index, target_index))
										after_zeros[select_index]=True
									rt[min_val].paths.append(Path(target_index, select_index))
								#   2
								# 2 4	
								elif select_tile+select_tile==target_tile:
									rt[min_val].paths.append(Path(select_index, target_index))
									if not after_zeros[target_index]:
										rt[min_val].paths.append(Path(target_index, select_index))
										after_zeros[target_index]=True
								else:
									rt[min(select_tile, target_tile)].paths.extend([Path(select_index, target_index), Path(target_index, select_index)])
						break

		for target_index in np.where(self.board > 1)[0]:
			for select_index in one_index:
				rt[1].paths.append(Path(select_index, target_index))
		for i, select_index in enumerate(one_index[:-1]):
			for target_index in one_index[i+1:]:
				rt[0].append(Path(select_index, target_index))
		return rt

	def copy_do_move_pair(self, loc:BoardLoc, path:Path):
		board=copy.copy(self.board)
		board[path.sel]=0
		board[path.tar]=0
		return Board(board, self.count-2, loc)
	
	def copy_do_move_lost(self, loc:BoardLoc, path:Path):
		board=copy.copy(self.board)
		board[path.tar]=abs(board[path.sel]-board[path.tar])
		board[path.sel]=0
		return Board(board, self.count-1, loc)

	def is_fever(self):
		return self.count <= FEVER

	def is_finished(self):
		return self.count==0

	@staticmethod
	def empty_board(last_board:BoardLoc):
		return Board(np.full(SIZE, 0, np.int8), 0, last_board)

	def __eq__(self, other: object) -> bool:
		return self.hash==other.hash and (self.board == other.board).all()

	def __hash__(self):
		return self.hash


class BoardManager:
	def __init__(self, root:Board, lost_cap=100) -> None:
		self.lost_cap=lost_cap
		self.boards=[[] for _ in repeat(None, lost_cap+1)]
		self.boards[0].append(root)
		self.paths=[[] for _ in repeat(None, lost_cap+1)]
		self.board_dict={}
		self.board_dict[root]=BoardLoc(0, 0)

	def board_at(self, board_loc:BoardLoc):
		return self.boards[board_loc.lost][board_loc.id]

	def add_board(self, lost:int, board:Board) -> BoardLoc:
		append_loc = BoardLoc(lost, len(self.boards[lost]))
		# the appending index if we do append it
		# saving len() computing time idk
		if board in self.board_dict:
			original_board_loc=self.board_dict[board]
			# if the board already exists,
			# check their "lost" values
			# if the incoming board's lost is lower, change the original board value to None
			# and on the path evaluation side, if the board is None, discard all paths
			# i am not entirely sure if this is faster than reallocating the path groups but since the valid path generation is fast, ill leave it as low priority
			# self.board[board] is 

			# return 0 if we dont even need to add the board
			if original_board_loc.lost <= lost:
				return None
			print("incoming board is better. assigning original board to None")
			# the incoming board's lost is lower
			# set the original board to None
			self.boards[original_board_loc.lost][original_board_loc.id]=None
			
		# now append
		self.boards[lost].append(board)
		self.board_dict[board]=append_loc
		return append_loc

	def construct_boards(self, board:Board):
		boards=[]
		while board.last_board is not None:
			boards.append(board)
			board=self.boards[board.last_board.lost][board.last_board.id]
		boards.append(self.boards[0][0])
		return boards[::-1]

	def add_B_Path(self, lost:int, bpath:B_Path):
		# paths always gets added
		# self.paths[lost].append(bpath)
		if lost <= self.lost_cap:
			self.paths[lost].append(bpath)


class BoardFinder:
	def __init__(self, board, limit=50) -> None:
		# first format and then stuff
		# self.original_board=board # idk why this is here
		self.limit=limit
		self.solution_set=[]
		self.board_manager=BoardManager(board)
		self.cut=0
	def find_internal(self) -> Board:
		# the main code
		print("finding...")
		for _ in repeat(None, self.limit+1):
			print(f"cut={self.cut}")
			for id, board in enumerate(self.board_manager.boards[self.cut][:]):
				if board is None: continue # failed board
				bl=BoardLoc(self.cut, id)
				if board.is_finished():
					return board
				if board.is_fever():
					fs=board.get_fever_score()
					# print(fs)
					if fs==0:
						loc=self.board_manager.add_board(self.cut, Board.empty_board(bl))
						return self.board_manager.board_at(loc)
					else:
						self.board_manager.add_board(self.cut+fs, Board.empty_board(bl))
					continue
				moves=board.get_valid_moves(bl)
				for paired_move in moves[0]:
					eval_res=self.recursive_board_eval(board.copy_do_move_pair(bl, paired_move))
					if eval_res is not None:
						if eval_res.is_finished():
							return eval_res
				for bpath_lost, bpath in enumerate(moves[1:], self.cut+1):
					if len(bpath.paths) > 0:
						self.board_manager.add_B_Path(bpath_lost, bpath)
			# since we found nothing
			self.cut+=1
			# eval paths
			for bpath in self.board_manager.paths[self.cut]:
				board=self.board_manager.board_at(bpath.loc)
				if board is not None:
					# board exists
					# evaluate and add to path
					for path in bpath.paths:
						self.board_manager.add_board(self.cut, board.copy_do_move_lost(bpath.loc, path))
			# remove memory
			self.board_manager.paths[self.cut]=None
			# remove board memory
			# idk how to implement this yet
		print("= FAILED =")
	def find(self) -> str:
		self.solution_set=self.board_manager.construct_boards(self.find_internal())
		return "\n".join(map(lambda x: repr(x), self.solution_set))
		
	def recursive_board_eval(self, root_board:Board):
		# recursive eval for the 0 lost stuff
		# return
		added_loc=self.board_manager.add_board(self.cut, root_board)
		if added_loc is None: return None
		if root_board.is_fever():
			fs=root_board.get_fever_score()
			if fs==0:
				loc=self.board_manager.add_board(self.cut, Board.empty_board(added_loc))
				return self.board_manager.board_at(loc)
			else:
				self.board_manager.add_board(self.cut+fs, Board.empty_board(added_loc))
		moves=root_board.get_valid_moves(added_loc)
		for paired_move in moves[0]:
			eval_res=root_board.copy_do_move_pair(added_loc, paired_move)
			if eval_res is not None:
				if eval_res.is_finished():
					print(eval_res)
					return eval_res
		for bpath_lost, bpath in enumerate(moves[1:], self.cut+1):
			if len(bpath.paths) > 0:
				self.board_manager.add_B_Path(bpath_lost, bpath)
		return None

	def __repr__(self) -> str:
		if not self.solution_set: return f"<BoardFinder 'board is not solved yet'>"
		return pprint.pformat(self.solution_set)





if __name__=="__main__":
	print("running default main")
	board=Board(np.array(
		[11,1,11,8,13,11,12,2,3,13,4,11,14,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.int8), 14)
	#
	# [11,1,11,8,13,11,12,2,3,13,4,11,15,1,4,3,12,3,3,12,4,6,9,2,13,5,13,1,1,9,11,12,10,10,1,11,11,2,10,2,3,9,6,4,9,10,13,12], dtype=np.int8), 48)
	# print(b.hash)
	game=BoardFinder(board, 7)
	print(game.find())
	# moves=b.get_valid_moves(BoardLoc(0,0))
	# print("-"*100)
	# print("0 lost moves")
	# for move in moves[0]:
	# 	print(move)
	# 	print(b.copy_do_move_pair(BoardLoc(0, 0), move))
	# for lost, bpath in enumerate(moves[1:], 1):
	# 	if len(bpath.paths) != 0:
	# 		print("-"*100)
	# 		print(f"{lost} lost moves")
	# 		for move in bpath.paths:
	# 			print(b.copy_do_move_lost(BoardLoc(0, 0), move))
			
	



	# game=BoardFinder(np.array(
	# 	[10, 15, 10,  5, 13, 11,  2,  4,  1, 11, 13,  7,  4,  1,  7,  5, 13,
    #     5,  1,  7,  8,  7, 10, 15, 13,  6, 14,  3,  1, 10,  1,  7,  7,  2,
    #    13, 10,  9, 15,  6,  2,  5,  6,  9,  2, 10,  4, 11, 10], dtype=np.byte))
	# game.find()
	# print(game)






