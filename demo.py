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
Provides a demo of the Communicative Exploration algorithm for a fixed base station.
"""


import AStar
import CommExplore
import ConfigFileReader
import GridUI


def main():

	cfgReader = ConfigFileReader.ConfigFileReader("freeworld.config")
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
	T = 1000

	algo = CommExplore.CommExplore(height, width, obstacles, numRobots, initLocs, R, k)
	algo.printGrid()
	print ''
	print ''
	cfgc = algo.generateCfgcPopulation()

	for j in range(T):
		algo.runOneIter()

	timeTaken = algo.printVisitedStatus()
	if timeTaken == 0:
		return T
	return timeTaken


if __name__ == '__main__':

	numTrials = 10
	average = 0
	for i in range(numTrials):
		average += main()
	average /= numTrials
	print average