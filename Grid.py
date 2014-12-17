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





import Cell
import Robot

class Grid:
	"""Class to hold a grid that represents the environment"""


	# Initializes the instance of Grid that is created
	def __init__(self, height, width, obstacles):

		# Number of rows in the grid
		self.height = height
		# Number of columns in the grid
		self.width = width
		# Array of grid cells
		self.cells = [[Cell.Cell(i, j) for j in range(width)] for i in range(height)]
		
		# print self.cells[1][1].x, self.cells[1][1].visited
		
		# Initialize the locations of the obstacles
		for obstacle in obstacles:
			self.cells[obstacle[0]][obstacle[1]].status = -1


	# Takes as input the X and Y coordinates of the sites where robots have to be initialized
	# Returns 0 if initialization is successful
	# Returns -1 if initialization fails (location not empty, or another robot has same location)
	def initRobotLocations(self, locX, locY, robotID):

		if self.cells[locX][locY].status != 0:
			return -1
		else:
			self.cells[locX][locY].status = robotID
			self.cells[locX][locY].visited = True
			return 0


	# Function to move a specified robot from one location to another
	# Note that we first have to check if it is a feasible move
	def moveRobot(self, robot, height, width, command):

		# Variables to hold the next location
		nextX = 0
		nextY = 0

		# Variables to hold the robot's current location
		curX = robot.curX
		curY = robot.curY

		# We first determine the cell which we have to move to, according to the command given
		if command == 0:
			if curY == width - 1:
				print 'Out of grid'
				return -1
			else:
				nextX = curX
				nextY = curY + 1

		if command == 1:
			if curY == width - 1 or curX == 0:
				print 'Out of grid'
				return -1
			else:
				nextX = curX - 1
				nextY = curY + 1

		if command == 2:
			if curX == 0:
				print 'Out of grid'
				return -1
			else:
				nextX = curX - 1
				nextY = curY

		if command == 3:
			if curY == 0 or curX == 0:
				print 'Out of grid'
				return -1
			else:
				nextX = curX - 1
				nextY = curY - 1

		if command == 4:
			if curY == 0:
				print 'Out of grid'
				return -1
			else:
				nextX = curX
				nextY = curY - 1

		if command == 5:
			if curY == 0 or curX == height - 1:
				print 'Out of grid'
				return -1
			else:
				nextX = curX + 1
				nextY = curY - 1

		if command == 6:
			if curX == height -1:
				print 'Out of grid'
				return -1
			else:
				nextX = curX + 1
				nextY = curY

		if command == 7:
			if curX == height - 1 or curY == width - 1:
				print 'Out of grid'
				return -1
			else:
				nextX = curX + 1
				nextY = curY + 1

		if command == 8:
			nextX = curX
			nextY = curY


		print 'Next', nextX, nextY

		# We now need to determine if (newX, newY) is feasible
		if command != 8 and self.cells[nextX][nextY].status != 0:
			print 'Next cell is an obstacle'
			return -1
		
		else:
			
			self.cells[curX][curY].status = 0
			self.cells[curX][curY].visited = True
			robot.curX = nextX
			robot.curY = nextY
			self.cells[nextX][nextY].status = robot.robotID

			return 0