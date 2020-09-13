import numpy as np

from itertools import repeat


table = np.fromfile("v9_fevertime_table", np.uint8, -1)


def nCr_precalculated():
	pre_calc_table = np.fromfile(
		"nCrTable0-31x0-31", np.uint32, -1).reshape([32, 32])

	def r_nCr(n, r):
		return pre_calc_table[n, r]
	return r_nCr


nCr = nCr_precalculated()


def nHr(n: int, r: int):
	return nCr((n+r-1), r)

def id_from_hnr(seq):
	formatted=np.zeros(16, np.uint8)
	for tile in seq:
		formatted[tile]+=1
	count=10
	id=0
	ln=15
	for loc in range(15, -1, -1):
		if formatted[loc]==0:
			continue
		for _ in repeat(None, formatted[loc]):
			count-=1
			for s in range(ln+1, loc+1, -1):
				id+=nHr(s, count)
			ln=loc
	return id




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







test_next = nHr_next(16, 10)
for i in range(10000000):
	tbl = test_next()
	# print("------")
	# print(tbl, " - ")
	if i % 1000 == 0:
		print("passed 1000 tests...")
	assert(i == id_from_hnr(tbl))





