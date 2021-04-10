import sys
import random
import numpy
import functools
import time

sizeOfSudoku = 9


class Chromosome:
    def __init__(self):
        self.values = None
        self.fitnessScore = 0

    def updateFitnessScore(self):
        rowCount = [0 for i in range(sizeOfSudoku)]
        columnCount = [0 for i in range(sizeOfSudoku)]
        blockCount = [0 for i in range(sizeOfSudoku)]
        rowFitness = 0
        columnFitness = 0
        blockFitness = 0

        # check row
        for row in range(sizeOfSudoku):
            for col in range(sizeOfSudoku):
                rowCount[self.values[row][col] - 1] += 1
            rowFitness += (1.0 / len(set(rowCount))) / sizeOfSudoku
            rowCount = [0 for i in range(sizeOfSudoku)]

        # check column
        for col in range(sizeOfSudoku):
            for row in range(sizeOfSudoku):
                columnCount[self.values[row][col] - 1] += 1
            columnFitness += (1.0 / len(set(columnCount))) / sizeOfSudoku
            columnCount = [0 for i in range(sizeOfSudoku)]

        # check block
        # block 1 -3
        for blockRow in range(3):
            for blockCol in range(3):
                for row in range(blockRow * 3, blockRow * 3 + 3):
                    for col in range(blockCol * 3, blockCol * 3 + 3):
                        blockCount[self.values[row][col] - 1] += 1
                blockFitness += (1.0 / len(set(blockCount))) / sizeOfSudoku
                blockCount = [0 for i in range(sizeOfSudoku)]

        # total fitness score
        if int(rowFitness) == 1 and int(columnFitness) == 1 and int(blockFitness) == 1:
            self.fitnessScore = 1   
        else:
            self.fitnessScore = columnFitness * blockFitness
        # print(self.fitnessScore)

    def mutate(self, mutateRate, givenSudoku):
        r = random.uniform(0, 1.1)
        while r > 1:
            r = random.uniform(0, 1.1)

        success = False
        if r < mutateRate:
            while not(success):
                row = random.randint(0, sizeOfSudoku - 1)

                column1 = random.randint(0, sizeOfSudoku - 1)
                column2 = random.randint(0, sizeOfSudoku - 1)
                while column1 == column2:
                    column1 = random.randint(0, sizeOfSudoku - 1)
                    column2 = random.randint(0, sizeOfSudoku - 1)

                # check gene not in legal value
                if givenSudoku.values[row][column1] == 0 and givenSudoku.values[row][column2] == 0:
                    # check possible exchange gene
                    if (not givenSudoku.isColumnDuplicate(column1, self.values[row][column2]) 
                        and not givenSudoku.isColumnDuplicate(column2, self.values[row][column1]) 
                        and not givenSudoku.isBlockDuplicate(row, column1, self.values[row][column2]) 
                        and not givenSudoku.isBlockDuplicate(row, column2, self.values[row][column1])):
                        
                        # exchange gene
                        temp = self.values[row][column1]
                        self.values[row][column1] = self.values[row][column2]
                        self.values[row][column2] = temp
                        
                        success = True
        return success


class Given(Chromosome):
    # For the given value of the Sudoku
    def __init__(self, values):
        self.values = values
        self.fitnessScore = 0

    def isRowDuplicate(self, row, value):
        if value in self.values[row]:
            return True
        return False

    def isColumnDuplicate(self, col, value):
        for row in range(sizeOfSudoku):
            if self.values[row][col] == value:
                return True
        return False

    def isBlockDuplicate(self, row, col, value):
        base_row = row // 3
        base_col = col // 3
        for i in range(base_row * 3, base_row * 3 + 3):
            for j in range(base_col * 3, base_col * 3 + 3):
                if self.values[i][j] == value:
                    return True
        return False


class Population:
    def __init__(self):
        self.chromosomes = []

    def seed(self, numberOfChromosomes, givenSudoku):

        # below is code for finding all legal values of each square
        legalValues = Chromosome()
        legalValues.values = [
            [[] for j in range(sizeOfSudoku)] for i in range(sizeOfSudoku)]  # 3d array
        for row in range(sizeOfSudoku):
            for col in range(sizeOfSudoku):
                if (givenSudoku.values[row][col] != 0):
                    legalValues.values[row][col].append(
                        int(givenSudoku.values[row][col]))
                elif (givenSudoku.values[row][col] == 0):
                    for value in range(1, 10):
                        if not(givenSudoku.isRowDuplicate(row, value) or givenSudoku.isColumnDuplicate(col, value) or givenSudoku.isBlockDuplicate(row, col, value)):
                            legalValues.values[row][col].append(value)

        # create a new population:
        for chr in range(numberOfChromosomes):
            # create new chromosome
            newChromosome = Chromosome()
            newChromosome.values = []
            for row in range(sizeOfSudoku):
                # for each row in chromosome
                aNewRow = [0 for j in range(sizeOfSudoku)]

                for col in range(sizeOfSudoku):
                    # for each square in row
                    if givenSudoku.values[row][col] != 0:
                        aNewRow[col] = givenSudoku.values[row][col]
                    elif givenSudoku.values[row][col] == 0:
                        # pick up a legal value to fill in square
                        aNewRow[col] = legalValues.values[row][col][random.randint(
                            0, len(legalValues.values[row][col]) - 1)]
                # Ensure that at least each row doesnot have duplicate value
                while len(set(aNewRow)) != 9:
                    for col in range(sizeOfSudoku):
                        if givenSudoku.values[row][col] == 0:
                            aNewRow[col] = legalValues.values[row][col][random.randint(
                                0, len(legalValues.values[row][col]) - 1)]
                newChromosome.values.append(aNewRow.copy())
            self.chromosomes.append(newChromosome)

        # update fitness score for all chromosome in population
        self.updateFitnessScore()

    def updateFitnessScore(self):
        for chromosome in self.chromosomes:
            chromosome.updateFitnessScore()

    def sortChromosome(self):
        self.chromosomes.sort(key = self.sortFitness, reverse = True)

    def sortFitness(self, x):
        return x.fitnessScore


class GeneticFunction:
    def __init__(self):
        return

    def select(self, chromosomes):
        c1 = chromosomes[random.randint(0, len(chromosomes) - 1)]
        c2 = chromosomes[random.randint(0, len(chromosomes) - 1)]
        f1 = c1.fitnessScore
        f2 = c2.fitnessScore

        stronger = None
        weaker = None
        if f1 > f2:
            stronger = c1
            weaker = c2
        else:
            stronger = c2
            weaker = c1

        selectionRate = 0.85
        rate = random.uniform(0, 1.1)
        while(rate > 1):
            rate = random.uniform(0, 1.1)
            
        if(rate < selectionRate):
            return stronger
        else:
            return weaker

    def crossover(self, father, mother, crossoverRate):
        child1 = Chromosome()
        child2 = Chromosome()

        # copy gene
        child1.values = father.values.copy()
        child2.values = mother.values.copy()

        # crossover
        rate = random.uniform(0, 1.1)
        while(rate > 1):
            rate = random.uniform(0, 1.1)

        if rate < crossoverRate:
            # find two point to exchange genes
            point1 = random.randint(0, 8)
            point2 = random.randint(1, 9)
            while point1 >= point2:
                point1 = random.randint(0, 8)
                point2 = random.randint(1, 9)

            for gene in range(point1, point2):
                # exchange gene
                temp = child1.values[gene].copy()
                child1.values[gene] = child2.values[gene].copy()
                child2.values[gene] = temp.copy()
        child1.updateFitnessScore()
        child2.updateFitnessScore()
        return child1, child2

    def crossover_row(self, row1, row2,):
        pass


class Sudoku:
    def __init__(self):
        self.given = None
        self.population = None
        self.solution = None

        # Sudoku variable
        self.numberOfChromosomes = 1000
        self.numberOfElites = int(0.05 * self.numberOfChromosomes)
        self.numberOfGenerations = 1000
        self.numberOfMutation = 0

    def solve(self):
        # mutate variable
        phi = 0
        sigma = 1
        mutationRate = 0.06

        # Create initial population
        self.population = Population()
        self.population.seed(self.numberOfChromosomes, self.given)

        # Loop in 1000 generations to find solution
        stale = 0
        for generation in range(self.numberOfGenerations):
            print("Generation "+ str(generation))

            # check for solution
            bestFitnessScore = 0.0
            for chr in self.population.chromosomes:
                fitnessScore = chr.fitnessScore
                if (int(fitnessScore) == 1):
                    print("Solution found at generation " + str(generation))
                    self.solution = chr
                    self.printSolution(self.solution)
                    return
                if (fitnessScore > bestFitnessScore):
                    bestFitnessScore = fitnessScore
            print("Best fitness score: " + str(bestFitnessScore))

            # select elites (the fittest chromosomes)
            self.population.sortChromosome()
            elites = []
            for e in range(self.numberOfElites):
                elite = Chromosome()
                elite.values = self.population.chromosomes[e].values.copy()
                elites.append(elite)

            # create new population
            newPopulation = []
            helper = GeneticFunction()
            for rest in range(self.numberOfElites, self.numberOfChromosomes, 2):
                # Select father and mother from population
                father = helper.select(self.population.chromosomes)
                mother = helper.select(self.population.chromosomes)

                # cross over father and mother to give new offspring
                child1, child2 = helper.crossover(
                    father, mother, crossoverRate=1.0)

                # mutate childrends

                oldFitnessScore = child1.fitnessScore
                if child1.mutate(mutationRate, self.given):
                    self.numberOfMutation += 1
                    if child1.fitnessScore > oldFitnessScore:
                        phi += 1

                oldFitnessScore = child2.fitnessScore
                if child2.mutate(mutationRate, self.given):
                    self.numberOfMutation += 1
                    if child2.fitnessScore > oldFitnessScore:
                        phi += 1

                # add new child
                newPopulation.append(child1)
                newPopulation.append(child2)

            # append the elites to the end of population
            for e in elites:
                newPopulation.append(e)

            # next generatation
            self.population.chromosomes = newPopulation
            self.population.updateFitnessScore()

            # calculate new adaptive mutation rate for the next generation:
            # base on 
            if self.numberOfMutation == 0:
                phi = 0  
            else:
                phi = phi / self.numberOfMutation

            if phi > 0.2:
                sigma = sigma / 0.998
            elif phi < 0.2:
                sigma = sigma * 0.998

            mutationRate = abs(numpy.random.normal(
                loc=0.0, scale=sigma, size=None))
            self.numberOfMutation = 0
            phi = 0

            # check stale population 
            self.population.sortChromosome()
            if(self.population.chromosomes[0].fitnessScore != self.population.chromosomes[1].fitnessScore):
                stale = 0
            else:
                stale += 1

            # re-seed population when stale
            if stale >= 100:
                print("The population has gone stale. Re-seeding...")
                self.population.seed(sizeOfSudoku, self.given)
                stale = 0
                phi = 0
                sigma = 1
                self.numberOfMutation = 0
                mutationRate = 0.06

        print("Can't find solution")

    def readInput(self, fileName):
        input = open(fileName, "r")
        givenValues = input.readlines()[0].split(" ")
        self.given = Given([[0 for col in range(sizeOfSudoku)]
                           for row in range(sizeOfSudoku)])
        for row in range(sizeOfSudoku):
            for col in range(sizeOfSudoku):
                self.given.values[row][col] = int(
                    givenValues[row * sizeOfSudoku + col])

        print("Initial sudoku: ")
        for row in self.given.values:
            print(row)

    def printSolution(self, solution):
        for row in solution.values:
            print(row)


def main(argv):
    inputSudoku = input("Enter input file: ")
    sudoku = Sudoku()
    sudoku.readInput(inputSudoku)
    start_time = time.time()
    sudoku.solve()
    end_time = time.time()
    timeOfSolving = end_time - start_time
    print("Running time: " + str(timeOfSolving))


if __name__ == "__main__":
    main(sys.argv[1:])
