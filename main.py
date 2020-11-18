from puzzle import Puzzle
from search import SolvePuzzle
from heuristics import h_zero, h_one , h_two
import time
import tkinter as tk
from tkinter import filedialog
import sys

print("Please select a puzzle file")
root = tk.Tk()
root.withdraw()
path = filedialog.askopenfilename()
fileName = path[path.rfind("/") + 1:path.rfind(".")]
source = open(path, 'r')

col = input("how many Columns are in these puzzles \n")
row = input("how many Rows are in these puzzles? \n")
duration = input("How long should the tests run for?\n")
methodChoice = input("which test(s) would you like to perform? \n [0] Uniform cost \n [1] Greedy h0 \n [2] Greedy h1 \n [3] Greedy h2 \n [4] Greedy all \n [5] A* h0 \n [6] A* h1 \n [7] A* h2 \n [8] A* all \n [9] All tests \n")

operationList = []
if methodChoice == "0" or methodChoice == "9":
    operationList.append(("UCS",None, "smallest"))
if methodChoice == "1" or methodChoice == "4" or methodChoice == "9":
    operationList.append(("GBFS",h_zero,"smallest"))
if methodChoice == "2" or methodChoice == "4" or methodChoice == "9":
    operationList.append(("GBFS",h_one, "greatest"))
if methodChoice == "3" or methodChoice == "4" or methodChoice == "9":
    operationList.append(("GBFS",h_two,"smallest"))
if methodChoice == "5" or methodChoice == "8" or methodChoice == "9":
    operationList.append(("ASTAR",h_zero,"smallest"))
if methodChoice == "6" or methodChoice == "8" or methodChoice == "9":
    operationList.append(("ASTAR",h_one,"greatest"))
if methodChoice == "7" or methodChoice == "8" or methodChoice == "9":
    operationList.append(("ASTAR",h_two,"smallest"))

for index, line in enumerate(source):
    for op in operationList:
        puzzle = Puzzle(int(col),int(row),line.rstrip())
        heuristicName  = None
        if op[1] != None:
            heuristicName = op[1].__name__
        print("Running Puzzle :", puzzle.getString() , "with method ", op[0] , "and hueristic ", heuristicName  )
        SolvePuzzle(puzzle, fileName + "_" + str(index) + "_" + op[0] + "-" + str(heuristicName) ,int(duration),op[0],op[1],op[2])
        
source.close()