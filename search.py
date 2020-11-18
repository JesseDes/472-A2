from puzzle import Puzzle
import heapq
import time
import os

def SolvePuzzle(puzzle: Puzzle , fileName, duration = 0, searchType = None, heuristicFunction = None , sortDirection = "smallest"):
    openList = []
    closedList = []
    currentPuzzle = puzzle
    puzzleShape = puzzle.puzzleTable.shape
    start = time.perf_counter()
    if heuristicFunction != None:
        currentPuzzle.heuristic = heuristicFunction(currentPuzzle.getString(),puzzleShape, currentPuzzle.getSolutions())

    while not currentPuzzle.isSolved() and (duration == 0 or time.perf_counter() - start < duration):
        closedList.append(currentPuzzle)
        for move in currentPuzzle.getMoves():                    # move[0] : cost of the move  |  move[1] : the puzzle state of the move | move[2] the tile that was moved
            if searchType == "ASTAR" or not alreadyVisited(move[1],closedList):
                if searchType == "UCS":
                    newMove = Puzzle(puzzleShape[0], puzzleShape[1], move[1],currentPuzzle,move[2] , move[0] + currentPuzzle.costTotal, move[0])
                elif searchType == "GBFS":
                    newMove = Puzzle(puzzleShape[0], puzzleShape[1], move[1],currentPuzzle, move[2],  move[0] + currentPuzzle.costTotal, move[0], heuristicFunction(move[1], puzzleShape, currentPuzzle.getSolutions()), sortDirection)
                else:
                    fn = move[0] + currentPuzzle.costTotal + heuristicFunction(move[1], puzzleShape, currentPuzzle.getSolutions())
                    skipMove, closedList, openList = aStarListCheck(move,closedList, openList, heuristicFunction, sortDirection,fn)
                    if skipMove:
                        continue
                    newMove = Puzzle(puzzleShape[0], puzzleShape[1], move[1],currentPuzzle ,move[2] , move[0] + currentPuzzle.costTotal, move[0],fn, sortDirection)

                heapq.heappush(openList, newMove)
        
        if len(openList) == 0:
            break
         
        currentPuzzle = heapq.heappop(openList)

    closedList.append(currentPuzzle)
    if currentPuzzle.isSolved():
        print("Correct solution found for :", puzzle.getString() ," of Cost: " , currentPuzzle.costTotal , " in " , time.perf_counter() - start)
        writeSolutionFile(currentPuzzle, fileName, time.perf_counter() - start)
        writeSearchFile(fileName,closedList,searchType,heuristicFunction)
    else:
        writeNoSolution(fileName, time.perf_counter() - start)
        print("Unable to solve ", puzzle.getString(), "within ", duration, " seconds")

    
def writeSolutionFile(puzzle, fileName, runTime):
    path = []
    totalPathCost = puzzle.costTotal
    currentPuzzle = puzzle
    while currentPuzzle != None:
        path.append((currentPuzzle.getString(), currentPuzzle.costToMove , currentPuzzle.movedTile))
        currentPuzzle = currentPuzzle.parent
    
    outputFolder = "./output/" + fileName[0:fileName.find("_")]
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)

    path.reverse()
    f = open(outputFolder + "/" + fileName + "_solution.txt", "w")
    for i in range(len(path)):
        f.write(str(path[i][2]) + " " +  str(path[i][1]) + " " + path[i][0] + "\n")
    
    f.write(str(totalPathCost) + " " + str(runTime))
    f.close()

def writeSearchFile(fileName,closedList, searchType ,heuristic ):
    outputFolder = "./output/" + fileName[0:fileName.find("_")]
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    f = open(outputFolder + "/" + fileName + "_search.txt", "w")

    for puzzle in closedList:
        hn = 0
        fn = 0
        gn = puzzle.costTotal
        if heuristic != None:
            hn = heuristic(puzzle.getString(), puzzle.puzzleTable.shape, puzzle.getSolutions())
        if searchType == "ASTAR":
            fn = hn + gn
        
        f.write(str(fn) + " " + str(gn) + " " + str(hn) + " " + puzzle.getString() + "\n")
    f.close()

def writeNoSolution(fileName, duration):
    outputFolder = "./output/" + fileName[0:fileName.find("_")]
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    f = open(outputFolder + "/" + fileName + "_search.txt", "w")
    g = open(outputFolder + "/" + fileName + "_solution.txt", "w")

    f.write("no solution found in " + str(duration) + " seconds")
    g.write("no solution found in " + str(duration) + " seconds")

    f.close()
    g.close()


def aStarListCheck(move, closedList, openList, heuristicFunction , sortDirection, fn):
    found = False
    for index, item in enumerate(closedList):
        if item.getString() == move[1]:
            found = True
            if resolveSortingDirection(item.heuristic, fn , sortDirection):
                del closedList[index]
                return False, closedList, openList
            else:
                break

    for index, item in enumerate(openList):
        if item.getString() == move[1]:
            found = True
            if resolveSortingDirection(item.heuristic, fn, sortDirection):
                item.heuristic = fn
                del openList[index]
                heapq.heapify(openList)
                return False, closedList, openList
            else:
                break

    return found, closedList, openList

def resolveSortingDirection(old , new , sortingDirection):
    if sortingDirection == "smallest":
        return old < new
    else:
        return old > new

def alreadyVisited(move , closedList):
    for puzzle in closedList:
        if move == puzzle.getString():
            return True
        
    return False