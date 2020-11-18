import random
puzzleCount = input("How many puzzles would you like to generate? \n")
col = input("how many columns are there in the puzzle? \n")
row = input("how many rows are there in the puzzle?\n")
fileName = input("What is the name of the file you'd like to store the tests in? \n")

f = open(fileName + ".txt", "w")

for x in range(int(puzzleCount)):
    puzzleData = list(map(str, range(0,int(col) * int(row))))
    random.shuffle(puzzleData)
    f.write(' '.join(puzzleData) +'\n')

f.close()
