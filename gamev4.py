import itertools
from itertools import repeat
import numpy as np
import pprint
import heapq
import copy



X=4
Y=3
SIZE=X*Y


CUT=50
MAX_BRANCH_POOL=100


FEVER=10
MAX_INT=15


class r_board:
	def __init__(self, board, count, lost, path=[]):
		self.board=board
		self.lost=lost
		self.count=count
		self.path=path
	
	def __eq__(self, other):
		return self.board.__hash__==other.board.__hash__
		

	def __repr__(self):
		i=0
		outstr="\n"+"-"*(X*3+2)+"\n"
		for yy in range(Y):
			outstr+="|"
			for xx in range(X):
				xx,yy
				outstr+=str(self.board[i]).rjust(2, " ")+" "
				i+=1
			outstr+="|\n"
		outstr+="-"*(X*3+2)+f"\nlost: {self.lost}\n"
		return outstr

	def __hash__(self):
		return hash(str(self.board))


	def get_valid_moves(self):
		if self.count==0:
			return [[Move(0, None, None)]]
		moves=[[] for x in repeat(None, MAX_INT)]
		if self.count==1:
			# only can be 15
			moves=[[] for x in repeat(None, MAX_INT+1)]
			for s in range(SIZE):
				# print(s)
				if self.board[s]!=0:
					moves[self.board[s]].append(Move(0, s, s))
					return moves
		else:
			moves=[[] for x in repeat(None, MAX_INT)]
		count_minus_1=self.count-1
		count_minus_2=self.count-2

		if self.count <= FEVER:
			# fever time
			for select_index in range(SIZE-1):
				if self.board[select_index] != 0:
					for target_index in range(select_index+1, SIZE):
						if self.board[target_index] != 0:
							if self.board[select_index]==self.board[target_index]:
								# dont flip
								moves[0].append(Move(count_minus_2, select_index, target_index))
							else:
								moves[min(self.board[select_index], self.board[target_index])].extend([Move(count_minus_1, select_index, target_index), Move(count_minus_1, target_index, select_index)])
		else:
			one_index=[]
			for row_idx in range(0, SIZE, X):
				for select_index in range(row_idx, row_idx+X):
					if self.board[select_index] != 0:
						if self.board[select_index] == 1:
							one_index.append(select_index)
						for target_index in list(range(select_index+1, row_idx+X)):
							if self.board[target_index] != 0:
								if self.board[select_index]==self.board[target_index]:
									moves[0].append(Move(count_minus_2, select_index, target_index))
								else:
									moves[min(self.board[select_index], self.board[target_index])].extend([Move(count_minus_1, select_index, target_index), Move(count_minus_1, target_index, select_index)])
								break
						for target_index in list(range(select_index+X, SIZE, X)):
							if self.board[target_index] != 0:
								if self.board[select_index]==self.board[target_index]:
									if self.board[select_index] != 1:
										moves[0].append(Move(count_minus_2, select_index, target_index))
								else:
									if self.board[select_index]==1:
										moves[1].append(Move(count_minus_1, target_index, select_index))
									else:
										moves[min(self.board[select_index], self.board[target_index])].extend([Move(count_minus_1, select_index, target_index), Move(count_minus_1, target_index, select_index)])
								break

			# print("*"*100)
			# pprint.pprint(moves)
			for target_index, val in enumerate(self.board):
				if val > 1:
					for select_index in one_index:
						moves[1].append(Move(count_minus_1, select_index, target_index))

			# print("*"*100)
			# pprint.pprint(moves)
			for i, select_index in enumerate(one_index[:-1]):
				for target_index in one_index[i+1:]:
					moves[0].append(Move(count_minus_2, select_index, target_index))

		return moves


	# def return_move(self, move):
	# 	# returns a new instance of self with new move
	# 	data=self.board[:]
	# 	# no need to calculate count
	# 	lost=min(data[move.select], data[move.target])
	# 	data[move.target]=abs(data[move.select]-data[move.target])
	# 	data[move.select]=0
		
	# 	return r_board(data, move.count, lost, self.path.append(move))
	
	def do_move(self, move):
		if move.select==None:
			return self
		if self.board[move.select]==self.board[move.target]:
			if move.select == move.target:
				lost=self.board[move.select]
			else:
				lost=0
		else:
			lost=min(self.board[move.select], self.board[move.target])
		self.board[move.target]=abs(self.board[move.select]-self.board[move.target])
		self.board[move.select]=0
		self.count=move.count
		self.path.append([move.select, move.target])
		self.lost+=lost
		return self



class Move:
	def __init__(self, count, select, target):
		self.count=count
		self.select=select
		self.target=target

	def __repr__(self):
		return f"<Move count:{repr(self.count)} select:{repr(self.select)} target:{repr(self.target)}>"
	
class Child_Move:
	def __init__(self, move, id):
		self.select=move.select
		self.target=move.target
		self.count=move.count
		self.id=id

	def __repr__(self):
		return f"<Move count:{repr(self.count)} select:{repr(self.select)} target:{repr(self.target)} id:{repr(self.id)}>"
	

	def __lt__(self, other):
		return self.count < other.count

# log_file=open()



if __name__=="__main__":
	# print("\n"*1000)
	# log_file=open("./outlog.txt", "w")
	# log_file.write("")
	# log_file.close()
	# log_file.
	# game_board=r_board(np.array(
	# 	[
	# 	 3,  9, 12,  3,  9, 10,
	# 	15,  3, 12, 10,  5, 11,
	# 	 6, 12,  7, 10,  1,  3,
	# 	 8, 13,  5,  8,  2,  8,
	# 	15,  1,  7, 10,  8, 15,
	# 	 3, 15, 14, 14, 15, 15,
	# 	 6,  1,  4, 14, 15,  8,
	# 	 7, 14,  4,  9,  3,  2
	# 	], dtype=np.byte), SIZE, 0)
	# game_board=r_board(np.array(
	# 	[
	# 	  4,  7,  2,  9, 12, 15,
	# 	  7,  4,  1,  5,  1,  4,
	# 	  8, 13, 13, 10,  4, 13,
	# 	  4, 15,  9,  4,  4, 12,
	# 	  4,  2,  4, 14, 13,  6,
	# 	 15, 13,  1,  4,  1, 10,
	# 	  9,  4,  6,  9,  2, 11,
	# 	 10, 11,  1,  9, 11, 11
	# 	], dtype=np.byte), SIZE, 0)
	game_board=r_board(np.array(
		[
		 1,4,3,5,
		 2,3,3,7,
		 10,5,10,12], dtype=np.byte), SIZE, 0)
	# game_board=r_board(np.array(
	# 	[
	# 	 1,2,
	# 	 3,4], dtype=np.byte), SIZE, 0)
	# game_board=r_board(np.array(
	# 	[
	# 	 3,4,4,3], dtype=np.byte), SIZE, 0)
	# print(game_board)
	

	# pprint.pprint(game_board.get_valid_moves())
	# s=0
	# for thing in game_board.get_valid_moves():
	# 	s+=len(thing)
	# print(s)
	# exit()

	
	old_list=[game_board]
	iterblock=0
	new_set=set()
	while True:
		print(f"iterating {iterblock} times...")
		# print("-"*100)
		# print(old_list)
		# until global pool doesnt have a count != 0
		again=False
		global_pool=[[] for x in repeat(None, CUT)]
		for id, root_game in enumerate(old_list):
			lost=root_game.lost
			# print("ENUMERATE")
			for lost_indexed_moves in root_game.get_valid_moves()[0:CUT-lost]:
				# print("LOST_INDEXED")
				# print(lost_indexed_moves)
				for move in lost_indexed_moves:
					if (again==False) and (move.count != 0):
						again=True
					# print(move)
					global_pool[lost].append(Child_Move(move, id))
				lost+=1
				if lost >= CUT:
					break
		# pprint.pprint(global_pool)
		# we have the global pool now
		if again==False:
			print("returning best")
			for child_move_lists in global_pool:
				if len(child_move_lists) > 0:
					for stuff in child_move_lists:
						final_board=copy.deepcopy(old_list[stuff.id])
						final_board.do_move(stuff)
						print("-"*100)
						print(final_board.path)
						print(final_board.lost)
						print("-"*100)
					exit()
			print(":(")

		remaining_branches=MAX_BRANCH_POOL


		for moves in global_pool:
			# print(remaining_branches)
			if len(moves) > remaining_branches:
				# print("iterating...")
				# do stuff here
				# pprint.pprint(heapq.nlargest(remaining_branches, moves))
				for cmove in heapq.nlargest(remaining_branches, moves):
					# we have time
					# move is a Child_Move
					if cmove.target == None:
						new_set.add(old_list[cmove.id])
					else:
						new_set.add(copy.deepcopy(old_list[cmove.id]).do_move(cmove))
			else:
				# print("not iterating...")
				# we have time
				for cmove in moves:
					# move is a Child_Move
					if cmove.target == None:
						new_set.add(old_list[cmove.id])
					else:
						new_set.add(copy.deepcopy(old_list[cmove.id]).do_move(cmove))
			
			remaining_branches-=len(moves)
			if remaining_branches<=0:
				break
		# input()
		# print("newset vvvvvvvvvvvvvvvv")
		# print(new_set)
		# print("-"*100)
		# print("setting old list to new set")
		old_list=list(new_set)
		if len(old_list) == 0:
			print("No solution under given parameters")
			break
		new_set=set()
		




		if iterblock > 100:
			print("overloop")
			break

		iterblock+=1
		# input()















































