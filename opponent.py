#!/usr/bin/python3

import random

class Opponent():
  def __init__(self):
    self.grid = [[0 for i in range(7)] for j in range(7)]
    self.enemyGrid = [[0 for i in range(7)] for j in range(7)]

    self.lastGuess = []

  def feedbackMove(self, result):
    if result == "hit":
      self.enemyGrid[self.lastGuess[1]][self.lastGuess[0]] = 1
    else:
      self.enemyGrid[self.lastGuess[1]][self.lastGuess[0]] = -1

  def makeMove(self):
    guessing = True
    x, y = 0, 0
    while guessing:
      x = random.randint(0, 6)
      y = random.randint(0, 6)

      if self.enemyGrid[y][x] == 0:
        guessing = False

    self.lastGuess = [x, y]
    return [x, y]

  def generateGrid(self, shipLengths):
    #Fill the grids with ships
    for shipLength in shipLengths:
      #Keep trying to place until it succeeds
      placing = True
      while placing:
        #Generate position
        flipped = bool(random.randint(0, 1))
        x, y = random.randint(0, 6), random.randint(0, 6)

        #Attempt to place the piece
        if self.placePiece(shipLength, x, y, flipped):
          placing = False

  def placePiece(self, length, x, y, flipped):
    #Return false if the ship won't fit
    if not flipped:
      if x + length > len(self.grid[0]):
        return False
    else:
      if y + length > len(self.grid):
        return False

    #Return false if another ship is in the way
    if not flipped:
      for i in range(x, x + length):
        if self.grid[y][i] != 0:
          return False
    else:
      for i in range(y, y + length):
        if self.grid[i][x] != 0:
          return False

    #Place the ship on the grid
    if not flipped:
      for i in range(x, x + length):
        self.grid[y][i] = 1
    else:
      for i in range(y, y + length):
        self.grid[i][x] = 1

    return True
