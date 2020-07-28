
import numpy as np
import math
from itertools import repeat
import pprint



CUT=5
# cut when the loss gets above that
SEARCH_DEPTH=2
SELECT=10
# how many branches to keep
# only select top 10 best branches
# the search depth for cutting stuff
# every branch will compete from there


# X of the board
X=5
Y=4
SIZE=20
FEVER=10
MAX_INT=15
# maximum integer for the tile
# fever time starting tile count


# the logic is weird but ill just go with it anyway
class board:
	# the interface board because i am trash at coding and didnt want to make branching code
	def __init__(self, data: list):

		self.board=data
		self.count=np.count_nonzero(self.board)


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

	def get_valid_moves_fever(self):
		# automatically assumes <=10
		# search linearly
		moves=[[] for x in repeat(14)]

		for cell_index in range(len(self.board)):
			if self.board[cell_index] != 0:
				for iter_index in range(cell_index+1, len(self.board)):
					if self.board[iter_index] != 0:
						moves[abs(self.board[cell_index]-self.board[iter_index])-1].append(tuple([cell_index, iter_index]))
		return moves

	def get_valid_moves_normal(self):
		# automatically assumes > 10
		moves=[[] for n in repeat(None, 14)]

		print(moves)
		for row_num_index in range(0, len(self.board), X):
			for col in range(row_num_index, row_num_index+X):
				if self.board[col] != 0:
					# check for the row cells
					for target in range(col+1, row_num_index+X):
						moves[abs(self.board[col]-self.board[target])].append(tuple([col, target]))
						if self.board[col] != self.board[target]:
							# add reverse case
							moves[abs(self.board[col]-self.board[target])].append(tuple([target, col]))
		return moves

	def min_find(self):
		# going to be cut and max

		# cut will cut a branch if exceeds
		# max will allow n amount of branches to be present
		return r_board(self.board).recursive_min_find()



class r_board:#                                                    calculated before recursive, 
	def __init__(self, data: list, lost=0, count: np.int16=None, this_move_a: np.int16=None, this_move_b: np.int16=None):
		# starts with 0 loss
		self.lost=lost
		# only save the last move
		self.last_move_a=this_move_a
		self.last_move_b=this_move_b

		self.board=data


		self.board[this_move_b]=abs(self.board[this_move_a]-self.board[this_move_b])

		if self.board[this_move_b] == 0:
			count-=2
		else:
			count-=1
			self.lost+=min([self.board[this_move_a], self.board[this_move_b]])
		# this bottom means removing 1 count
		self.board[this_move_a]=0
			


		# print(self.board)
		# i=0
		# for yy in range(y):
		# 	for xx in range(x):
		# 		# if isinstance(data[i], np.byte) == False:
		# 		# 	raise TypeError(f"TypeError: expected an instance of type 'int' got {repr(type(data[i]).__name__)} instead")
		# 		self.board[yy][xx]=data[i]
		# 		if data[i] != 0:
		# 			self.count+=1
		# 		i+=1



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
	
	# there are 3 types of moves
	# paired moves, unequal moves, and single moves
	# the paired and unequal moves are delt by numbers that are NOT 1
	# the single moves are ONLY delt by the number 1

	# paired moves happen when two blocks disappear together
	# when searching for paired moves, only look in the down right diagonal
	# so no duplicates can appear

	# for unequal moves, search down right diagonal but add a reverse one as well (optimized search time)
	# for example, 8->3 works and also 3->8 works as well

	# for single moves, only "1" blocks can access this
	# "1" blocks move to the other block
	# this cannot produce duplicates

	# a move is formatted like this
	# ((x,y), (x,y))

	# use pigeon sort for the move selecting
	# max lost is always MAX_INT
	# 0 loss is index 0
	# pigeon sort using MAX_INT slots

	# the next move cann


	def get_valid_moves_fever(self):
		# automatically assumes <=FEVER
		# search linearly
		moves=[[] for x in repeat(MAX_INT)]

		for cell_index in range(len(self.board)):
			if self.board[cell_index] != 0:
				for iter_index in range(cell_index+1, len(self.board)):
					if self.board[iter_index] != 0:
						moves[abs(self.board[cell_index]-self.board[iter_index])-1].append(tuple([cell_index, iter_index]))
		return moves

	def get_valid_moves_normal(self):
		# automatically assumes > FEVER
		moves=[[] for n in repeat(None, MAX_INT)]

		print(moves)
		for row_num_index in range(0, len(self.board), X):
			for col in range(row_num_index, row_num_index+X):
				if self.board[col] != 0:
					# check for the row cells
					for target in range(col+1, row_num_index+X):
						moves[abs(self.board[col]-self.board[target])].append(tuple([col, target]))
						if self.board[col] != self.board[target]:
							# add reverse case
							moves[abs(self.board[col]-self.board[target])].append(tuple([target, col]))
		return moves

	def recursive_min_find(self, branch:int):
		# __init__(self, data: list, lost=0, count: np.int16=None, this_move_a: np.int16=None, this_move_b: np.int16=None):
		# checks for fever
		if self.count <= FEVER:
			pass
		else:

			return r_board(self.board, lost=self.lost, count=self.count)
	
	def recursive_min_find_fever(self, branch:int):
		# assumes fever and calls fever too
		return {}


class solution:
	def __init__(self, lost:int, path:list, solved:bool):
		self.lost=lost
		self.path=path
		self.solved=solved

	def __lt__(self):
		if self.lost == other.lost:
			if self.solved == True:
				return True
			return False
		return self.lost < other.lost


if __name__=="__main__":
	game_board=board(np.array([10,9,2,1,10,4,13,2,12,2,5,10,8,10,11,14,15,10,11], dtype=np.byte))
	print(game_board)
	pprint.pprint(game_board.get_valid_moves_normal())
	print(game_board.min_find())
























