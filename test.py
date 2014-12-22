import AStar
import CommExplore
import ConfigFileReader

# grid = GridWorld.GridWorld(10, 10, [[4, 4], [4, 5]])
# # print grid.get8Neighbors(8, 8)
# aStar = AStar.AStar()
# start = (4, 6)
# goal = (4, 0)
# path, cost = aStar.aStarSearch(grid, start, goal)
# print 'path: ', path
# print 'cost: ', cost[goal]
# print grid.checkCommand(9, 9, 0)

obstacles = [[0, 0], [1, 0],[2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 8]]
initLocs = [[0, 9], [1, 9]]
# initLocs = [[2, 3], [3, 4]]
# print algo.isObstacleEncountered()
# print algo.isWithinR([4, 3])
# print algo.computeUtility([4, 4])
# print algo.gridworld.inBounds((0, 9))
# print algo.gridworld.inBounds((1, 9))
# print algo.gridworld.inBounds((0, 8))

# for j in range(1000):
# 	algo.runOneIter()
# algo.printVisitedStatus()

cfgReader = ConfigFileReader.ConfigFileReader("barmaze.config")
ret, height, width, numRobots, R, baseX, baseY, initLocs, obstacles = cfgReader.readCfg()
if ret == -1:
	print 'readCfg() Unsuccessful!'
	sys.exit(-1)

print 'height', height
print 'width', width
print 'numRobots', numRobots
print 'R', R
print 'baseX', baseX
print 'baseY', baseY
print 'initLocs', initLocs
print 'obstacles', obstacles

k = 10
T = 100

algo = CommExplore.CommExplore(height, width, obstacles, numRobots, initLocs, R, k)
algo.printGrid()
print ''
print ''
cfgc = algo.generateCfgcPopulation()

for j in range(1000):
	algo.runOneIter()
algo.printVisitedStatus()







# # The MIT License (MIT)

# # Copyright (c) 2014 INSPIRE Lab, BITS Pilani

# # Permission is hereby granted, free of charge, to any person obtaining a copy
# # of this software and associated documentation files (the "Software"), to deal
# # in the Software without restriction, including without limitation the rights
# # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# # copies of the Software, and to permit persons to whom the Software is
# # furnished to do so, subject to the following conditions:

# # The above copyright notice and this permission notice shall be included in all
# # copies or substantial portions of the Software.

# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# # SOFTWARE.


# """
# Provides a demo of the Communicative Exploration algorithm for a fixed base station.
# """

# from math import floor
# from time import sleep
# import time
# import Tkinter

# import AStar
# import CommExplore
# import ConfigFileReader
# import GridUI


# cfgReader = ConfigFileReader.ConfigFileReader("freeworld.config")
# ret, height, width, numRobots, R, baseX, baseY, initLocs, obstacles = cfgReader.readCfg()
# if ret == -1:
# 	print 'readCfg() Unsuccessful!'
# 	sys.exit(-1)

# # print 'height', height
# # print 'width', width
# # print 'numRobots', numRobots
# # print 'R', R
# # print 'baseX', baseX
# # print 'baseY', baseY
# # print 'initLocs', initLocs
# # print 'obstacles', obstacles

# k = 10
# T = 100

# algo = CommExplore.CommExplore(height, width, obstacles, numRobots, initLocs, R, k)
# algo.printGrid()
# print ''
# print ''
# cfgc = algo.generateCfgcPopulation()

# for j in range(1000):
# 	algo.runOneIter()
# algo.printVisitedStatus()


# ##
# # algo.runOneIter()
# # algo.runOneIter()
# # algo.runOneIter()
# # algo.runOneIter()

# # print 'frontier', algo.frontier
# ##


# # if height <= 10:
# # 	xoffset = 300
# # else:
# # 	xoffset = 100
# # if width <= 10:
# # 	yoffset = 300
# # else:
# # 	yoffset = 100

# # maxScreenHeight = 700
# # cellSize = int(floor(maxScreenHeight / (height + 2)))

# # root = Tkinter.Tk()
# # # ex = Example(root)
# # # root.geometry('400x100+500+500')
# # # root.mainloop()

# # gui = GridUI.GridUI(root, height, width, cellSize, algo.gridworld, algo.robots, algo.frontier)
# # guiHeight = str((height + 2) * cellSize)
# # guiWidth = str((width + 2) * cellSize)
# # xOffset = str(xoffset)
# # yOffset = str(yoffset)
# # geometryParam = guiWidth + 'x' + guiHeight + '+' + xOffset + '+' + yOffset
# # root.geometry(geometryParam)

# # def hello():

# # 	print 'Hello'
# # 	root.after(500, hello)

# # def run():

# # 	algo.runOneIter()
# # 	gui.redraw(height, width, cellSize, algo.gridworld, algo.robots, algo.frontier)
# # 	root.after(500, run)

# # root.after(500, run)
# # root.mainloop()