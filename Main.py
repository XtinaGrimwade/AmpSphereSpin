# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:49:13 2020

@author: Christina Grimwade

For Ellie <3

Still to do:
    finish level selection. Possibly import CSV? That'll be cleaner.
    progress to next level
    level increment. Special rules to skip forwards
    Dropping back a level: do with a variable that incriments when you click?
    Help with game rules
    Pretty up GUI. Looks a bit basic
"""


from random import shuffle
from random import choice
from numpy import transpose
import math
import tkinter as tk


root = tk.Tk()   
    
class GameElement(tk.Frame):
    def __init__(self, master=root):
        super().__init__(master)
        self.master = master
        self.pack(side = 'bottom')
        self.widgetGameTiles()

    
    def widgetGameTiles(self):
        self.levelTiles = len(levelTiles)
        global tilesSet
        global rowScore
        global columnScore
        for i in range(self.levelTiles):
            self.gameTiles = tk.Button(self, width = 2, height = 2)
            self.gameTiles["text"] = "x" #lambda x=i: levelTiles[x]
            self.gameTiles["command"] = lambda x=i: checkForBomb(x) 
            self.gameTiles.grid(row=math.floor(i/gridSize), column= i%gridSize)
            tilesSet.append(self.gameTiles)
        
        for j in range(gridSize):            
            self.rowScore = tk.Text(self, height=1, width=4)
            self.currentRow = rowData(grid[j])
            self.rowScore.insert('insert',self.currentRow.zerosInRow() + "/" + self.currentRow.rowPointsTotal())
            self.rowScore.grid(row =j , column = 6)
            rowScore = self.rowScore
            
        for k in range(gridSize):            
            self.columnScore = tk.Text(self, height=4, width=1)
            self.currentColumn = rowData(gridColumns[k])
            self.columnScore.insert('insert',self.currentColumn.zerosInRow() + "/" + self.currentColumn.rowPointsTotal())
            self.columnScore.grid(row =7 , column = k)
            columnScore = self.columnScore
            

class Scores(tk.Frame):
    def __init__(self, master=root):
        super().__init__(master)
        self.master = master
        self.pack(side = "top")
        self.widgetScoreBoard()
        
    def widgetScoreBoard(self):
        global score
        global roundScore
        global varRoundScore
        global varScore
        self.totalScore = tk.Text(self, height=1, width = 30)
        self.totalScore.insert('insert',"Total score: ")
        self.totalScore.insert('end',varScore)
        score = self.totalScore
        self.totalScore.pack()
        self.currentScore = tk.Text(self, height=1, width = 30)
        self.currentScore.insert('insert',"This game: ")
        self.currentScore.insert('end',varRoundScore)
        self.currentScore.pack()
        roundScore = self.currentScore

        
class rowData:
    def __init__(self, rowDataList):
        self.rowDataList = rowDataList
    
    def zerosInRow(self):
        return(str(self.rowDataList.count(0)))
    
    def rowPointsTotal(self):
        return(str(sum(self.rowDataList)))
    
def checkForBomb(x):
    global score
    global roundScore
    global varRoundScore
    global appFrame1
    global levelTiles
    if levelTiles[x] == 0:
        tk.messagebox.showinfo("Game over")
        varScore.append(varRoundScore)
        score.delete(1.13,'end')
        score.insert('end',sum(varScore))
        varRoundScore = 0
        roundScore.delete(1.11,'end')
        roundScore.insert('end', varRoundScore)
        
        shuffle(levelTiles) 
        appFrame1.pack_forget()
        del appFrame1
        LevelSetup()
        appFrame1 = GameElement(master=root)
        
    else:
        updated = tilesSet[x]
        updated["text"] = levelTiles[x]
        roundScore.delete(1.11,'end')
        if varRoundScore == 0:
            varRoundScore +=  levelTiles[x]
        else:
            varRoundScore *= levelTiles[x]
        roundScore.insert('end', varRoundScore)

def LevelSetup():
    global levelTiles
    global tilesSet
    global row
    global grid
    global gridColumnsArray
    global gridColumns
    global level
    global currentLevel
    levelTiles = []
    tilesSet = []
    row = []
    grid = []
    gridColumnsArray = []
    gridColumns = []
    level = levelSetup(currentLevel)
      
    #Add the 0s
    for x in range(level["0s"]):
        levelTiles.append(0)
    
    #Add the 2s
    for x in range(level["2s"]):
        levelTiles.append(2)
    
    #Add the 3s
    for x in range(level["3s"]):
        levelTiles.append(3)
        
    onesTotal = pow(gridSize,2) - len(levelTiles)
        
    #Fill up list with 1s
    for x in range(onesTotal):
            levelTiles.append(1)
            
    shuffle(levelTiles) 
    
    for x in levelTiles:
        row.append(x)
        if len(row) == gridSize:
            grid.append(row.copy())
            row.clear()    
            
    gridColumnsArray = transpose(grid)
    gridColumns = gridColumnsArray.tolist()

def levelSetup(x):
    level = [{"0s":6,"2s":3,"3s":1},{"0s":6,"2s":0,"3s":3},{"0s":6,"2s":5,"3s":0},{"0s":6,"2s":2,"3s":2},{"0s":6,"2s":4,"3s":1}]
    #level.append([{"0s":7,"2s":1,"3s":3},{"0s":7,"2s":6,"3s":2},{"0s":7,"2s":5,"3s":0},{"0s":7,"2s":2,"3s":2},{"0s":7,"2s":4,"3s":1}])
    return choice(level)
        
currentLevel = 1
tilesSet = []
varScore = [0]
varRoundScore = 0  

gridSize = 5


LevelSetup()


appFrame1 = GameElement(master=root)
appFrame2 = Scores(master=root)
root.mainloop()