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
		return f"<[{self.lost}][{self.idx}]>"


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
	def __init__(self, board, paths=[], lost=0) -> None:
		self.board=board
		self.paths=paths
		self.lost=lost
		# originally had the idea of having a separate array of 0 indices
	def __repr__(self) -> str:
		return f"<r_board path count={len(self.paths)} last path={self.paths[-1] if len(self.paths) > 0 else 'None'}\nboard={self.paths}>"
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
	def get_valid_moves(self, id:int=0) -> List[B_path]:
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
		rt = [copy.deepcopy(B_path(id)) for x in repeat(None, MAX_INT_MINUS_ONE)]
		# 15 elements
		# print(rt)
		nonzero=np.where(self.board != 0)[0]
		# print(nonzero)
		for key, select in enumerate(nonzero):
			# print("-- select --")
			# print(select)
			if self.board[select] > 1:
				# print("tile appears more than twice. adding paired")
				rt[0].paths.append(Path(np.byte(select), np.byte(select))) # in c, it would be presented as a single byte
			# print("-- target --")
			for target in nonzero[key+1:]:
				# print(target)
				rt[target-select].paths.append(Path(np.byte(select), np.byte(target)))
		return rt			
	def format_path_table(rt):
		# inefficient function
		strl=[]
		for k,v in enumerate(rt):
			strl.append(f"{k}:{v}")
		return "Board Paths:\n"+"\n".join(strl)








if __name__=="__main__":
	print("="*100)
	b=r_board(r_board.format_board([1,4,4,5,5,7,10]))
	print(b)
	print(b.show_board())
	print(r_board.format_path_table(b.get_valid_moves(0)))
	# increase this value after scanning all global branches

	# global_base=0
	# not going to be utilized here
	# the lowest loss
	# this feature is only going to be effective on the c code
	# this allows the global pool to always start at index 0 saving a ton of space (theoretically)

	global_board_pool=[[b]]
	# this is now b with id (0,0)
	# 0,0 means
	# 0 lost, 0th index board
	# will not use global_base
	# boards once assigned are static
	# when an entire loss pool fails, it gets manually assigned to None
	# which dereferences every board of that lost
	
	global_branch_pool=[]
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

	def recursive_brancher(path):
		# generate local pools and assign more global pools if needed
		pass
	cut=0
	for i in range(2):
		# a while True loop would do better, but this is just preventing overlooping
		




		cut+=1
		# adaptively increase cut




















