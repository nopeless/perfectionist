# gamev10 fever time gile gen is just about cleaning code again so that i dont need to mess around anymore




# made with love by nope ❤

from copy import Error
import math
import time
import numpy as np
from itertools import repeat













def nCr_precalculated():
	pre_calc_table = np.fromfile(
		"nCrTable0-31x0-31", np.uint32, -1).reshape([32, 32])

	def r_nCr(n, r):
		return pre_calc_table[n, r]
	return r_nCr


nCr = nCr_precalculated()


def nHr(n: int, r: int):
	return nCr((n+r-1), r)

def nHr_next(n, r):
	arrange = np.full(r, n-1, dtype=np.uint8, order='C')
	arrange[-1] = n

	def nHr_recursive():
		nonlocal arrange

		if arrange[0] == 0:
			print("SOFTWARN: overloop")
			arrange = np.full(r, n-1, dtype=np.uint8, order='C')
			arrange[-1] = n
		p = r-1
		while arrange[p] == 0:
			p -= 1
		arrange[p] -= 1
		for i in range(p+1, r):
			arrange[i] = arrange[p]
		return arrange
	return nHr_recursive




# table = np.full(3268760, 255, dtype=np.uint8, order='C')
table = np.fromfile("v10_fevertime_table.bin", np.uint8, -1)

class FeverBoard:
	def __init__(self, board) -> None:
		self.board = board
		# print(self)
		self.id = self.id_from_stacked()

	def __repr__(self) -> str:
		return f"<FeverBoard {self.board}>"

	def id_from_stacked(self):
		# deal with frikin nHr stuff
		count = 10
		id = 0
		ln = 15
		for loc in range(15, -1, -1):
			# print(f"looping loc : {loc}")
			if self.board[loc] == 0:
				continue
			for _ in repeat(None, self.board[loc]):
				# print("  repeating...")
				count -= 1
				# nHr(?, count)
				for s in range(ln+1, loc+1, -1):
					# print(f"s:{s}")
					id += nHr(s, count)
					# print(f"id is now {id}")
				ln = loc
		return id

	@classmethod
	def format_board(cls, board):
		return_board = np.zeros(16, np.uint8)  # extremely efficient
		for tile in board:
			return_board[tile] += 1
		return return_board

	def rcc_fill_table(self):
		if table[self.id] != 255:
			return table[self.id]
		if self.board[0] > 10:
			raise Exception("more than 10 zeros?????? WTF")
			# FIXMEEEEEE
		if self.board[0] == 10:
			return 0

			# raise Exception("Why did i get an empty board???")
		if self.board[0] == 9:
			for k, v in enumerate(self.board[1:], 1):
				if v != 0:
					table[self.id] = k
					return table[self.id]
		# for every other case
		nonzero = np.where(self.board != 0)[0]
		if nonzero[0] == 0:
			nonzero=nonzero[1:]
		if len(nonzero) == 0:
			print(self.board)
			raise Exception(
				"WHAT... len was 0 which means zero count should be 0")
		minlost = 254
		# print(nonzero)
		for key, select in enumerate(nonzero, 1):
			if self.board[select] > 1:
				board = self.board.copy()
				board[select] -= 2
				board[0] += 2
				minlost = min(FeverBoard(board).rcc_fill_table(), minlost)
			for target in nonzero[key:]:
				# paired stuff
				# print(f" ({select}, {target})")

				board = self.board.copy()
				board[select] -= 1
				board[target] -= 1
				board[target-select] += 1
				board[0] += 1
				minlost = min(FeverBoard(board).rcc_fill_table()+select, minlost)
		table[self.id] = minlost
		return table[self.id]


original_board = FeverBoard(FeverBoard.format_board(
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
print(original_board.id)
original_board = FeverBoard(FeverBoard.format_board(
	[13, 15, 15, 15, 15, 15, 15, 15, 15, 15]))
print(original_board.id)


# print(original_board)

# testing purpose

test_next = nHr_next(16, 10)
for i in range(1000):
	tbl = test_next()
	# print("------")
	print(tbl, " - ", end="")
	print(FeverBoard(FeverBoard.format_board(tbl)).id)
	assert(i == FeverBoard(FeverBoard.format_board(tbl)).id)


# 255 is the marker for "not calculated yet"

# table[0] = 0
# next = nHr_next(16, 10)
# counter = 0
# kcounter=0
# for id in range(3268760):
# 	arr = next()
# 	if table[id] != 255:
# 		continue
# 	FeverBoard(FeverBoard.format_board(arr)).rcc_fill_table()
# 	counter+=1
# 	if counter == 1000:
# 		counter = 0
# 		kcounter += 1
# 		if kcounter % 10 == 0:
# 			print(f"{kcounter}k+ values written id {id}")
# 			table.tofile("v10_fevertime_table.bin")
# 			print("done writing on file")


# # # add main logic


# table.tofile("v10_fevertime_table.bin")









