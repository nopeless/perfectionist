# v7 revision
# v3 implements a recursive board and an actual board class (not in the code)
# it has various features but was discarded for a better branch logix


import itertools
from itertools import repeat
import numpy as np
import pprint



X=5
Y=4
SIZE=20
CUT=5
MAX_BRANCH_POOL=10


FEVER=10
MAX_INT=15

class r_board:

	def __init__(self, board, count, lost, path=[]):
		self.board=board
		self.lost=lost
		self.count=count
		self.path=[]
		# use count for solved

	def __eq__(self, other):
		return self.board==other.board

	def __lt__(self):
		if self.lost == other.lost:
			return self.count < other.count
		return self.lost < other.lost

	def __hash__(self):
		return hash(str(self.board))

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

	def get_valid_moves(self):
		moves=[[] for x in repeat(None, MAX_INT)]
		if self.count <= FEVER:
			for cell_index in range(len(self.board)):
				if self.board[cell_index] != 0:
					for iter_index in range(cell_index, len(self.board)):
						if self.board[iter_index] != 0:
							if self.board[cell_index] == self.board[iter_index]:
								moves[abs(self.board[cell_index]-self.board[iter_index])-1].append(tuple([self.count-2, self.lost, cell_index, iter_index]))
							else:
								moves[abs(self.board[cell_index]-self.board[iter_index])-1].append(tuple([self.count-1, self.lost+min(self.board[cell_index], self.board[iter_index]),cell_index, iter_index]))
								moves[abs(self.board[cell_index]-self.board[iter_index])-1].append(tuple([self.count-1, self.lost+min(self.board[cell_index], self.board[iter_index]),iter_index, cell_index]))
		else:
			for row_num_index in range(0, len(self.board), X):
				for col in range(row_num_index, row_num_index+Y):
					if self.board[col] != 0:
						# check for the row cells
						for target in range(col, row_num_index+X):
							if self.board[col] == self.board[target]:
								moves[abs(self.board[col]-self.board[target])-1].append(tuple([self.count-2, self.lost, target, col]))
							else:
								#     the lost                                                               accumulated lost
								moves[abs(self.board[col]-self.board[target])-1].append(tuple([self.count-1, self.lost+min(self.board[col],self.board[target]),col, target]))
								moves[abs(self.board[col]-self.board[target])-1].append(tuple([self.count-1, self.lost+min(self.board[col],self.board[target]), col, target]))
		
		return moves







if __name__=="__main__":
	game_board=r_board(np.array([10,9,2,1,10,4,13,2,12,2,5,10,8,10,11,14,15,10,11,12], dtype=np.byte), X*Y, 0, )
	print(game_board)
	global_pool=[[] for x in repeat(None, CUT)]
	print(global_pool)
	old_set={game_board}
	iterblock=0


	# TUPLE DOC
	# 0: count
	# 1: accumulated lost
	# 2: point a
	# 3: point b
	while True:
		again=False
		if iterblock > 4:
			break
			print("broke by iterbreak")
		for root_board in old_set:
			# get valid moves returns something like
			# [
			# [(),()],
			# [(),()]
			# ]
			lost_index=0
			for moves in root_board.get_valid_moves():
				for move in moves:
					print(move)
					if again and move[0] != 0:
						again=True
					if move[1] <= CUT:
						global_pool[move[1]].append(tuple([]))
				lost_index+=1
				
		print("appended everything")
		print(global_pool)
		print("going to need " + int(MAX_BRANCH_POOL) + " branches")
	
		print(global_pool)
		break


		iterblock+=1

	print("something")
















