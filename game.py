#!/usr/bin/python3
import random
import model
import dataset

def getWeights(weightFile, networkSize):
  #Attempt to load existing weights from file
  weightsValid = False
  weights = []
  try:
    with open(weightFile) as file:
      weights = file.readlines()

    for i in range(len(weights)):
      weights[i] = float(weights[i].strip("\n"))

    weightsValid = (len(weights) == networkSize)
  except:
    print(f"Couldn't open {weightFile}")

  #Fail if weights couldn't be used
  if not weightsValid:
    print("Failed to load existing model")
    exit(1)
  else:
    print("Loaded existing model")

  return weights

#Define network parameters
inputDimensions = 7
networkSize = (inputDimensions ** 2) ** 2

#Load weights in from file, or generate default
weightFile = "weights.dmp"
weights = getWeights(weightFile, networkSize)

#Create model and load weights
exampleNetwork = model.Network(inputDimensions ** 2)
exampleNetwork.loadWeights(weights)

#Define dataset parameters and generate data
datasetSize, boardDimensions = 1, 7
maxHits = 0
generatedData = dataset.buildDataset(datasetSize, boardDimensions, maxHits)


grid = generatedData[0][0]
ships = generatedData[0][1]

print(grid)
print(ships)

def checkGrid(ships):
  if 1 in ships:
    return False
  return True

totalGuesses = 0
while not checkGrid(ships):
  totalGuesses += 1
  guesses = exampleNetwork.sampleData(grid)

  maxGuess = 0
  maxGuessIndex = -1
  for i in range(len(guesses)):
    if guesses[i] >= maxGuess:
      if grid[i] == 0:
        print("setting to" + str(maxGuessIndex))
        maxGuess = guesses[i]
        maxGuessIndex = i
  guess = maxGuessIndex

  if guess == -1:
    print("No guess")
    guess = random.randint(0, len(grid) - 1)
    while grid[guess] == -1:
      guess = random.randint(0, len(grid) - 1)

  print(guess)

  if ships[guess] == 1:
    grid[guess] = 1
    ships[guess] = 0
    print("Hit")
  else:
    grid[guess] = -1
    print("Miss")

  for y in range(boardDimensions):
    for x in range(boardDimensions):
      tile = grid[(y * boardDimensions) + x]
      if tile == -1:
        print("M", end = "")
      elif tile == 1:
        print("X", end = "")
      else:
        print("0", end = "")
    print()

print(totalGuesses)
