import numpy as np
from itertools import chain 


class Puzzle:
  def __init__(self, height, width, source, parent = None , movedTile = 0 , costTotal = 0, costToMove = 0, heuristic = None , sortDirection = "smallest"):
      puzzleData = source.split(" ")
      if len(puzzleData) != width * height:
          print("ERROR: Puzzle data does not much size given")
      
      self.parent = parent
      self.movedTile = movedTile
      self.costToMove = costToMove
      self.costTotal = costTotal
      self.heuristic = heuristic
      self.sortDirection = sortDirection
      self.freeSlot = None
      rowCounter = 0
      heightcounter = 0
      self.puzzleTable = np.zeros((height,width), dtype=str)
      for tile in puzzleData:
        if tile == '0':
            self.freeSlot = (heightcounter,rowCounter)
        
        self.puzzleTable[heightcounter][rowCounter] = tile
        rowCounter = (rowCounter + 1) % width
        if rowCounter == 0:
            heightcounter += 1

      if self.freeSlot == None:
        print("ERROR FREESLOT WAS NOT FOUND IN ", source )

  def isInCorner(self):
      if (self.freeSlot[0] == 0 or self.freeSlot[0] == self.puzzleTable.shape[0] - 1) and  (self.freeSlot[1] == 0 or self.freeSlot[1] == self.puzzleTable.shape[1] - 1):
          return True
      else:
          return False

  def getMoves(self):
      moveList = []
      if self.isInCorner():
          moveList += self.getDiagonalMoves()

      moveList += self.getVerticleMoves()
      moveList += self.getHorizontalMoves()
      return moveList
    

  def getVerticleMoves(self):
      moveList = []
      
      upCost = 1
      if(self.freeSlot[0] == 0 and self.puzzleTable.shape[0] > 2 ):
          upCost = 2

      upMove = self.puzzleTable.copy()
      oldValue = upMove[(self.freeSlot[0] - 1) % self.puzzleTable.shape[0]][self.freeSlot[1]]
      upMove[(self.freeSlot[0] - 1) % self.puzzleTable.shape[0]][self.freeSlot[1]] = '0'
      upMove[self.freeSlot[0]][self.freeSlot[1]] = oldValue
      moveList.append((upCost, ' '.join(chain(*upMove)),oldValue ))

      if self.puzzleTable.shape[0] > 2:
          downCost = 1
          if self.freeSlot[0] == self.puzzleTable.shape[0] - 1:
              downCost = 2
        
          downMove = self.puzzleTable.copy()
          oldValue = downMove[(self.freeSlot[0] + 1) % self.puzzleTable.shape[0]][self.freeSlot[1]]
          downMove[(self.freeSlot[0] + 1) % self.puzzleTable.shape[0]][self.freeSlot[1]] = '0'
          downMove[self.freeSlot[0]][self.freeSlot[1]] = oldValue
          moveList.append((downCost, ' '.join(chain(*downMove)), oldValue))
    
      return moveList


  def getHorizontalMoves(self):
      moveList = []
      leftCost = 1
      if(self.freeSlot[1] == 0):
          leftCost = 2

      leftMove = self.puzzleTable.copy()
      oldValue = leftMove[self.freeSlot[0]][(self.freeSlot[1] - 1) % self.puzzleTable.shape[1]]
      leftMove[self.freeSlot[0]][(self.freeSlot[1] - 1) % self.puzzleTable.shape[1]] = '0'
      leftMove[self.freeSlot[0]][self.freeSlot[1]] = oldValue
      moveList.append((leftCost, ' '.join(chain(*leftMove)), oldValue))
      
      rightCost = 1
      if(self.freeSlot[1] == self.puzzleTable.shape[1] - 1):
          rightCost = 2

      rightMove = self.puzzleTable.copy()
      oldValue = rightMove[self.freeSlot[0]][(self.freeSlot[1] + 1) % self.puzzleTable.shape[1]]
      rightMove[self.freeSlot[0]][(self.freeSlot[1] + 1) % self.puzzleTable.shape[1]] = '0'
      rightMove[self.freeSlot[0]][self.freeSlot[1]] = oldValue
      moveList.append((rightCost, ' '.join(chain(*rightMove)), oldValue))
    
      return moveList      
       
  def getDiagonalMoves(self):
      moveList = []
      outerHorizontal = 1
      outerVeritcal = 1
      if self.freeSlot[1] == 0:
          outerHorizontal = -1
      if self.freeSlot[0] == 0:
          outerVeritcal = -1

      outerMove = self.puzzleTable.copy()
      oldValue = outerMove[(self.freeSlot[0] + (1 * outerVeritcal)) % self.puzzleTable.shape[0]][(self.freeSlot[1] + (1 * outerHorizontal)) % self.puzzleTable.shape[1]]
      outerMove[(self.freeSlot[0] + (1 * outerVeritcal)) % self.puzzleTable.shape[0]][(self.freeSlot[1] + (1 * outerHorizontal)) % self.puzzleTable.shape[1]] = '0'
      outerMove[self.freeSlot[0]][self.freeSlot[1]] = oldValue
      moveList.append((3, ' '.join(chain(*outerMove)), oldValue))

      innerMove = self.puzzleTable.copy()
      oldValue = innerMove[(self.freeSlot[0] - (1 * outerVeritcal)) % self.puzzleTable.shape[0]][(self.freeSlot[1] - (1 * outerHorizontal)) % self.puzzleTable.shape[1]]
      innerMove[(self.freeSlot[0] - (1 * outerVeritcal)) % self.puzzleTable.shape[0]][(self.freeSlot[1] - (1 * outerHorizontal)) % self.puzzleTable.shape[1]] = '0'
      innerMove[self.freeSlot[0]][self.freeSlot[1]] = oldValue
      moveList.append((3, ' '.join(chain(*innerMove)), oldValue))

      return moveList


  def getString(self):
      return ' '.join(chain(*self.puzzleTable)) 
  
  def isSolved(self):
      
      for solution in self.getSolutions():
          if self.getString() == ' '.join(chain(*solution)):
              return True

      return False

  def getSolutions(self):
      limit = self.puzzleTable.shape[0] * self.puzzleTable.shape[1]
      solutionOne = []
      for x in range(1,limit):
          solutionOne.append(str(x))
      solutionOne.append('0')

      solutionTwo = []

      for y in range(self.puzzleTable.shape[0]):
          solutionTwo.append(str(y + 1))
          for x in range(1, self.puzzleTable.shape[1]):
              solutionTwo.append(str(y + 1 + (x * self.puzzleTable.shape[0] )))
       
      solutionTwo[len(solutionTwo) - 1] = "0"

      return [solutionOne,solutionTwo]

  def __lt__(self, other):
      if self.heuristic == None:
          return self.costTotal < other.costTotal
      elif self.sortDirection == "smallest": 
          return self.heuristic < other.heuristic
      else:
          return self.heuristic > other.heuristic

  def __eq__(self, other):
      if other == None:
          return False

      return self.getString() == other.getString()
