








class BoardLoc:
	def __init__(self, lost:int, id:int) -> None:
		self.lost=lost
		self.id=id
	def __repr__(self) -> str:
		return f"({self.lost}, {self.id})"
	# def is_origin(self) -> bool:
	# 	return (self.lost==0) and (self.id==0)



class B_path:
	def __init__(self, id:BoardLoc=BoardLoc(0,0), paths=[]) -> None:
		self.id=id
		# list of paths
		self.paths=paths[:]
		print("init")
	def __repr__(self) -> str:
		return f"<B_path id={self.id} paths={self.paths}>"

loc = BoardLoc(1,1)

rt = [None, None]

rt[0] = B_path(loc)
rt[1] = B_path(loc)

rt[0].paths.append(3)
rt[1].paths.append(4)

print(rt)
"""
Output:
init
init
[<B_path id=(1, 1) paths=[3, 4]>, <B_path id=(1, 1) paths=[3, 4]>]"""


