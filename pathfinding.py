import pygame
import math
from queue import PriorityQueue

# =================== Pathfindind size ==============
WIDTH = 800
NUMOFROWS = 50
# NUMOFCOLS = NUMOFROWS

# ===== Set up display to visualize pathfinding =====
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfiding using A* algorithm")

#  ================== State color =====================
ORANGE = (255, 165, 0)          # Start node
TURQUOISE = (64, 224, 208)      # End Node
WHITE = (255, 255, 255)         # Not visited
BLACK = (0, 0, 0)               # Wall, cannot visit
RED = (255, 0, 0)               # Been visited
PURPLE = (128, 0, 128)          # Path node
GREEN = (0, 255, 0)             # Node in open set
GREY = (128, 128, 128)          # Gridline color
YELLOW = (255, 255, 0)
BLUE = (0, 255, 0)


class Node:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.totalRows = totalRows
        self.color = WHITE
        self.neighbors = []

    def getPosition(self):
        return self.row, self.col

    def isClosed(self):
        # been visited ?
        return self.color == RED

    def isOpen(self):
        # is in the priority queue?
        return self.color == GREEN

    def isWall(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == ORANGE

    def isEnd(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def makeStart(self):
        self.color = ORANGE

    def makeClosed(self):
        self.color = YELLOW

    def makeOpen(self):
        self.color = GREEN

    def makeWall(self):
        self.color = BLACK

    def makeEnd(self):
        self.color = TURQUOISE

    def makePath(self):
        self.color = PURPLE

    def draw(self, win):
        # Draw this node in display at position x and y
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        # down
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall():
            self.neighbors.append(grid[self.row + 1][self.col])

        # up
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():  
            self.neighbors.append(grid[self.row - 1][self.col])

        # right
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall():
            self.neighbors.append(grid[self.row][self.col + 1])

        # left
        if self.col > 0 and not grid[self.row][self.col - 1].isWall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def hScore(node1, node2):
    # h function to calculate manhattan's distance between two node
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1 - x2) + abs(y1 - y2)


def algorithm(draw, grid, startNode, endNode):
    # A* Algorithm uses f(n) = h(n) + g(n) to evaluate a node then traverse the node with have the smallest score (best to reach end Node)
    # h(n): distance from node n to end node
    # g(n): distante from node n to start node
    # store g score of each node
    gScore = {node: float("inf") for row in grid for node in row}
    gScore[startNode] = 0
    # store f score of each node
    fScore = {node: float("inf") for row in grid for node in row}
    fScore[startNode] = hScore(startNode.getPosition(), endNode.getPosition())

    count = 0  # for keep track which node is put to Queue first, then when we have two node with same f score, we choose the first-in node
    cameFrom = {}  # store the came_from_node of each node
    openSet = PriorityQueue()
    openSet.put((0, count, startNode))
    # For purpose of checking if the node is in the openSet.
    openSetHash = {startNode}

    while not openSet.empty():
        # for exit while running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        currentNode = openSet.get()[2]
        openSetHash.remove(currentNode)

        if currentNode == endNode:  # found
            findPath(cameFrom, endNode, draw)
            startNode.makeStart()
            endNode.makeEnd()
            return True

        currentNode.updateNeighbors(grid)
        for neighbor in currentNode.neighbors:
            temp_gScore = gScore[currentNode] + 1

            if temp_gScore < gScore[neighbor]:
                cameFrom[neighbor] = currentNode
                gScore[neighbor] = temp_gScore
                fScore[neighbor] = gScore[neighbor] + \
                    hScore(neighbor.getPosition(), endNode.getPosition())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()

        draw()

        if currentNode != startNode:
            currentNode.makeClosed()

    return False


def findPath(cameFrom, currentNode, draw):
    # Find the path from start to end node
    while currentNode in cameFrom:
        currentNode = cameFrom[currentNode]
        currentNode.makePath()
        draw()


def makeGrid(numberOfRows, width):
    grid = []
    widthOfRow = width // numberOfRows

    for i in range(numberOfRows):
        # make 2d array
        grid.append([])
        for j in range(numberOfRows):
            node = Node(i, j, widthOfRow, numberOfRows)
            grid[i].append(node)

    return grid


def drawGridLine(win, numberOfRows, width):
    # Draw the grid lines
    widthOfRow = width // numberOfRows
    for i in range(numberOfRows):
        pygame.draw.line(win, GREY, (0, i * widthOfRow), (width, i * widthOfRow))
    for i in range(numberOfRows):
        pygame.draw.line(win, GREY, (i * widthOfRow, 0), (i * widthOfRow, width))


def draw(win, grid, numberOfRows, width):
    # Draw everything to display
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    drawGridLine(win, numberOfRows, width)
    pygame.display.update()


def getClickedPosition(position, numberOfRows, width):
    # Return row, col of the the clicked position
    widthOfRow = width // numberOfRows
    y, x = position
    return y // widthOfRow, x // widthOfRow


def main(win, width):
    numberOfRow = NUMOFROWS
    grid = makeGrid(numberOfRow, width)

    startNode = None
    endNode = None

    # Main loop
    run = True
    while run:
        draw(win, grid, numberOfRow, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Set the start node, end node, wall node
            if pygame.mouse.get_pressed()[0]:  # If left mouse
                # access to the node been pressed
                position = pygame.mouse.get_pos()
                row, col = getClickedPosition(position, numberOfRow, width)
                node = grid[row][col]

                if startNode is None and node != endNode:
                    startNode = node
                    startNode.makeStart()
                elif endNode is None and node != startNode:
                    endNode = node
                    endNode.makeEnd()
                elif node != startNode and node != endNode:
                    node.makeWall()

            elif pygame.mouse.get_pressed()[2]:  # If right mouse -> reset node
                position = pygame.mouse.get_pos()
                row, col = getClickedPosition(position, numberOfRow, width)
                node = grid[row][col]

                node.reset()
                if node == startNode:
                    startNode = None
                elif node == endNode:
                    endNode = None

            if event.type == pygame.KEYDOWN:
                # Start the A* algorithm visualization - press SPACE
                if event.key == pygame.K_SPACE and startNode is not None and endNode is not None:
                    algorithm(lambda: draw(win, grid, numberOfRow,
                              width), grid, startNode, endNode)
                # To start again - press C
                if event.key == pygame.K_c:
                    startNode = None
                    endNode = None
                    grid = makeGrid(numberOfRow, width)

    pygame.quit()


main(WIN, WIDTH)
