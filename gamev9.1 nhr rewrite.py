import numpy as np


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




next=nHr_next(4, 3)

for i in range(21):
	print(next())
