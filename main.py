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





# Importing standard modules
import math
import random
import sys

# Importing own modules
import Grid
import Robot


# Generates a random configuration change (set of commands) for each robots
def generateRandomCfg(numRobots):
	cfg = []
	for i in range(numRobots):
		cfg.append(random.randint(0, 8))
	return cfg


# Computes the next coordinates given the current coordinates and the new command
def getNextXY(curX, curY, command):
	if command == 0:
		if curY == width - 1:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX
			nextY = curY + 1
			return nextX, nextY

	if command == 1:
		if curY == width - 1 or curX == 0:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX - 1
			nextY = curY + 1
			return nextX, nextY

	if command == 2:
		if curX == 0:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX - 1
			nextY = curY
			return nextX, nextY

	if command == 3:
		if curY == 0 or curX == 0:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX - 1
			nextY = curY - 1
			return nextX, nextY

	if command == 4:
		if curY == 0:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX
			nextY = curY - 1
			return nextX, nextY

	if command == 5:
		if curY == 0 or curX == height - 1:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX + 1
			nextY = curY - 1
			return nextX, nextY

	if command == 6:
		if curX == height -1:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX + 1
			nextY = curY
			return nextX, nextY

	if command == 7:
		if curX == height - 1 or curY == width - 1:
			# print 'Out of grid'
			return -1, -1
		else:
			nextX = curX + 1
			nextY = curY + 1
			return nextX, nextY

	if command == 8:
		nextX = curX
		nextY = curY

		return nextX, nextY


# Computes the new configuration, given a configuration change
def computeNewCfg(newcmd):

	newcfg = []
	infeasibleFlag = False
	for i in range(len(newcmd)):
		curX = robot[i].curX
		curY = robot[i].curY
		nextX, nextY = getNextXY(curX, curY, newcmd[i])
		# print nextX, nextY
		if nextX == -1:
			infeasibleFlag = True
		newcfg.append([nextX, nextY])

	if infeasibleFlag == True:
		return -1
	else:
		return newcfg


# Get the 8-neighbors of the given cell (Used in computing the frontier cells)
def get8Neighbors(x, y):
	
	nbhrs = []
	
	# If (x, y) is a corner, it will only have 3 neighbors
	if x == 0 and y == 0:
		nbhrs.append([x, y+1])
		nbhrs.append([x+1, y+1])
		nbhrs.append([x+1, y])
		return nbhrs
	if x == 0 and y == width - 1:
		nbhrs.append([x+1, y])
		nbhrs.append([x+1, y-1])
		nbhrs.append([x, y-1])
		return nbhrs
	if x == height - 1 and y == width - 1:
		nbhrs.append([x, y-1])
		nbhrs.append([x-1, y-1])
		nbhrs.append([x-1, y])
		return nbhrs
	if x == height - 1 and y == 0:
		nbhrs.append([x-1, y])
		nbhrs.append([x-1, y+1])
		nbhrs.append([x, y+1])
		return nbhrs

	# If (x, y) is a point on an edge, it will only have 5 neighbors
	if x == 0:
		nbhrs.append([x, y+1])
		nbhrs.append([x+1, y+1])
		nbhrs.append([x+1, y])
		nbhrs.append([x+1, y-1])
		nbhrs.append([x, y-1])
		return nbhrs
	if x == height - 1:
		nbhrs.append([x, y+1])
		nbhrs.append([x-1, y+1])
		nbhrs.append([x-1, y])
		nbhrs.append([x-1, y-1])
		nbhrs.append([x, y-1])
		return nbhrs
	if y == 0:
		nbhrs.append([x-1, y])
		nbhrs.append([x-1, y+1])
		nbhrs.append([x, y+1])
		nbhrs.append([x+1, y+1])
		nbhrs.append([x+1, y])
		return nbhrs
	if y == width - 1:
		nbhrs.append([x+1, y])
		nbhrs.append([x+1, y-1])
		nbhrs.append([x, y-1])
		nbhrs.append([x-1, y-1])
		nbhrs.append([x-1, y])
		return nbhrs

	# Otherwise a point will have 8 neighbors
	nbhrs.append([x-1, y])
	nbhrs.append([x-1, y+1])
	nbhrs.append([x, y+1])
	nbhrs.append([x+1, y+1])
	nbhrs.append([x+1, y])
	nbhrs.append([x+1, y-1])
	nbhrs.append([x, y-1])
	nbhrs.append([x-1, y-1])
	return nbhrs


# Create a list of frontier cells
def getFrontierCells():

	frontier = []

	# Iterate over all cells in the grid
	for i in range(height):
		for j in range(width):
			# Compute the neighbors for those cells which haven't been visited or are not obstacles
			# Only such cells are possible candidates for the frontier
			if grid.cells[i][j].visited == False and grid.cells[i][j].status != -1:
				nbhrs = get8Neighbors(i, j)
				# Now we see if there is at least one neighbor of the current cell which has been visited
				# In such a case, the current cell would become a frontier cell
				frontierFlag = False
				for nbhr in nbhrs:
					if grid.cells[nbhr[0]][nbhr[1]].visited == True:
						frontierFlag = True

				if frontierFlag == True:
					frontier.append([i, j])

	return frontier




# Defining variables to store the height and width of the grid
height = 10
width = 10
# Defining a variable to hold a very large value
inf = 1000000000
# obstacles = [[0, 0], [1, 1],[2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 8]]
obstacles = [[0, 0], [1, 0],[2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 8]]
grid = Grid.Grid(height, width, obstacles)
initLocs = [[0, 9], [8, 9]]
	
numRobots = 2
robot = [Robot.Robot(j+1, -1, -1, -1) for j in range(numRobots)]

# robotID = 1
# for initLoc in initLocs:
# 	# print initLoc[0], initLoc[1], robotID
# 	ret = grid.initRobotLocations(initLoc[0], initLoc[1], robotID)
# 	if ret == 0:
# 		print 'Success', robotID
# 		robot[robotID].reinit(initLoc[0], initLoc[1], 0)
# 		print robot[robotID].curX, robot[robotID].curY, robot[robotID].orientation
# 	else:
# 		print 'Failed', robotID
# 	robotID += 1

idx = 0
for bot in robot:
	ret = grid.initRobotLocations(initLocs[idx][0], initLocs[idx][1], bot.robotID)
	if ret == 0:
		# print 'Success', bot.robotID
		bot.reinit(initLocs[idx][0], initLocs[idx][1], 0)
		# print bot.curX, bot.curY, bot.status
	else:
		print 'Failed', bot.robotID
	# robotID += 1
	idx += 1

# if grid.moveRobot(robot[1], height, width, 8) == 0:
# 	print 'Command allowed'
# else:
# 	print 'Command denied'

for i in range(height):
	for j in range(width):
		# print grid.cells[i][j].status
		sys.stdout.write(str(grid.cells[i][j].status))
		sys.stdout.write(" ")
	sys.stdout.write("\n")


# Let R be the communication radius of each robot
R = 15
# Let baseX and baseY be the coordinates of the base station
baseX = 0
baseY = 0


# Run the following instructions for T time steps
T = 200
for t in range(T):

	# Get a list of the current frontier cells
	frontier = getFrontierCells()
	print 'frontier:', frontier

	if frontier == []:
		print 'Frontier empty at t =', t
		break

	# Generate k random configuration changes (cfgc)
	# For each cfgc, compute the new config (cfg), the utility of the cfg
	# Also, store the cfgc with the max utility
	k = 10
	cfgc = []
	utility = []
	for i in range(k):
		if i == k-1:
			newcmd = []
			for j in range(numRobots):
				newcmd.append(8)
		else:
			newcmd = generateRandomCfg(numRobots)
		cfgc.append(newcmd)
		print newcmd
		newcfg = computeNewCfg(newcmd)
		# print newcfg
		# Now we compute the utility of this configuration
		if newcfg == -1:
			# We use a temporary variable to store the utility
			util = -3 * numRobots
			# We then append it to the global list of utilities
			utility.append(util)
			# print 'Impossible configuration'
		else:
			# print newcfg
			# We now determine if there is a possible loss of communication in this configuration
			lossFlag = False
			for cfg in newcfg:
				dist = math.sqrt(((cfg[0]-baseX)*(cfg[0]-baseX)) + ((cfg[1]- baseY)*(cfg[1]-baseY)))
				if dist > R:
					lossFlag = True
			if lossFlag == True:
				util = -3 * numRobots
				utility.append(util)
				# print 'Loss of communication'
			else:
				# In this case the utility is equal to the Manhattan distance of the nearest frontier point
				# print 'Manhattan distance'
			
				# Get the closest point on the frontier (for each robot)
				for i in range(numRobots):
					curX = robot[i].curX
					curY = robot[i].curY
					minDist = inf
					minIndex = -1
					idx = 0
					for pt in frontier:
						dist = math.sqrt(((pt[0]-curX)*(pt[0]-curX)) + ((pt[1]- curY)*(pt[1]-curY)))
						if dist <= minDist:
							minDist = dist
							minIndex = idx
						idx += 1
					robot[i].nearestFrontier = minIndex

				# Compute the Manhattan distance of each robot's new position to its closest frontier point
				util = 0
				idx = 0
				for cfg in newcfg:
					manhattan = int( math.fabs(frontier[robot[idx].nearestFrontier][0] - cfg[0]) + math.fabs(frontier[robot[idx].nearestFrontier][1] - cfg[1]) )
					# print 'man', manhattan
					util += (-1 * manhattan)
					idx += 1
				utility.append(util)

	print 'cfgc:'
	print cfgc
	print 'Utilities: ', utility
	sortedIndices = [i[0] for i in sorted(enumerate(utility), key = lambda x:x[1], reverse = True)]
	print 'sortedIndices:', sortedIndices
	selectedCmd = sortedIndices[0]
	print 'selectedCmd:', selectedCmd, cfgc[selectedCmd]

	# Pass on the selected commands to the robots
	for idx in range(numRobots):
		# Execute the command
		grid.moveRobot(robot[idx], height, width, cfgc[selectedCmd][idx])
		# Print the grid to the output
		for i in range(height):
			for j in range(width):
				# print grid.cells[i][j].status
				sys.stdout.write(str(grid.cells[i][j].status))
				sys.stdout.write(" ")
			sys.stdout.write("\n")


print '---------------------'
print 'Final coverage status'
print '---------------------'
# Print the status of the cells (1 if the cell has been visited, 0 otherwise)
for i in range(height):
	for j in range(width):
		# print grid.cells[i][j].status
		if grid.cells[i][j].visited == True:
			sys.stdout.write("1")
		else:
			sys.stdout.write("0")
		sys.stdout.write(" ")
	sys.stdout.write("\n")