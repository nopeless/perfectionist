from typing import List
import itertools
from itertools import repeat
import numpy as np
import pprint
import heapq
import copy

import numpy


# the second fevertime logic that i am writing



MAX_INT=15
# Fever time is not specified here, but it NEEDS to be lower than 15 (numpy dtype byte)



class Path:
	def __init__(self, num1:np.byte, num2:np.byte) -> None:
		# store the indices
		self.num1=num1
		self.num2=num2
	def __repr__(self) -> str:
		return f"<Path [{self.num1}, {self.num2}]>"



class B_path:
	"""the class for paths with pair id(id ndarray of 2) OR 1"""
	def __init__(self, id, paths:List[Path]=[]) -> None:
		self.id=id
		self.paths=paths
	def __repr__(self) -> str:
		return f"<B_path id={self.id} paths={self.paths}>"




class r_board:
	"""
	the number range 1 to `MAX_INT` will be changed to 0 to `MAX_INT-1`"""

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
			0: B_path
			1: B_path
			2: B_path
			...\n
		]\n
		Remember to not append 0 length path values"""
		# could use numpy to make the code more efficient
		# HERE
		rt = [copy.deepcopy(B_path(id)) for x in repeat(None, MAX_INT)]
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
	local_board_pool=[]
	# 1 dimensional array
	local_branch_pool=[]
	# 1 dimensional array

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
		# for 
	cut=0
	for i in range(2):
		# a while True loop would do better, but this is just preventing overlooping
		




		cut+=1
		# adaptively increase cut



























