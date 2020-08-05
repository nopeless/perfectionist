# v7 revision
# v6 was the first attempt to implement a tree-leaf search
# it got scrapped due to it not utilizing memory efficiently
# to be specific, v7 could shave off 1 memory writing step
# which is huge when it comes to gcs





# the 5th rewrite








from typing import List

# yeets space complexity for best speed and constant performance
# unfortunately had a memory issue. going for v7






class Path:
	def __init__(self, start, end) -> None:
		self.start=start
		self.end=end
	def __repr__(self) -> str:
		return f"<Path [{self.start}, {self.end}]>"



class B_path:
	def __init__(self, id, paths:List[Path]=[]) -> None:
		self.id=id
		self.paths=paths



class r_board:
	# recursive board
	# dont need to care about the name honestly
	def __init__(self, data, paths:List[Path]=[]) -> None:
		self.data=data
		self.paths=paths
	def get_valid_moves(self, id) -> List[List[B_path]]:
		# returns array clump
		pass
	def __repr__(self):
		return f"<r_board pathcount={len(self.paths)}, most recent path={self.paths[-1]}>"












































