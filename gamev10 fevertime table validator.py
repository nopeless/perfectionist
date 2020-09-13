# a validator script to check if the thing actually works




import random

import gamev10_v8_1_fevertime_migration as mig

import numpy as np

from itertools import repeat




def get_rnd_seq():
	ret=[]
	for i in range(10):
		ret.append(random.randint(0, 15))
	return ret


table = np.fromfile("v10_fevertime_table.bin", np.uint8, -1)


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

for i in range(100):
	if i % 10 == 0:
		print(f"i: {i}")
	rnd_seq=get_rnd_seq()
	rnd_seq_no_zero=rnd_seq[:]
	while 0 in rnd_seq_no_zero:
		rnd_seq_no_zero.remove(0)
	actual=mig.main(rnd_seq_no_zero)
	tabled=table[id_from_hnr(rnd_seq)]
	if not actual==tabled:
		print(f"MISMATCH on seq: {rnd_seq}   -     no zero: {rnd_seq_no_zero}")
		print(f"    actual: {actual} tabled: {tabled}")

# print(mig.main([11, 5, 5, 4, 14, 15, 3, 1, 13]))





