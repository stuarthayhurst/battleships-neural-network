#!/usr/bin/python3
import random

def placePiece(grid, length, x, y, flipped):
  #Return false if the ship won't fit
  if not flipped:
    if x + length > len(grid[0]):
      return False
  else:
    if y + length > len(grid):
      return False

  #Return false if another ship is in the way
  if not flipped:
    for i in range(x, x + length):
      if grid[y][i] != 0:
        return False
  else:
    for i in range(y, y + length):
      if grid[i][x] != 0:
        return False

  #Place the ship on the grid
  if not flipped:
    for i in range(x, x + length):
      grid[y][i] = 1
  else:
    for i in range(y, y + length):
      grid[i][x] = 1

  return True

def placeShips(grid, boardDimensions):
    #Fill the grids with ships
    for shipLength in [5, 4, 3, 3, 2]:
      #Keep trying to place until it succeeds
      placing = True
      while placing:
        #Generate position
        flipped = bool(random.randint(0, 1))
        x, y = random.randint(0, boardDimensions - 1), random.randint(0, boardDimensions - 1)

        #Attempt to place the piece
        placing = not placePiece(grid, shipLength, x, y, flipped)

def buildDataset(datasetSize, boardDimensions, maxHits):
  dataset = []

  #Build the fresh boards, with ships placed on each
  for gridCount in range(datasetSize):
    dataset.append([None, None])
    dataset[gridCount][0] = [[0 for x in range(boardDimensions)] for i in range(boardDimensions)]
    dataset[gridCount][1] = [[0 for x in range(boardDimensions)] for i in range(boardDimensions)]
    placeShips(dataset[gridCount][1], boardDimensions)

  #Place a random number of hits on each board
  for gridCount in range(datasetSize):
    hitCount = random.randint(0, maxHits)
    for i in range(hitCount):
      makingShot = True
      while makingShot:
        x, y = random.randint(0, boardDimensions - 1), random.randint(0, boardDimensions - 1)

        #Check if the tile has been guessed yet
        if dataset[gridCount][0][y][x] == 0:
          #If the tile was a hit, mark with 1
          if dataset[gridCount][1][y][x] == 1:
            dataset[gridCount][0][y][x] = 1
          #If the tile was a miss, mark with -1
          else:
            dataset[gridCount][0][y][x] = -1

          #Trigger next shot
          makingShot = False

    #Concatenate data
    for item in [0, 1]:
      tempData = []
      for i in range(boardDimensions):
        tempData += dataset[gridCount][item][i]
      dataset[gridCount][item] = tempData

  return dataset
