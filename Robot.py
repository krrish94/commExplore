# The MIT License (MIT)

# Copyright (c) 2014 Krishna Murthy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



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