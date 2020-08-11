






import math
import time



def nCr(n:int, r:int):
	return math.factorial(n)//(math.factorial(r)*math.factorial(n-r))
def nHr(n:int, r:int):
	return nCr((n+r-1), r)


print(nHr(4,0))


"""
`seq`: the list; must be sorted beforehand
`num_range`: the upper limit""" 
def id_from_seq(seq, start, end, p:int=0):
	print(f"seq {seq}, start {start}, end {end}, p {p}")
	c=len(seq)-p-1
	if c == 0:
		return seq[p]-start+1
	id=0
	
	# lists only pass references
	# hence not a good idea to modify the original seq
	for n in range(end-start+1, end+1-seq[p], -1):
		print("loop")
		id+=nHr(n, c)
	
	return id + id_from_seq(seq, seq[p], end, p+1)



start=time.time()
for i in range(1000000):
	num_seq=[15,15,15,15,15,15,15,15,15,15]

print(time.time()-start)




