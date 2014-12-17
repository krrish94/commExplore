class Robot:

	""" Class to hold the location and orientation of a robot """

	# Initializes the instance of the robot created
	def __init__(self, robotID, locX, locY, orientation):

		self.robotID = robotID
		self.curX = locX
		self.curY = locY
		self.orientation = orientation
		# A status bit to indicate whether the robot is successfully placed on the grid
		self.status = False


	# Perform reinitialization (Used while placing robots on the grid)
	def reinit(self, locX, locY, orientation):

		self.curX = locX
		self.curY = locY
		self.orientation = orientation
		self.status = True
		# Adding variables to store the index of the nearest frontier point
		self.nearestFrontier = -1