#!/usr/bin/python3

import random
#Import the neural network
import neural_network_playground.model as model

#Class to contain the AI opponent
# - Contains a neural network
# - Loads a weight file to determine difficulty
# - Returns a loaction to guess when requested
# - Returns a valid battleships board when requested
# - Takes feedback on its last move when sent
class Opponent():
  def __init__(self):
    #Separate structures for the generated grid, and the grid to track known guess data
    self.grid = [[0 for i in range(7)] for j in range(7)]
    self.enemyGrid = [[0 for i in range(7)] for j in range(7)]
    self.lastGuess = []

    self.network = model.Network(7 ** 2)

  #Function to load weights in from a file
  # - Weights file determines model behaviour, in this case difficulty
  # - Weights are loaded from a file, then handed off to the neural network
  def loadWeights(self, weightsPath):
    #Read in the weights
    with open(weightsPath) as file:
      weights = file.readlines()

    #Strip whitespace and ensure they're floats not strings
    for i in range(len(weights)):
      weights[i] = float(weights[i].strip("\n"))

    #Hand off weights to the network
    self.network.loadWeights(weights)
    print(f"Loaded {weightsPath}")

  #Take the result of the last guess and save it
  def feedbackMove(self, result):
    if result == "hit":
      #Mark the last guess as a hit on the guess tracker
      self.enemyGrid[self.lastGuess[1]][self.lastGuess[0]] = 1
    else:
      #Mark the last guess as a miss on the guess tracker
      self.enemyGrid[self.lastGuess[1]][self.lastGuess[0]] = -1

  #Returns the location of the tile to fire at
  def makeMove(self):
    #Convert the saved grid data into a single list
    # - Format for the neural network, treats it as a vector
    convertedGrid = []
    for i in range(7):
      convertedGrid += self.enemyGrid[i]

    #Sample the neural network will the known guesses as the input data
    guesses = self.network.sampleData(convertedGrid)

    #Go through the confidence values returned from the neural network
    # - Select the highest confidence value that hasn't already been guessed
    maxGuess = 0
    maxGuessIndex = -1
    for i in range(len(guesses)):
      if guesses[i] >= maxGuess:
        if convertedGrid[i] == 0:
          maxGuess = guesses[i]
          maxGuessIndex = i
    guess = maxGuessIndex

    #x and y flipped compared to other sections of code
    #This is because the neural network returns data in as a concatenated list of rows
    #But the tiles are indexed top -> bottom, then left to right, effectively the opposite of this
    x = guess % 7
    y = guess // 7

    #Save the last guess for feedback later, and return the location
    self.lastGuess = [x, y]
    return [x, y]

  #Return a valid battleships grid for the user to fire at
  # - Locations are randomly generated
  def generateGrid(self, shipLengths):
    #Fill the grids with ships
    for shipLength in shipLengths:
      #Keep trying to place until it succeeds
      placing = True
      while placing:
        #Generate position and rotation
        flipped = bool(random.randint(0, 1))
        x, y = random.randint(0, 6), random.randint(0, 6)

        #Attempt to place the piece
        if self.placePiece(shipLength, x, y, flipped):
          placing = False

  #Attempt to place the ship
  # - If it will fit (on the board, no collisions), save it and return True
  # - If it won't fit, make no changes to the board and return False
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
