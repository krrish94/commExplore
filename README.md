commExplore
===========

An implementation of the paper "Multi-Robot Exploration Under the Constraints of Wireless Networking" in Python


In order to run the code, dowload all the files in the repository and execute

    $ python main.py

The following variables would be of particular interest to those who wish to test the implementation in various scenarios.

    height - corresponds to the height of the grid world
    width - corresponds to the width of the grid world
    numRobots - corresponds to the number of robots
    obstacles - corresponds to the list of cells that belong to the class of obstacles
    initLocs - corresponds to the list of initial positions of each of the robots
    R - corresponds to the communication radius (range) of each of the robots; R is same for all the robots
    baseX - corresponds to the X coordinate of the base station
    baseY - corresponds to the Y coordinate of the base station
    T - corresponds to the number of time steps for which robots should explore
    k - corresponds to the size of the population of configuration changes that need to be considered