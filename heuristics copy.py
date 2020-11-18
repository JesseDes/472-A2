import math

def h_zero(puzzle:str , shape, solutions):
    return int(puzzle[len(puzzle) - 1] == "0")

def h_one(puzzleData:str, shape, solutions):
    puzzle = [int(x) for x in puzzleData.split(" ")]
    pazzle = puzzleData.split(" ")
    score = 0

    for solution in solutions:
        solution

    for index, value in enumerate(puzzle):
        if value == 0:
            currentValue = shape[0] * shape[1]
        else:
            currentValue = value

        baseOneIndex = index + 1
        expectedRow = math.ceil(baseOneIndex / shape[1] )
        expectedColumn = baseOneIndex % (shape[1])

        if shape[1] * (expectedRow - 1) < currentValue and currentValue < (shape[1] * expectedRow) + 1:
            score += 1

        if expectedColumn == currentValue % shape[1]:
           score += 1
                
    return score

#toroidal distance calculation
def h_two(puzzleData:str, shape):
    puzzle = [int(x) for x in puzzleData.split(" ")]
    score = 0

    for index, value in enumerate(puzzle):
        if value == 0:
            currentValue = shape[0] * shape[1]
        else:
            currentValue = value

        baseOneIndex = index + 1
        expectedRow = math.ceil(baseOneIndex / shape[1] )
        expectedColumn = baseOneIndex % (shape[1])
        valueRow = math.ceil(currentValue / shape[1])
        valueColumn = currentValue % (shape[1])

        rowDistance = math.fabs(valueRow - expectedRow)
        if rowDistance > shape[1] / 2:
            rowDistance = math.fabs(shape[1] - rowDistance)
        
        colDistance = math.fabs(valueColumn - expectedColumn)

        if colDistance > shape[0] / 2:
            colDistance = math.fabs(shape[0] - colDistance)
        
        score += rowDistance + colDistance
   
    return score

