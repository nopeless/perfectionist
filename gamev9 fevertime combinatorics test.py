






import math
import time
from itertools import repeat
import pprofile


import numpy as np

import pprofile
profiler=pprofile.Profile()


def nCr(n:int, r:int):
	return math.factorial(n)//(math.factorial(r)*math.factorial(n-r))
def nHr(n:int, r:int):
	return nCr((n+r-1), r)

def nCr_precalculated():
	pre_calc_table=np.fromfile("nCrTable0-31x0-31", np.uint32, -1).reshape([32,32])
	def r_nCr(n, r):
		return pre_calc_table[n, r]
	return r_nCr




# unit test

nCr_=nCr_precalculated()
for n in range(32):
	for r in range(0, n):
		assert(nCr(n, r) == nCr_(n, r))


# gentbl=np.zeros([32, 32], dtype=np.uint32)
# def gen():
# 	for n in range(32):
# 		for r in range(0, n):
# 			gentbl[n, r]=nCr(n, r)

# gen()
# gentbl.tofile("nCrTable0-31x0-31")
# print(nHr(4,0))


"""
`seq`: the list; must be sorted beforehand
`num_range`: the upper limit""" 
def id_from_seq(seq, start, end, p:int=0):
	# print(f"seq {seq}, start {start}, end {end}, p {p}")
	c=len(seq)-p-1
	if c == 0:
		return seq[p]-start+1
	id=0
	
	# lists only pass references
	# hence not a good idea to modify the original seq
	for n in range(end-start+1, end+1-seq[p], -1):
		# print("loop")
		id+=nHr(n, c)
	
	return id + id_from_seq(seq, seq[p], end, p+1)



# nCr_=nCr_precalculated()
num_seq=[15,15,15,15,15,15,15,15,15,15]
def main():
	start=time.time()
	for _ in repeat(None, 1000000):
		nCr_(31,10)
		# id_from_seq(num_seq, 0, 15)
	print(time.time()-start)

with profiler:
	main()

profiler.dump_stats("v9 combinatorics profile.txt")


