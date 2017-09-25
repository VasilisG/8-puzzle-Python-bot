import math

class Node:

    "This class will hold every state of the puzzle problem."

    def __init__(self, matrix, coords, parent, children):
        
        self.matrix = [x[:] for x in matrix]
        self.coords = coords

        self.gScore = 0
        self.hScore = 0
        self.fScore = 0

        self.parent = parent
        self.children = children


    def getFScore(self):
        return self.fScore


    def getGScore(self):
        return self.gScore


    def getHScore(self):
        return self.hScore

    
    def getMatrix(self):
        return self.matrix


    def setMatrix(self, matrix):
        self.matrix = matrix


    def getNodeCoords(self):
        return self.coords


    def setNodeCoords(self, coords):
        self.coords = coords


    def getParent(self):
        return self.parent


    def getChildren(self):
        return self.children


    def isEqualTo(self, node):
        return self.getMatrix() == node.getMatrix()


    def isNodeInChildrenList(self, node):

        for child in self.children:
            if node.isEqualTo(child):
                return True

        return False


    def getCoords(self, number):

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == number:
                    return tuple([i,j])
        return None

    
    # Function that prints the elements of a 2D matrix.
    def showMatrix(self):

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if j == 0:
                    print("| %d |" % (self.matrix[i][j]), end="")
                else:
                    print(" %d |" % (self.matrix[i][j]), end="")
            print()


    # Method that calculates the G score of a node.
    def calculateGScore(self):
        if self.getParent() is None:
            self.gScore = 0
        else:
            self.gScore = self.getParent().getGScore() + 1


    # Method that calculates the Manhattan distance of every tile in the puzzle.
    def calculateHScore(self, endingNode):

        totalDistance = 0

        for i in range(1,9):

            currentPos = self.getCoords(i)
            finalPos = endingNode.getCoords(i)
            totalDistance = totalDistance + int(math.fabs(currentPos[0] - finalPos[0]) + math.fabs(currentPos[1] - finalPos[1]))

        self.hScore = totalDistance

    
    # Method that calculates the total F score of a node.
    def calculateFScore(self):
        self.fScore = self.gScore + self.hScore


    # Method that finds the empty tile in the puzzle in order to calculate the available moves.
    def getEmptyTile(self):

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    return (i,j)
        return None


    # Method that checks whether a (x,y) coordinate is inside the puzzle matrix, so that a move can be made.
    def isWithinBounds(self, x, y, lowerX, lowerY, upperX, upperY):

        return (x >= lowerX and x <= upperX) and (y >= lowerY and y <= upperY)


    # Method that swaps the values between two elements of the puzzle matrix.
    def swapValues(self, matrix, x1, y1, x2, y2):

        newMatrix = [x[:] for x in matrix]
        temp = newMatrix[x1][y1]
        newMatrix[x1][y1] = newMatrix[x2][y2]
        newMatrix[x2][y2] = temp

        return newMatrix

    
    # Method that calculates the number of misplaced tiles in the puzzle.
    def misplacedTiles(self):

        misplacedTiles = 0
        rows = 3

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if not self.matrix[i][j] == (((i * rows) + j + 1) % (rows^2)):
                    misplacedTiles = misplacedTiles + 1

        return misplacedTiles

    
    # Method that finds all children coordinates for future states of the puzzle.
    def getChildrenCoords(self, coordX, coordY):

        childrenCoords = []

        if self.isWithinBounds(coordX-1, coordY, 0, 0, 2, 2): childrenCoords.append([coordX-1, coordY])
        if self.isWithinBounds(coordX+1, coordY, 0, 0, 2, 2): childrenCoords.append([coordX+1, coordY])
        if self.isWithinBounds(coordX, coordY-1, 0, 0, 2, 2): childrenCoords.append([coordX, coordY-1])
        if self.isWithinBounds(coordX, coordY+1, 0, 0, 2, 2): childrenCoords.append([coordX, coordY+1])

        return childrenCoords

    # Method that generates all possible new states for the puzzle.
    def generateChildren(self):

        children = []
        matrix = self.getMatrix()
        coords = self.getEmptyTile()
        childrenCoords = self.getChildrenCoords(coords[0], coords[1])

        for childCoords in childrenCoords:
            node = Node(matrix, childCoords, self, None)
            node.setMatrix(node.swapValues(matrix, coords[0], coords[1], childCoords[0], childCoords[1]))
            node.setNodeCoords(childCoords)
            children.append(node)
            
        return children


    # Method that sets a node as a parent for future states.
    def setNewNode(self, node):

        self.matrix = node.matrix
        self.coords = node.coords

        self.gScore = node.gScore
        self.hScore = node.hScore
        self.fScore = node.fScore

        self.parent = node.parent
        self.children = node.children
