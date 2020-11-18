import math

def h_zero(puzzle:str , shape, solutions):
    return int(puzzle[len(puzzle) - 1] == "0")

def h_one(puzzleData:str, shape, solutions):
    puzzle = puzzleData.split(" ")
    score = 0

    for solution in solutions:
        currentScore = 0
        for index in range(shape[0]):
            expectedRowMembers =  solution[shape[1] * index:shape[1] * (index + 1)]
            currentRowMembers = puzzle[shape[1] * index:shape[1] * (index + 1)]
            for member in currentRowMembers:
                if member in expectedRowMembers:
                    currentScore += 1

        for index in range(shape[1]):
            expectedColMembers = []
            currentColMembers = []
            for j in range(shape[0]):
                expectedColMembers.append(solution[index % shape[1] + j * shape[1]])
                currentColMembers.append(puzzle[index % shape[1] + j * shape[1]])

            for member in currentColMembers:
                if member in expectedColMembers:
                    currentScore += 1
        if currentScore > score:
            score = currentScore
        
    return score

#toroidal distance calculation
def h_two(puzzleData:str, shape, solutions):
    puzzle = [int(x) for x in puzzleData.split(" ")]
    score = 0

    for solution in solutions:
        currentScore = 0
        for index, value in enumerate(puzzle):
            expectedRow = int(solution.index(str(value)) % shape[1])
            expectedCol = int(solution.index(str(value)) / shape[1])
            valueRow = int(index % shape[1])
            valueCol = int(index / shape[1])

            rowDistance = math.fabs(valueRow - expectedRow)
            if rowDistance > shape[1] / 2:
                rowDistance = math.fabs(shape[1] - rowDistance)
            
            colDistance = math.fabs(valueCol - expectedCol)

            if colDistance > shape[0] / 2:
                colDistance = math.fabs(shape[0] - colDistance)
            
            currentScore += colDistance + rowDistance 

        if score > currentScore:
            score = currentScore
    return score
