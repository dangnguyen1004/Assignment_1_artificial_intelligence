import sys, getopt
import random
import time
# sys.setrecursionlimit(100000)

class State:
    def __init__(self, parent, board, move, lstSuccessor):
        self.parent = parent
        self.previousMove = move
        self.board = board
        self.lstSuccessor = lstSuccessor

class Puzzle:
    def __init__(self, k):
        self.k = k
        self.n = k*k - 1
        self.sizeOfBoard = k*k
        self.timeOfSolving = 0
        # self.inititalState = State(None, self.createInitialState(), None, [])
        self.inititalState = State(None, [0,8,3,6,7,1,5,4,2], None, [])
        self.goalState = self.createGoalSate()
        self.stateStorage = [] #Store states that have visited
        self.path = [] #Store states that lead to goalstate
        self.stack = []

    def isSolvable(self, board):
        # count invertion in puzzle's board
        invCount = 0
        for i in range(0, self.sizeOfBoard - 1):
            if board[i] == 0: continue
            for j in range(i+1, self.sizeOfBoard):
                 if board[j] == 0: continue
                 if board[i] > board[j]:
                     invCount += 1
        # print(invCount)
        if (invCount % 2 == 0): return True
        return False

    def createInitialState(self):
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
            if self.isSolvable(board): break
        return board

    def createGoalSate(self):
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

        # slide zero to left
        if rowIndexOfZero != 0:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero - 1]
            newState[indexOfZero - 1] = 0
            currentState.lstSuccessor.append(State(currentState, newState, 'left', []))
        # Slide zero to right
        if rowIndexOfZero != self.k - 1:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero + 1]
            newState[indexOfZero + 1] = 0
            currentState.lstSuccessor.append(State(currentState, newState, 'right', []))
        # Slide to zero to up
        if colIndexOfZero != 0:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero - self.k]
            newState[indexOfZero - self.k] = 0
            currentState.lstSuccessor.append(State(currentState, newState, 'up', []))
        # Slide zero to down
        if colIndexOfZero != self.k - 1:
            newState = currentState.board.copy()
            newState[indexOfZero] = newState[indexOfZero + self.k]
            newState[indexOfZero + self.k] = 0
            currentState.lstSuccessor.append(State(currentState, newState, 'down', []))
    
    def solvePuzzle(self, currentState):
        self.stack.append(currentState)
        while len(self.stack) > 0:
            currentState = self.stack.pop()
            self.isSolvable(currentState.board)
            if currentState.board in self.stateStorage:
                continue
            self.stateStorage.append(currentState.board.copy())
            if currentState.board == self.goalState:
                # find path
                self.printBoard(currentState.board)
                return
            self.generateSuccessors(currentState)
            for successor in currentState.lstSuccessor:
                self.stack.append(successor)

    def solve(self):
        self.solvePuzzle(self.inititalState)

def main(argv):
    # if (len(argv) != 1 or int(argv[0]) not in range(1, 10000)):
    #     print("Input must be k of integer, which is k*k matrix of puzzle")
    #     exit()
    # eight_puzzle = Puzzle(int(argv[0]))
    eight_puzzle = Puzzle(3)
    eight_puzzle.printBoard(eight_puzzle.inititalState.board)
    print()
    start_time = time.time()
    eight_puzzle.solve()
    end_time = time.time()
    print(end_time-start_time)
    # eight_puzzle.isSolvable([7,0,3,5,4,8,1,2,6])

if __name__ == "__main__":
   main(sys.argv[1:])