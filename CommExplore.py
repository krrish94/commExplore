# The MIT License (MIT)

# Copyright (c) 2014 INSPIRE Lab, BITS Pilani

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


"""
Provides an implementation of the Communicative Exploration algorithm for a fixed base station.
"""


import math
import random
import sys

import AStar
import GridWorld
import Robot


# The CommExplore class
class CommExplore:

	"""
	height and width specify the dimensions of the environment
	obstacles is a list of locations which are to be initialized as obstacles
	R specifies the range of communication
	numRobots specifies the number of robot objects to be initialized
	initLocs specifies the initial locations for each of the robots
	k specifies the size of the population of configuration changes
	T specifies the number of time steps to run the simulation for
	base specifies the coordinates of the base station
	"""
	def __init__(self, height, width, obstacles, numRobots, initLocs, R = 10, k = 10, T = 10, base = [0, 0]):

		# Initialize the grid world
		self.gridworld = GridWorld.GridWorld(height, width, obstacles)
		
		# Initialize a list of robots
		self.robots = [Robot.Robot(j+1, -1, -1) for j in range(numRobots)]
		# Initialize the starting location of each robot
		i = 0
		for initLoc in initLocs:
			# If any robot is placed out of bounds or on an obstacle, print an error message and exit
			currentPoint = (initLoc[0], initLoc[1])
			if not self.gridworld.inBounds(currentPoint) or not self.gridworld.passable(currentPoint):
				print 'Initial location', currentPoint, 'is not possible'
				sys.exit(-1)
			# Otherwise, modify the current location of the robot to currentPoint
			self.robots[i].setLocation(initLoc[0], initLoc[1])
			# Update that particular grid cell's occupied status
			self.gridworld.cells[initLoc[0]][initLoc[1]].occupied = True
			self.gridworld.cells[initLoc[0]][initLoc[1]].visited = True
			i += 1

		# Initialize other parameters of the algorithm
		self.height = height
		self.width = width
		self.numRobots = numRobots
		self.R = R
		self.k = k
		self.T = T
		self.base = base

		# keeps track of the number of time steps elapsed
		self.t = 0
		# keeps track of the time taken to exhaust the frontier
		self.completionTime = 0
		self.completedFlag = False
		# froniter
		self.frontier = []
		# new positions of each of the robots
		self.newPos = []
		# population of configurations
		self.cfgc = []
		# keeps track of the number of stalls
		self.stalls = 0

		# We also initialize an instance of AStar, which helps us in computing Manhattan distance
		self.astar = AStar.AStar()


	# Method to print the current gridworld to the output descriptor
	def printGrid(self):

		## Comment this later
		frontier = self.computeFrontier()
		##
		print 'occupied cells:'
		for i in range(self.height):
			for j in range(self.width):
				if self.gridworld.cells[i][j].occupied == True:
					print i, j
		print 'robot locations:'
		for robot in self.robots:
			print robot.curX, robot.curY

		for i in range(self.height):
			for j in range(self.width):
				# If the current cell is an obstacle, print #
				if self.gridworld.cells[i][j].obstacle == True:
					sys.stdout.write(' # ')
				# If the current cell is occupied by a robot, print its id
				elif self.gridworld.cells[i][j].occupied == True:
					robotId = 0
					for robot in self.robots:
						if robot.curX == i and robot.curY == j:
							robotId = robot.id
					temp = ' ' + str(robotId) + ' '
					sys.stdout.write(temp)
				# If the current cell is a frontier, print a |
				elif (i, j) in frontier:
					sys.stdout.write(' | ')
				# Otherwise, print -
				else:
					if self.gridworld.cells[i][j].visited == True:
						sys.stdout.write(' . ')
					else:
						sys.stdout.write(' - ')
			sys.stdout.write('\n')


	# Method to print the status of each cell to the output descriptor
	def printVisitedStatus(self):

		## Comment this later
		# frontier = self.computeFrontier()
		##
		visited = 0
		visitable = self.height * self.width

		for i in range(self.height):
			for j in range(self.width):
				# If the current cell is an obstacle, print #
				if self.gridworld.cells[i][j].visited == True:
					sys.stdout.write(' 1 ')
					visited += 1
				# If the current cell is a frontier, print a |
				else:
					sys.stdout.write(' 0 ')
					if self.gridworld.cells[i][j].obstacle == True:
						visitable -= 1
			sys.stdout.write('\n')

		print 'visited:', visited, ' of ', visitable
		print 'stalls:', self.stalls

		return self.completionTime


	# Method to compute the frontier
	def computeFrontier(self):

		frontier = []

		# Iterate over all cells in the grid
		for i in range(self.height):
			for j in range(self.width):
				# We compute 8-neighbors for only those cells that haven't been visited or are obstacles
				# Only such cells are possible candidates for the frontier
				if self.gridworld.cells[i][j].visited == False and self.gridworld.cells[i][j].obstacle == False:
					point = (i, j)
					neighbors = self.gridworld.get8Neighbors(point)
					# Now we see if there is at least one neighbor of the current cell which has been visited
					# In such a case, the current cell would become a frontier cell
					frontierFlag = False
					for nbhr in neighbors:
						if self.gridworld.cells[nbhr[0]][nbhr[1]].visited == True:
							frontierFlag = True

					if frontierFlag == True:
						frontier.append((i, j))

		return frontier


	# Method to generate a random command vector (configuration change)
	def generateNewCmd(self):

		cmd = []
		for i in range(self.numRobots):
			cmd.append(random.randint(0, 8))
		return cmd


	# Method to generate a population of k configuration changes
	# Note that k has already been set for the experiment during the initialization
	# Hence, it will not be passed as a parameter
	# Also, note that, one configuration change must always be present in which all robots remain where they are
	# So, we include that as the last configuration change in every population
	def generateCfgcPopulation(self):

		cfgc = []

		# First, generate k - 1 random configuration changes
		for i in range(self.k - 1):
			cfgc.append(self.generateNewCmd())

		# Now, append the last configuration change
		# Here, all robots remain in their current locations
		temp = []
		for i in range(self.numRobots):
			temp.append(8)

		cfgc.append(temp)

		return cfgc


	# Method to compute the new locations of each robot, given a command vector
	def getNewPositions(self, cmd):

		newPos = []

		for i in range(self.numRobots):

			nextX, nextY = self.gridworld.getNextPos(self.robots[i].curX, self.robots[i].curY, cmd[i])
			newPos.append((nextX, nextY))

		return newPos


	# Method to check if a given configuration is possible
	# We return an integer that describes the nature of the impossibility of a configuration
	# 0 denotes that all robots move into non-obstacle cells
	# 1 denotes that two robots occupy the same cell
	# 2 denotes that one robot encounters an obstacle
	def isCfgPossible(self, cfg):

		# We first compute the new positions and see if two next positions coincide
		# newPos = self.getNewPositions(cfg)
		if any(self.newPos.count(element) > 1 for element in self.newPos) == True:
			return 1

		# Now we check if some robot encounters an obstacle
		retval = 0
		for i in range(self.numRobots):
			if self.gridworld.checkCommand(self.robots[i].curX, self.robots[i].curY, cfg[i]) == False:
				retval = 2

		# Otherwise, the configuration is possible
		return retval


	# Method to check if a given configuration is within communication radius
	def isWithinR(self, cfg):

		# We first compute the new positions
		# newPos = self.getNewPositions(cfg)

		# Now, for each robot, we compute the Euclidean distance from its new position to the base station
		# We then check if that distance is less than the communication radius R
		i = 0
		for pos in self.newPos:
			dist = math.sqrt(((pos[0] - self.base[0]) * (pos[0] - self.base[0])) + ((pos[1] - self.base[1]) * (pos[1] - self.base[1])))
			if dist > self.R:
				return False
		return True


	# Method to compute the utility of a configuration
	def computeUtility(self, cfg):

		self.newPos = self.getNewPositions(cfg)
		
		##
		# print 'newPos', self.newPos
		##

		## Comment this out later
		# self.frontier = self.computeFrontier()
		##

		utility = 0
		possible = self.isCfgPossible(cfg)
		connectivity = self.isWithinR(cfg)
		
		# If two robots occupy the same cell or if the network constraint is not satisfied, 
		# assign a negative utility to the whole configuration
		if possible == 1 or connectivity == False:
			# print '-6 case'
			utility = -3 * self.numRobots
			return utility
		
		# Otherwise, we have to compute the utility for each robot and sum it up

		i = 0
		for robot in self.robots:
			# First check if the next move encounters an obstacle
			# print 'cfg[i]', cfg[i]
			tempX = self.newPos[i][0]
			tempY = self.newPos[i][1]
			# print 'newPos[i]', self.newPos[i][0], self.newPos[i][1]
			if cfg[i] != 8:
				if (robot.curX == tempX and robot.curY == tempY) or self.gridworld.cells[tempX][tempY].obstacle == True:
					utility += -3
			# if cfg[i] != 8:
			# 	if self.gridworld.cells[self.newPos[i][0]][self.newPos[i][1]].obstacle == True or self.gridworld.inBounds((self.newPos[i][0], self.newPos[1])) == False:
			# 		# if self.gridworld.inBounds((self.newPos[i][0], self.newPos[1])) == False:
			# 		# 	print '###2', self.newPos[i][0], self.newPos[1][1]
			# 		# else:
			# 		# 	print '###1'
			# 		utility += -3
			# Else, compute the Manhattan distance from its new position to its nearest point on the frontier
			else:
				start = (robot.curX, robot.curY)
				dists = []
				
				for pt in self.frontier:
					
					# Use the following statments for A* (with a Manhattan distance heuristic)
					path, cost = self.astar.aStarSearch(self.gridworld, start, pt)
					dists.append(cost[pt])
					
					# Use the followint statements for Manhattan distance
					# cost = abs(start[0] - pt[0]) + abs(start[1] - pt[1])
					# dists.append(cost)

				manhattan = sorted(dists)[0]
				utility += -1 * manhattan

			i += 1

		return utility


	# Method to determine the optimal configuration from a population of configuration changes
	def getBestCfgc(self):

		util = []
		for cfg in self.cfgc:
			util.append(self.computeUtility(cfg))

		print 'cfgc:', self.cfgc
		print 'util:', util
		sortedIndices = [i[0] for i in sorted(enumerate(util), key = lambda x:x[1], reverse = True)]
		return sortedIndices[0]


	# Execute the commands given by the best cfgc
	def executeBestCfgc(self, bestCfgc):

		i = 0
		for cmd in self.cfgc[bestCfgc]:
			tempX = self.robots[i].curX
			tempY = self.robots[i].curY
			if self.gridworld.checkCommand(tempX, tempY, cmd) == True:
				nextX, nextY = self.gridworld.getNextPos(tempX, tempY, cmd)
				self.gridworld.cells[tempX][tempY].occupied = False
				self.robots[i].curX = nextX
				self.robots[i].curY = nextY
				self.gridworld.cells[nextX][nextY].occupied = True
				self.gridworld.cells[nextX][nextY].visited = True
			i += 1



	# Run the algorithm for 1 iteration
	def runOneIter(self):

		# If t time steps have already expired, return
		self.t += 1
		if self.t == self.T:
			return

		# Else, run the algorithm for one time step
		self.frontier = self.computeFrontier()
		if self.frontier == []:
			if self.completedFlag == False:
				self.completedFlag = True
				self.completionTime = self.t
				print 'Completed in time', self.completionTime
			return
		self.cfgc = self.generateCfgcPopulation()
		bestCfgc = self.getBestCfgc()
		# print 'best:', bestCfgc
		if bestCfgc == self.k - 1:
			self.stalls += 1

		print self.cfgc[bestCfgc]
		self.executeBestCfgc(bestCfgc)

		self.printGrid()
		print ''
		print ''