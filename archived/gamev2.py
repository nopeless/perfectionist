# v7 revision
# this version tried to pair boards with branches
# but i quickly realized a memory waste
# and made path instance lists instead

import numpy as np
import math





VALID_MAX=2048
# max amount of valid returns

# X of the board
X=5
Y=4

# the logic is weird but ill just go with it anyway
class board:#                                      calculated before recursive, 
	def __init__(self, data: list, lost=0, this_move=None):
		# starts with 0 loss
		# accumulated loss
		self.lost=lost
		# only save the last move
		self.last_move=this_move

		self.board=data


		if this_move != None:
			# do stuff
			pass # edit data


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
				xx
				yy
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
	# max lost is always 14
	# 1 loss is index 0
	# pigeon sort using 14 slots

	# the next move cann


	def get_valid_moves_fever(self):
		# automatically assumes <=10
		# search linearly
		moves=[]*14

		for cell_index in range(len(self.board)):
			if self.board[cell_index] != 0:
				for iter_index in range(cell_index, len(self.board)):
					if self.board[iter_index] != 0:
						moves[abs(self.board[cell_index]-self.board[iter_index])-1].append(tuple(cell_index, iter_index))
		return moves

	def get_valid_moves_normal(self):
		# automatically assumes > 10
		moves=[]*14
		for row_num_index in range(0, len(self.board), X):
			for col in range(row_num_index, row_num_index+Y):
				if self.board[col] != 0:
					# check for the row cells
					for target in range(col, row_num_index+X):
						if self.board[col] != self.board[target]:
							# add reverse case
							moves[abs(self.board[col]-self.board[target])-1].append(tuple(target, col))
						moves[abs(self.board[col]-self.board[target])-1].append(tuple(col, target))
		return moves



if __name__=="__main__":
	game_board=board(5, 4, np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,1,2,3,4,5], dtype=np.byte))
	print(game_board)
























