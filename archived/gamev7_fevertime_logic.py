# v7 (current version) revision
# this version should implement a recursive function to search 0 lost branches
# its the best method i have at the current time

from typing import List
import itertools
from itertools import repeat
import numpy as np
import pprint
import heapq
import copy

import numpy
from numpy.core.function_base import linspace




# improved branching algorithm by creating local and global pools, releasing memory on local pools when they are found useless


# practicing the logic in fevertime before applying it to the main game


# Basically, paths with 0 losses are a bit different and needs to be branched immediently


# the return object is 2 arrays (finally some major design change from v1)
# is it actually 2 arrays? no
# but its almost the same a... idk my brain fried here. im not terry davis or smth
# due to how global pool allocation works, this is memory efficient (at least in theory. idk how exactly python gc works)
# 



"""stupid design draft
	what is this????
	old design
	???????????????????????????????
	{
		immute:[
			int, int, int,...
		]
		mute:[ 
			0: None(by design?),
			1: B_path,...
		]
	}
	the mute list will be sent to the global pool
	since b_path itself is a list, its sends the pointer
	which is why 'None' is ok as first element
"""

# design 2

# global_pool
# [
#   0:[int,int,int...]
#   1:B_path(directly gets appended to global pool, minimizing memory allocation)
#   2:B_path(sometimes, the length is 0. if its 0, it doesnt get appended to the global pool)
#   3:B_path
#   ...
#   14:B_path(14 is the last index. if this was a low level language, we can take an advantage of this)
# ]

# local pools will be populated with boards from those 0 paths






MAX_INT=15
MAX_INT_MINUS_ONE=MAX_INT-1
# Fever time is not specified here, but it NEEDS to be lower than 15 (numpy dtype byte)

class Board_id:
	# only used to reference a board in a global pool
	def __init__(self, lost, idx) -> None:
		self.lost=lost
		self.idx=idx
	def __repr__(self) -> str:
		return f"({self.lost}, {self.idx})"


class Path:
	# only used to show a non-zero lost path
	def __init__(self, sel:int, tar:int) -> None:
		self.sel=sel
		self.tar=tar
	def __repr__(self) -> str:
		return f"<Path {self.sel}->{self.tar}>"

class B_path:
	def __init__(self, id:Board_id=Board_id(0,0), paths:List[Path]=[]) -> None:
		self.id=id
		# list of paths
		self.paths=paths
	def __repr__(self) -> str:
		return f"<B_path id={self.id} paths={self.paths}>"




class r_board:
	def __init__(self, board, paths=[]) -> None:
		self.board=board
		self.paths=paths
		# originally had the idea of having a separate array of 0 indices
	def __repr__(self) -> str:
		return f"<r_board path count={len(self.paths)} paths={self.paths}>"
	def show_board(self) -> str:
		return f"Board:\n{self.board}"

	def format_board(board):
		return_board=np.zeros(MAX_INT, numpy.byte) # extremely efficient 
		i=0
		for tile in board:
			return_board[tile-1]+=1
		return return_board
	def __eq__(self, other) -> None:
		"""checks if boards are equal"""
		for k, v in enumerate(self.board):
			if v != other.board[k]:
				return False
		return True
	def get_valid_moves(self, id:Board_id=Board_id(0,0)) -> List[B_path]:
		"""returns a list of B_paths which is also a list\n
		will be concatnated later\n
		ex)\n
		[\n
			0: [int,int,int]
			1: B_path
			2: B_path
			...\n
		]\n
		Remember to not append 0 length path values"""
		# could use numpy to make the code more efficient
		# HERE
		rt = [[]]+[copy.deepcopy(B_path(id)) for x in repeat(None, MAX_INT_MINUS_ONE)]
		# 15 elements
		# print(rt)

		nonzero=np.where(self.board != 0)[0]
		# print(nonzero)
		for key, select in enumerate(nonzero):
			# print("-- select --")
			# print(select)
			if self.board[select] > 1:
				# print("tile appears more than twice. adding paired")
				rt[0].append(np.byte(select)) # in c, it would be presented as a single byte
			# print("-- target --")
			for target in nonzero[key+1:]:
				# print(target)
				rt[target-select].paths.append(Path(np.byte(select), np.byte(target)))
		return rt
	
	def get_valid_moves_no_id(self):
		"""returns a list of B_paths which is also a list\n
		will be concatnated later\n
		ex)\n
		[\n
			0: [int,int,int]
			1: B_path
			2: B_path
			...\n
		]\n
		Remember to not append 0 length path values"""
		# could use numpy to make the code more efficient
		# HERE
		rt = [[]]+[[] for x in repeat(None, MAX_INT_MINUS_ONE)]
		# 15 elements
		# print(rt)

		nonzero=np.where(self.board != 0)[0]
		# print(nonzero)
		for key, select in enumerate(nonzero):
			# print("-- select --")
			# print(select)
			if self.board[select] > 1:
				# print("tile appears more than twice. adding paired")
				rt[0].append(np.byte(select)) # in c, it would be presented as a single byte
			# print("-- target --")
			for target in nonzero[key+1:]:
				# print(target)
				rt[target-select].append(Path(np.byte(select), np.byte(target)))
		return rt			
	def format_path_table(rt):
		# inefficient function
		strl=[]
		for k,v in enumerate(rt):
			strl.append(f"{k}:{v}")
		return "Board Paths:\n"+"\n".join(strl)


	# methods to do stuff
	def do_move_pair_move(self, sel):
		# move
		self.board[sel]-=2
		return self
	def do_move_lost(self, sel, tar):
		self.board[sel]-=1
		self.board[tar]-=1
		return self
	def append_path(self, path):
		self.paths.append(path)
		return self
	def is_finished(self):
		return not np.any(self.board, 0)
	
	def __hash__(self):
		return hash(str(self.board))
		
	def __eq__(self, other):
		return self.board.__hash__==other.board.__hash__

# a board is always irrelevent when its lost is lower than current cut - (max integer-1)



if __name__=="__main__":
	board_skim=-MAX_INT
	print("="*100)
	b=r_board(r_board.format_board([1,4,4,5,5,7,10]))
	print(b)
	print(b.show_board())
	print(r_board.format_path_table(b.get_valid_moves(0)))
	# increase this value after scanning all global branches

	board_lost_dict={}
	# create an empty dicitonary
	# basically the thing is like
	# {
	#    __hash__:(id)..
	# }
	# using the id we can find the lost
	# and do stuff based on that
	# only affects globall pools because uh... idk why
	global_board_pool=[[b]]+[[] for _ in repeat(None, 40)] # the 100 here is just an arbitrary big number
	# this is now b with id (0,0)
	# 0,0 means
	# 0 lost, 0th index board
	# will not use global_base
	# boards once assigned are static
	# board_skimmmer will automatically dereference them
	print(global_board_pool)

	global_branch_pool=[[] for _ in repeat(None, 40)]
	# a global branch pool
	# will be something like
	# [
	#   0: [B_path, B_path,...],
	#   ...
	# ]
	# 2 dimensional array
	# local_board_pool=[]
	# # 1 dimensional array
	# local_branch_pool=[]
	# # 1 dimensional array
	# the above needs to be defined in the recursive scope

	# logic
	# step 0
	# first eval boards
	# get paths
	# except for the 0's(append in local branch pool), list them in the global branch(global branch list always grows by 1, which is also cut)
	# local branch pool means its the active pool that will get dereferenced when it hits end
	# if there are delta loss 0 boards
	# 	eval the paths to get other boards
	#	list the non 0 lost boards to global_pool
	# 	0 lost boards are stored in local pool
	# 	if a board hits total 0, then the stop
	# else
	# 	increase the cut by 1 and go to step 0 (full loop)
	
	# local pools will be executed until they hit the end and get dereferenced by python's gc
	# basically this logic will store the "leafs" of the tree

	"""
	id is the id in local branch, NOT global"""
	def recursive_brancher(board:r_board, lost, paths:List[int]):
		# generate local pools and assign more global pools if needed
		# is_finished is not checked here
		print(">> recursive brancher ==================== <<")
		# the paths are all 0 lost paths
		boards=[]
		for path in paths:
			boards.append(copy.deepcopy(board).append_path(Path(np.byte(path), np.byte(path))).do_move_pair_move(path))
		print(">> boards")
		pprint.pprint(boards)
		for recursive_branch_board in boards:
			moves=recursive_branch_board.get_valid_moves_no_id()
			# this is because we are going to generate the board right away

			# send another pair of board and 0 lost moves into the function
			if len(moves[0]) > 0:
				recursive_brancher(recursive_branch_board, lost, moves[0])
			lost=1
			print(">> moves")
			pprint.pprint(moves)
			for lost_idx in range(1+lost, MAX_INT+lost):
				# loop max_int-1 times
				# print(lost)
				if len(moves[lost]) > 0:
					for path in moves[lost]:
						global_board_pool[lost_idx].append(copy.deepcopy(recursive_branch_board).do_move_lost(path.sel, path.tar))
				lost+=1
	cut=0


	# ROOT
	for i in range(5):
		# a while True loop would do better, but this is just preventing overlooping
		print("=============LOOP=============")
		print(f"iterating {i} times")
		for idx, board in enumerate(global_board_pool[i]):
			print(board)
			id=Board_id(i, idx)
			print(id)
			moves=board.get_valid_moves(id)
			if len(moves[0]) > 0:
				recursive_brancher(board, i, moves[0])
			lost=1
			for lost_idx in range(1+i,MAX_INT+i):
				# loop max_int-1 times
				if len(moves[lost].paths)>0:
					global_branch_pool[lost_idx].append(moves[lost])
			lost+=1
		print("GLOBAL BOARD POOL============================")
		pprint.pprint(global_board_pool)
		print("GLOBAL BRANCH POOL============================")
		pprint.pprint(global_branch_pool)
		break




		cut+=1
		# skimming logic will be added later
		# adaptively increase cut
		# if (board_skim>=0):
		# 	print(f"skimming board of value {board_skim}")

		board_skim+=1

		




















