
# v9 includes 0 in feverboard
# which is the MAIN difference between other boards
# this code is incompatible with v8

import math
import time
import numpy as np
from itertools import repeat


def nCr(n: int, r: int):
	return math.factorial(n)//(math.factorial(r)*math.factorial(n-r))


def nHr(n: int, r: int):
	return nCr((n+r-1), r)


"""
`seq`: the list; must be sorted beforehand
`num_range`: the upper limit"""


def id_from_seq(seq, start, end, p: int = 0):
	c = len(seq)-p-1
	if c == 0:
		return seq[p]-start+1
	id = 0

	# lists only pass references
	# hence not a good idea to modify the original seq
	for n in range(end-start+1, end+1-seq[p], -1):
		id += nHr(n, c)

	return id + id_from_seq(seq, seq[p], end, p+1)


"""
returns an array size r with numbers ranging from 0 to r-1"""
def nHr_next(n, r):
	arrange = np.full(r, 0, dtype=np.uint8, order='C')
	arrange[-1]=-1
	def nHr_recursive():
		nonlocal arrange
		if arrange[0] == n-1:
			print("SOFTWARN: overloop")
			arrange = np.full(r, 0, dtype=np.uint8, order='C')
			arrange[-1]=-1
		p = -1
		while arrange[p] == n-1:
			p -= 1
		arrange[p]+=1
		for i in range(p+1, 0):
			arrange[i]=arrange[p]
		return arrange
	return nHr_recursive
# for _ in range(21):
# 	print(next())


class FeverBoard:
	def __init__(self, board) -> None:
		self.board=board
		print(self)
		self.id=self.id_from_stacked()

	def __repr__(self) -> str:
		return f"<FeverBoard {self.board}>"

	def id_from_stacked(self):
		# deal with frikin nHr stuff
		count=10
		id=0
		ln=0
		for loc in range(0, 16):
			# print(f"looping loc : {loc}")
			if self.board[loc] == 0: continue
			for _ in repeat(None, self.board[loc]):
				# print("  repeating...")
				count-=1
				# nHr(?, count)
				for s in range(16-ln, 16-loc, -1):
					id+=nHr(s, count)
					# print(f"id is now {id}")
				ln=loc
		return id


	def format_board(board):
		return_board=np.zeros(16, np.uint8) # extremely efficient
		for tile in board:
			return_board[tile]+=1
		return return_board

original_board=FeverBoard(FeverBoard.format_board([0,15,15,15,15,15,15,15,15,15]))
print(original_board.id)
# print(original_board)

#testing purpose
# test_next = nHr_next(16, 10)
# for i in range(100):
# 	tbl = test_next()
# 	print("------")
# 	print(FeverBoard(FeverBoard.format_board(tbl)).id)
# 	print(id_from_seq(tbl))
	




# table = np.full(3268760, 255, dtype=np.uint8, order='C')
# # 255 is the marker for "not calculated yet"

# next = nHr_next(16,10)
# for id in range(0, 3268760):
# 	if table[id] != 255: continue
# 	arr=next()
	# get the array









# add main logic


# table.tofile("v9_fevertime_table")
