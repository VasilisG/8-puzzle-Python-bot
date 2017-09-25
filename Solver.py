import math

try:
    from Node import Node

except ImportError as error:
    print("Could not import 'Node' module.")


def getShortestNode(nodeList):

    shortestNode = nodeList[0]

    for i in range(1, len(nodeList)):

        if nodeList[i].getFScore() < shortestNode.getFScore():
            shortestNode = nodeList[i]

    return shortestNode


def isNodeInList(node, nodeList):

    for n in nodeList:
        if node.isEqualTo(n):
            return True

    return False

def reconstructPath(cameFrom, currentNode):

    totalPath = []
    totalPath.append(currentNode)

    while True:
        parent = currentNode.getParent()
        if parent is None:
            break
        else:
            currentNode = parent
            totalPath.append(currentNode)

    return totalPath


def shortestPath(startingNode, endingNode):

    openList = []
    closedList = []
    cameFrom = []

    startingNode.calculateHScore(endingNode)
    startingNode.calculateFScore()
    openList.append(startingNode)

    while not len(openList) == 0:
        
        currentNode = getShortestNode(openList)

        if currentNode.isEqualTo(endingNode):
            return reconstructPath(closedList, currentNode)

        openList.remove(currentNode)
        closedList.append(currentNode)
        neighbors = currentNode.generateChildren()

        for neighbor in neighbors:

            if not isNodeInList(neighbor, openList):
                openList.append(neighbor)

            neighbor.calculateGScore()
            neighbor.calculateHScore(endingNode)
            neighbor.calculateFScore()

            cameFrom.append(currentNode)
           
    return None
