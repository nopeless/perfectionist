# v8 logic =
# v7 logic + set pooling + different algos for each mode - skimming(incompatible with v8 logic)
# basically have a set of dead pools
# once a board dies, it goes into the hashed set
# taking of set union lookup O(1)

# v8.1
# removed atrocious deepcopy from the code


from copy import Error
from typing import List
import itertools
from itertools import repeat
import numpy as np
import pprint
import heapq
import copy

import numpy
import time


# improved branching algorithm by creating local and global pools, releasing memory on local pools when they are found useless


# practicing the logic in fevertime before applying it to the main game




start = time.time()



MAX_INT=15

REMOVED_FROM_MEMORY=None


class Path:
	# only used to show a non-zero lost path
	def __init__(self, sel:int, tar:int) -> None:
		self.sel=sel
		self.tar=tar
	def __repr__(self) -> str:
		return f"<Path {self.sel}->{self.tar}>"


class BoardLoc:
	def __init__(self, lost:int, id:int) -> None:
		self.lost=lost
		self.id=id
	def __repr__(self) -> str:
		return f"({self.lost}, {self.id})"
	# def is_origin(self) -> bool:
	# 	return (self.lost==0) and (self.id==0)


class B_path:
	def __init__(self, id:BoardLoc=BoardLoc(0,0), paths:List[Path]=[]) -> None:
		self.id=id
		# list of paths
		self.paths=paths[:]
	def __repr__(self) -> str:
		return f"<B_path id={self.id} paths={self.paths}>"
	
# a board class
# a board always has its id but its never stored inside the id

class FeverBoard:
	# completely changed in form
	def __init__(self, board, last_board:BoardLoc) -> None:
		self.board=board
		self.last_board=last_board
		self.hash=hash(board.tobytes())
	
	def __repr__(self) -> str:
		return f"<FeverBoard {self.board} last_board={self.last_board}>"


	def get_valid_moves(self, loc:BoardLoc):
		# advantages of having a path group
		# share same id and reduce the amount of evaluation at a given time
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
		rt = [[]]+[B_path(loc) for x in repeat(None, MAX_INT)]
		# 15 elements
		# print(rt)

		nonzero=np.where(self.board != 0)[0]
		if len(nonzero) == 0:
			raise Error("ASKED TO FIND PATHS ON AN EMPTY BOARD")
		if len(nonzero) == 1:
			# there are multiple cases here
			if self.board[nonzero[0]] == 1:
				# if there is only 1 number
				rt[nonzero[0]+1].paths.append(Path(np.byte(nonzero[0]), np.byte(nonzero[0])))
				return rt
			rt[0].append(nonzero[0])
			return rt
		for key, select in enumerate(nonzero):
			# print("-- select --")
			# print(select)
			if self.board[select] > 1:
				# print("tile appears more than twice. adding paired")
				rt[0].append(np.byte(select)) # in c, it would be presented as a single byte
			# print("-- target --")
			for target in nonzero[key+1:]:
				# print(target)
				rt[min(target, select)+1].paths.append(Path(np.byte(select), np.byte(target)))
		return rt

	# methods to do stuff
	def copy_do_move_pair_move(self, loc:BoardLoc, sel:int):
		"""
		this method does a move thats "paired" and returns a new instance
		"""
		board=copy.copy(self.board)
		# board elements are primitives.
		# shallow copy will work as well
		board[sel]-=2
		# change the value
		return FeverBoard(board, loc)
	def copy_do_move_lost(self, loc:BoardLoc, sel:int, tar:int):
		"""
		this method does a move where "sel" and "tar" are different and returns a new instance
		"""
		board=copy.copy(self.board)
		if sel == tar:
			# the only time it is the same is when the board only has 1 number
			# otherwise, its going to be a paired move with lost 0
			board[sel]-=1
		else:
			board[sel]-=1
			board[tar]-=1
			board[tar-sel-1]+=1
		# board elements are primitives.
		# shallow copy will work as well
		# change the value
		return FeverBoard(board, loc)



	def __hash__(self):
		return self.hash
	def __eq__(self, other: object) -> bool:
		return self.hash==other.hash

	def is_finished(self) -> bool:
		return not np.any(self.board, 0)

	def format_board(board):
		return_board=np.zeros(MAX_INT, numpy.byte) # extremely efficient
		for tile in board:
			return_board[tile-1]+=1
		return return_board




hash_dict={}
# stores hash
# {
# 	__hash__:BoardLoc
# 	__hash__:BoardLoc
# }

# used to look up instances
# BoardLoc contains the attribute lost which can be used to evalutate which board is better


global_board_pool=[[] for _ in repeat(None, 30)]
global_path_pool=[[] for _ in repeat(None, 30)]


# we dont evaluate paths until needed
# evalutate boards
# evalutate paths
# repeat



# print("="*100)
original_board=FeverBoard(FeverBoard.format_board([6,10,6,7,15,9,7,3,4,8]), None)
# print(original_board)
global_board_pool[0].append(original_board)
hash_dict[original_board.hash]=BoardLoc(0,0)


# pprint.pprint(global_board_pool)
# pprint.pprint(hash_dict)

# pprint.pprint(FeverBoard(FeverBoard.format_board([3]), None).get_valid_moves(BoardLoc(0,0)))

# new_board=original_board.copy_do_move_pair_move(BoardLoc(0,0), 0)
# new_board=FeverBoard(FeverBoard.format_board([6,10,6,7,15,9,7,3,4,8]), BoardLoc(1,2))
# print(original_board.hash)
# print(new_board.hash)


# exit()

cut=0
def board_eval_recursive(root_board, board_lost):
	# print(root_board.hash)
	if root_board.is_finished() == True:
		print(f"found at cut {cut}")
		print("time took")
		print(time.time()-start)
		return
	bl=BoardLoc(board_lost, len(global_board_pool[board_lost]))
	if root_board.hash in hash_dict:
		if hash_dict[root_board.hash].lost < board_lost:
			# raise Error("AN EXISTING HASH DICTIONARY HAD LOWER LOST THAN NEW")
			# this statement should also return the funciton
			# i just wanted to test some theory
			return
		if hash_dict[root_board.hash].lost > board_lost:
			print("DEBUG: dictionary board had higher lost than new board. replacing...")
			global_board_pool[hash_dict[root_board.hash].lost][hash_dict[root_board.hash].id]=None
			# set the original board to a compromised board = "None"
			# this is a bad practice but memorywise better
			hash_dict[root_board.hash]=bl
		else:
			return
	else:
		hash_dict[root_board.hash]=bl
	# print(bl)
	global_board_pool[bl.lost].append(root_board)
	moves=root_board.get_valid_moves(bl)
	for move in moves[0]:
		board_eval_recursive(root_board.copy_do_move_pair_move(bl, move), board_lost)
	path_lost=board_lost
	for bpath in moves[1:]:
		# get the remaining paths
		path_lost+=1
		if len(bpath.paths) > 0:
			global_path_pool[path_lost].append(bpath)
	# means we didnt find a solution
	return None
def construct_boards(board):
	boards=[board]
	board=global_board_pool[board.last_board.lost][board.last_board.id]
	while board.last_board != None:
		boards.append(board)
		board=global_board_pool[board.last_board.lost][board.last_board.id]
	boards.append(global_board_pool[0][0])
	return boards[::-1]




def main():
	cut=0
	for _ in repeat(None, 20):
		# print("----------")
		print(f"cut={cut}")
		# evaluate all 0 boards
		#                                                this shallow copy will allow the board to not get interuppted by the for loop
		for id, board in enumerate(global_board_pool[cut][:]):
			if board is None: continue
			bl=BoardLoc(cut, id)
			# print(f"Looping board id {bl}")
			moves=board.get_valid_moves(bl)
			for paired_move in moves[0]:
				board_eval_recursive(board.copy_do_move_pair_move(bl, paired_move), cut)

			path_lost=cut
			for bpath in moves[1:]:
				# get the remaining paths
				path_lost+=1
				if len(bpath.paths) > 0:
					global_path_pool[path_lost].append(bpath)
		
		# print("="*100)
		# print("board pool")
		# pprint.pprint(global_board_pool)
		# print("="*100)
		# # print("path pool")
		# # pprint.pprint(global_path_pool)
		# print("="*100)
		# print("dict pool")
		# pprint.pprint(hash_dict)

		# print("-----")
		# print(f"failed to find within cut:{cut}")
		cut+=1
		# print(f"cut is now {cut}")
		# print("generating new boards...")
		for bpath in global_path_pool[cut]:
			# print(f"evaluating board at loc {bpath.id}")
			stem_board=global_board_pool[bpath.id.lost][bpath.id.id]
			for p in bpath.paths:
				bl=BoardLoc(cut, len(global_board_pool[cut]))
				new_board=stem_board.copy_do_move_lost(bpath.id, p.sel, p.tar)
				# check hash before adding a board
				# probably optimize this in v9
				if new_board.is_finished() == True:
					print(f"found at cut {cut}")
					print("time took")
					print(time.time()-start)
					return
				if new_board.hash in hash_dict:
					if hash_dict[new_board.hash].lost < cut+1:
						# raise Error("AN EXISTING HASH DICTIONARY HAD LOWER LOST THAN NEW")
						# # this statement should also return the funciton
						# # i just wanted to test some theory
						# do nothing
						pass
					if hash_dict[new_board.hash].lost > cut+1:
						print("DEBUG: dictionary board had higher lost than new board. replacing...")
						global_board_pool[hash_dict[new_board.hash].lost][hash_dict[new_board.hash].id]=None
						# set the original board to a compromised board = "None"
						# this is a bad practice but memorywise better
						hash_dict[new_board.hash]=bl
						# append because this is a better board
						global_board_pool[cut].append(new_board)
					# if hash_dict[new_board.hash].lost == new_board:
					# 	print("++++++++++++++++++++++++++")
				else:
					hash_dict[new_board.hash]=bl
					# append if hash was different
					global_board_pool[cut].append(new_board)
		global_path_pool[cut]=REMOVED_FROM_MEMORY
		# print("done adding boards")
		# print("="*100)
		# print("board pool")
		# pprint.pprint(global_board_pool)
		# print("="*100)
		# print("path pool")
		# pprint.pprint(global_path_pool)
		# print("="*100)
		# print("dict pool")
		# pprint.pprint(hash_dict)
main()
main()
main()
main()
