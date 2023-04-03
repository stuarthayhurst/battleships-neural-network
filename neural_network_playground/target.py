#!/usr/bin/python3
import time, random
import model
import dataset

#Return the time on seconds, with nanosecond resolution
def getSeconds():
  return time.time_ns() / 1000000000

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

  #Load empty weights if file couldn't be used
  if not weightsValid:
    print("Failed to load existing model, using new empty weights")
    weights = [random.randint(-10, 10) for i in range(networkSize)]
  else:
    print("Loaded existing model")

  return weights

#Return False if any ships remain
def checkGrid(ships):
  if 1 in ships:
    return False
  return True

#Write the current weights to a file
def saveModel(trainingNetwork, outputWeightFile):
  #Save model weights to file
  trainedWeights = trainingNetwork.dumpNetwork()
  with open(outputWeightFile, "w") as file:
    for i in range(networkSize):
      file.write(f"{trainedWeights[i]}\n")

#Calculate average number of guesses to clear a board over a given sample size
def benchmark(sampleNetwork, sampleSize):
  requiredGuesses = 0
  for sample in range(sampleSize):
    #Generate one board to play against
    generatedData = dataset.buildDataset(1, 7, 0)
    grid = generatedData[0][0]
    ships = generatedData[0][1]

    #Carry out each test
    totalGuesses = 0
    while not checkGrid(ships):
      #Sample the neural network
      totalGuesses += 1
      guesses = sampleNetwork.sampleData(grid)

      #Sample highest, unguessed probability
      maxGuess = 0
      maxGuessIndex = -1
      for i in range(len(guesses)):
        if guesses[i] >= maxGuess:
          if grid[i] == 0:
            maxGuess = guesses[i]
            maxGuessIndex = i
      guess = maxGuessIndex

      if guess == -1:
        guess = random.randint(0, len(grid) - 1)
        while grid[guess] != 0:
          guess = random.randint(0, len(grid) - 1)

      #Mark the board
      if ships[guess] == 1:
        grid[guess] = 1
        ships[guess] = 0
      else:
        grid[guess] = -1

    requiredGuesses += totalGuesses

  return requiredGuesses / sampleSize

#Define network, dataset and sampling parameters
inputSize = 49
networkSize = inputSize ** 2

#Network parameters
batchCount, batchSize = 100000, 10
learningRate = 0.00005
datasetSize = 100000
sampleCount = 1000

targetValue = 33.1
outputWeightFile = f"training/weights-{targetValue}-avg.dmp"

override = 0
if override != 0:
  inputWeightFile = f"training/weights-{override}-avg.dmp"
else:
  inputWeightFile = f"training/weights-current-avg.dmp"
  input("No override specified, using last set of weights")

#Load weights in from file, or generate default
startTime = getSeconds()
weights = getWeights(inputWeightFile, networkSize)

#Create model and load weights
trainingNetwork = model.Network(inputSize)
trainingNetwork.loadWeights(weights)
print(f"\nLoaded network in {round(getSeconds() - startTime, 4)}s")

training = True
currentValue = benchmark(trainingNetwork, sampleCount)
print(f"Average guesses: {currentValue}")
if currentValue <= targetValue:
  training = False

#Keep training until stopped by reaching the target
while training:
  #Generate training data
  startTime = getSeconds()
  generatedData = dataset.buildDataset(datasetSize, 7, inputSize)
  print(f"Generated dataset in {round(getSeconds() - startTime, 4)}s")

  startTime = getSeconds()
  if not trainingNetwork.loadDataset(generatedData):
    print("Failed to load dataset")
    exit(1)
  print(f"Loaded dataset in {round(getSeconds() - startTime, 4)}s")

  startTime = getSeconds()
  trainingNetwork.trainNetwork(batchCount, batchSize, learningRate)
  print(f"Trained network in {round(getSeconds() - startTime, 4)}s")

  currentValue = benchmark(trainingNetwork, sampleCount)
  print(f"Average guesses: {currentValue}")
  if round(currentValue, 1) <= targetValue:
    training = False

  #Output the weights as the current working values, and against the measured value
  saveModel(trainingNetwork, f"training/weights-{round(currentValue, 1)}-avg.dmp")
  saveModel(trainingNetwork, "training/weights-current-avg.dmp")
