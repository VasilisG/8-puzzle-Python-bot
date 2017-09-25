try:
    from PIL import Image, ImageGrab, ImageChops
except ImportError:
    print("Could not import 'PIL' module.")

try:
    from Node import Node
except ImportError:
    print("Could not import 'Node' module.")

try:
    import Solver
except ImportError:
    print("Could not import 'Solver' module.")

try:
    import pyautogui
except ImportError:
    print("Could not import 'pyautogui' module.")

import time


# Global color variables.
BLACK = (0,0,0)
WHITE = (255,255,255)

# Variables needed to get a proper screenshot of the game area.
paddingX = 583
paddingY = 335
screenWidth = 298
screenHeight = 298

tileSize = 98
tileDistance = 100

# The bounding box of the game area.
bbox = (paddingX, paddingY, paddingX + screenWidth, paddingY + screenHeight)

# Image tile filenames.
filenames = ("tileOne.png", "tileTwo.png", "tileThree.png", "tileFour.png", "tileFive.png", "tileSix.png", "tileSeven.png", "tileEight.png")


# Function that takes a screenshot the part of the screen defined by the coordinates in bbox.
def screenGrab(boundingBox):

    image = ImageGrab.grab(boundingBox)
    gray = image.convert('L')
    newImage = gray.point(lambda x: 0 if x<150 else 255, '1')
    return newImage


# Function that imports all cropped puzzle tiles.
def loadTiles(filenames):

    imageTiles = []

    for filename in filenames:
        imageTiles.append(Image.open(filename,"r"))

    return imageTiles


# Function that initializes a 2D matrix.
def initMatrix(dimX, dimY):
    matrix = [[0 for y in range(dimY)] for x in range(dimX)]
    return matrix


# Function that prints the elements of a 2D matrix.
def showMatrix(matrix):

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j == 0:
                print("| %d |" % (matrix[i][j]), end="")
            else:
                print(" %d |" % (matrix[i][j]), end="")
        print()



# Function that checks if two images are identical.
def equalImages(image1, image2):

    #print(image1.size)
    #print(image2.size)
    #print("-----------")

    if image1.size == image2.size:
        return ImageChops.difference(image1.convert("L"),image2.convert("L")).getbbox() is None
    else:
        return None

def equalImages2(image1, image2):

    if image1.size == image2.size:
        return image1.getdata() == image2.getdata()
    else:
        return False


# Function that creates the game matrix from the screenshot.
def createMatrix(image, importedImageTiles):

    dimX, dimY = (3,3)
    matrix = initMatrix(dimX, dimY)
    index = 1
    
    for i in range(dimX):
        for j in range(dimY):
            index = 1
            tileImage = image.crop((j*tileDistance, i*tileDistance, j*tileDistance + tileSize, i*tileDistance + tileSize))
            for importedImageTile in importedImageTiles:
                if equalImages(tileImage, importedImageTile):
                    matrix[i][j] = index
                    index = 1
                    #print("We have a match.")
                else:
                    #print("We do not have a match.")
                    index = index + 1
    return matrix


# Method that returns the final state of the board.
def getFinalMatrix(dimX, dimY):

    finalMatrix = []
    tempMatrix = []
    rows = 3

    for i in range(dimX):
        for j in range(dimY):

            number = ((i * rows) + j + 1) % 9
            tempMatrix.append(number)

        finalMatrix.append(tempMatrix)
        tempMatrix = []

    return finalMatrix
   

# Function that checks if a tile contains a specific number.
def containsNumber(imageTile, number):

    for n in numbers:
        pixel = tileImage.getpixel(n)
        if pixel == BLACK:
            return False
    return True


# Function that gets the image of the puzzle board and returns the board as a 2D array.
def getImageTiles(image, dimX, dimY):

    imageTiles = []

    for i in range(dimX):
        for j in range(dimY):
            tempImage = image.crop((i*tileDistance, j*tileDistance, i*tileDistance + tileSize, j*tileDistance + tileSize))
            imageTiles.append(tempImage)

    return imageTiles



# Function that checks if the puzzle is solvable.
def isSolvable(matrix):

    linearMatrix = []
    inversions = 0

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                continue 
            else:
                linearMatrix.append(matrix[i][j])

    length = len(linearMatrix)
    
    for i in range(length):
        for j in range(i,length):
            if linearMatrix[j]<linearMatrix[i]:
                inversions = inversions + 1
    
    return inversions % 2 == 0


# Function that simulates mouse clicks on the puzzle tiles
def clickSolve(nodeList):

    nodeList.reverse()

    pyautogui.click()
    time.sleep(2)

    counter = 0

    for n in range(0,len(nodeList)-1):
        coords = nodeList[n+1].getNodeCoords()
        clickX = paddingX + coords[1] * tileDistance + tileSize / 2
        clickY = paddingY + coords[0] * tileDistance + tileSize / 2
        print("Click coordinates: (%d,%d)" % (clickX, clickY))
        pyautogui.click(clickX, clickY)
        time.sleep(0.5)
        counter = counter + 1
        print("Counter: ", counter)


# Function that plays the game.
def playGame():
    gameImage = screenGrab(bbox)
    imageTiles = getImageTiles(gameImage,3,3)
    matrix = initMatrix(3,3)

    print("Loading tiles...")
    importedImageTiles = loadTiles(filenames)
    print("Tiles loaded.")

    print("Creating matrix...")
    matrix = createMatrix(gameImage, importedImageTiles)
    print("Matrix created.")
    showMatrix(matrix)

    finalMatrix = getFinalMatrix(3,3)

    startNode = Node(matrix, (0,0), None, None)
    endNode = Node(finalMatrix, (3,3), None, None)

    print("Calculating shortest path...")
    totalPath = Solver.shortestPath(startNode, endNode)
    print("Shortest path calculated.")

    print("Total path length: ", len(totalPath))

    for node in reversed(totalPath):
        node.showMatrix()
        print()

    clickSolve(totalPath)


################################################################

playGame()