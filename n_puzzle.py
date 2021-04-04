import sys
import getopt
import random
import time
# sys.setrecursionlimit(100000)


class State:
    def __init__(self, parent, board, move, depth):
        self.parent = parent
        self.previousMove = move
        self.board = board
        self.map = ''.join(str(e) for e in board)
        self.depth = depth
        self.cost = self.calculateCost()

    def calculateCost(self):
        pos = 1
        count = 0
        for tile in self.board:
            if tile == pos:
                count += 1
            pos += 1
        return self.depth + 8 - count



class Puzzle:
    def __init__(self, k):
        self.k = k
        self.n = k*k - 1
        self.sizeOfBoard = k*k
        self.timeOfSolving = 0
        self.timeOfGenerateSuccessors = 0
        self.maxDeepSearch = 0
        self.inititalState = State(None, self.createInitialBoard(), 'Start', 0)
        # self.inititalState = State(None, [1, 2, 3, 4, 5, 6, 7, 0, 8], None, 0)
        self.goalBoard = self.createGoalBoard()
        self.finalState = None
        self.stateStorage = set()  # Store states that have visited
        self.path = []  # Store states that lead to goalstate
        self.stack = []

    def isSolvable(self, board):
        # count invertion in puzzle's board
        invCount = 0
        for i in range(0, self.sizeOfBoard - 1):
            if board[i] == 0:
                continue
            for j in range(i+1, self.sizeOfBoard):
                if board[j] == 0:
                    continue
                if board[i] > board[j]:
                    invCount += 1
        # print(invCount)
        if (invCount % 2 == 0):
            return True
        return False

    def createInitialBoard(self):
        print("Creating initial state")
        board = []
        lstAddSuccess = []
        while 1:
            board.clear()
            lstAddSuccess.clear()
            for count in range(0, self.k*self.k):
                newTile = random.randint(0, self.n)
                while newTile in lstAddSuccess:
                    newTile = random.randint(0, self.n)
                lstAddSuccess += [newTile]
                board += [newTile]
            if self.isSolvable(board):
                break
        return board

    def createGoalBoard(self):
        board = []
        for count in range(1, self.n + 1):
            board += [count]
        board += [0]
        return board

    def printBoard(self, board):
        for row in range(0, self.sizeOfBoard, self.k):
            # for col in range(row, row + self.k):
            print(board[row:row + self.k])

    def generateSuccessors(self, currentState):
        indexOfZero = currentState.board.index(0)
        rowIndexOfZero = indexOfZero % self.k
        colIndexOfZero = indexOfZero // self.k
        lstSuccessors = []

        # Slide to zero to up
        if colIndexOfZero != 0:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero - self.k]
            newState[indexOfZero - self.k] = 0
            lstSuccessors.append(
                State(currentState, newState, 'up', currentState.depth + 1))
        # Slide zero to down
        if colIndexOfZero != self.k - 1:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero + self.k]
            newState[indexOfZero + self.k] = 0
            lstSuccessors.append(
                State(currentState, newState, 'down', currentState.depth + 1))
        # slide zero to left
        if rowIndexOfZero != 0:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero - 1]   
            newState[indexOfZero - 1] = 0
            lstSuccessors.append(
                State(currentState, newState, 'left', currentState.depth + 1))
        # Slide zero to right
        if rowIndexOfZero != self.k - 1:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero + 1]
            newState[indexOfZero + 1] = 0
            lstSuccessors.append(
                State(currentState, newState, 'right', currentState.depth + 1))
        
        lstSuccessorsCost = [ele.cost for ele in lstSuccessors]
        lstSuccessorsInOrderOfCost = []
        for i in range(0, len(lstSuccessorsCost)):
            lstSuccessorsInOrderOfCost.append(lstSuccessors[lstSuccessorsCost.index(min(lstSuccessorsCost))])
            lstSuccessorsCost[lstSuccessorsCost.index(min(lstSuccessorsCost))] = 100

        return lstSuccessorsInOrderOfCost

    def solvePuzzle(self, currentState):
        self.stack.append(currentState)
        self.stateStorage.add(currentState.map)
        while len(self.stack) > 0:
            currentState = self.stack.pop()
            if currentState.board == self.goalBoard:
                # find path
                # self.printBoard(currentState.board)
                self.finalState = currentState
                print("Solving " + str(self.n) + " puzzle done!")
                return
            start_time_gen = time.time()
            lstSuccessor = self.generateSuccessors(currentState)
            end_time_gen = time.time()
            timeOfGen = end_time_gen - start_time_gen
            self.timeOfGenerateSuccessors += timeOfGen
            for successor in lstSuccessor[::-1]:
                if successor.map not in self.stateStorage:
                    self.stack.append(successor)
                    self.stateStorage.add(successor.map)
                    if successor.depth > self.maxDeepSearch:
                        self.maxDeepSearch += 1

    def solve(self):
        start_time = time.time()
        self.solvePuzzle(self.inititalState)
        end_time = time.time()
        self.timeOfSolving = end_time - start_time
        print("Running time: " + str(self.timeOfSolving))
        print("Max Search Dept: " + str(self.maxDeepSearch))
        print("Final State Dept: " + str(self.finalState.depth))

    def printInitialBoard(self):
        self.printBoard(self.inititalState.board)
    
    def printPath(self):
        path = []
        state = self.finalState
        while (state is not None):
            if state.previousMove is not None:
                path.append(state.previousMove)
            state = state.parent
        
        print("path: "),
        print(path[::-1])



def main(argv):
    # if (len(argv) != 1 or int(argv[0]) not in range(1, 10000)):
    #     print("Input must be k of integer, which is k*k matrix of puzzle")
    #     exit()
    # eight_puzzle = Puzzle(int(argv[0]))
    eight_puzzle = Puzzle(4)
    eight_puzzle.printInitialBoard()
    print()
    eight_puzzle.solve()
    # eight_puzzle.printPath()

if __name__ == "__main__":
    main(sys.argv[1:])
