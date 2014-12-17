class Cell(object):
	"""Class to hold a grid cell"""

	def __init__(self, x, y):

		self.x = x
		self.y = y
		self.status = 0
		self.visited = False
		# print self.x, self.y