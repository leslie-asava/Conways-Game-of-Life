# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from numpy import array, zeros
from random import choice

class ConwaysCanvas(QWidget):
    def __init__(self, cellsize=20, gridx=10, gridy=10, parent=None):
        super(ConwaysCanvas, self).__init__()
        self.gridheight = gridx
        self.gridwidth  = gridy
        self.cellsize   = cellsize
        self.colorLine  = [175,175,175] # Gray
        self.colorOn    = [100,100,255] # Blue
        self.colorOff   = [255,255,255] # White

        self.valueOn    = 0
        self.valueOff   = 1
        self.grid       = []
        self.cleargrid()

        # Initialize values, chose the lowest value that wouldn't be reached normally as initial values
        self.__oldmouseMovePos_x = -1
        self.__oldmouseMovePos_y = -1

    # Function called when Reset is pressed
    def regen(self):
        self.grid           = self._generateRandomgrid()
        self.update()

    # Clear grid by setting each value to off
    def cleargrid(self):
        self.grid           = [[self.valueOff]*self.gridwidth]*self.gridheight
        self.applyRules()
        self.update()

    # Update grid
    def updateGridEvent(self):
        if len(self.grid) != 0:
            self.applyRules()
            self.update()

    # Draw and colour squares depending on values
    def paintEvent(self, e):
        # Check if grid exists
        if len(self.grid) != 0:

            # Define painter object and pen
            qp = QPainter(self)
            qp.setPen(QColor(self.colorLine[0], self.colorLine[1], self.colorLine[2]))

            # Iterate through grid rows
            for xk in range(len(self.grid)):

                # Iterate through grid columns
                for yk in range(len(self.grid[0])):

                    # If cell value is 1, set pen color to colorOn (blue)
                    if self.grid[xk][yk] == self.valueOn:
                        qp.setBrush(QColor(self.colorOn[0], self.colorOn[1], self.colorOn[2]))

                    # If cell value is 0, set pen color to colorOff (white)
                    else :
                        qp.setBrush(QColor(self.colorOff[0], self.colorOff[1], self.colorOff[2]))

                    # Draw Rectangle on provided coordinates
                    qp.drawRect(self.cellsize*xk, self.cellsize*yk, self.cellsize*(xk+1), self.cellsize*(yk+1))

    # Called when mouse is pressed
    def mousePressEvent(self, event):
        # If left button is pressed
        if event.buttons() == Qt.LeftButton:
            # Update old mouse position
            self.__oldmouseMovePos_x = max(min(event.x()//self.cellsize, self.gridheight-1), 0)
            self.__oldmouseMovePos_y = max(min(event.y()//self.cellsize, self.gridwidth-1), 0)

            # Set value of cell to 1
            self.grid[max(min(event.x()//self.cellsize, self.gridheight-1), 0)][max(min(event.y()//self.cellsize, self.gridwidth-1), 0)] = 1 ^ self.grid[max(min(event.x()//self.cellsize, self.gridheight-1), 0)][max(min(event.y()//self.cellsize, self.gridwidth-1), 0)]
            self.update()

    # Called whenever mouse is moved
    def mouseMoveEvent(self, event):

        # If left mouse button is being pressed
        if event.buttons() == Qt.LeftButton:
            if self.__oldmouseMovePos_x != max(min(event.x()//self.cellsize, self.gridheight-1), 0) or self.__oldmouseMovePos_y != max(min(event.y()//self.cellsize, self.gridwidth-1), 0) :
                self.grid[max(min(event.x()//self.cellsize, self.gridheight-1), 0)][max(min(event.y()//self.cellsize, self.gridwidth-1), 0)] = 1 ^ self.grid[max(min(event.x()//self.cellsize, self.gridheight-1), 0)][max(min(event.y()//self.cellsize, self.gridwidth-1), 0)]
                self.update()
            self.__oldmouseMovePos_x = max(min(event.x()//self.cellsize, self.gridheight-1), 0)
            self.__oldmouseMovePos_y = max(min(event.y()//self.cellsize, self.gridwidth-1), 0)


    def _getNeighbours(self, x, y):
        """
            Function that, for a given cell, identified with its coordinates x and y, return the coordinates and values of its neighbours
            Parameters :
                - x : the coordinate of the cell on the x-axis
                - y : the coordinate of the cell on the y-axis
            Return :
                - neighbours : a dictionary containing the coordinates and the values of the neighbours of the cell
            Note : to access to the value of a given cell neighbour, use 'neighbours[x][y]', considering that 'neighbours' is returned by the function and 'x' and 'y' are the coordinates of the cell of which we want to have access
        """
        neighbours = {}
        if (x == 0):
            if (y == 0): # Upper left corner
                neighbours = {(x,y+1):self.grid[x][y+1],(x+1,y):self.grid[x+1][y],(x+1,y+1):self.grid[x+1][y+1]}
            elif (y == len(self.grid[0])-1): # Upper right corner
                neighbours = {(x,y-1):self.grid[x][y-1],(x+1,y):self.grid[x+1][y],(x+1,y-1):self.grid[x+1][y-1]}
            else: # Upper border
                neighbours = {(x,y-1):self.grid[x][y-1],(x,y+1):self.grid[x][y+1],(x+1,y-1):self.grid[x+1][y-1],(x+1,y):self.grid[x+1][y],(x+1,y+1):self.grid[x+1][y-1]}
        elif (x == len(self.grid)-1):
            if (y == 0): # Left down corner
                neighbours = {(x-1,y):self.grid[x-1][y],(x,y+1):self.grid[x][y+1],(x-1,y+1):self.grid[x-1][y+1]}
            elif (y == len(self.grid[0])-1): # Right down corner
                neighbours = {(x,y-1):self.grid[x][y-1],(x-1,y):self.grid[x-1][y],(x-1,y-1):self.grid[x-1][y-1]}
            else: # Down border
                neighbours = {(x,y+1):self.grid[x][y+1],(x,y-1):self.grid[x][y-1],(x-1,y-1):self.grid[x-1][y-1],(x-1,y):self.grid[x-1][y],(x-1,y+1):self.grid[x-1][y+1]}
        else:
            if(y == 0): # Left border
                neighbours = {(x-1,y):self.grid[x-1][y],(x+1,y):self.grid[x+1][y],(x-1,y+1):self.grid[x-1][y+1],(x,y+1):self.grid[x][y+1],(x+1,y+1):self.grid[x+1][y+1]}
            elif(y == len(self.grid[0])-1): # Right border
                neighbours = {(x-1,y):self.grid[x-1][y],(x+1,y):self.grid[x+1][y],(x-1,y-1):self.grid[x-1][y-1],(x,y-1):self.grid[x][y-1],(x+1,y-1):self.grid[x+1][y-1]}
            else: # Middle
                neighbours = {(x-1,y-1):self.grid[x-1][y-1],(x-1,y):self.grid[x-1][y],(x-1,y+1):self.grid[x-1][y+1],(x,y-1):self.grid[x][y-1],(x,y+1):self.grid[x][y+1],(x+1,y-1):self.grid[x+1][y-1],(x+1,y):self.grid[x+1][y],(x+1,y+1):self.grid[x+1][y+1]}
        neighbours.update({(x,y):2}) # Add the value of the cell for which we look the neighbours, make sure not to use the value 2 for either self.valueOn and self.valueOff as it's used here
        return neighbours

    def _countNeighbours(self, x, y):
        """
            Function that, for a given cell, identified with its coordinates x and y, return the number of cells in its neighbourhood that are on and the number that are off
            Parameters :
                - x : the coordinate of the cell on the x-axis
                - y : the coordinate of the cell on the y-axis
            Return :
                - numberOn, numberOff : the number of cells neighbouring a particular cell that are on and off
        """
        
        # Initialize both cells to 0
        numberOn, numberOff = 0, 0

        # Get a dictionary containing the neighbors of a particular cell
        neighbours = self._getNeighbours(x, y)

        # Iterate through neighbors
        for key in neighbours.keys(): # we go through all the keys in the dict, so all the coordinates of the neighbours
            
            # If neighbour is alive, increment numberOn
            if(neighbours[key] == self.valueOn):
                numberOn += 1

            # If neighbour is dead, increment numberOff
            elif(neighbours[key] == self.valueOff):
                numberOff += 1
        return numberOn, numberOff

    def applyRules(self):
        """
            Function that, for a given grid, apply the rules of the game (see below for the detail)

            Return :
                - nextgrid : the self.grid updated with the rules of the game (see below for the detail)
            Note : the rules are the following
                1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
                2. Any live cell with two or three live neighbours lives on to the next generation.
                3. Any live cell with more than three live neighbours dies, as if by overpopulation.
                4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        
        # Initialize array with 0's
        nextgrid = [[self.valueOff for y in range(len(self.grid[0]))] for x in range(len(self.grid))]

        # Iterate through rows and columns
        for x in range(len(self.grid)): # we go through all the point on the x-axis
            for y in range(len(self.grid[0])): # we go through all the point on the y-axis

                # Count the number of neighbours both dead and alive
                numberOn, numberOff = self._countNeighbours(x, y)

                # Apply rules defined above depending on conditions met
                if(self.grid[x][y] == self.valueOn): # For the rules 1, 2 and 3
                    if(numberOn < 2): # For the rule 1
                        nextgrid[x][y] = self.valueOff
                    elif(numberOn == 2 or numberOn == 3): # For the rule 2
                        nextgrid[x][y] = self.valueOn
                    elif(numberOn > 3): # For the rule 3
                        nextgrid[x][y] = self.valueOff
                elif(self.grid[x][y] == self.valueOff and numberOn == 3): # For the rule 4
                    nextgrid[x][y] = self.valueOn
        self.grid = nextgrid

    # Generate a random array of 1's and 0's
    def _generateRandomgrid(self):
        # Fill grid initially with 0's
        self.grid = zeros((self.gridheight, self.gridwidth), dtype=int)

        # Iterate through rows
        for x in range(len(self.grid)):

            # Iterate through columns
            for y in range(len(self.grid[0])):
                self.grid[x][y] = choice([self.valueOn, self.valueOff]) # for each cell, we choose randomly a value between self.valueOn and self.valueOff
        return self.grid


    # *----------------------------GET--SET------------------------------------*
    # Get the value that represents a live cell on the grid (default 1)
    def get_valueOn (self):
        return self.valueOn

    # Set the value that will represent a live cell on the grid (default 1)
    def set_valueOn (self, valueOn):
        self.valueOn = valueOn

    # Get the value that represents a dead cell on the grid (default 0)
    def get_valueOff (self):
        return self.valueOff

    # Set the value that will represent a dead cell on the grid (default 0)
    def set_valueOff (self, valueOff):
        self.valueOff = valueOff

    # Get the color used to represent live cells (default blue)
    def get_colorOn (self):
        return self.colorOn

    # Set the color that will be used to represent live cells (default blue)
    def set_colorOn (self, colorOn):
        self.colorOn = colorOn

    # Get the color used to represent dead cells on the grid (default white)
    def get_colorOff (self):
        return self.colorOff

    # Set the color that will be used to represent dead cells (default white)
    def set_colorOff (self, colorOff):
        self.colorOff = colorOff

    # Get array of values representing the grid. Values can either be 0 or 1
    def get_grid (self):
        return self.grid

    # Set values of array representing the grid
    def set_grid (self, grid):
        self.grid = grid

    # Get number of rows in grid
    def get_gridheight (self):
        return self.gridheight

    # Set number of rows in grid
    def set_gridheight (self, gridheight):
        self.gridheight = max(0,gridheight)

    # Get the number of columns in grid
    def get_gridwidth (self):
        return self.gridwidth

    # Set number of columns in grid
    def set_gridwidth (self, gridwidth):
        self.gridwidth = max(0,gridwidth)

    # Get the size of a single cell
    def get_cellsize (self):
        return self.cellsize

    # Set the size to be used as cell width and height
    def set_cellsize (self, cellsize):
        self.cellsize = max(0,cellsize)
