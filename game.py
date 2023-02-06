#!/usr/bin/python3
import random
import model
import dataset
import sys

#Return list of weight values if found, otherwise exit (no point recovering if the opponent won't run)
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
    print(f"Failed to load existing model ({weightFile})")
    exit(1)
  else:
    print(f"Loaded existing model ({weightFile})")

  return weights

#Define network parameters
inputDimensions = 7
networkSize = (inputDimensions ** 2) ** 2

#Load weights in from file, or generate default
sys.argv.append(None)
if sys.argv[1] == None:
  weightFile = "weights.dmp"
else:
  weightFile = sys.argv[1]
  print(weightFile)
weights = getWeights(weightFile, networkSize)

#Create model and load weights
exampleNetwork = model.Network(inputDimensions ** 2)
exampleNetwork.loadWeights(weights)

#Return False if any ships remain on the board
def checkGrid(ships):
  if 1 in ships:
    return False
  return True

#Run configured number of games, and measure the average number of hits
sampleSize = 1000
requiredGuesses = 0
for sample in range(sampleSize):
  #Define dataset parameters and generate data
  datasetSize, boardDimensions = 1, 7
  maxHits = 0
  generatedData = dataset.buildDataset(datasetSize, boardDimensions, maxHits)

  grid = generatedData[0][0]
  ships = generatedData[0][1]

  #Guess until all ships are cleared
  totalGuesses = 0
  while not checkGrid(ships):
    #Sample the neural network (generate probabilities)
    totalGuesses += 1
    guesses = exampleNetwork.sampleData(grid)

    #Pick the highest probability, that hasn't already been guessed
    maxGuess = 0
    maxGuessIndex = -1
    for i in range(len(guesses)):
      if guesses[i] >= maxGuess:
        if grid[i] == 0:
          maxGuess = guesses[i]
          maxGuessIndex = i
    guess = maxGuessIndex

    #Fallback to random number if no probability is given
    if guess == -1:
      guess = random.randint(0, len(grid) - 1)
      while grid[guess] != 0:
        guess = random.randint(0, len(grid) - 1)

    #Mark the result of the hit on the board
    if ships[guess] == 1:
      grid[guess] = 1
      ships[guess] = 0
    else:
      grid[guess] = -1

  requiredGuesses += totalGuesses

print(f"Average guesses: {requiredGuesses / sampleSize}")
